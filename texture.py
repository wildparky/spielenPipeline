#coding:utf-8
'''
Created on 2012-7-6

@author: spielen
'''
import maya.cmds as mc
import os

class Texture(object):
    '''
    对于场景贴图的处理
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.sceneName = mc.file(q=1, sn=1)
        self.workSpace = mc.workspace(q=1, rd=1)
        self.texture='textures'
        self.dirName = os.path.splitext(os.path.split(self.sceneName)[1])[0][0:-16]
    
    def creatSTD(self):
        '''
        
        creatSTD=creat Scence Texture Dir 创建场景的贴图文件夹，根据场景名，在工程目录的texture文件夹下自动创建新文件夹
        '''
        if not os.path.exists(self.workSpace+self.texture+os.sep+self.dirName):
            os.makedirs(os.path.normpath(self.workSpace+self.texture+os.sep+self.dirName+os.sep))

        print '------ %s ------' %(os.path.normpath(self.workSpace+self.texture+os.sep+self.dirName+os.sep))
            
        
#======================= If the code is runinig directly create the main UI =====================#
if __name__ == '__main__':
    Texture().creatSTD()