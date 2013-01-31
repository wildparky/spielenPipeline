from PyQt4 import QtCore, QtGui

class ListWidgetWithPopupMenu(QtGui.QListWidget):
    def __init__(self, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        
        for i in range(10):
            self.addItem('item%d' % i)
    
        self.contextMenu = QtGui.QMenu(self)
        action = QtGui.QAction('Current Item', self)
        self.connect(action, QtCore.SIGNAL("triggered()"), self.showCurrentItem)
        self.contextMenu.addAction(action)
    
    def showCurrentItem(self):
        print self.currentItem().text()
    
    def contextMenuEvent(self, event):
        self.contextMenu.exec_(event.globalPos())

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    lw = ListWidgetWithPopupMenu()
    lw.show()
    sys.exit(app.exec_())