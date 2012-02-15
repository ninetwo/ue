import sys

from PyQt4 import QtCore, QtGui

global render
global renderFrom, currentRender

__render_options__ = ["Render Local",
                      "Render Remote",
                      "Render on the Cloud"]

def getValues():
    return render

def setRenderFrom(rf):
    global renderFrom
    renderFrom = rf

def setCurrentRender(cr):
    global currentRender
    currentRender = cr

class Render(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        global render
        render = [0, [], {}]

        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self.renderFromList = QtGui.QListWidget()
        self.renderBox = QtGui.QComboBox()

        self.renderFromList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        for option in __render_options__:
            self.renderBox.addItem(option)

        renderFromSorted = sorted(renderFrom)
        for rf in renderFromSorted:
            self.renderFromList.addItem(QtGui.QListWidgetItem(rf))
        if len(renderFrom) > 0:
            self.renderFromList.setCurrentItem(self.renderFromList.item(
                                               renderFromSorted.index(currentRender)))
            render[1] = [str(self.renderFromList.currentItem().text())]

        self.layout().addWidget(self.renderBox)
        self.layout().addWidget(self.renderFromList)

        self.renderBox.activated.connect(self.setRender)
        self.renderFromList.itemSelectionChanged.connect(self.setRenderFrom)

    def setRender(self):
        global render
        render[0] = self.renderBox.currentIndex()

    def setRenderFrom(self):
        global render
        render[1] = []
        for i in self.renderFromList.selectedItems():
            render[1].append(str(i.text()))


#if __name__ == "__main__":
#    app = QtGui.QApplication(sys.argv)
#    win = Render()
#    win.show()
#    sys.exit(app.exec_())

