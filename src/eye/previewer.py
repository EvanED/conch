#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2010 Hans-Peter Jansen <hpj@urpla.net>.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
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


import sip
sip.setapi('QString', 3)

from PyQt4 import QtCore, QtGui, QtWebKit

from ui_previewer import Ui_Form

import conch.parser
import conch.engine
import conch.ouiji


def append_paragraphs(body, p):
    template = '<p class="{}" id="{}"><span>{}</span></p>'
    lines = '</span><span>'.join(p.get_lines())
    html = template.format(p.get_style(),
                           p.get_id(),
                           lines)
                           
    body.appendInside(html)

def append_output(webpage, output):
    frame = webpage.mainFrame()
    body_collection = frame.findAllElements("body")
    assert body_collection.count() == 1
    body = body_collection.first()

    paragraphs = conch.ouiji.styleize_output(output)
    for p in paragraphs:
        append_paragraphs(body, p)

class Previewer(QtGui.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Previewer, self).__init__(parent)

        self.setupUi(self)
        self.baseUrl = QtCore.QUrl()

        self.plainTextEdit.returnPressed.connect(self.changedText)

    def setBaseUrl(self, url):
        self.baseUrl = url

    def changedText(self, text):
        command_ast = conch.parser.parse_to_ast(text)
        child = conch.engine.execute(command_ast)
        child.stdin.close()
        child.wait()
        output = child.stdout.read() + child.stderr.read()
        #self.webView.setHtml(output, self.baseUrl)
        append_output(self.webView.page(), output)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.centralWidget = Previewer(self)
        self.setCentralWidget(self.centralWidget)
        self.setStartupText()

    def setStartupText(self):
        self.centralWidget.webView.setHtml("""
<html>
<head>
  <style type="text/css">
    .mono {
      font-family: monospace;
      white-space: pre;
    }
  </style>
</head>
<body>
</body></html>""")


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
