import os
import sip

import maya.cmds as cmds
import maya.OpenMayaUI as mui

from PyQt4 import QtGui, QtCore, uic

def getMayaWindow():
	'Get the maya main window as a QMainWindow instance'
	ptr = mui.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)

#Get the absolute path to my ui file
uiFile = os.path.join(cmds.internalVar(upd=True), 'ui', 'demo.ui')
print 'Loading ui file:', os.path.normpath(uiFile)

#Load the ui file, and create my class
form_class, base_class = uic.loadUiType(uiFile)
class Window(base_class, form_class):
	def __init__(self, parent=getMayaWindow()):
		'''A custom window with a demo set of ui widgets'''
		#init our ui using the MayaWindow as parent
		super(base_class, self).__init__(parent)
		#uic adds a function to our class called setupUi, calling this creates all the widgets from the .ui file
		self.setupUi(self)
		self.setObjectName('myWindow')
		self.setWindowTitle("My Qt Demo Window")

def main():
	global myWindow
	myWindow = Window()
	myWindow.show()