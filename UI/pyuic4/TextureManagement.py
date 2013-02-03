# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TextureManagement.ui'
#
# Created: Sun Feb 03 15:47:28 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TextureManager(object):
    def setupUi(self, TextureManager):
        TextureManager.setObjectName(_fromUtf8("TextureManager"))
        TextureManager.resize(445, 318)
        self.centralwidget = QtGui.QWidget(TextureManager)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        TextureManager.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(TextureManager)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 445, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFileTextureManagement = QtGui.QMenu(self.menubar)
        self.menuFileTextureManagement.setObjectName(_fromUtf8("menuFileTextureManagement"))
        TextureManager.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(TextureManager)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        TextureManager.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(TextureManager)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuFileTextureManagement.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFileTextureManagement.menuAction())

        self.retranslateUi(TextureManager)
        QtCore.QMetaObject.connectSlotsByName(TextureManager)

    def retranslateUi(self, TextureManager):
        TextureManager.setWindowTitle(QtGui.QApplication.translate("TextureManager", "TextureManager", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFileTextureManagement.setTitle(QtGui.QApplication.translate("TextureManager", "Texture Management", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("TextureManager", "about", None, QtGui.QApplication.UnicodeUTF8))

