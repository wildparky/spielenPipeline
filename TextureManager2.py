'''
Created on 2013-1-25

Function:
��FileTextureManager.melת��Ϊpython�汾(�ʵ�����),ͬʱѧϰpy
 
@author: :     Yuan Wang
@version: :    0.1
@contact: :    play.wang1988@gmail.com
'''
# coding=gbk

from pymel.core import *
import os

class TextureManager(object):
    '''
    classdocs
    '''  
    textureNodes = {}  # ���Node����ͼ·��,key:node value:filename
    texturePaths = []  # ���������ͼ��·��
    fileNodes = ls(type='file')
    for fileNode in fileNodes:
        fileName = fileNode.ftn.get()
        if fileName == '':
            delete(fileNode)
            continue
        textureNodes.setdefault(fileNode, fileName)  # �����ֵ�
        Path = os.path.dirname(fileNode)
        texturePaths.append(Path)
    texturePaths = sorted(set(texturePaths), key=texturePaths.index)
    
    def __init__(selfparams):
        '''
        Constructor
        '''





    def FTM_SelCheck(self, Node):
        '''
        �ж��Ƿ�ѡ����file�ڵ�
        :param Node:�ڵ�
        '''
        sel = 0
        if len(Node):
            sel = 1
        else:     
            confirmDialog(title='File Texture Manager', message='����ѡ��һ����ͼ�ļ�!', button=['ok'])
        return sel
    
    def FTM_End(self):
        '''
        ����ʹ�����������.
        '''
        confirmDialog(title='File Texture Manager', message='�������.\n����ο�Script Editor.', messageAlign='center', button=['ok'])
    
    def FTM_log(self, type, Node, log):
        '''
        �ṩlog,��Script����ʾ
        :param type:
        :param Node:
        :param log:
        '''
        if len(Node):
            log = Node + '\n'
        else:
            log = '\t' + log + '\n'
        if type == 'start':
            finlog = '\n---------------------------------------------------------------------------------------------------------------\n\
    File Texture Manager Log starts...\n\
    ---------------------------------------------------------------------------------------------------------------\n'
        elif type == 'end':
            finlog = '---------------------------------------------------------------------------------------------------------------\n\
    File Texture Manager Log ends...\n\
    ---------------------------------------------------------------------------------------------------------------\n'
        else:
            finlog = log
        print finlog
    #===============================================================================
    # �������?��
    #===============================================================================
    def FTM_FileTextureFind(self):
        '''
        ����������file��ͼ�ļ�,ͬʱ�Զ�ɾ��δʹ�õ�fileNode
        '''
        
        textureNodes = {}  # ���Node����ͼ·��
        
        fileNodes = ls(type='file')
        if len(fileNodes):
            for fileNode in fileNodes:
                fileName = fileNode.ftn.get()
                if fileName == '':
                    delete(fileNode)
                    continue
                textureNodes.setdefault(fileNode, fileName)  # �����ֵ�,key:node value:filename
            return textureNodes
        else:
            confirmDialog(title='File Texture Manager', message='������û��File�ڵ�', button=['ok'])
    
    def FTM_FileTextureAnalyst_dir(self):
        '''
        ���?���е���ͼ�ļ�.�����ļ��е�����
        '''
        textureNodes = FTM_FileTextureFind()
        texturePaths = []
        dirPaths = []
        for fileName in textureNodes.values():
            texturePaths.append(fileName)  # �õ��ļ�·�����ļ���
            
        for path in texturePaths:
            dirPath = os.path.dirname(path)
            dirPaths.append(dirPath)  # ��ȡ�ļ�·��
        
        dirPaths = sorted(set(dirPaths), key=dirPaths.index)  # ȥ���ظ� dirPaths=list(set(dirPaths))
        return dirPaths
    
    def FTM_FileTextureAnalyst_badFileNode(self):
        '''
        �ҳ���ͼ��ʧ��fileNode
        '''
        textureNodes = FTM_FileTextureFind()
        badNodes = []
        for Node, fileName in textureNodes.items():
            if os.path.isabs(fileName) == False:  # �Д��Ƿ�������·��,�����,�t���ӹ���Ŀ�
                projectPath = workspace.getPath()
                fileName = os.path.join(projectPath, fileName)
            if os.path.exists(fileName) == False:
                badNodes.append(Node)
        return badNodes
    
    # badNodes �Ϊ��г�\��������ļ�����Ŀ䛷��
    def FTM_FileTextureAnalyst_badDirpath(self):
        '''
        �õ��e�`�N�D���ļ�·��
        '''
        badNodes = FTM_FileTextureAnalyst_badFileNode()
        textureNodes = FTM_FileTextureFind()
        badDirpath = []
        for fileNode, fileName in textureNodes.items() :
            for badNode in badNodes :
                if badNode == fileNode:
                    Dir = os.path.dirname(fileName)
                    badDirpath.append(Dir)
        return badDirpath
    
    def FTM_FileTextureAnalyst_dirDict(self):
        '''
        �õ���filename����key���ֵ�,{fileName:(node1,node2)}
        '''
        textureNodes = FTM_FileTextureFind()
        dirPaths = FTM_FileTextureAnalyst_dir()
        dirDict = {}
        for path in dirPaths:
            nodes = []
            for fileNode, fileName in textureNodes.items():
                if path == os.path.dirname(fileName):
                    nodes.append(fileNode)
            dirDict.setdefault(path, nodes)
        return dirDict  
    
    #===============================================================================
    # �ļ���������
    #===============================================================================
    def FTM_FileTexture_setNode(self, nodes, path):
        '''
        �O��filenode��ֵ
        :param nodes:�x�е�filenode
        :param path:Ŀ��·��
        '''
        textureNode = FTM_FileTextureFind()
        for node in nodes :
            textureName = os.path.basename(textureNode[node])
            neuPath = os.path.join(path, textureName)       
            node.ftn.set(neuPath, typ='string')
#===============================================================================
# 
#===============================================================================
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSignature

class Ui_formDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        uic.loadUi("form.ui", self)        #form.ui  为QT界面文件 QListWidget对象名为 listView1
        self.listDataBind()                  #添加QListWidgetItme
        self.listView1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)   #定义右键菜单
        
    def listDataBind(self):
        item = ['OaK','Banana','Apple','Orange','Grapes','Jayesh']
        for lst in item:
            self.listView1.addItem(QtGui.QListWidgetItem(lst))
   
    #激活菜单事件
    @pyqtSignature('QPoint')
    def on_listView1_customContextMenuRequested(self, point):
        item = self.listView1.itemAt(point)
        #空白区域不显示菜单
        if item != None:
           self.rightMenuShow()

    #创建右键菜单
    def rightMenuShow(self):
        rightMenu = QtGui.QMenu(self.listView1)
        removeAction = QtGui.QAction(u"删除", self, triggered=self.close)       # triggered 为右键菜单点击后的激活事件。这里slef.close调用的是系统自带的关闭事件。
        rightMenu.addAction(removeAction)
        
        addAction = QtGui.QAction(u"添加", self, triggered=self.addItem)       # 也可以指定自定义对象事件
        rightMenu.addAction(addAction)
        rightMenu.exec_(QtGui.QCursor.pos())
       
    def addItem(self):
        pass
#===============================================================================
# 
#===============================================================================

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


