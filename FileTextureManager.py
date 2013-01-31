# coding=gbk
"""
Function:
将FileTextureManager.mel转化为python版本(适当改造),同时学习py
 
Author:     Yuan Wang
Version:    19-01-2013
Contact:    play.wang1988@gmail.com
"""
from pymel.core import *
import os


def FTM_SelCheck(Node):
    '''
    判断是否选择了file节点
    :param Node:节点
    '''
    sel = 0
    if len(Node):
        sel = 1
    else:     
        confirmDialog(title='File Texture Manager', message='至少选择一个贴图文件!', button=['ok'])
    return sel

def FTM_End():
    '''
    提醒使用者任务完成.
    '''
    confirmDialog(title='File Texture Manager', message='处理完成.\n详情参考Script Editor.', messageAlign='center', button=['ok'])

def FTM_log(type, Node, log):
    '''
    提供log,在Script中显示
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
# 場景整理部分
#===============================================================================
def FTM_FileTextureFind():
    '''
    搜索场景中file贴图文件,同时自动删除未使用的fileNode
    '''
    
    textureNodes = {}  # 存放Node与贴图路径
    
    fileNodes = ls(type='file')
    if len(fileNodes):
        for fileNode in fileNodes:
            fileName = fileNode.ftn.get()
            if fileName == '':
                delete(fileNode)
                continue
            textureNodes.setdefault(fileNode, fileName) #創建字典,key:node value:filename
        return textureNodes
    else:
        confirmDialog(title='File Texture Manager', message='场景中没有File节点', button=['ok'])

def FTM_FileTextureAnalyst_dir():
    '''
    整理场景中的贴图文件.整理文件夹的数量
    '''
    textureNodes = FTM_FileTextureFind()
    texturePaths = []
    dirPaths = []
    for fileName in textureNodes.values():
        texturePaths.append(fileName)  # 得到文件路径与文件名
        
    for path in texturePaths:
        dirPath = os.path.dirname(path)
        dirPaths.append(dirPath)  # 提取文件路径
    
    dirPaths = sorted(set(dirPaths), key=dirPaths.index)  # 去除重复 dirPaths=list(set(dirPaths))
    return dirPaths

def FTM_FileTextureAnalyst_badFileNode():
    '''
    找出贴图丢失的fileNode
    '''
    textureNodes = FTM_FileTextureFind()
    badNodes = []
    for Node, fileName in textureNodes.items():
        if os.path.isabs(fileName) == False: #判斷是否是相對路徑,如果是,則增加工程目錄
            projectPath = workspace.getPath()
            fileName = os.path.join(projectPath, fileName)
        if os.path.exists(fileName) == False:
            badNodes.append(Node)
    return badNodes

#badNodes 單獨列出\其他的正常文件按照目錄分類
def FTM_FileTextureAnalyst_badDirpath():
    '''
    得到錯誤貼圖的文件路徑
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
    得到以filename作爲key的字典,{fileName:(node1,node2)}
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
# 文件操作部分
#===============================================================================
def FTM_FileTexture_setNode(nodes,path):
    '''
    設置filenode的值
    :param nodes:選中的filenode
    :param path:目標路徑
    '''
    textureNode=FTM_FileTextureFind()
    for node in nodes :
        textureName=os.path.basename(textureNode[node])
        neuPath=os.path.join(path,textureName)       
        node.ftn.set(neuPath,typ='string')
    
        
