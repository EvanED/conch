from PyQt4 import QtCore, QtGui

class EnterActionTextEdit(QtGui.QPlainTextEdit):
    returnPressed = QtCore.pyqtSignal('QString')

    def keyPressEvent(self, event):
        if (event.key() == QtCore.Qt.Key_Return):
            self.returnPressed.emit(self.toPlainText())
        else:
            super(EnterActionTextEdit, self).keyPressEvent(event)

    def say_hi(self, string):
        print(string)

    def __init__(self, *args, **kwargs):
        super(EnterActionTextEdit, self).__init__(*args, **kwargs)
        self.returnPressed.connect(self.say_hi)

