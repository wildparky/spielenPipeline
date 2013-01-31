# coding=gbk
'''
Created on 2013-1-25

Function:
�ο�FileTextureManager.mel��������python�汾(�ʵ�����),ͬʱѧϰpy
ʹ��PyQt4��ΪUI
 
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
# ��ʾ����
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
        
        self.ui.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # �����Ҽ��˵�
        self.ui.treeWidget.connect(self.ui.treeWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.rightMenuShow)
        
        self.ui.targetDir.setText(os.path.normcase(os.path.join(workspace.getPath(), 'textures')))  # ��ʼ�趨targetDir
        
        self.ui.refreshButton.clicked.connect(self.FTM_view)
        self.ui.browseFloderbutton.clicked.connect(self.browseFloderbutton)
#===============================================================================
# ���涨��
#===============================================================================
#    def listRightmenu(self):
#        item=['move','copy']

    
    @pyqtSignature('QPoint')
    def rightMenuShow(self, point):
        item = self.ui.treeWidget.itemAt(point)

        #�հ�������ʾ�˵�
        if item != None:
            self.CreatrightMenu()

    #�����Ҽ��˵�
    def CreatrightMenu(self):
        self.rightMenu = QtGui.QMenu(self.ui.treeWidget)
        removeAction = QtGui.QAction(u"ɾ��", self.ui.treeWidget)       # triggered Ϊ�Ҽ��˵������ļ����¼�������slef.close���õ���ϵͳ�Դ��Ĺر��¼���
        self.connect(removeAction, QtCore.SIGNAL("triggered()"), self.addItem)
        self.rightMenu.addAction(removeAction)
        
        addAction = QtGui.QAction(u"���", self, triggered=self.addItem)       # Ҳ����ָ���Զ�������¼�
        self.rightMenu.addAction(addAction)
        self.rightMenu.exec_(QtGui.QCursor.pos())
    def addItem(self):
        print 'a'
#===============================================================================
# ��������
#===============================================================================
    def fileNameDialog(self):
        '''
        �����Ի���ѡ���ļ�
        '''
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open file", '/', "Image Files(*.png *.jpg *.bmp)")
        return fileName
    
    def floderDialog(self):
        '''
        ѡ���ļ���
        '''
        floderName = QtGui.QFileDialog.getExistingDirectory(self, "Find Floder", QtCore.QDir.currentPath())
        return floderName
    
    def intersectionList(self, a, b):
        '''
        �õ������б�Ľ���
        :param a:
        :param b:
        '''
        s = set(b)
        return [item for item in a if item in s]
    def differenceList(self, a, b):
        '''
        �õ������б�Ĳ
        :param a:
        :param b:
        '''
        s = set(b)
        return [item for item in a if item not in s]     
#===============================================================================
# view����
#===============================================================================
    def FTM_FileTextureFind(self):
        '''
        ����������file��ͼ�ļ�,ͬʱ�Զ�ɾ��δʹ�õ�fileNode
        '''
        
        textureNodes = {}  # ���Node����ͼ·��
        texturePaths = []  # �����ͼ·��
        
        fileNodes = ls(type='file')
        if not len(fileNodes) == 0:
            for fileNode in fileNodes:
                fileName = fileNode.ftn.get()
#                if fileName == '':
#                    delete(fileNode)
#                    continue
                textureNodes.setdefault(fileNode, fileName)  # �����ֵ�,key:node value:filename
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
        �ҳ���ͼ��ʧ��fileNode
        '''
        textureNodes, texturePaths = self.FTM_FileTextureFind()
        badNodes = []
        for Node, fileName in textureNodes.items():
            if os.path.isabs(fileName) == False:  # �Д��Ƿ�������·��,�����,�t���ӹ���Ŀ�
                projectPath = workspace.getPath()
                fileName = os.path.join(projectPath, fileName)
            if os.path.exists(fileName) == False:
                badNodes.append(Node)
        return badNodes
    
    def FTM_FileTextureAnalyst_dirDict(self):
        '''
        �õ���filename����key���ֵ�,{filePath:(node1,node2,����)}
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
        ˢ��view��ʹ��QtviewWidget
        '''
        dirDict = self.FTM_FileTextureAnalyst_dirDict()
        badNodes = self.FTM_FileTextureAnalyst_badFileNode()

        self.ui.treeWidget.clear()          
        for filePath, fileNode in dirDict.iteritems() :
            path = QtGui.QTreeWidgetItem(self.ui.treeWidget)  # �õ�treewidget
            if filePath == "":
                path.setText(0, ' %s texture(s) NOT specified. ' % str(len(fileNode)))
                path.setText(1, 'So they are NOT exist(s).')
            else:
                path.setText(0, ' %s texture(s) point to' % str(len(fileNode)))
                path.setText(0, ' %s texture(s) point to' % str(len(fileNode)))
                path.setText(1, filePath)
                noExistNode = []  # ��¼ÿ����·����file�ڵ�����
                ExistNode = []
                if self.intersectionList(fileNode, badNodes) != 0:
                    noExistNode = self.intersectionList(fileNode, badNodes)          
                    ExistNode = self.differenceList(fileNode, badNodes)
                else:
                    ExistNode = fileNode
                             
                numnoExistNode = QtGui.QTreeWidgetItem(path)
                numnoExistNode.setText(0, ' %s of them NOT exist(s).' % str(len(noExistNode)))
                for node in noExistNode :
                    nodeID = QtGui.QTreeWidgetItem(numnoExistNode)
                    nodeID.setText(0, '%s' % str(node))
                    nodeID.setText(1, '....../%s' % os.path.split(node.ftn.get())[1])
                    
                numExistNode = QtGui.QTreeWidgetItem(path)
                numExistNode.setText(0, ' %s of them exist(s).' % str(len(ExistNode)))   
                for node in ExistNode :
                    nodeID = QtGui.QTreeWidgetItem(numExistNode)
                    nodeID.setText(0, '%s' % str(node))
                    nodeID.setText(1, '....../%s' % os.path.split(node.ftn.get())[1])
           
                        
                    

#===============================================================================
# �ļ��в�������
#===============================================================================
    def browseFloderbutton(self):
        '''
        browsebutton������dialog���õ�ѡ����ļ���
        '''
        floder = self.floderDialog()
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
