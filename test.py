#-*- coding:utf-8 -*-
'''
Created on 2012-7-31

@author: spielen
'''
from pymel.core import *

class test(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self.select = selected()
        
    def toMaxwellshader(self):
        '''
        将所选择的材质转换为maxwell的材质
        '''
#        tfile = listConnections(self.select)[0]
        slShader=listConnections(self.select,type='shadingEngine')
        objs=listConnections(slShader,type='mesh')
        for obj in objs:
            select(obj,add=1)
        mel.eval('maxwellCreateMaterial 0;')
        

            


            
#        
#        if len(self.select) > 1 :
#            shapeList = listRelatives(self.select[0], ad=1, pa=1, type='surfaceShape')
#            shapeList = sorted(set(shapeList), key=shapeList.index) #去除列表中的重复元素
#            sg = listConnections(self.select, type='shadingEngine')
#        else:
#            shapeList = listRelatives(self.select, ad=1, pa=1, type='surfaceShape')
#            shapeList = sorted(set(shapeList), key=shapeList.index) #去除列表中的重复元素
#            sg = listConnections(self.select, type='shadingEngine')
#        mShader=listHistory(sg[0])
#        print mShader
#        
#        mfile = listHistory(sg)

if __name__ == '__main__':
    test().toMaxwellshader()