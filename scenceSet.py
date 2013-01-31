#-*- coding:utf-8 -*-
'''
Created on 2012-7-22

@author: spielen
'''
import maya.cmds as mc
from pymel.core import *

class scenceSet():
    '''
    一些对于场景的设定与整理功能
    1：clearSceneNames：清理场景

    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.listObject=ls(o=1)
        self.sl=selected()
    
    def clearSceneNames(self):
        '''
        清除场景中物体多余的前缀，例如：pasted__ pasted__: selected
        同时清理未使用的shader，layder以及render layer
        '''
        for i in range(len(self.listObject)-1):
            if objExists(self.listObject[i]):
                if referenceQuery(self.listObject[i],inr=1)==0:
                    lockNode(self.listObject[i],lock=0)
        select(all=1,hierarchy=1)
        for i in range(10):
            mel.eval('searchReplaceNames "pasted__" "pasted__:" "selected";')
        select(cl=1)
        mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
        mel.eval('layerEditorSelectUnused;')
        mel.eval('layerEditorDeleteLayer "";')
        mel.eval('renderLayerEditorDeleteUnused RenderLayerTab;')
#        mc.DeleteHistory()


    def remRef(self):
        '''
        移除所选择的ref物体（2013版貌似自带这个功能）
        '''
        for eachRef in self.sl :
            if referenceQuery(eachRef,inr=1):
                refName = referenceQuery(eachRef,f=1)
                mc.file(refName,rr=1)
            else:
                mc.error('选择Reference')
                
sc=scenceSet()

if __name__ == '__main__':
    sc.clearSceneNames()
