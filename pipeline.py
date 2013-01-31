# coding=gbk
unicode(“中文”, “gbk”)
'''
Created on 2012-7-8

@author: spielen
'''
import sys
import os
import maya.cmds as mc
import maya.mel as mel



mayaVersion = '2012-x64'

class Spielen(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.spielenPath = os.path.normpath(mayautils.getUserScriptsDir()) + os.sep + 'spielenPipeline'
        self.sceneName = system.sceneName()  
        self.proj = Workspace.getPath()

        
    def creatWorkspaceUI(self):
        import time
        UI = cmds.loadUI(f='D:/Arbeit/meine_kuaipan/Document/eclipse_work/maya/spielenPipeline/UI/creatProject.ui')
        mc.showWindow(UI)
        jeztZeit = time.strftime("%Y-%m-%d", time.localtime())
        textField('project_3', e=1, tx=jeztZeit)
        textField('project_4', e=1, tx=jeztZeit)
        pass

    def creatWorkspace(self):
        '''
        获取项目名称与路径
        创建Folder
        指定工程目录
        设定所对应的文件夹
            pValueList[0:13] ______project_0 项目名称 中
                                 |_project_1 项目名称 EN
                                 |_project_2 工程目录
                                 |_project_3 启动日期
                                 |_project_4 截止日期
                                 |_project_5 master
                                 |_project_6 workshop
                                 |_project_7 asset library
                                 |_project_8 scenes library
                                 |_project_9 shot library
                                 |_project_10 scripts
                                 |_project_11 texture
                                 |_project_12 particles
        '''
        if len(textField('project_1', q=1, tx=1)) != 0 and len(textField('project_2', q=1, tx=1)) != 0:
            pValueList = []
            for x in xrange(13):
                x = str(x)
                textFieldValue = 'project_' + x
                pValue = textField(textFieldValue, q=1, tx=1)
                pValueList.append(pValue)
     
            for x in pValueList[7:13]:
                folder = pValueList[2] + os.sep + x
                os.makedirs(folder)
                pass

            Workspace.chdir(pValueList[2])            
            pass

    def getpPath(self, qName):
        '''
        获取目标文件夹的路径
        qName : 1 project_1 ----工程目录
        '''
        textPath = fileDialog2(fileMode=3, caption="spielenPipeline", dialogStyle=1) #dialogStyle: 1--win或者mac os风格 2--maya默认风格
        
        if qName == 'project_2' :
            textField(qName, e=1, tx=textPath[0] + os.sep + textField('project_1', q=1, tx=1))
            
        pass
        
import xml