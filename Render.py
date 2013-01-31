# coding=gbk

unicode(“中文”, “gbk”)

import maya.cmds as cmds

class Render():
	"""关于渲染设置的一些东西
		1：bakeCAM 烘焙摄像机，利于渲染或者导出到Nuke里使用
	"""
	def __init__(self, arg):
		super(Render, self).__init__()
		self.arg = arg
		self.select=cmds.ls(sl=1)

	def creat_cam():
		cmds.loadUI('') #创建UI 尝试pyQT?
		scenesCameras=cmds.ls(cameras=1) #获取场景摄像机 隐藏默认摄像机？
		# 修改UI列表 显示cam
		if cmds.objExists('bakeCAM')!=1:
			cameraName=cmds.camera()
			cameraShape=cameraName[1]
			cmds.rename('cameraShape', 'bakeCAM')
			pass
	
	def bake_CAM_ani():

		sourceCAM=cmds.select('cam_hcam:shot')
		#确定UI上选择的摄像机,取得摄像机名称
		#确定烘焙范围
		cmds.listCameras( p=True ) #场景中所有透视摄像机
		cameraName = cmds.camera() #创建新摄像机
		cameraShape = cameraName[1]#获得新摄像机名称
		bakeCAMnode='baked_CAM'
		cmds.rename(cameraShape,bakeCAMnode) #修改bakecam的名字
		sourceCAMtransfer=cmds.listHistory( sourceCAM, il=1)[1]
		cmds.parentConstraint(sourceCAMtransfer, bakeCAMnode)
		cmds.select(bakeCAMnode)
		cmds.bakeSimulation(selectCam,t=(starten,ende),hi='below')
		cmds.select(bakeCAMnode)
		cmds.file(*args, **kwargs)
		
		pass
	def maxwell_renderfiles_output():
		
		pass
	pass