from PyQt4 import QtCore, QtGui

class EnterActionTextEdit(QtGui.QPlainTextEdit):
    returnPressed = QtCore.pyqtSignal('QString')

    def __init__(self, parent=None):
        my_super = super(EnterActionTextEdit, self)
        my_super.__init__(parent)
        self._my_super = my_super

    def keyPressEvent(self, event):
        if (event.key() == QtCore.Qt.Key_Return):
            self.returnPressed.emit(self.toPlainText())
        else:
            self._my_super.keyPressEvent(event)

