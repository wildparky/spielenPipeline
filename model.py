#-*- coding:utf-8 -*-

'''
Created on 2012-7-5

@author: spielen
'''
import maya.cmds as mc

class Model(object):
    '''
    对于模型本身的一些操作
    '''
    _instance = None  # Suppose there is not an instance aleardy in the mermory

    def __init__(self):
        '''
        得到所选物体的基本信息
        '''
        self.select = mc.ls(sl=1)
        
    def __new__(self, *args, **kwargs):
        # Method that returns the existing instance or create a new one for the call
        if not self._instance:
            self._instance = super(Model, self).__new__(self, *args, **kwargs)
        return self._instance
                
        
    def getBounds(self):       
        self.getBB = mc.xform(self.select, q=1, ws=1, bb=1)
        self.bbX = (self.getBB[3] + self.getBB[0]) / 2
        self.bbY = (self.getBB[4] + self.getBB[1]) / 2
        self.bbZ = (self.getBB[5] + self.getBB[2]) / 2
        self.getBB.append(self.bbX)
        self.getBB.append(self.bbY)
        self.getBB.append(self.bbZ)
        
#    def test(self):
#        Model.getBounds(self)
#        print u'obj ist %s' % self.getBB
                
    def Pivot(self, p):        
        '''
        p,区分button
        '''
        Model.getBounds(self) 
        for objP in self.select :
            objRP = objP + '.rotatePivot'
            objSP = objP + '.scalePivot' 
            if p == 0:      
                mc.CenterPivot(objP)   
            if p == 1:#world 0 0 0
                mc.move(0, 0, 0, objRP , objSP, a=1, rpr=1)
            if p == 2:#X_max
                mc.move(self.getBB[3], self.getBB[7], self.getBB[8], objRP, objSP, a=1, rpr=1)
            if p == 3:#X_min
                mc.move(self.getBB[0], self.getBB[7], self.getBB[8], objRP, objSP, a=1, rpr=1)
            if p == 4:#Y_max
                mc.move(self.getBB[6], self.getBB[4], self.getBB[8], objRP, objSP, a=1, rpr=1)
            if p == 5:#Y_min
                mc.move(self.getBB[6], self.getBB[1], self.getBB[8], objRP, objSP, a=1, rpr=1)
            if p == 6:#Z_max
                mc.move(self.getBB[6], self.getBB[7], self.getBB[5], objRP, objSP, a=1, rpr=1)
            if p == 7:#Z_min
                mc.move(self.getBB[6], self.getBB[7], self.getBB[2], objRP, objSP, a=1, rpr=1)  
    def objMove(self, m):
        '''nehmen obj nach WorldOrigin,oder B zu A,m是为了区分ui中不同的button
        '''
        if m == 0:
            for obj in self.select :
                mc.move(0, 0, 0, obj, a=1, rpr=1)
        if m == 1:
            selObjT = mc.ls(sl=1, tail=1)
            objXform = mc.xform(selObjT[0], q=1, ws=1, piv=1)
            selObj = mc.ls(sl=1)
            for objM in selObj:
                mc.move(objXform[0], objXform[1], objXform[2], objM, rpr=1, a=1)
                
    def combineShapes(self):
        
        '''
        合并物体形状节点
        '''
        mc.makeIdentity(a=1, t=1, r=1, s=1, n=0)
        mc.delete(ch=1)
        objShape = mc.listRelatives(self.select, shapes=1)
        
        for i in xrange(len(objShape) - 1):
            mc.parent(objShape[i], self.select[-1], add=1, shape=1)
            mc.delete(self.select[i])
            mc.select(self.select[-1], replace=1)
            
    def unLock(self, name):
        '''
        物体所有属性的unlock
        '''
        zero = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
        one = ['sx', 'sy', 'sz', 'v']
        for attr in zero:
            try:
                mc.setAttr('%s.%s' % (name, attr), l=0)            
            except RuntimeError:
                pass
        for attr in one:
            try:
                mc.setAttr('%s.%s' % (name, attr), l=0) 
            except RuntimeError:
                pass
            
#    def groupC(self):
#        '''
#        将物体合并成统一的组，整理场景结构
#        '''
#        if mc.objExists('__M') == 0:
#            mc.group(em=1, n='__M')
##        Mseh = mc.ls(typ='mesh')
#        Mesh=self.select
#        for num in range(10):
#            mc.PickWalkUp()
#        mc.Group()
#        print Mesh
#            

            
class ModelWindow(Model):
    
    # Defining the main elements of ui #
    
    windowName = 'ModelWindow'   
    layoutname='dock'
    _UI_File =mc.internalVar(userScriptDir=True) + 'tool/model.ui'
    
    def __new__(self):
        # Create only one instance of the class and return it after #
        if not self._instance:
            self._instance = super(ModelWindow, self).__new__(self)
            return self._instance
        else:
            return self._instance     
    
    def __init__(self):      
        if mc.layout(self.layoutname, query=True, exists=True) == True:
            mc.deleteUI(self.layoutname, lay=True)
        if mc.layout(self.layoutname, query=True, exists=True) != True:
            self.windowName = mc.loadUI(f=self._UI_File)
            mc.showWindow(self.windowName)

            allowedAreas = ['right', 'left']
            self.layout=mc.dockControl(area='right', content=self.windowName, l='SP_2012', w=390, h=490, allowedArea=allowedAreas)
            self.layoutname=mc.dockControl(self.layout,q=1,fpn=1)


            
#======================= If the code is runinig directly create the main UI =====================#
if __name__ == '__main__':
    ModelWindow()
