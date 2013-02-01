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
    
class DataDnDListWidget(QListWidget):
    '''A drag and drop list widget for the data view of the pivot table.
    Append measurement to the end of the text after drop.
    '''

    def __init__(self, parent=None):
        super(DataDnDListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

        #calculate Mean by default.
        self.StatOptionLabel = "Mean"

        self.__initActions__()
        self.__initContextMenus__()

    def __initActions__(self):
        self.StatOption = QAction("Statistics Option",  self)
        self.StatOption.setShortcut("Alt+O")
        self.addAction(self.StatOption)
        self.connect(self.StatOption, SIGNAL("triggered()"), self.ChooseStatOption)
       

    def __initContextMenus__(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self, SIGNAL("customContextMenuRequested(QPoint)"), self.ListWidgetContext)
        # the item doubleclicked signal does not respond. 
##        self.connect(self, SIGNAL('itemDoubleClicked(QListWidgetItem)'), self.ChooseStatOption)
        
    def ListWidgetContext(self, point):
        '''Create a menu for the QListWidget and associated actions'''
        tw_menu = QMenu("Menu", self)
        tw_menu.addAction(self.StatOption)
        tw_menu.exec_(self.mapToGlobal(point))

    def ChooseStatOption(self):
##        print 'option activated'
        dialog = PivotStatOption(self)
        if dialog.exec_():
            self.StatOptionLabel=dialog.OptionSelected()
##            print self.StatOptionLabel
            #update the current row with the new stat option label.
            SelectedItemRow=self.currentRow()
            
            CurrentText=str(self.currentItem().text())
            VariableText=CurrentText[:CurrentText.find('(')]
            NewText=VariableText+"(%s)"%self.StatOptionLabel
            NewText=QString(NewText)
            item = QListWidgetItem(NewText, self)

            self.takeItem(SelectedItemRow)        
            self.insertItem(SelectedItemRow-1,item)

            self.StatOptionLabel = "Mean"
            