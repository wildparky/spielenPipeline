# coding=gbk
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
                  
        self.ui.targetDir.setText(os.path.normcase(os.path.join(workspace.getPath(),'textures')))
        #初始设定targetDir
        
        self.ui.refreshButton.clicked.connect(self.FTM_view)
        self.ui.browseFloderbutton.clicked.connect(self.browseFloderbutton)

#===============================================================================
#辅助功能
#===============================================================================
    def fileNameDialog(self):
        '''
        产生对话框，选择文件
        '''
        fileName=QtGui.QFileDialog.getOpenFileName(self,"Open file",'/',"Image Files(*.png *.jpg *.bmp)")
        return fileName
    
    def floderDialog(self):
        '''
        选择文件夹
        '''
        floderName=QtGui.QFileDialog.getExistingDirectory(self, "Find Floder", QtCore.QDir.currentPath())
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
        textureNodes, texturePaths = self.FTM_FileTextureFind()
        badNodes = []
        for Node, fileName in textureNodes.items():
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

        self.ui.treeWidget.clear()          
        for filePath, fileNode in dirDict.iteritems() :
            path = QtGui.QTreeWidgetItem(self.ui.treeWidget) #得到treewidget
            if filePath == "":
                path.setText(0, ' %s texture(s) NOT specified. ' % str(len(fileNode)))
                path.setText(1, 'So they are NOT exist(s).')
            else:
                path.setText(0, ' %s texture(s) point to' % str(len(fileNode)))
                path.setText(0, ' %s texture(s) point to' % str(len(fileNode)))
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
                for node in noExistNode :
                    nodeID=QtGui.QTreeWidgetItem(numnoExistNode)
                    nodeID.setText(0,'%s' % str(node))
                    nodeID.setText(1,'....../%s' % os.path.split(node.ftn.get())[1])
                    
                numExistNode = QtGui.QTreeWidgetItem(path)
                numExistNode.setText(0, ' %s of them exist(s).' % str(len(ExistNode)))   
                for node in ExistNode :
                    nodeID=QtGui.QTreeWidgetItem(numExistNode)
                    nodeID.setText(0,'%s' % str(node))
                    nodeID.setText(1,'....../%s' % os.path.split(node.ftn.get())[1])
           
                        
                    

#===============================================================================
# 文件夹操作部分
#===============================================================================
    def browseFloderbutton(self):
        '''
        browsebutton，创建dialog，得到选择的文件夹
        '''
        floder=self.floderDialog()
        print floder
        self.ui.targetDir.setText('%s' % floder)
        
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
