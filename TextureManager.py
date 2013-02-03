# -*- coding:utf-8 -*-
'''
Created on 2013-1-25

Function:
参考FileTextureManager.mel，创建其python版本(适当改造),同时学习py
使用PyQt4作为UI
 
@author: :     Yuan Wang
@version: :    0.1
@contact: :    play.wang1988@gmail.com
'''

from pymel.core import *
import maya.OpenMayaUI as mui

import os

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignature
import sip

from UI.TextureManagement import Ui_TextureManager
from UI.TextureManagementFind import Ui_textureView

class Window(QtGui.QMainWindow, Ui_TextureManager):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        
        self.setupUi(self)

        self.TextureManager_viewWidget = TextureManager_view()
        self.setCentralWidget(self.TextureManager_viewWidget)
#===============================================================================
# 显示部分
#===============================================================================
class TextureManager_view(QtGui.QWidget):
    '''
    classdocs
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        super(TextureManager_view, self).__init__(*args, **kwargs)
      
        self.ui = Ui_textureView()
        self.ui.setupUi(self)
        
        self.ui.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # 定义右键菜单
        self.ui.treeWidget.connect(self.ui.treeWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.rightMenuShow)
        
        self.ui.targetDir.setText(os.path.normcase(os.path.join(workspace.getPath(), 'textures')))  # 初始设定targetDir
        
        self.ui.refreshButton.clicked.connect(self.FTM_view)
        self.ui.browseFloderbutton.clicked.connect(self.browseFloderbutton)
#===============================================================================
# 界面定制
#===============================================================================
    
    @pyqtSignature('QPoint')
    def rightMenuShow(self, point):
        item = self.ui.treeWidget.itemAt(point)

        # 空白区域不显示菜单
        if item != None:
            self.CreatrightMenu()

    # 创建右键菜单
    def CreatrightMenu(self):
        self.rightMenu = QtGui.QMenu(self.ui.treeWidget)

        OpenAction = QtGui.QAction(u"Open", self.ui.treeWidget)  # triggered 为右键菜单点击后的激活事件。
        self.connect(OpenAction, QtCore.SIGNAL("triggered()"), self.findChildNodes)
        self.rightMenu.addAction(OpenAction)
        
        MoveAction = QtGui.QAction(u"Move", self.ui.treeWidget)  
        self.connect(MoveAction, QtCore.SIGNAL("triggered()"), self.FTM_FileTextureMove)
        self.rightMenu.addAction(MoveAction)
        
        CopyAction = QtGui.QAction(u"Copy", self.ui.treeWidget)  
        self.connect(CopyAction, QtCore.SIGNAL("triggered()"), self.FTM_FileTextureCopy)
        self.rightMenu.addAction(CopyAction)
        
        self.rightMenu.exec_(QtGui.QCursor.pos())

#===============================================================================
# 辅助功能
#===============================================================================
    def fileNameDialog(self):
        '''
        产生对话框，选择文件
        '''
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open file", '/', "Image Files(*.png *.jpg *.bmp)")
        return fileName
    
    def floderDialog(self):
        '''
        选择文件夹
        '''
        floderName = QtGui.QFileDialog.getExistingDirectory(self, "Find Floder", QtCore.QDir.currentPath())
        return floderName
    
    def intersectionList(self, a, b):
        '''
        得到两个列表的交集
        :param a:
        :param b:
        '''
        s = set(b)
        return [item for item in a if item in s]
    def differenceList(self, a, b):
        '''
        得到两个列表的差集
        :param a:
        :param b:
        '''
        s = set(b)
        return [item for item in a if item not in s]     
#===============================================================================
# view主体
#===============================================================================
    def FTM_FileTextureFind(self):
        '''
        搜索场景中file贴图文件,同时自动删除未使用的fileNode
        '''
        
        textureNodes = {}  # 存放Node与贴图路径
        texturePaths = []  # 存放贴图路径
        
        fileNodes = ls(type='file')
        if not len(fileNodes) == 0:
            for fileNode in fileNodes:
                fileName = fileNode.ftn.get()
#                if fileName == '':
#                    delete(fileNode)
#                    continue
                textureNodes.setdefault(fileNode, fileName)  # 創建字典,key:node value:filename
                texturePath = os.path.dirname(fileName)
                texturePaths.append(texturePath)
                texturePaths = sorted(set(texturePaths), key=texturePaths.index)
            return textureNodes, texturePaths
        else :
            QtGui.QMessageBox.warning(self,
                "warning",
                "No file textures found!\n")
            
    def FTM_FileTextureAnalyst_badFileNode(self):
        '''
        找出贴图丢失的fileNode
        '''
        textureNodes = self.FTM_FileTextureFind()
        badNodes = []
        for Node, fileName in textureNodes[0].items():
            if os.path.isabs(fileName) == False:  # 判斷是否是相對路徑,如果是,則增加工程目錄
                projectPath = workspace.getPath()
                fileName = os.path.join(projectPath, fileName)
            if os.path.exists(fileName) == False:
                badNodes.append(Node)
        return badNodes
    
    def FTM_FileTextureAnalyst_dirDict(self):
        '''
        得到以filename作爲key的字典,{filePath:(node1,node2,……)}
        '''
        textureNodes, texturePaths = self.FTM_FileTextureFind()
        dirDict = {}
        for path in texturePaths:
            nodes = []
            for fileNode, fileName in textureNodes.iteritems():
                if path == os.path.dirname(fileName):
                    nodes.append(fileNode)
            dirDict.setdefault(path, nodes)
        return dirDict 
    
    def FTM_view(self):
        '''
        刷新view，使用QtviewWidget
        '''
        dirDict = self.FTM_FileTextureAnalyst_dirDict()
        badNodes = self.FTM_FileTextureAnalyst_badFileNode()
        filePaths = sorted(dirDict.keys())
        path = QtGui.QTreeWidgetItem(self.ui.treeWidget)  # 得到QTreewidget
        self.ui.treeWidget.clear()   
        for  filePath in filePaths:
            fileNode = dirDict[filePath]
            path = QtGui.QTreeWidgetItem(self.ui.treeWidget)  # 得到QTreewidget
            if filePath == "":
                path.setText(0, ' %s texture(s) NOT specified. ' % str(len(fileNode)))
                path.setText(1, 'So they are NOT exist(s).')
                path.setTextColor(0, QtGui.QColor(224, 27, 106)) 
                path.setToolTip(0, 'path not exist(s)') 
                for node in fileNode :
                    specifiedNode = QtGui.QTreeWidgetItem(path)
                    specifiedNode.setText(0, '%s' % node)
                    specifiedNode.setToolTip(0, 'filenode')  # 标识出这是filenode节点
            else:
                path.setText(0, ' %s texture(s) point to' % str(len(fileNode)))
                path.setToolTip(0, 'path')
                path.setText(1, filePath)
                noExistNode = []  # 记录每个了路径下file节点的情况
                ExistNode = []
                if self.intersectionList(fileNode, badNodes) != 0:
                    noExistNode = self.intersectionList(fileNode, badNodes)          
                    ExistNode = self.differenceList(fileNode, badNodes)
                else:
                    ExistNode = fileNode
                             
                numnoExistNode = QtGui.QTreeWidgetItem(path)
                numnoExistNode.setText(0, ' %s of them NOT exist(s).' % str(len(noExistNode)))
                numnoExistNode.setToolTip(0, 'file not exist(s)')
                numnoExistNode.setTextColor(0, QtGui.QColor(224, 27, 106))  
                for node in noExistNode :
                    nodeID = QtGui.QTreeWidgetItem(numnoExistNode)
                    nodeID.setText(0, '%s' % str(node))
                    nodeID.setToolTip(0, 'filenode')
                    nodeID.setText(1, '....../%s' % os.path.split(node.ftn.get())[1])
                    
                numExistNode = QtGui.QTreeWidgetItem(path)
                numExistNode.setText(0, ' %s of them exist(s).' % str(len(ExistNode)))
                numExistNode.setToolTip(0, 'file exist(s)') 
                numExistNode.setTextColor(0, QtGui.QColor(73, 209, 73))  
                for node in ExistNode :
                    nodeID = QtGui.QTreeWidgetItem(numExistNode)
                    nodeID.setText(0, '%s' % str(node))
                    nodeID.setToolTip(0, 'filenode')
                    nodeID.setText(1, '....../%s' % os.path.split(node.ftn.get())[1])

#===============================================================================
# 文件夹操作部分
#===============================================================================
    def browseFloderbutton(self):
        '''
        browsebutton，创建dialog，得到选择的文件夹
        '''
        floder = self.floderDialog()
        print floder
        self.ui.targetDir.setText('%s' % floder)
        
    def findChildNodes(self):
        '''
        找到鼠标选择的qtreewidget的file节点
        '''
        path = self.ui.treeWidget.currentItem()  # 得到当前鼠标所选择的Item
        pathToolTip = path.toolTip(0)
        nodes = []
        
        if pathToolTip == 'filenode':  # 直接选择了node的情况
            nodes.append(path.text(0))
            
        elif pathToolTip == 'file exist(s)' or pathToolTip == 'file not exist(s)' :  # 选择了
            childCount = path.childCount()
            if childCount != 0 :
                for i in range(childCount):
                    node = path.child(i).text(0)
                    nodes.append(node)
            else :
                QtGui.QMessageBox.warning(self,
                "warning",
                "No fileNode found!\n")
                
        elif pathToolTip == 'path':
            for i in range(2):
                child = path.child(i)
                childCount = child.childCount()
                if childCount != 0:
                    for i in range(childCount):
                        node = child.child(i)
                        if node.toolTip(0) == 'filenode':
                            nodes.append(node.text(0))
                            
        elif pathToolTip == 'path not exist(s)':
            count = path.childCount()
            for i in range(count):
                node = path.child(i).text(0)
                nodes.append(node)
            
        return nodes
            
    def FTM_FileTextureOpen(self):
#        node = 
#        selected = QtGui.QTreeWidgetItem(self.ui.treeWidget)
        selected = self.ui.treeWidget.currentItem().child(0)
        child = self.ui.treeWidget.findChild(QtGui.QTreeWidget, 'treeWidget')
        print selected
    
    def FTM_FileTextureMove(self):
        '''
        移动选择的贴图文件到targetDir
        :param file:
        '''
        print 'move'
    def FTM_FileTextureCopy(self):
        print 'copy'
        
#===============================================================================
# show
#===============================================================================

def getMainWindow():
    ptr = mui.MQtUtil.mainWindow()
    mainWin = sip.wrapinstance(long(ptr), QtCore.QObject)
    return mainWin
def show():
    win = Window(parent=getMainWindow())
    win.show()
    win.raise_()
    return win    
