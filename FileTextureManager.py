# coding=gbk
"""
Function:
��FileTextureManager.melת��Ϊpython�汾(�ʵ�����),ͬʱѧϰpy
 
Author:     Yuan Wang
Version:    19-01-2013
Contact:    play.wang1988@gmail.com
"""
from pymel.core import *
import os


def FTM_SelCheck(Node):
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

def FTM_End():
    '''
    ����ʹ�����������.
    '''
    confirmDialog(title='File Texture Manager', message='�������.\n����ο�Script Editor.', messageAlign='center', button=['ok'])

def FTM_log(type, Node, log):
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
# ����������
#===============================================================================
def FTM_FileTextureFind():
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
            textureNodes.setdefault(fileNode, fileName) #�����ֵ�,key:node value:filename
        return textureNodes
    else:
        confirmDialog(title='File Texture Manager', message='������û��File�ڵ�', button=['ok'])

def FTM_FileTextureAnalyst_dir():
    '''
    �������е���ͼ�ļ�.�����ļ��е�����
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

def FTM_FileTextureAnalyst_badFileNode():
    '''
    �ҳ���ͼ��ʧ��fileNode
    '''
    textureNodes = FTM_FileTextureFind()
    badNodes = []
    for Node, fileName in textureNodes.items():
        if os.path.isabs(fileName) == False: #�Д��Ƿ�������·��,�����,�t���ӹ���Ŀ�
            projectPath = workspace.getPath()
            fileName = os.path.join(projectPath, fileName)
        if os.path.exists(fileName) == False:
            badNodes.append(Node)
    return badNodes

#badNodes �Ϊ��г�\�����������ļ�����Ŀ䛷��
def FTM_FileTextureAnalyst_badDirpath():
    '''
    �õ��e�`�N�D���ļ�·��
    '''
    badNodes=FTM_FileTextureAnalyst_badFileNode()
    textureNodes=FTM_FileTextureFind()
    badDirpath=[]
    for fileNode,fileName in textureNodes.items() :
        for badNode in badNodes :
            if badNode==fileNode:
                Dir=os.path.dirname(fileName)
                badDirpath.append(Dir)
    return badDirpath

def FTM_FileTextureAnalyst_dirDict():
    '''
    �õ���filename����key���ֵ�,{fileName:(node1,node2)}
    '''
    textureNodes=FTM_FileTextureFind()
    dirPaths=FTM_FileTextureAnalyst_dir()
    dirDict={}
    for path in dirPaths:
        nodes=[]
        for fileNode,fileName in textureNodes.items():
            if path == os.path.dirname(fileName):
                nodes.append(fileNode)
        dirDict.setdefault(path,nodes)
    return dirDict  

#===============================================================================
# �ļ���������
#===============================================================================
def FTM_FileTexture_setNode(nodes,path):
    '''
    �O��filenode��ֵ
    :param nodes:�x�е�filenode
    :param path:Ŀ��·��
    '''
    textureNode=FTM_FileTextureFind()
    for node in nodes :
        textureName=os.path.basename(textureNode[node])
        neuPath=os.path.join(path,textureName)       
        node.ftn.set(neuPath,typ='string')
    
        
