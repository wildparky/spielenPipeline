#-*- coding:utf-8 -*-

'''
Created on 2012-10-22
@author: spielen
'''
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
import sys
from test.test_iterlen import len

patha = 'c:/testa.xml'
pathb = 'c:/testb.xml'

def creat_xml(out_path):
	'''
	创建xml文件，并创建root节点，设置注释与版本信息
	@param root_name:root节点名称
	@param description:注释
	'''
	root = Element('spielenPipeline')
	project = SubElement(root, 'projectDate')
	project.text = unicode('工程文件管理' , "gbk")
	author = SubElement(root, 'author')
	author.text = unicode('工作室人员' , "gbk")
	write_xml(root, out_path)

	
def read_xml(in_path):
	'''
	读取并解析xml文件
	@param in_path:xml文件路径
	return:ElementTree
	'''
	tree = ElementTree()
	tree.parse(in_path)
	root = tree.getroot()
	return tree, root
	pass

def write_xml(root, out_path):
	'''
	将文件写出
	@param root:根节点
	@param out_path:写出路径
	'''
	tree = ElementTree(root)
	tree.write(out_path, encoding="utf-8")

def prettify_xml(elem):
    rough_string = tostring(elem, 'utf-8') #要转化的xml文件
    reparsed = minidom.parseString(rough_string) 
    return reparsed.toprettyxml(indent="  ") #美化显示xml
	
def if_match(node, map):
	'''
	判断某个节点是否包含所有传入参数属性
	@param node:节点
	@param map:属性.数组
	'''
	for key in map:
		if node.get(key) != map.get(key):
			return False
	return True #疑惑！ retur的位置

##---------------search-----------------

def find_nodes(tree, path):
	'''
	查找某个路径所匹配的所有节点
	@param tree:xml树
	@param path:节点路径
	'''
	return tree.findall(path)

def get_node_by_keyvalue(nodelist, map):
	'''
	根据属性及属性值定位符合的节点，返回节点
	@param nodelist:节点类表
	@param map:匹配属性及属性值
	'''
	result_nodes = []
	for node in nodelist:
		if if_match(node, map):
			result_nodes.append(node)
	return result_nodes

##---------------change-----------------

def chage_node_properties(nodelist, map, is_delete=False):
	'''
	修改/增加/删除 节点的属性以及属性值
	@param nodelist:节点列表
	@param map:属性以及属性值
	@param is_delete:是否删除
	'''
	for node in nodelist:
		for key in map:
			if is_delete:
				if key in node.attrib:
					del node.attrib[key]
				else:
					node.set(key, map.get(key))
					
def change_node_text(nodelist, text, is_add=False, is_delete=False):					
	'''
	改变/增加/删除 节点的文本
	@param nodelist:节点列表
	@param text:最终文本
	@param is_add:
	@param is_delete: 
	'''
	for node in nodelist:
		if is_add:
			node.text += text
		elif is_delete:
			node.text = ''
		else:
			node.text = text

def create_node(parent, tag, content='',):
	'''
	创建一个新节点
	@param parent:父节点 
	@param tag:子节点标签
	@param content:节点闭合标签里的文本内容
	'''
	element = SubElement(parent, tag)
	if len(content) != 0:
		element.text = unicode(content , "gbk") #unicode转换
	return element

def create_node_attrib(parent, tag, attrib, content=''):
	'''
	创建一个新节点,带有属性
	@param parent:父节点 
	@param tag:子节点标签
	@param attrib:属性及属性值 z.B={'NUM':'123'}
	@param content:节点闭合标签里的文本内容
	'''
	element = SubElement(parent, tag, attrib)
	if len(content) != 0:
		element.text = unicode(content , "gbk") #unicode转换
	return element

def add_child_node(nodelist, element):
	'''
	给一个节点添加子节点
	@param nodelist:节点列表
	@param element:子节点
	'''
	for node in nodelist:
		node.append(element)

def del_node_by_tagekeyvalue(nodelist, tag, map):
	'''
	通过属性以及属性值定位一个节点，并删除
	@param nodelist:父节点列表
	@param tag:子节点列表
	@param map:属性及属性值
	'''
	for parent_node in nodelist:
		children = parent_node.getchildren()
		for child in children:
			if child.tag == tag and if_match(child, map):
				parent_node.remove(child)
