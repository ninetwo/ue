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
        render = [0, [], {"newVersion": True, "clearLastVersion": False}]

        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self.renderFromList = QtGui.QListWidget()
        self.renderBox = QtGui.QComboBox()
        self.createNewVersion = QtGui.QCheckBox("Create new version?")
        self.clearLastVersion = QtGui.QCheckBox("Delete files from previous version?")

        self.createNewVersion.setChecked(render[2]["newVersion"])
        self.clearLastVersion.setChecked(render[2]["clearLastVersion"])

        self.renderFromList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        for option in __render_options__:
            self.renderBox.addItem(option)

        renderFromSorted = sorted(renderFrom)
        for rf in renderFromSorted:
            self.renderFromList.addItem(QtGui.QListWidgetItem(rf))
        if len(renderFrom) > 0 and not currentRender == None:
            self.renderFromList.setCurrentItem(self.renderFromList.item(
                                               renderFromSorted.index(currentRender)))
            render[1] = [str(self.renderFromList.currentItem().text())]

        self.layout().addWidget(self.renderBox)
        self.layout().addWidget(self.renderFromList)
        self.layout().addWidget(self.createNewVersion)
        self.layout().addWidget(self.clearLastVersion)

        self.renderBox.activated.connect(self.setRender)
        self.renderFromList.itemSelectionChanged.connect(self.setRenderFrom)
        self.createNewVersion.stateChanged.connect(self.setCreateNewVersion)
        self.clearLastVersion.stateChanged.connect(self.setClearLastVersion)

    def setRender(self):
        global render
        render[0] = self.renderBox.currentIndex()

    def setRenderFrom(self):
        global render
        render[1] = []
        for i in self.renderFromList.selectedItems():
            render[1].append(str(i.text()))

    def setCreateNewVersion(self):
        global render
        render[2]["newVersion"] = self.createNewVersion.isChecked()

    def setClearLastVersion(self):
        global render
        render[2]["clearLastVersion"] = self.clearLastVersion.isChecked()


#if __name__ == "__main__":
#    app = QtGui.QApplication(sys.argv)
#    win = Render()
#    win.show()
#    sys.exit(app.exec_())

