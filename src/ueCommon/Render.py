import sys

from PyQt4 import QtCore, QtGui

global render

__render_options__ = ["Render Local",
                      "Render Remote",
                      "Render on the Cloud"]

def getValues():
    return render

class Render(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        global render
        render = [0, {}]

        self.setLayout(QtGui.QHBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self.renderBox = QtGui.QComboBox()

        for option in __render_options__:
            self.renderBox.addItem(option)

        self.layout().addWidget(self.renderBox)

        self.renderBox.activated.connect(self.setRender)

    def setRender(self):
        global render
        render[0] = self.renderBox.currentIndex()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = Render()
    win.show()
    sys.exit(app.exec_())

