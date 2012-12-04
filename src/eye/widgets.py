from PyQt4 import QtCore, QtGui

class EnterActionTextEdit(QtGui.QPlainTextEdit):
    returnPressed = QtCore.pyqtSignal('QString')

    def keyPressEvent(self, event):
        if (event.key() == QtCore.Qt.Key_Return):
            self.returnPressed.emit(self.toPlainText())
        else:
            super(EnterActionTextEdit, self).keyPressEvent(event)

