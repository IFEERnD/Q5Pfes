#!/usr/bin/env python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------
#	v5pfes_dialogs - Dialog classes for v5pfes
#
#	begin				: 21/03/2020
#	copyright			: (c) 2020 by IFEE
#	email				: ifee@ifee.edu.vn
# --------------------------------------------------------
import csv
import math
import os.path
import operator
import sys
import time
import shutil
import re
import glob
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QDir
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.core import QgsProject, Qgis, QgsApplication
from PyQt5.QtSql import *
from osgeo import ogr
import pandas as pd
import numpy as np
import decimal
import xlrd
from collections import OrderedDict
import simplejson as json
import json
from json import *

# Initialize Qt resources from file resources.py
import psycopg2
import socket
import subprocess
from subprocess import Popen
import os

# Import the code for the dialog
import os.path
import processing

from qgis.core import *
import qgis.utils
from qgis.utils import iface
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .v5pfes_library import *
from PyQt5.QtGui import QIntValidator
#from PyQt6.QtGui import QIntValidator


#from .spilit_layer_dialog import SplitByAttributesDialog

from qgis.gui import QgsMessageBar
import pathlib
from pathlib import Path


sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/forms")
from Dlg_DownloadDBR import *
from Dlg_ChuanHoaDBR import *
from Dlg_XayDungCTDL import *
from Dlg_CapNhatVCT import *
from Dlg_CapNhatDTCT import *
from Dlg_XayDungCSDL import *
from Dlg_XuatBieuNhom1 import *
from Dlg_XuatBieuNhom2 import *
from Dlg_CapNhatDG import *

class DownloadDBR_Dlg(QDialog, Ui_Dialog_DownloadDBR):

	def __init__(self, iface):
		QDialog.__init__(self)
		self.iface = iface
		self.setupUi(self)
		self.btn_checkcon.clicked.connect(self.check_conn)
		self.btn_start.clicked.connect(self.start_db)
		self.btn_stop.clicked.connect(self.stop_db)
		self.btn_browse.clicked.connect(self.save_as)
		self.btn_download.clicked.connect(self.checkRun)
		self.inHost.clear()
		self.inHost.addItems(['LOCAL', 'VNFOREST'])
		self.inHost.currentIndexChanged.connect(self.set_defauled)
		self.inPort.setText("5433")
		self.inUsername.setText("postgres")
		self.inPassword.setText("vidagis")
		self.outPath.setText('')										 
		self.inProvince.currentIndexChanged.connect(self.laydanhsachhuyen)
		self.inDistrict.currentIndexChanged.connect(self.laydanhsachxa)
		self.outProjection.setCrs(QgsCoordinateReferenceSystem('EPSG:3405'))
		self.laydanhsachtinh()
		self.laydanhsachhuyen()
		self.laydanhsachxa()

	def check_conn(self):
	  # Check postgres is running
		inhost = self.set_defauled()["host"]
		inport = self.inPort.text()
		indatabase = "data_forest"
		inuser = self.inUsername.text()
		inpass = self.inPassword.text()
		try:
			conn = psycopg2.connect(database = indatabase, user = inuser, password= inpass, host = inhost, port= inport)
			cursor = conn.cursor()
			self.btn_start.setEnabled(False)
			self.btn_stop.setEnabled(True)
			self.iface.messageBar().pushMessage("Đã kết nối đến máy chủ " + inhost, level=Qgis.Success, duration=5)
		except:
			self.btn_start.setEnabled(True)
			self.btn_stop.setEnabled(False)
			self.iface.messageBar().pushMessage("Chưa kết nối đến máy chủ " + inhost, level=Qgis.Warning, duration=5)

	def start_db(self):
		inhost = self.set_defauled()["host"]
		start_dir = QFileDialog.getExistingDirectory(caption="Choose Postgres folder",directory="",options=QFileDialog.ShowDirsOnly)
		start_part = f'{start_dir}/startlocaldb.bat'
		subprocess.Popen(start_part, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		self.btn_start.setEnabled(False)
		self.btn_stop.setEnabled(True)
		self.iface.messageBar().pushMessage("Đã kết nối đến máy chủ " + inhost, level=Qgis.Success, duration=5)

	def stop_db(self):
		inhost = self.set_defauled()["host"]
		start_dir = QFileDialog.getExistingDirectory(caption="Choose Postgres folder",directory="",options=QFileDialog.ShowDirsOnly)
		start_part = f'{start_dir}/stoplocaldb.bat'
		subprocess.Popen(start_part, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		self.btn_start.setEnabled(True)
		self.btn_stop.setEnabled(False)
		self.iface.messageBar().pushMessage("Đã ngắt kết nối đến máy chủ " + inhost, level=Qgis.Warning, duration=5)

	def save_as(self):
		dir = QFileDialog.getSaveFileName(caption="v5PFES-Chọn thư mục lưu kết quả tải về",directory = "", filter= "Shape file(*.shp)", options = QFileDialog.Options() )[0]
		self.outPath.setText(dir)

	def checkRun(self):
		if self.outPath.text() != '':
			self.run()
		else:
			self.iface.messageBar().pushMessage("Chưa chọn thư mục lưu bản đồ tải về", level=Qgis.Warning, duration=5)

	def prj_crs(self, _tinh):
		_tinh = _tinh.split(' - ')[-1]
		_dstinh = docdstinh()
		for tinh in _dstinh:
			if tinh['TINH'] == _tinh:
				_crs = tinh['CRS']
				return _crs

	def set_defauled(self):
		ind = self.inHost.currentIndex()
		if ind == 0:
			host = "localhost"
			use = "postgres"
			pas = "vidagis"
			port = "5433"
			self.inPort.setText(port)
			self.inUsername.setText(use)
			self.inPassword.setText(pas)
			defaul = {
			"host": host,
			"use": use,
			"pas": pas,
			"port": port
			}
			return defaul
		
		else:
			host = "vnforest.gov.vn"
			use = ""
			pas = ""
			port = "5433"
			self.inPort.setText(port)
			self.inUsername.setText(use)
			self.inPassword.setText(pas)
			defaul = {
			"host": host,
			"use": use,
			"pas": pas,
			"port": port
			}
			return defaul

	def laydanhsachtinh(self):
		self.inProvince.clear()
		selected_tinh = self.inProvince.currentText()
		tinhs = docdstinh()
		
		self.inProvince.addItems(['-- Chọn tỉnh --'])
		for tinh in tinhs:
			tname = tinh['MATINH'] + " - " + tinh['TINH']
			self.inProvince.addItems([tname])

	def laydanhsachhuyen(self):
		self.inDistrict.clear()
		tentinh = self.inProvince.currentText()
		matinh = tentinh.split(' - ')[0]
		if self.inProvince.currentIndex() == 0:
			_crs = "EPSG:3405"
		else:
			_crs = self.prj_crs(tentinh.split(' - ')[-1])
		self.outProjection.setCrs(QgsCoordinateReferenceSystem(_crs))
		listhuyen = docdshuyen()

		self.inDistrict.addItems(['-- Chọn huyện --'])
		for chon in listhuyen:
			if chon['MATINH'] == matinh:
				hname = chon['MAHUYEN'] + " - " + chon['HUYEN']
				self.inDistrict.addItems([hname])

	def laydanhsachxa(self):
		self.inCommune.clear()
		tenhuyen = self.inDistrict.currentText()
		mahuyen = tenhuyen.split(' - ')[0]
		listxa = docdsxa()

		self.inCommune.addItems(['-- Chọn xã --'])
		for xachon in listxa:
			if xachon['MAHUYEN'] == mahuyen:
				xname = xachon['MAXA'] + " - " + xachon['XA']
				self.inCommune.addItems([xname])

	def laymacode(self):
		selected_xa = self.inCommune.currentText()
		selected_huyen = self.inDistrict.currentText()
		selected_tinh = self.inProvince.currentText()

		if self.inCommune.currentIndex() > 0:
			code = selected_xa.split(" - ")[0]
			syn = 'commune_code = ' + code
			return syn

		elif self.inDistrict.currentIndex() > 0:
			code = selected_huyen.split(" - ")[0]
			syn = 'district_code = ' + code
			return syn

		else:
			code = selected_tinh.split(" - ")[0]
			syn = 'province_code = ' + code
			return syn

	def run(self):

		qgis.utils.iface.messageBar().clearWidgets()
		progressMessageBar = qgis.utils.iface.messageBar()
		progress = QProgressBar()
		progress.setMaximum(100)
		progressMessageBar.pushWidget(progress)

		inhost = self.set_defauled()["host"]
		inport = self.inPort.text()
		indatabase = "data_forest"
		inuser = self.inUsername.text()
		inpass = self.inPassword.text()
		fix_tempo = str(Path(__file__).parent.absolute()) + '/tempo/fixgeo.shp'
		deldup_tempo = str(Path(__file__).parent.absolute()) + '/tempo/deldup.shp'	 
		outpath = self.outPath.text()
		crs = self.outProjection.crs()
		_tinh = self.inProvince.currentText()
		if _tinh == "-- Chọn tỉnh --":
			self.iface.messageBar().pushMessage("Chưa chọn đơn vị hành chính", level=Qgis.Warning, duration=10)
		else:
			code = self.laymacode()		
			sql = query(code)
			bname = os.path.split(outpath)[1]
			fname = os.path.splitext(bname)[0]

			try:
				i=0
				for n in range (1, 10):
					if n == 1:
						uri = QgsDataSourceUri()
					elif n == 2:
						uri.setConnection(inhost, inport, indatabase, inuser, inpass)
					elif n == 3:
						uri.setDataSource("", u'(%s\n)' % sql, "geom", "", "tt")
					elif n == 4:
						vlayer = QgsVectorLayer(uri.uri(),fname,"postgres")
					elif n == 5:
						QgsVectorFileWriter.writeAsVectorFormat(vlayer, fix_tempo, "UTF-8", crs, "ESRI Shapefile")
					elif n == 6:
						fixgeometry(fix_tempo,deldup_tempo)
					elif n == 7:
						delete_duplicate(deldup_tempo,outpath)						
					elif n == 8:
						update_malr3(outpath)
					else:
						QgsProject.instance().removeAllMapLayers()
						shp =  QgsVectorLayer(outpath, fname, 'ogr')
						layer = QgsProject.instance().addMapLayer(shp)
					i = i + 1

					percent = (i / float(9)) * 100
					progress.setValue(percent)
					time.sleep(1)
				qgis.utils.iface.messageBar().clearWidgets()

				self.iface.messageBar().pushMessage(
					"Quá trình tải bản đồ thành công và được lưu trong thư mục " + outpath, level=Qgis.Success, duration=10)
			except:
				QgsProject.instance().removeAllMapLayers()
				qgis.utils.iface.messageBar().clearWidgets()
				self.iface.messageBar().pushMessage("Quá trình tải bản đồ thất bại", level=Qgis.Critical, duration=10)

class ChuanHoaDBR_Dlg(QDialog, Ui_Dialog_ChuanHoa):

	def __init__(self, iface):
		QDialog.__init__(self)
		self.iface = iface
		self.setupUi(self)
		self.inputShapefile.setText('')
		self.btnInputShp.clicked.connect(self.select_input_shape)
		self.inputChurung.setText('')
		self.btnChurung.clicked.connect(self.select_input_xls)
		self.outputShapefile.setText('')											 
		self.btnOutput.clicked.connect(self.select_output_shape)
		self.buttonBox.accepted.connect(self.checkRun)

		orgEncoding=QgsSettings().value('/Processing/encoding') # save setting
		QgsSettings().setValue('/Processing/encoding', 'utf-8') # set uft8
		
	def checkRun(self):
		if self.inputShapefile.text() != '' and self.inputChurung.text() != '' and self.outputShapefile.text() != '':
			self.run()
		else:
			self.iface.messageBar().pushMessage("Chưa chọn đủ dữ liệu", level=Qgis.Warning, duration=5)	

	def select_input_shape(self):
	 
		self.path_solution = str(QFileDialog.getOpenFileName(self, "v5PFES-Chọn lớp bản đồ diễn biến rừng", "", "Shapefile (*.shp)")[0])
		self.inputShapefile.setText(self.path_solution)

		if self.path_solution != '':
			in_shp = self.path_solution
			driver = ogr.GetDriverByName("ESRI Shapefile")
			dataSource = driver.Open(in_shp, 0)
			layer = dataSource.GetLayer()
			file_kq = []
			field_chuan = ['commune_co','compt_code','sub_compt_','plot_code','parcel_cod','map_sheet','village','area','forest_org','forest_typ','tree_spec_','planting_y','p_forest_o','plant_stat','volume_per','stem_per_h','volume_p_1','stem_per_p','site_cond_','forest_fun','actor_type','actor_id','conflict_s','land_use_c','land_use_t','prot_contr','forest_use','actor_id_p','actor_id_c','nar_for_or','old_plot_c','pos_status']
			field_names = [field.name for field in layer.schema]
			for x in field_chuan:
				if(x not in field_names):
					file_kq.append(x)
			
			if len(file_kq) > 0:
				self.iface.messageBar().pushMessage("Dữ liệu đầu vào không hợp lệ", level=Qgis.Warning, duration=5)
				self.buttonBox.setEnabled(False)
			else:
				self.buttonBox.setEnabled(True)

	def select_input_xls(self):
		self.path_solution = str(QFileDialog.getOpenFileName(self, "v5PFES-Chọn danh sách chủ rừng", "", "MS - Excel (*.xlsx);;MS - Excel (*.xls)")[0])
		self.inputChurung.setText(self.path_solution)

		if self.path_solution != '':
			in_exc = self.path_solution
			col_kq = []
			col_chuan = ['commune_code','actor_id','actor_type_code','actor_name']
			col_exc = pd.read_excel(in_exc,skiprows=0).columns
			for x in col_chuan:
				if(x not in col_exc):
					col_kq.append(x)
			
			if len(col_kq) > 0:
				self.iface.messageBar().pushMessage("Dữ liệu đầu vào không hợp lệ", level=Qgis.Warning, duration=5)
				self.buttonBox.setEnabled(False)
			else:
				self.buttonBox.setEnabled(True)
		
	def select_output_shape(self):
		self.path_solution = str(QFileDialog.getSaveFileName(self, "v5PFES-Chọn thư mục lưu kết quả chuẩn hóa", "", "Shapefile (*.shp)")[0])
		self.outputShapefile.setText(self.path_solution)
		
	def run(self):
		try:
			#clear the message bar		
			qgis.utils.iface.messageBar().clearWidgets() 
			#set a new message bar
			progressMessageBar = qgis.utils.iface.messageBar()
			######################################
			# Prepare your progress Bar
			######################################
			progress = QProgressBar()
			#Maximum is set to 100, making it easy to work with percentage of completion
			progress.setMaximum(100) 
			#pass the progress bar to the message Bar
			progressMessageBar.pushWidget(progress)

			inpath = self.inputShapefile.text()
			outpath = self.outputShapefile.text()
			inputChurung = self.inputChurung.text()
			bname = os.path.split(outpath)[1]
			fname = os.path.splitext(bname)[0]
			bpath = os.path.dirname(inpath)

			i=0
			for n in range(1,6):
				i=i+1
				if n ==1:
				#1
					delete_fields(inpath,outpath)
					shp =  QgsVectorLayer(outpath, fname, 'ogr')
					layer = QgsProject.instance().addMapLayer(shp)
				#2
				elif n==2:
					add_fields(layer)
				#3
				elif n==3:
					rename_fields(layer)
					QgsProject.instance().removeAllMapLayers()
				#4
				elif n==4:
					join_fields(outpath,inputChurung)
				else:	
					update_loaicay(outpath)
					QgsProject.instance().removeAllMapLayers()
					shp =  QgsVectorLayer(outpath, fname, 'ogr')
					layer = QgsProject.instance().addMapLayer(shp)

				percent = (i/float(5)) * 100
				progress.setValue(percent)				
				time.sleep(1)
			qgis.utils.iface.messageBar().clearWidgets()								
			self.iface.messageBar().pushMessage("Quá trình chuẩn hóa thành công!", level=Qgis.Success, duration=5)
		except:
			QgsProject.instance().removeAllMapLayers()
			qgis.utils.iface.messageBar().clearWidgets()
			self.iface.messageBar().pushMessage("Quá trình chuẩn hóa thất bại", level=Qgis.Critical, duration=5)

class XayDungCTDL_Dlg(QDialog, Ui_Dialog_XayDungCTDL):

	def __init__(self, iface):
		QDialog.__init__(self)
		self.iface = iface
		self.setupUi(self)
		self.lineEdit.setText('')
		self.pushButton.clicked.connect(self.select_input_shape)
		self.lineEdit_2.setText('')
		self.pushButton_2.clicked.connect(self.select_input_xls)
		self.lineEdit_3.setText('')											 
		self.pushButton_3.clicked.connect(self.select_output_shape)
		self.buttonBox.accepted.connect(self.checkRun)	
		
		orgEncoding=QgsSettings().value('/Processing/encoding') # save setting
		QgsSettings().setValue('/Processing/encoding', 'utf-8') # set uft8
		
	def checkRun(self):
		if self.lineEdit.text() != '' and self.lineEdit_2.text() != '' and self.lineEdit_3.text() != '':
			self.run()
		else:
			self.iface.messageBar().pushMessage("Chưa chọn đủ dữ liệu", level=Qgis.Warning, duration=5)	

	def select_input_shape(self):
	  
		self.path_solution = str(QFileDialog.getOpenFileName(self, "v5PFES-Chọn lớp bản đồ hiện trạng rừng", "", "Shapefile (*.shp)")[0])
		self.lineEdit.setText(self.path_solution)

		if self.path_solution != '':
			in_shp = self.path_solution
			driver = ogr.GetDriverByName("ESRI Shapefile")
			dataSource = driver.Open(in_shp, 0)
			layer = dataSource.GetLayer()
			file_kq = []
			field_chuan = ['maxa','mahuyen','matinh','xa','huyen','tinh','tk','khoanh','lo','thuad','tobando','ddanh','dtich','nggocr','maldlr','ldlr','sldlr','malr3','nggocrt','thanhrung','mgo','mtn','mgolo','mtnlo','lapdia','mamdsd','dtuong','machur','churung']
			field_names = [field.name for field in layer.schema]
			for x in field_chuan:
				if(x not in field_names):
					file_kq.append(x)
			
			if len(file_kq) > 0:
				self.iface.messageBar().pushMessage("Dữ liệu đầu vào không hợp lệ", level=Qgis.Warning, duration=5)
				self.buttonBox.setEnabled(False)
			else:
				self.buttonBox.setEnabled(True)						

	def select_input_xls(self):
		self.path_solution = str(QFileDialog.getOpenFileName(self, "v5PFES-Chọn danh sách lưu vực", "", "MS - Excel (*.xlsx);;MS - Excel (*.xls)")[0])
		self.lineEdit_2.setText(self.path_solution)

		if self.path_solution != '':
			in_exc = self.path_solution
			col_kq = []
			col_chuan = ['malv','tenlv']
			col_exc = pd.read_excel(in_exc,skiprows=0).columns
			for x in col_chuan:
				if(x not in col_exc):
					col_kq.append(x)
			
			if len(col_kq) > 0:
				self.iface.messageBar().pushMessage("Dữ liệu đầu vào không hợp lệ", level=Qgis.Warning, duration=5)
				self.buttonBox.setEnabled(False)
			else:
				self.buttonBox.setEnabled(True)
		
	def select_output_shape(self):
		self.path_solution = str(QFileDialog.getSaveFileName(self, "v5PFES-Chọn thư mục chứa lớp bản đồ đầu ra", "", "Shapefile (*.shp)")[0])
		self.lineEdit_3.setText(self.path_solution)	

	def run(self):
		try:
			#clear the message bar		
			qgis.utils.iface.messageBar().clearWidgets() 
			#set a new message bar
			progressMessageBar = qgis.utils.iface.messageBar()
			######################################
			# Prepare your progress Bar
			######################################
			progress = QProgressBar()
			#Maximum is set to 100, making it easy to work with percentage of completion
			progress.setMaximum(100) 
			#pass the progress bar to the message Bar
			progressMessageBar.pushWidget(progress)
			
			tempo = str(Path(__file__).parent.absolute()) + '/tempo/tempo.shp'  
			inpath = self.lineEdit.text()
			outpath = self.lineEdit_3.text()
			inputLuuvuc = self.lineEdit_2.text()
			bname = os.path.split(outpath)[1]
			fname = os.path.splitext(bname)[0]
			bpath = os.path.dirname(inpath)

			i=0
			for n in range(1,4):
				i=i+1
				if n ==1:		   
					shp =  QgsVectorLayer(inpath, '', 'ogr')
					layer = QgsProject.instance().addMapLayer(shp)
					QgsVectorFileWriter.writeAsVectorFormat(layer, tempo, "UTF-8", layer.crs(), "ESRI Shapefile")
					QgsProject.instance().removeAllMapLayers()

				elif n ==2:
					nshp =  QgsVectorLayer(tempo, '', 'ogr')
					nlayer = QgsProject.instance().addMapLayer(nshp)
					add_newfields(nlayer, outpath)

				else:
					convert_json(inputLuuvuc)	 
					QgsProject.instance().removeAllMapLayers()
					shp =  QgsVectorLayer(outpath, fname, 'ogr')
					layer = QgsProject.instance().addMapLayer(shp)

				percent = (i/float(3)) * 100
				progress.setValue(percent)				
				time.sleep(1) 
			qgis.utils.iface.messageBar().clearWidgets()					  
			self.iface.messageBar().pushMessage("Quá trình xây dựng cấu trúc dữ liệu thành công", level=Qgis.Success, duration=5)
		except:
			qgis.utils.iface.messageBar().clearWidgets()
			QgsProject.instance().removeAllMapLayers()
			self.iface.messageBar().pushMessage("Error","Quá trình xây dựng cấu trúc dữ liệu thất bại", level=Qgis.Critical, duration=5)

class CapNhatVCT_Dlg(QDialog, Ui_Dialog_CapNhatVCT):

	def __init__(self, iface):
		QDialog.__init__(self)
		self.iface = iface
		self.setupUi(self)
		self.lineEdit.setText('')
		self.pushButton.clicked.connect(self.select_input_shape)
		self.lineEdit_2.setText('')
		self.checkBox.setChecked(True)
		self.pushButton_2.clicked.connect(self.select_input_luuvuc)
		self.lineEdit_4.setText('')											 
		self.pushButton_3.clicked.connect(self.select_output_shape)
		self.buttonBox.accepted.connect(self.checkRun)
		self.laydsluuvuc()

		orgEncoding=QgsSettings().value('/Processing/encoding') # save setting
		QgsSettings().setValue('/Processing/encoding', 'utf-8') # set uft8
		
	def checkRun(self):
		if self.lineEdit.text() != '' and self.lineEdit_2.text() != '' and self.lineEdit_4.text() != '':
			self.run()
		else:
			self.iface.messageBar().pushMessage("Chưa chọn đủ dữ liệu", level=Qgis.Warning, duration=5)

	def select_input_shape(self):
	  
		self.path_solution = str(QFileDialog.getOpenFileName(self, "v5PFES-Chọn lớp bản đồ đầu vào", "", "Shapefile (*.shp)")[0])
		self.lineEdit.setText(self.path_solution)

		if self.path_solution != '':
			in_shp = self.path_solution
			driver = ogr.GetDriverByName("ESRI Shapefile")
			dataSource = driver.Open(in_shp, 0)
			layer = dataSource.GetLayer()
			file_kq = []
			field_chuan = ['maxa','mahuyen','matinh','xa','huyen','tinh','tk','khoanh','lo','thuad','tobando','ddanh','dtich','nggocr','maldlr','ldlr','sldlr','malr3','nggocrt','thanhrung','mgo','mtn','mgolo','mtnlo','lapdia','mamdsd','dtuong','machur','churung','vungchitra','chitra','maluuvuc','k0','k1','k2','k3','k4','khuvuc','dtichct']
			field_names = [field.name for field in layer.schema]
			for x in field_chuan:
				if(x not in field_names):
					file_kq.append(x)
			
			if len(file_kq) > 0:
				self.iface.messageBar().pushMessage("Dữ liệu đầu vào không hợp lệ", level=Qgis.Warning, duration=5)
				self.buttonBox.setEnabled(False)
			else:
				self.buttonBox.setEnabled(True)

	def laydsluuvuc(self):
		try:
			self.comboBox.clear()
			watershed = docdsluuvuc()
			for catchment in watershed:
				cname = catchment['Tenlv']
				ccode = catchment['malv']
				self.comboBox.addItems([cname])
		except:
			self.iface.messageBar().pushMessage("Chưa xây dựng cấu trúc dữ liệu", level=Qgis.Warning, duration=5)		  

	def select_input_luuvuc(self):
		self.path_solution = str(QFileDialog.getOpenFileName(self, "v5PFES-Chọn lớp ranh giới lưu vực", "", "Shapefile (*.shp)")[0])
		self.lineEdit_2.setText(self.path_solution)

		err =0
		if self.path_solution != '':
			inputLV = self.lineEdit_2.text()
			driver = ogr.GetDriverByName("ESRI Shapefile")
			dataSource = driver.Open(inputLV, 0)
			layer = dataSource.GetLayer()
			count_row = layer.GetFeatureCount()
			if count_row > 1:
				err +=1

			if err > 0:
				self.iface.messageBar().pushMessage("Dữ liệu đầu vào không hợp lệ", level=Qgis.Warning, duration=5)
				self.buttonBox.setEnabled(False)
			else:
				self.buttonBox.setEnabled(True)

	def select_output_shape(self):
		self.path_solution = str(QFileDialog.getSaveFileName(self, "v5PFES-Chọn thư mục chứa lớp bản đồ đầu ra", "", "Shapefile (*.shp)")[0])
		self.lineEdit_4.setText(self.path_solution)

	def run(self):
		try:
			threadcount = QThread.idealThreadCount()
			QgsApplication.setMaxThreads(threadcount)
			QSettings().setValue("/qgis/parallel_rendering", True)
			QSettings().setValue("/core/OpenClEnabled", True)

			#clear the message bar		
			qgis.utils.iface.messageBar().clearWidgets() 
			#set a new message bar
			progressMessageBar = qgis.utils.iface.messageBar()
			######################################
			# Prepare your progress Bar
			######################################
			progress = QProgressBar()
			#Maximum is set to 100, making it easy to work with percentage of completion
			progress.setMaximum(100) 
			#pass the progress bar to the message Bar
			progressMessageBar.pushWidget(progress)
			
			fixInput_tempo = str(Path(__file__).parent.absolute()) + '/tempo/fixInput.shp'
			fixLV_tempo = str(Path(__file__).parent.absolute()) + '/tempo/fixLV.shp'
			fixOutput_tempo = str(Path(__file__).parent.absolute()) + '/tempo/fixOutput.shp'
			clip_tempo = str(Path(__file__).parent.absolute()) + '/tempo/clip.shp'
			dt2_tempo = str(Path(__file__).parent.absolute()) + '/tempo/dt2.shp'
			union_tempo = str(Path(__file__).parent.absolute()) + '/tempo/union.shp'
			buffer_tempo = str(Path(__file__).parent.absolute()) + '/tempo/buffer.shp'
			selected_tempo = str(Path(__file__).parent.absolute()) + '/tempo/selected.shp'
			recal_tempo = str(Path(__file__).parent.absolute()) + '/tempo/area.shp'
			
			inpath = self.lineEdit.text()
			outpath = self.lineEdit_4.text()
			inputLuuvuc = self.lineEdit_2.text()
			mlv = laymalv(self.comboBox.currentText())
			bname = os.path.split(outpath)[1]
			fname = os.path.splitext(bname)[0]
			bpath = os.path.dirname(inpath)
				
			k=8
			i=0
			for n in range(1,k):
				i=i+1
				if n == 1:
					fixgeometry(inpath, fixInput_tempo)
					fixgeometry(inputLuuvuc, fixLV_tempo)
				elif n == 2:
					clip_extent(fixLV_tempo,inpath,clip_tempo)
					mshp =  QgsVectorLayer(fixInput_tempo, '', 'ogr')
					mlayer = QgsProject.instance().addMapLayer(mshp)
					add_dtich2(mlayer,dt2_tempo)
				elif n == 3:
					union(dt2_tempo,clip_tempo,union_tempo)
				elif n == 4:
					buffer(fixLV_tempo,buffer_tempo)
				elif n == 5:
					selectbylocation(union_tempo,buffer_tempo,mlv,selected_tempo)
					QgsProject.instance().removeAllMapLayers()
				elif n==6:
					nshp =  QgsVectorLayer(selected_tempo, '', 'ogr')
					nlayer = QgsProject.instance().addMapLayer(nshp)	
					if self.checkBox.isChecked():
						recalculate_area_1(nlayer, recal_tempo)
					else:
						recalculate_area_2(nlayer, recal_tempo)
					QgsProject.instance().removeAllMapLayers()
				else:
					fixgeometry(recal_tempo,fixOutput_tempo)
					eliminate(fixOutput_tempo,outpath)
					QgsProject.instance().removeAllMapLayers()
					shp = QgsVectorLayer(outpath, fname, 'ogr')
					layer = QgsProject.instance().addMapLayer(shp)

				percent = (i/float(k-1)) * 100
				progress.setValue(percent)				
				time.sleep(1) 
					
			qgis.utils.iface.messageBar().clearWidgets()
			self.iface.messageBar().pushMessage("Quá trình cập nhật vùng chi trả thành công", level=Qgis.Success, duration=5)
		except:
			qgis.utils.iface.messageBar().clearWidgets()
			QgsProject.instance().removeAllMapLayers()
			self.iface.messageBar().pushMessage("Error","Quá trình cập nhật vùng chi trả thất bại", level=Qgis.Critical, duration=5)

class CapNhatDG_Dlg(QDialog, Ui_Dialog_CapNhatDG):

	def __init__(self, iface):
		QDialog.__init__(self)
		self.iface = iface
		self.setupUi(self)
		self.inputShapefile.setText('')
		self.btnInputShp.clicked.connect(self.select_input_shape)
		self.InMoney.setText('1000000000')
		self.spBx_Price.setValue(0)
		self.spBx_Price.setSingleStep(10000)
		self.spBx_Price.setMaximum(10000000)
		self.dg_cBx.setChecked(True)
		self.xdmct_cBx.setChecked(False)
		self.dg_cBx.stateChanged.connect(self.checkbox)											 
		self.btnPrice.clicked.connect(self.calculate_price)
		self.btnUpdate.clicked.connect(self.update_price)
		self.buttonBox.accepted.connect(self.checkRun)
		self.laydsluuvuc()

	def select_input_shape(self):	 
		self.path_solution = str(QFileDialog.getOpenFileName(self, "v5PFES-Chọn lớp bản đồ diễn biến rừng", "", "Shapefile (*.shp)")[0])
		self.inputShapefile.setText(self.path_solution)

		if self.path_solution != '':
			inputShapefile = self.path_solution
			driver = ogr.GetDriverByName("ESRI Shapefile")
			dataSource = driver.Open(inputShapefile, 0)
			layer = dataSource.GetLayer()
			file_kq = []
			field_chuan = ['maxa','mahuyen','matinh','xa','huyen','tinh','tk','khoanh','lo','thuad','tobando','ddanh','dtich','nggocr','maldlr','ldlr','sldlr','malr3','nggocrt','thanhrung','mgo','mtn','mgolo','mtnlo','lapdia','mamdsd','dtuong','machur','churung','vungchitra','chitra','maluuvuc','k0','k1','k2','k3','k4','khuvuc','dtichct']
			field_names = [field.name for field in layer.schema]
			for x in field_chuan:
				if(x not in field_names):
					file_kq.append(x)
			
			if len(file_kq) > 0:
				self.iface.messageBar().pushMessage("Dữ liệu đầu vào không hợp lệ", level=Qgis.Warning, duration=5)
				self.btnPrice.setEnabled(False)
			else:
				self.btnPrice.setEnabled(True)

	def checkbox(self):
		if self.dg_cBx.isChecked():
			self.xdmct_cBx.setEnabled(True)
		else:
			self.xdmct_cBx.setEnabled(False)
			self.xdmct_cBx.setChecked(False)

	def checkRun(self):
		if self.inputShapefile.text() != '':
			self.run()
		else:
			self.iface.messageBar().pushMessage("Chưa chọn đủ dữ liệu", level=Qgis.Warning, duration=5)

	def laydsluuvuc(self):
		try:
			self.comboBox.clear()
			watershed = docdsluuvuc()
			for catchment in watershed:
				cname = catchment['Tenlv']
				self.comboBox.addItems([cname])
		except:
			self.iface.messageBar().pushMessage("Chưa xây dựng cấu trúc dữ liệu", level=Qgis.Warning, duration=5)

	def calculate_price(self):
		try:
			inpath = self.inputShapefile.text()
			money = long(self.InMoney.text())
			mlv = laymalv(self.comboBox.currentText())		
			bpath = os.path.dirname(inpath)

			layer = QgsVectorLayer(inpath, '', 'ogr')
			QgsProject.instance().addMapLayer(layer)
			exp= 'nggocr=1 OR nggocr=2'
			processing.run("qgis:selectbyattribute", {"FIELD":'maluuvuc', "INPUT":layer, "METHOD": 0,"OPERATOR": 7,"VALUE":mlv})
			processing.run("qgis:selectbyexpression", {"EXPRESSION":exp, "INPUT":layer, "METHOD": 3})

			fArea = []
			for feat in layer.getSelectedFeatures():
				fArea.append(float(feat['dtichct']))
			
			total = sum(fArea)
			p = money/total
			self.spBx_Price.setValue(p)
			QgsProject.instance().removeAllMapLayers()
		except:
			qgis.utils.iface.messageBar().clearWidgets()
			QgsProject.instance().removeAllMapLayers()
			self.iface.messageBar().pushMessage("Chưa cập nhật vùng chi trả cho lưu vực này", level=Qgis.Warning, duration=5)

	def update_price(self):
		mlv = int(laymalv(self.comboBox.currentText()))
		price = self.spBx_Price.value()
		edit_price(mlv,price)

	def run(self):
		try:
			#clear the message bar		
			qgis.utils.iface.messageBar().clearWidgets() 
			#set a new message bar
			progressMessageBar = qgis.utils.iface.messageBar()
			######################################
			# Prepare your progress Bar
			######################################
			progress = QProgressBar()
			#Maximum is set to 100, making it easy to work with percentage of completion
			progress.setMaximum(100) 
			#pass the progress bar to the message Bar
			progressMessageBar.pushWidget(progress)

			inpath = self.inputShapefile.text()
			bpath = os.path.dirname(inpath)
			bname = os.path.split(inpath)[1]
			fname = os.path.splitext(bname)[0]

			i=0
			for n in range(1,3):
				i=i+1
				if n ==1:
					if self.dg_cBx.isChecked():
						price(inpath)				
					else:
						pass
				else:
					if self.xdmct_cBx.isChecked():
						payment_level(inpath)				
					else:
						pass

					QgsProject.instance().removeAllMapLayers()		
					shp =  QgsVectorLayer(inpath, fname, 'ogr')
					layer = QgsProject.instance().addMapLayer(shp)

				percent = (i/float(2)) * 100
				progress.setValue(percent)				
				time.sleep(1) 
			qgis.utils.iface.messageBar().clearWidgets()					  
			self.iface.messageBar().pushMessage("Quá trình tính đơn giá chi trả thành công", level=Qgis.Success, duration=5)
		except:
			self.iface.messageBar().pushMessage("Error","Quá trình tính đơn giá chi trả thất bại", level=Qgis.Critical, duration=5)

class CapNhatDTCT_Dlg(QDialog, Ui_Dialog_CapNhatDTCT):

	def __init__(self, iface):
		QDialog.__init__(self)
		self.iface = iface
		self.setupUi(self)
		self.inPath.setText('')
		self.inBtn.clicked.connect(self.select_input_shape)
		self.rtn_checkbox.setChecked(True)
		self.rtg_checkbox.setChecked(True)
		self.rttn_checkbox.setChecked(True)
		self.rtk_checkbox.setChecked(False)
		self.ctr_checkbox.setChecked(False)
		self.lc_checkbox.setEnabled(False)
		self.lc_checkbox.setChecked(False)
		self.lc_checkbox.stateChanged.connect(self.select_treespecies)
		self.xkk_cBx.setEnabled(False)
		self.xkk_cBx.setChecked(False)
		self.xkk_cBx.stateChanged.connect(self.edit_remoteArea)
		self.k1_cBx.setEnabled(False)
		self.k2_cBx.setEnabled(False)
		self.k3_cBx.setEnabled(False)
		self.k4_cBx.setEnabled(False)
		self.noK_rBtn.setChecked(True)
		self.noK_rBtn.toggled.connect(self.check_k)
		self.outPath.setText('')											 
		self.outBtn.clicked.connect(self.select_output_shape)
		self.buttonBox.accepted.connect(self.checkRun)

		orgEncoding=QgsSettings().value('/Processing/encoding') # save setting
		QgsSettings().setValue('/Processing/encoding', 'utf-8') # set uft8
		
	def checkRun(self):
		if self.inPath.text() != '' and self.outPath.text()!= '':
			self.run()
		else:
			self.iface.messageBar().pushMessage("Chưa chọn đủ dữ liệu", level=Qgis.Warning, duration=5)

	def select_input_shape(self):
	  
		self.path_solution = str(QFileDialog.getOpenFileName(self, "v5PFES-Chọn lớp bản đồ đầu vào", "", "Shapefile (*.shp)")[0])
		self.inPath.setText(self.path_solution)

		if self.path_solution != '':
			in_shp = self.path_solution
			driver = ogr.GetDriverByName("ESRI Shapefile")
			dataSource = driver.Open(in_shp, 0)
			layer = dataSource.GetLayer()
			file_kq = []
			field_chuan = ['maxa','mahuyen','matinh','xa','huyen','tinh','tk','khoanh','lo','thuad','tobando','ddanh','dtich','nggocr','maldlr','ldlr','sldlr','malr3','nggocrt','thanhrung','mgo','mtn','mgolo','mtnlo','lapdia','mamdsd','dtuong','machur','churung','vungchitra','chitra','maluuvuc','k0','k1','k2','k3','k4','khuvuc','dtichct']
			field_names = [field.name for field in layer.schema]
			for x in field_chuan:
				if(x not in field_names):
					file_kq.append(x)
			
			if len(file_kq) > 0:
				self.iface.messageBar().pushMessage("Dữ liệu đầu vào không hợp lệ", level=Qgis.Warning, duration=5)			
				self.lc_checkbox.setEnabled(False)
				self.xkk_cBx.setEnabled(False)
				self.lc_checkbox.setChecked(False)
				self.xkk_cBx.setChecked(False)
				self.buttonBox.setEnabled(False)
				for i in reversed (range (self.tableWidget.rowCount())):
					self.tableWidget.removeRow(i)
				for i in reversed (range (self.tableWidget_2.rowCount())):
					self.tableWidget_2.removeRow(i)
			else:
				self.lc_checkbox.setEnabled(True)
				self.xkk_cBx.setEnabled(True)
				self.buttonBox.setEnabled(True)

	def select_treespecies(self):
		try:
			if self.lc_checkbox.isChecked():
				self.tableWidget.clear()

				in_shp = str(self.inPath.text())
				driver = ogr.GetDriverByName("ESRI Shapefile")
				dataSource = driver.Open(in_shp, 1)
				layer = dataSource.GetLayer()

				listlc = []
				for feature in layer:
					if feature['vungchitra'] == 1:
						listlc.append(feature['sldlr'])
				unique_lc = list(set(listlc))
				lc = list(filter(None,unique_lc))
			
				self.tableWidget.setRowCount(len(lc))
				self.tableWidget.setColumnCount(2)
				self.tableWidget.setHorizontalHeaderLabels(["Tên loài cây", "Chitrả"])
				self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.EditTriggers(2))

				for i in range (self.tableWidget.rowCount()):
					self.tableWidget.setItem(i,0,QTableWidgetItem(lc[i]))
					self.tableWidget.setItem(i,1,QTableWidgetItem("1"))
			else:
				for i in reversed (range (self.tableWidget.rowCount())):
					self.tableWidget.removeRow(i)
		except:
			self.iface.messageBar().pushMessage("Chưa cập nhật vùng chi trả", level=Qgis.Warning, duration=5)

	def edit_remoteArea(self):
		try:
			if self.xkk_cBx.isChecked():
				self.tableWidget_2.clear()
				xakhokhan = docdsxkk()
				in_shp = str(self.inPath.text())
				driver = ogr.GetDriverByName("ESRI Shapefile")
				dataSource = driver.Open(in_shp, 1)
				layer = dataSource.GetLayer()

				vct = []
				for feature in layer:
					if feature['vungchitra'] == 1:
						vct.append(feature['maxa'])
				listvct = list(set(vct))

				listmaxa = []
				listxa = []
				listkhuvuc = []

				for feature in xakhokhan:
					giatri = int(feature['MAXA'])
					if giatri in listvct:
						listmaxa.append(feature['MAXA'])
						listxa.append(feature['XA'])
						listkhuvuc.append(feature['KHUVUC'])

				self.tableWidget_2.setRowCount(len(listmaxa))
				self.tableWidget_2.setColumnCount(3)
				self.tableWidget_2.setHorizontalHeaderLabels(["Mã xã", "Tên xã", "Khu vực"])
				self.tableWidget_2.setEditTriggers(QtWidgets.QTableWidget.EditTriggers(2))

				for i in range (self.tableWidget_2.rowCount()):
					self.tableWidget_2.setItem(i,0,QTableWidgetItem(listmaxa[i]))
					self.tableWidget_2.setItem(i,1,QTableWidgetItem(listxa[i]))
					self.tableWidget_2.setItem(i,2,QTableWidgetItem(listkhuvuc[i]))
			else:
				for i in reversed (range (self.tableWidget_2.rowCount())):
						self.tableWidget_2.removeRow(i)
		except:
			self.iface.messageBar().pushMessage("Chưa cập nhật vùng chi trả", level=Qgis.Warning, duration=5)

	def check_k(self):
		if self.noK_rBtn.isChecked():
			self.k1_cBx.setEnabled(False)
			self.k2_cBx.setEnabled(False)
			self.k3_cBx.setEnabled(False)
			self.k4_cBx.setEnabled(False)
			self.k1_cBx.setChecked(False)
			self.k2_cBx.setChecked(False)
			self.k3_cBx.setChecked(False)
			self.k4_cBx.setChecked(False)
		else:
			self.k1_cBx.setEnabled(True)
			self.k2_cBx.setEnabled(True)
			self.k3_cBx.setEnabled(True)
			self.k4_cBx.setEnabled(True)
  
	def select_output_shape(self):
		self.path_solution = str(QFileDialog.getSaveFileName(self, "v5PFES-Chọn thư mục chứa lớp bản đồ đầu ra", "", "Shapefile (*.shp)")[0])
		self.outPath.setText(self.path_solution)

	def run(self):
		try:
			#clear the message bar		
			qgis.utils.iface.messageBar().clearWidgets() 
			#set a new message bar
			progressMessageBar = qgis.utils.iface.messageBar()
			######################################
			# Prepare your progress Bar
			######################################
			progress = QProgressBar()
			#Maximum is set to 100, making it easy to work with percentage of completion
			progress.setMaximum(100) 
			#pass the progress bar to the message Bar
			progressMessageBar.pushWidget(progress)
			
			tempo = str(Path(__file__).parent.absolute()) + '/tempo/tempo.shp'  
			inpath = self.inPath.text()
			outpath = self.outPath.text()
			bname = os.path.split(outpath)[1]
			fname = os.path.splitext(bname)[0]
			bpath = os.path.dirname(inpath)

			ds_loaicay_ct = []
			for i in range (self.tableWidget.rowCount()):
				chitra = self.tableWidget.item(i,1).text()
				if chitra == "1":
					ds_loaicay_ct.append(self.tableWidget.item(i,0).text())	

			ds_khuvuc = []
			ds_maxa = []
			for i in range (self.tableWidget_2.rowCount()):
				xkk= self.tableWidget_2.item(i,2).text()
				lmx = self.tableWidget_2.item(i,0).text()
				ds_khuvuc.append(xkk)
				ds_maxa.append(lmx)	   
			
			i=0
			for n in range(1,11):
				i=i+1
				if n ==1:		 
					shp =  QgsVectorLayer(inpath, '', 'ogr')
					layer = QgsProject.instance().addMapLayer(shp)

					QgsVectorFileWriter.writeAsVectorFormat(layer, tempo, "UTF-8", layer.crs(), "ESRI Shapefile")
					QgsProject.instance().removeAllMapLayers()

				elif n==2:
					nshp =  QgsVectorLayer(tempo, '', 'ogr')
					nlayer = QgsProject.instance().addMapLayer(nshp)	
					if self.rtn_checkbox.isChecked():
						rtn_payment(nlayer)					
					else:
						pass

				elif n==3:
					if self.rtg_checkbox.isChecked():
						rtg_payment(nlayer) 
					else:
						pass
						
				elif n==4:
					if self.rttn_checkbox.isChecked():
						rttn_payment(nlayer) 
					else:
						pass	

				elif n==5:
					if self.rtk_checkbox.isChecked():
						rtk_payment(nlayer) 
					else:
						pass

				elif n==6:
					if self.ctr_checkbox.isChecked():
						ctr_payment(nlayer) 
					else:
						pass

				elif n==7:
					if self.lc_checkbox.isChecked():
						lc_payment(nlayer,ds_loaicay_ct,outpath)
					else:
						lc__non_payment(nlayer,outpath)
					QgsProject.instance().removeAllMapLayers()
						
				elif n==8:
					if self.xkk_cBx.isChecked():		 
						mshp =  QgsVectorLayer(outpath, '', 'ogr')
						mlayer = QgsProject.instance().addMapLayer(mshp)
						update_xkk(mlayer,ds_maxa,ds_khuvuc)
						edit_dsxkk(ds_maxa,ds_khuvuc)
					else:
						join_xkk(outpath)
					QgsProject.instance().removeAllMapLayers()

				elif n==9:
					if self.noK_rBtn.isChecked():
						update_K(outpath)					
					else:
						if self.k1_cBx.isChecked():
							update_K1(outpath)
						else:
							update_K1_uncheck(outpath)

						if self.k2_cBx.isChecked():
							update_K2(outpath)
						else:
							update_K2_uncheck(outpath)

						if self.k3_cBx.isChecked():
							update_K3(outpath)
						else:
							update_K3_uncheck(outpath)

						if self.k4_cBx.isChecked():
							update_K4(outpath)
						else:
							update_K4_uncheck(outpath)
						
						update_K0(outpath)
				
				else:
					payment_area(outpath)		
									 
					QgsProject.instance().removeAllMapLayers()		
					shp =  QgsVectorLayer(outpath, fname, 'ogr')
					layer = QgsProject.instance().addMapLayer(shp)

				percent = (i/float(10)) * 100
				progress.setValue(percent)				
				time.sleep(1) 
			qgis.utils.iface.messageBar().clearWidgets()					  
			self.iface.messageBar().pushMessage("Quá trình cập nhật dữ liệu chi trả thành công", level=Qgis.Success, duration=5)
		except:
			QgsProject.instance().removeAllMapLayers()
			qgis.utils.iface.messageBar().clearWidgets()
			self.iface.messageBar().pushMessage("Error","Quá trình cập nhật dữ liệu chi trả thất bại", level=Qgis.Critical, duration=5)

class XayDungCSDL_Dlg(QDialog, Ui_Dialog_XayDungCSDL):

	def __init__(self, iface):
		QDialog.__init__(self)
		self.iface = iface
		self.setupUi(self)
		self.lineEdit.setText('')
		self.InButton.clicked.connect(self.select_input_shape)
		self.buttonBox.accepted.connect(self.checkRun)
		#self.inPath.setText('')
		orgEncoding=QgsSettings().value('/Processing/encoding') # save setting
		QgsSettings().setValue('/Processing/encoding', 'utf-8') # set uft8	

	def checkRun(self):
		if self.lineEdit.text() != '':
			self.run()
		else:
			self.iface.messageBar().pushMessage("Chưa chọn dữ liệu đầu vào", level=Qgis.Warning, duration=5)

	def select_input_shape(self):	  
		self.path_solution = str(QFileDialog.getOpenFileName(self, "v5PFES-Chọn lớp bản đồ đầu vào", "", "Shapefile (*.shp)")[0])
		self.lineEdit.setText(self.path_solution)

		if self.path_solution != '':
			in_shp = self.path_solution
			driver = ogr.GetDriverByName("ESRI Shapefile")
			dataSource = driver.Open(in_shp, 0)
			layer = dataSource.GetLayer()
			file_kq = []
			field_chuan = ['maxa','mahuyen','matinh','xa','huyen','tinh','tk','khoanh','lo','thuad','tobando','ddanh','dtich','nggocr','maldlr','ldlr','sldlr','malr3','mgo','mtn','dtuong','machur','churung','vungchitra','chitra','maluuvuc','k0','k1','k2','k3','k4','dtichct','dgia']
			field_names = [field.name for field in layer.schema]
			for x in field_chuan:
				if(x not in field_names):
					file_kq.append(x)
			
			if len(file_kq) > 0:
				self.iface.messageBar().pushMessage("Dữ liệu đầu vào không hợp lệ", level=Qgis.Warning, duration=5)
				self.buttonBox.setEnabled(False)
			else:
				self.buttonBox.setEnabled(True)				

	def run(self):
		try:
			#clear the message bar		
			qgis.utils.iface.messageBar().clearWidgets() 
			#set a new message bar
			progressMessageBar = qgis.utils.iface.messageBar()
			######################################
			# Prepare your progress Bar
			######################################
			progress = QProgressBar()
			#Maximum is set to 100, making it easy to work with percentage of completion
			progress.setMaximum(100) 
			#pass the progress bar to the message Bar
			progressMessageBar.pushWidget(progress)
	  
			tempo = str(Path(__file__).parent.absolute()) + '/tempo/tempo.xlsx'
			tempo_THX = str(Path(__file__).parent.absolute()) + '/tempo/THX.json'
			tempo_ChuRung = str(Path(__file__).parent.absolute()) + '/tempo/ChuRung.json'
			inpath = self.lineEdit.text()

			i=0
			for n in range(1,4):
				i=i+1
				if n==1:
					shp =  QgsVectorLayer(inpath, '', 'ogr')
					layer = QgsProject.instance().addMapLayer(shp)
					QgsVectorFileWriter.writeAsVectorFormat(layer, tempo, "UTF-8", layer.crs(), "xlsx")	
					QgsProject.instance().removeAllMapLayers()				
				elif n==2:
					export_THX(tempo,tempo_THX)
				else:
					export_ChuRung(tempo,tempo_ChuRung)								 
					

				percent = (i/float(3)) * 100
				progress.setValue(percent)				
				time.sleep(1) 
			qgis.utils.iface.messageBar().clearWidgets()
			QgsProject.instance().removeAllMapLayers()					  
			self.iface.messageBar().pushMessage("Quá trình xây dựng cơ sở dữ liệu thành công", level=Qgis.Success, duration=5)
		except:
			QgsProject.instance().removeAllMapLayers()
			qgis.utils.iface.messageBar().clearWidgets()
			self.iface.messageBar().pushMessage("Error","Quá trình xây dựng cơ sở dữ liệu thất bại", level=Qgis.Critical, duration=5)

class XuatBieuNhom1_Dlg(QDialog, Ui_Dialog_XuatBieuNhom1):

	def __init__(self, iface):
		QDialog.__init__(self)
		self.iface = iface
		self.setupUi(self)
		self.output_path.setText('')
		self.toolButton.clicked.connect(self.select_output)
		self.rBtn_156.setChecked(True)
		self.rBtn_156.toggled.connect(self.checkCombo)
		self.combo_thonban.setEnabled(False)
		self.combo_thonban.clear()
		self.btn_OK.clicked.connect(self.checkRun)
		self.btn_cancel.clicked.connect(self.close_form)
		self.laydstinh()
		self.laydshuyen()
		self.laydsxa()		
		self.com_tinh.currentIndexChanged.connect(self.laydshuyen)
		self.com_huyen.currentIndexChanged.connect(self.laydsxa)
		self.combo_xa.currentIndexChanged.connect(self.laydsthonban)
		orgEncoding=QgsSettings().value('/Processing/encoding') # save setting
		QgsSettings().setValue('/Processing/encoding', 'utf-8') # set uft8	

	def checkRun(self):
		if self.output_path.text() != '':
			self.run()
		else:
			self.iface.messageBar().pushMessage("Chưa chọn thư mục lưu file kết quả", level=Qgis.Warning, duration=5)

	def checkCombo(self):
		if self.rBtn_156.isChecked():
			self.combo_thonban.setEnabled(False)
			self.combo_thonban.clear()
		else:
			self.combo_thonban.setEnabled(True)
			self.laydsthonban()

	def laydstinh(self):
		try:
			self.com_tinh.clear()
			dstinh = docdshanhchinh()
			for item in dstinh:
				tname = item['tinh']
			self.com_tinh.addItems([tname])
		except:
			self.iface.messageBar().pushMessage("Chưa xây dựng CSDL", level=Qgis.Warning, duration=2)

	def laydshuyen(self):
		try:
			self.com_huyen.clear()
			dshuyen = docdshanhchinh()
			tentinh = self.com_tinh.currentText()	
			listhuyen = []	
			for item in dshuyen:
				if item['tinh'] == tentinh:
					hname = item['huyen']
					if hname in listhuyen:
						pass
					else:
						listhuyen.append(hname)
			self.com_huyen.addItems(listhuyen)
		except:
			self.iface.messageBar().pushMessage("Chưa xây dựng CSDL", level=Qgis.Warning, duration=2)

	def laydsxa(self):
		try:
			self.combo_xa.clear()
			dsxa = docdshanhchinh()
			tenhuyen = self.com_huyen.currentText()
			listxa = []
			for item in dsxa:
				if item['huyen'] == tenhuyen:
					xname = item['xa']
					if xname in listxa:
						pass
					else:
						listxa.append(xname)
			self.combo_xa.addItems(listxa)
		except:
			self.iface.messageBar().pushMessage("Chưa xây dựng CSDL", level=Qgis.Warning, duration=2)

	def laydsthonban(self):
		dsthonban = docdshanhchinh()
		tenxa = self.combo_xa.currentText()
		self.combo_thonban.clear()
		for item in dsthonban:
			if item['xa'] == tenxa:
				tbname = item['ddanh']
				self.combo_thonban.addItems([tbname])

	def laymaxa(self):
		try:
			tenxa = self.combo_xa.currentText()
			dsxa = docdshanhchinh()
			for xa in dsxa:
				if xa['xa'] == tenxa:
					maxa = xa['maxa']
					value = {'maxa': maxa}
					return value
		except:
			self.iface.messageBar().pushMessage("Chưa xây dựng CSDL", level=Qgis.Warning, duration=2)

	def select_output(self):
		self.path_solution = str(QFileDialog.getExistingDirectory(self, "v5PFES-Chọn thư mục lưu kết quả"))
		self.output_path.setText(self.path_solution)

	def run(self):
		try:		
			qgis.utils.iface.messageBar().clearWidgets() 
			#set a new message bar
			progressMessageBar = qgis.utils.iface.messageBar()
			######################################
			# Prepare your progress Bar
			######################################
			progress = QProgressBar()
			#Maximum is set to 100, making it easy to work with percentage of completion
			progress.setMaximum(100) 
			#pass the progress bar to the message Bar
			progressMessageBar.pushWidget(progress)

			tempo = str(Path(__file__).parent.absolute()) + '/tempo/tempo.xlsx'
			outpath = self.output_path.text()
			tinh = self.com_tinh.currentText()
			huyen = self.com_huyen.currentText()
			xa = self.combo_xa.currentText()
			thonban = self.combo_thonban.currentText()
			maxa = (self.laymaxa())['maxa']

			export = outpath + '/bieu1.xlsx'
			hc_out = outpath + '/TenHanhChinh.xlsx'
			tinh_out = outpath + '/TenTinh.xlsx'
			xa_out = outpath + '/TenXa.xlsx'
			copy = str(Path(__file__).parent.absolute()) + '/data/Mau12_14.xlsm'
			copy_HB = str(Path(__file__).parent.absolute()) + '/data/Mau12_14_HB.xlsm'
			copy_js = str(Path(__file__).parent.absolute()) + '/data/dsluuvuc.json'
			paste = outpath + '/' + str(maxa) +'_'+ convert_TVKD(xa)+'.xlsm'
			paste_HB = outpath + '/' + str(maxa) +'_'+ convert_TVKD(xa)+'_'+ convert_TVKD(thonban) + '.xlsm'
			paste_js = outpath + '/dsluuvuc.json'
			run = 'start excel.exe '

			if self.rBtn_156.isChecked():
				self.combo_thonban.setEnabled(False)
				i=0
				for n in range(1,7):
					i=i+1
					if n==1:
						df_pfes = pd.read_excel(tempo)
						# ds_maxa = sorted(df_pfes['maxa'].unique().tolist())
						df_pfes = df_pfes.sort_values(by=['maxa','dtuong','churung'], ascending=True)
						df_pfes = df_pfes.loc[((df_pfes['chitra'] == 1))]				
					elif n==2:
						report_comumune(df_pfes,maxa,export)
					elif n==3:
						hanhchinh_export(tempo,maxa,hc_out)
					elif n==4:
						tinh_export(tempo,maxa,tinh_out)
					elif n==5:
						xa_export(tempo,maxa,xa_out)
					else:
						shutil.copy2(copy, paste)
						os.system(run + paste)
					QgsProject.instance().removeAllMapLayers()	

					percent = (i/float(6)) * 100
					progress.setValue(percent)				
					time.sleep(1) 
				qgis.utils.iface.messageBar().clearWidgets()					  
				self.iface.messageBar().pushMessage("Quá trình xuất biểu thành công", level=Qgis.Success, duration=5)
			else:
				self.combo_thonban.setEnabled(True)
				i=0
				for n in range(1,7):
					i=i+1
					if n==1:
						df_pfes = pd.read_excel(tempo)
						# ds_maxa = sorted(df_pfes['maxa'].unique().tolist())
						df_pfes = df_pfes.sort_values(by=['ddanh','dtuong','churung'], ascending=True)
						df_pfes = df_pfes.loc[((df_pfes['chitra'] == 1))]				
					elif n==2:
						report_comumune_HB(df_pfes,thonban,export)
					elif n==3:
						hanhchinh_HB_export(tempo,thonban,hc_out)
					elif n==4:
						tinh_export(tempo,maxa,tinh_out)
					elif n==5:
						xa_export(tempo,maxa,xa_out)
					else:
						shutil.copy2(copy_HB, paste_HB)
						shutil.copy2(copy_js, paste_js)
						os.system(run + paste_HB)
					QgsProject.instance().removeAllMapLayers()	
				
					percent = (i/float(6)) * 100
					progress.setValue(percent)				
					time.sleep(1) 
				qgis.utils.iface.messageBar().clearWidgets()					  
				self.iface.messageBar().pushMessage("Quá trình xuất biểu thành công", level=Qgis.Success, duration=5)
		except:
			qgis.utils.iface.messageBar().clearWidgets()
			self.iface.messageBar().pushMessage("Error","Quá trình xuất biểu thất bại", level=Qgis.Critical, duration=5)
	
	def close_form(self):
		pathout = self.output_path.text()
		databases = filter(os.path.isfile, glob.glob(pathout + '/*.xlsm'))
		if databases:
			for file in databases:
				os.remove(file)
		if os.path.exists(pathout + '/TenHanhChinh.xlsx'):
			os.remove(pathout + '/TenHanhChinh.xlsx')
		if os.path.exists(pathout + '/TenXa.xlsx'):
			os.remove(pathout + '/TenXa.xlsx')
		if os.path.exists(pathout + '/TenTinh.xlsx'):
			os.remove(pathout + '/TenTinh.xlsx')
		if os.path.exists(pathout + '/bieu1.xlsx'):
			os.remove(pathout + '/bieu1.xlsx')
		if os.path.exists(pathout + '/bieu2.xlsx'):
			os.remove(pathout + '/bieu2.xlsx')
		if os.path.exists(pathout + '/dsluuvuc.json'):
			os.remove(pathout + '/dsluuvuc.json')
		self.close()
	

class XuatBieuNhom2_Dlg(QDialog, Ui_Dialog_XuatBieuNhom2):
	def __init__(self, iface):
		QDialog.__init__(self)
		self.iface = iface
		self.setupUi(self)
		self.out_path.setText('')											 
		self.btn_path.clicked.connect(self.select_output)
		self.rBtn_156.setChecked(True)
		self.btn_ok.clicked.connect(self.checkRun)
		self.btn_cancel.clicked.connect(self.close_form)
		self.laydscr()
		self.laydstinh()
		orgEncoding=QgsSettings().value('/Processing/encoding') # save setting
		QgsSettings().setValue('/Processing/encoding', 'utf-8') # set uft8

	def checkRun(self):
		if self.out_path.text() != '':
			self.run()
		else:
			self.iface.messageBar().pushMessage("Chưa chọn thư mục lưu file kết quả", level=Qgis.Warning, duration=5)

	def laydstinh(self):
		try:
			dstinh = docdschurung()
			values = set()
			for item in dstinh:
				values.add(item['tinh'])
			self.com_tinh.addItems(values)
		except:
			self.iface.messageBar().pushMessage("Chưa xây dựng CSDL", level=Qgis.Warning, duration=2)

	def laydscr(self):
		try:
			dscr = docdschurung()
			self.com_churung.clear()
			for cr in dscr:
				tencr = cr['churung']
				self.com_churung.addItems([tencr])
		except:
			self.iface.messageBar().pushMessage("Chưa xây dựng CSDL", level=Qgis.Warning, duration=2)

	def layma(self):
		try:
			tencr = self.com_churung.currentText()
			dscr = docdschurung()
			for cr in dscr:
				if cr['churung'] == tencr:
					macr = cr['machur']
					tentinh = cr['tinh']
					value = {'macr': macr, 'tinh': tentinh}
					return value
		except:
			self.iface.messageBar().pushMessage("Chưa xây dựng CSDL", level=Qgis.Warning, duration=1)

	def select_output(self):
		self.path_solution = str(QFileDialog.getExistingDirectory(self, "v5PFES-Chọn thư mục lưu kết quả"))
		self.out_path.setText(self.path_solution)

	def run(self):
		try:
			#clear the message bar
			qgis.utils.iface.messageBar().clearWidgets() 
			#set a new message bar
			progressMessageBar = qgis.utils.iface.messageBar()
			######################################
			# Prepare your progress Bar
			######################################
			progress = QProgressBar()
			#Maximum is set to 100, making it easy to work with percentage of completion
			progress.setMaximum(100) 
			#pass the progress bar to the message Bar
			progressMessageBar.pushWidget(progress)

			tempo = str(Path(__file__).parent.absolute()) + '/tempo/tempo.xlsx'
			outpath = self.out_path.text()
			cr = self.com_churung.currentText()
			machur = (self.layma())['macr']
			export = outpath + '/bieu2.xlsx'
			chur_out = outpath + '/TenHanhChinh.xlsx'
			tinh_out = outpath + '/TenTinh.xlsx'
			copy = str(Path(__file__).parent.absolute()) + '/data/Mau13_14.xlsm'
			copy_HB = str(Path(__file__).parent.absolute()) + '/data/Mau13_14_HB.xlsm'
			copy_js = str(Path(__file__).parent.absolute()) + '/data/dsluuvuc.json'
			paste = outpath + '/' + str(machur) +'_'+ convert_TVKD(cr)+'.xlsm'
			paste_js = outpath + '/dsluuvuc.json'
			run = 'start excel.exe '
			if self.rBtn_156.isChecked():
				i=0
				for n in range(1,6):
					i=i+1
					if n==1:
						df_pfes = pd.read_excel(tempo)
						df_pfes = df_pfes.loc[(df_pfes['machur'] == machur)]
						df_pfes = df_pfes.loc[((df_pfes['chitra'] == 1))]
						df_pfes = df_pfes.loc[(df_pfes['dtichct'] > 0)]
					elif n==2:
						report_forestActor(df_pfes, export)
					elif n==3:
						churung_export(tempo,machur,chur_out)
					elif n==4:
						province_export(tempo,machur,tinh_out)
					else:
						shutil.copy2(copy, paste)
						os.system(run + paste)
					QgsProject.instance().removeAllMapLayers()

					percent = (i/float(5)) * 100
					progress.setValue(percent)
					time.sleep(1)
				qgis.utils.iface.messageBar().clearWidgets()
				self.iface.messageBar().pushMessage("Quá trình xuất biểu thành công", level=Qgis.Success, duration=5)

			else:
				i=0
				for n in range(1,6):
					i=i+1
					if n==1:
						df_pfes = pd.read_excel(tempo)
						df_pfes = df_pfes.loc[(df_pfes['machur'] == machur)]
						df_pfes = df_pfes.loc[((df_pfes['chitra'] == 1))]
						df_pfes = df_pfes.loc[(df_pfes['dtichct'] > 0)]
					elif n==2:
						report_forestActor_HB(df_pfes, export)
					elif n==3:
						churung_export(tempo,machur,chur_out)
					elif n==4:
						province_export(tempo,machur,tinh_out)
					else:
						shutil.copy2(copy_HB, paste)
						shutil.copy2(copy_js, paste_js)
						os.system(run + paste)
					QgsProject.instance().removeAllMapLayers()

					percent = (i/float(5)) * 100
					progress.setValue(percent)
					time.sleep(1)
				qgis.utils.iface.messageBar().clearWidgets()
				self.iface.messageBar().pushMessage("Quá trình xuất biểu thành công", level=Qgis.Success, duration=5)
		except:
			qgis.utils.iface.messageBar().clearWidgets()
			self.iface.messageBar().pushMessage("Error","Quá trình xuất biểu thất bại", level=Qgis.Critical, duration=5)

	
	def close_form(self):
		pathout = self.out_path.text()
		databases = filter(os.path.isfile, glob.glob(pathout + '/*.xlsm'))
		if databases:
			for file in databases:
				os.remove(file)
		if os.path.exists(pathout + '/TenHanhChinh.xlsx'):
			os.remove(pathout + '/TenHanhChinh.xlsx')
		if os.path.exists(pathout + '/TenXa.xlsx'):
			os.remove(pathout + '/TenXa.xlsx')
		if os.path.exists(pathout + '/TenTinh.xlsx'):
			os.remove(pathout + '/TenTinh.xlsx')
		if os.path.exists(pathout + '/bieu1.xlsx'):
			os.remove(pathout + '/bieu1.xlsx')
		if os.path.exists(pathout + '/bieu2.xlsx'):
			os.remove(pathout + '/bieu2.xlsx')
		if os.path.exists(pathout + '/dsluuvuc.json'):
			os.remove(pathout + '/dsluuvuc.json')
		self.close()
	