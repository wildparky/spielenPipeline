#-*- coding:utf-8 -*-
'''
Created on 2012-8-18

@author: spielen
'''
import os
import time


class File(object):
    '''
    对于工程文件夹的整理。
    包涵以下功能：
        clearDir()：找到包涵.mb(也可以是别的格式的文件)文件的所有文件夹,
        并将之前版本的文件转移到 deleted/日期 文件夹中，例如 deleted/2012-08-27
                
                
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.mbDir = []
        self.targetDir = os.path.abspath(os.getcwd()) + os.sep + 'lib'
        self.getDir = os.path.abspath(os.getcwd())
        
        
    def clearDir(self, fileFormat='.mb', kDir=1, cFile=1):
        '''       
        运行参数 ：
                    kDir 是否显示完整路径 
                                    0：否 1：是
                    cFile 是否清理早期版本文件 
                                    0：否 1：是
                    默认 kDir=1, cFile=1
        '''
        print self.time
        if cFile == 1:
#            创建备份文件夹 deleted                            
            if os.path.exists(self.getDir + os.sep + 'deleted' + os.sep + self.time) == 0:
                os.makedirs('deleted' + os.sep + self.time)  
                      
        for i in os.walk(self.targetDir):

#    在当前py脚本所在的文件夹中搜索需要的文件格式 
            for file in os.listdir(i[0]):    
                if os.path.splitext(file)[1] == fileFormat:
                    self.mbDir.append(str(i[0])) 
                    self.mbDir = sorted(set(self.mbDir), key=self.mbDir.index)
                    
        for dir in self.mbDir:
            print '  '
            if kDir == 1:               
                print  dir.replace(self.targetDir, '')
            else:
                print  dir   
                          
            numFile = []
            for workfile in os.listdir(dir):          
                if os.path.splitext(workfile) [1] == fileFormat:
                    numFile.append(workfile)                                      
                    print workfile 
                      
            if cFile == 1:


                if len(numFile) != 1:
#                    neudelDir = dir.replace(self.targetDir, '')
                    if os.path.exists(self.getDir + os.sep + 'deleted' + os.sep + self.time + dir.replace(self.targetDir, '')) == 0:
                        os.makedirs(self.getDir + os.sep + 'deleted' + os.sep + self.time + dir.replace(self.targetDir, ''))                       
                    for delFile in numFile[0:-1]:
                        os.rename(dir + os.sep + delFile, self.getDir + os.sep + 'deleted' + os.sep + self.time + dir.replace(self.targetDir, '') + os.sep + delFile)
                    os.rename(dir + os.sep + numFile[-1], dir + os.sep + os.path.splitext(numFile[-1])[0][0:-4] + '0001' + fileFormat) 
                    
                         
                                    
            
        


File().clearDir()
