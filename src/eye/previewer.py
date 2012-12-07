#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2012 Evan Driscoll <driscoll@cs.wisc.edu>
##
## Copyright (C) 2010 Hans-Peter Jansen <hpj@urpla.net>.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
###########################################################################

all_classes = ["pre", "mono", "prewrap", "nowrap", "text"]

import sip
sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui, QtWebKit

from ui_previewer import Ui_Form

import conch.parser
import conch.engine
import conch.ouiji
from threading import Thread

def find_body(webpage):
    frame = webpage.mainFrame()
    body_collection = frame.findAllElements("#content")
    assert body_collection.count() == 1
    return body_collection.first()

_next_stanza_id = 1
def append_new_stanza(webpage, command_element):
    global _next_stanza_id
    id = 'stanza_{}'.format(_next_stanza_id)
    html = '<p id="{}"></p>'.format(id)
    _next_stanza_id += 1
    command_element.appendInside(html)
    frame = webpage.mainFrame()    
    paragraph_collection = frame.findAllElements("#" + id)
    assert paragraph_collection.count() == 1
    return paragraph_collection.first()

_next_command_id = 1
def append_command_placeholder(webpage):
    global _next_command_id
    body = find_body(webpage)
    id = "command_{}".format(_next_command_id)
    _next_command_id += 1
    html = '<div id="{}" class="prewrap"></div>'.format(id, id)
    body.appendInside(html)
    frame = webpage.mainFrame()
    command_collection = frame.findAllElements("#" + id)
    assert command_collection.count() == 1
    return (command_collection.first(),
            append_new_stanza(webpage, command_collection.first()))

def append_command(webpage, prompt, command):
    body = find_body(webpage)
    template = '<p class="user_command mono">{} {}</p>'
    body.appendInside(template.format(prompt, command))


def scroll_to_bottom(frame):
    frame.scrollToAnchor("end")

def set_class_to(element, class_):
    for remove_this in all_classes:
        element.removeClass(remove_this)
    element.addClass(class_)

class Previewer(QtGui.QWidget, Ui_Form):
    childDataAvailable = QtCore.pyqtSignal('QString')

    def __init__(self, parent=None):
        super(Previewer, self).__init__(parent)

        self.setupUi(self)
        self.baseUrl = QtCore.QUrl()

        self.saw_one_newline = False

        self.childDataAvailable.connect(self.dataAvailable)
        self.plainTextEdit.returnPressed.connect(self.changedText)
        self.plainTextEdit.alt1Pressed.connect(self.setLastToPreWrap)
        self.plainTextEdit.alt2Pressed.connect(self.setLastToPre)
        self.plainTextEdit.alt3Pressed.connect(self.setLastToNoWrap)
        self.plainTextEdit.alt4Pressed.connect(self.setLastToMono)
        self.plainTextEdit.alt5Pressed.connect(self.setLastToText)

    def setLastToPreWrap(self):
        set_class_to(self._current_cmd_element, "prewrap")
    def setLastToPre(self):
        set_class_to(self._current_cmd_element, "pre")
    def setLastToMono(self):
        set_class_to(self._current_cmd_element, "mono")
    def setLastToNoWrap(self):
        set_class_to(self._current_cmd_element, "nowrap")
    def setLastToText(self):
        set_class_to(self._current_cmd_element, "text")

    def setBaseUrl(self, url):
        self.baseUrl = url

    def dataAvailable(self, text):
        if text == "\r":
            return
        if not self.saw_one_newline and text == "\n":
            self.saw_one_newline = True
            return
        if self.saw_one_newline and text == "\n":
            # second newline!...
            self._current_par_element = append_new_stanza(self.webView.page(), self._current_cmd_element)
            return
        if self.saw_one_newline:
            text = "\n" + text
            self.saw_one_newline = False
        self._current_par_element.appendInside(text)
        scroll_to_bottom(self.webView.page().mainFrame())

    def daemonChildReader(self, stream, template="{}"):
        while True:
            data = stream.read(1)
            if data == "":
                stream.close()
                return
            self.childDataAvailable.emit(template.format(data))

    def changedText(self, text):
        if text == "dumphtml":
            print(self.webView.page().mainFrame().toHtml())
            return
        command_ast = conch.parser.parse_to_ast(text)
        append_command(self.webView.page(), ">:", text)
        t = append_command_placeholder(self.webView.page())
        (self._current_cmd_element, self._current_par_element) = t

        child = conch.engine.execute(command_ast)

        t = Thread(target=self.daemonChildReader,
                   args=(child.stdout,))
        t.daemon = True
        t.start()
        t = Thread(target=self.daemonChildReader,
                   args=(child.stderr, '<span class="stderr">{}</span>'))
        t.daemon = True
        t.start()

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.centralWidget = Previewer(self)
        self.setCentralWidget(self.centralWidget)
        self.setStartupText()

    def setStartupText(self):
        with open("src/eye/template.html", "r") as template:
            self.centralWidget.webView.setHtml(template.read())


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
