from PyQt4 import QtCore, QtGui

# Much of this code from
# http://rowinggolfer.blogspot.com/2010/08/qtextedit-with-autocompletion-using.html,
# but it has also been modified to use Python unicode strings instead
# of QString and some other things like that.

class DictionaryCompleter(QtGui.QCompleter):
    def __init__(self, parent=None):
        words = []
        try:
            f = open("/usr/share/dict/words","r")
            for word in f:
                words.append(word.strip())
            f.close()
        except IOError:
            print "dictionary not in anticipated location"
        QtGui.QCompleter.__init__(self, words, parent)


def is_alt_and(event, key):
    return (event.modifiers() == QtCore.Qt.AltModifier
            and event.key() == key)


class EnterActionTextEdit(QtGui.QPlainTextEdit):
    returnPressed = QtCore.pyqtSignal('QString')
    alt1Pressed = QtCore.pyqtSignal()
    alt2Pressed = QtCore.pyqtSignal()
    alt3Pressed = QtCore.pyqtSignal()
    alt4Pressed = QtCore.pyqtSignal()
    alt5Pressed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        my_super = super(EnterActionTextEdit, self)
        my_super.__init__(parent)
        self.completer = DictionaryCompleter()
        self._my_super = my_super

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup().isVisible():
            ignore_these = [
                QtCore.Qt.Key_Enter,
                QtCore.Qt.Key_Return,
                QtCore.Qt.Key_Escape,
                QtCore.Qt.Key_Tab,
                QtCore.Qt.Key_Backtab
                ]
            if event.key() in ignore_these:
                event.ignore()
                return

        if (event.key() == QtCore.Qt.Key_Return):
            self.returnPressed.emit(self.toPlainText())
            return

        if (is_alt_and(event, QtCore.Qt.Key_1)):
            self.alt1Pressed.emit()
            return
        if (is_alt_and(event, QtCore.Qt.Key_2)):
            self.alt2Pressed.emit()
            return
        if (is_alt_and(event, QtCore.Qt.Key_3)):
            self.alt3Pressed.emit()
            return
        if (is_alt_and(event, QtCore.Qt.Key_4)):
            self.alt4Pressed.emit()
            return
        if (is_alt_and(event, QtCore.Qt.Key_5)):
            self.alt5Pressed.emit()
            return
            

        ## has ctrl-E been pressed??
        isShortcut = (event.modifiers() == QtCore.Qt.ControlModifier
                      and event.key() == QtCore.Qt.Key_E)
        if (not self.completer or not isShortcut):
            self._my_super.keyPressEvent(event)


        ## ctrl or shift key on it's own??
        ctrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier ,
                QtCore.Qt.ShiftModifier)
        if ctrlOrShift and event.text() == u"":
            # ctrl or shift key on it's own
            return

        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=" #end of word

        hasModifier = ((event.modifiers() != QtCore.Qt.NoModifier) and
                        not ctrlOrShift)

        completionPrefix = self.textUnderCursor()

        if (not isShortcut
            and (hasModifier
                 or event.text() == ""
                 or len(completionPrefix) < 3
                 or event.text()[-1] in eow)):
            self.completer.popup().hide()
            return

        if (completionPrefix != self.completer.completionPrefix()):
            self.completer.setCompletionPrefix(completionPrefix)
            popup = self.completer.popup()
            popup.setCurrentIndex(
                self.completer.completionModel().index(0,0))

        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0)
            + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr) ## popup it up!


    def setCompleter(self, completer):
        if self.completer:
            self.disconnect(self.completer, 0, self, 0)
        if not completer:
            return

        completer.setWidget(self)
        completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer = completer
        self.connect(self.completer,
            QtCore.SIGNAL("activated(const QString&)"), self.insertCompletion)

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = (completion.length() -
            self.completer.completionPrefix().length())
        tc.movePosition(QtGui.QTextCursor.Left)
        tc.movePosition(QtGui.QTextCursor.EndOfWord)
        tc.insertText(completion.right(extra))
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        self._my_super.focusInEvent(event)

