from PyQt4 import QtCore, QtGui

class EnterActionTextEdit(QtGui.QPlainTextEdit):
    def keyPressEvent(self, event):
        print("key:", event.key())
        if (event.key() == QtCore.Qt.Key_Return):
            print("enter!")
        else:
            super(EnterActionTextEdit, self).keyPressEvent(event)
