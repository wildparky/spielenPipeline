
'''
Created on 2012-7-12

@author: spielen
'''
import maya.cmds as cmds
from pymel.core import *


class Shader():
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self.sl = selected()




    def toArnoidshader(self):
        '''
        将所选择的材质转换为Arnoidshader
        '''
        for shader in selected():
            shadingEngine = listConnections(shader, type='shadingEngine')
            if nodeType(shadingEngine[0])=='shadingEngine':
                objs = listConnections(shadingEngine[0] , type='mesh')
                for obj in objs :
                    select(obj,add=1) 
                createNode('aiStandard',n=shader+'_ard') #这样创建的aiStandard材质不会再Hy中显示
                print 'ok'



    
    def FilterNodeType(self, type):
        '''
        
        返回所选择物体的shader，也可以直接选择shader
        '''
        outputNodeList = []
        for input in self.sl :
            inputType = cmds.nodeType(input)
            if inputType == type:     
                outputNodeList.append(input) 
            elif inputType == 'transform' or inputType == "mesh" or inputType == "nurbsSurface" :
                shapeList = cmds.listRelatives(input, ad=1, pa=1, type='surfaceShape')
                shapeList = sorted(set(shapeList), key=shapeList.index) #去除列表中的重复元素
                for shape in shapeList:
                    sg = cmds.listConnections(shape, type='shadingEngine')
                    if sg[0] != 'initialShadingGroup' and len(sg):
                        shadingNetwork = cmds.listHistory(sg[0], pdo=1)
                        if len(shadingNetwork):
                            for outputNode in shadingNetwork:
                                if cmds.nodeType(outputNode) == type:
                                    outputNodeList.append(outputNode) 
            else:
                shadingNetwork = cmds.listHistory(input, pdo=1)
                if len(shadingNetwork):
                    for outputNode in shadingNetwork:
                        if cmds.nodeType(outputNode) == type:
                            outputNodeList.append(outputNode) 
            self.outputNodeList = sorted(set(outputNodeList), key=outputNodeList.index)
    
    def createMia(self, shadername):
        mia = cmds.shadingNode('mia_material_x', n=shadername + '_mia', asShader=1)
#        setAttr(mia+'.brdf_0_degree_refl',1)
#        setAttr(mia+'.skip_inside_refl',1)
#        setAttr(mia+'.refr_ior',1)
#        setAttr(mia+'.brdf_conserve_energy',0)

    def copyAttribute(self, src, dest):
        srcSplit = src.split('.')
        srcNode = srcSplit[0]
        srcAttr = srcSplit[1]
        srcScalar = cmds.listAttr(src, s=1)
#        print srcScalar
        
        destSplit = src.dest('.')
        destNode = destSplit[0]
        destAttr = destSplit[1]
        destScalar = cmds.listAttr(dest, s=1)
#        print destScalar
        if cmds.attributeQuery(n=srcNode, uac=srcAttr) and cmds.connectionInfo(src, id=1):
            inputNode = cmds.connectionInfo(src, sfd=1)
            cmds.connectAttr(inputNode, dest, f=1)
        else:
            for i in range(len(srcScalar)) :
                if cmds.connectionInfo(srcNode + '.' + srcScalar[i], id=1):
                    inputNode = cmds.connectionInfo(srcNode + '.' + srcScalar[i], sfd=1)
                    cmds.connectAttr(inputNode, srcNode + '.' + srcScalar[i], sfd=1, f=1)
                else:
                    srcValue = (srcNode + '.' + srcScalar[i]).get()
                    (destNode + '.' + destScalar[i]).set(srcValue)
                    


   
                
    def toMaxwellshader(self):
        '''
        将所选择的材质转换为maxwell的材质
        '''
        texFile = cmds.listConnections(cmds.selected(), type='file')
        slShader = cmds.listConnections(cmds.selected(), type='shadingEngine')
        objs = cmds.listConnections(slShader, type='mesh')
        for obj in objs:
            cmds.select(obj, add=1)
        mel.eval('maxwellCreateMaterial 0;')
        maxwellshader = cmds.listConnections(cmds.listRelatives(cmds.selected(), ad=1, pa=1, type='surfaceShape'), type='shadingEngine')
        maxwellshader = sorted(set(maxwellshader), key=maxwellshader.index) #去除列表中的重复元素
        cmds.connectAttr((texFile[0] + '.outColor'), ((cmds.listConnections(cmds.listConnections(cmds.listConnections(maxwellshader, type='maxwellLayeredMaterial')[0])[0])[0]) + '.refl0'), f=1)

#        tfile = listConnections(self.sl)[0]
#        hyperShade(o=self.sl)
#        mel.eval('maxwellCreateMaterial 0;')
#        sg=[]
#        if len(self.sl) > 1 :
#            shapeList = listRelatives(self.sl[0], ad=1, pa=1, type='surfaceShape')
#            shapeList = sorted(set(shapeList), key=shapeList.index) #去除列表中的重复元素
#            sg = listConnections(self.sl, type='shadingEngine')[0]
#        else:
#            shapeList = listRelatives(self.sl, ad=1, pa=1, type='surfaceShape')
#            shapeList = sorted(set(shapeList), key=shapeList.index) #去除列表中的重复元素
#            sg = listConnections(self.sl, type='shadingEngine')[0]
#        mShader=listHistory(sg[0])[1]
#        print mShader
#        
#        mfile = listHistory(sg)
        
        
        
        
        
#connectAttr -force file1.outColor maxwellBsdf32.refl0; 



 
#    def delightShader(self):
#        '''
#        3deligt的一个shader，支持PTC，自动linework
#        '''
#        shader_path = 'C:/Program Files/3Delight/shaders/dProduction.sdl'
#        Shader().FilterNodeType()
#        for selShader in self.outputNodelist:
#            mel.hyperShade(objects=selShader)
#            selObj = selected()
#            surface_shader = mel.DL_createSurfaceShader(shader_path, 0)
#            mel.DL_setAssignmentPanelAttrib(selObj, "surface", surface_shader)
            
s=Shader()