#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------
#    q5pfes_menu - QGIS plugins menu class
##  --------------------------------------------------------

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from .q5pfes_dialogs import *
from .q5pfes_library import *
# ---------------------------------------------

class q5pfes_menu:
	
	def __init__(self, iface):
		self.iface = iface
		self.q5pfes_menu = None
		self._about_browser = None

	def ifee_add_submenu(self, submenu,icon):
		if self.q5pfes_menu != None:
			submenu.setIcon(QIcon(icon))
			self.q5pfes_menu.addMenu(submenu)
		else:
			self.iface.addPluginToMenu("&ifee", submenu.menuAction())

	def initGui(self):


		# Khởi tạo IFEE trên menubar của QGIS
		self.q5pfes_menu = QMenu(QCoreApplication.translate("q5pfes", "Q5PFES"))
		self.iface.mainWindow().menuBar().insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.q5pfes_menu)

		# Menu

		icon = QIcon(os.path.dirname(__file__) + "/icons/configuration.png")
		self.cauhinh_action = QAction(icon, u'Cấu hình làm việc', self.iface.mainWindow())
		self.cauhinh_action.triggered.connect(self.cauhinh)
		self.q5pfes_menu.addAction(self.cauhinh_action) 

		icon = QIcon(os.path.dirname(__file__) + "/icons/layers.png")
		self.bando_DBR = QMenu(u'Khai thác bản đồ DBR')		
		self.ifee_add_submenu(self.bando_DBR, icon)
 
		icon = QIcon(os.path.dirname(__file__) + "/icons/download.png")
		self.downbd_action = QAction(icon, u'Tải bản đồ DBR', self.iface.mainWindow())
		self.downbd_action.triggered.connect(self.downbd)
		self.bando_DBR.addAction(self.downbd_action)

		icon = QIcon(os.path.dirname(__file__) + "/icons/standardized.png")
		self.chuanhoabd_action = QAction(icon, u'Chuẩn hóa bản đồ DBR', self.iface.mainWindow())
		self.chuanhoabd_action.triggered.connect(self.chuanhoabd)
		self.bando_DBR.addAction(self.chuanhoabd_action)

		# --- Menu Build map ---
		icon = QIcon(os.path.dirname(__file__) + "/icons/buildmap.png")
		self.xaydungbando_DVMTR = QMenu(u'Xây dựng bản đồ DVMTR')		
		self.ifee_add_submenu(self.xaydungbando_DVMTR, icon)

		# Menu Build data structure
		icon = QIcon(os.path.dirname(__file__) + "/icons/structure.png")
		self.congcu1 = QAction(icon, u'Xây dựng cấu trúc dữ liệu', self.iface.mainWindow())
		self.congcu1.triggered.connect(self.xaydungCTDL)
		self.xaydungbando_DVMTR.addAction(self.congcu1)

		# Menu Update payment area
		icon = QIcon(os.path.dirname(__file__) + "/icons/overlap.png")
		self.congcu2 = QAction(icon, u'Cập nhật vùng chi trả', self.iface.mainWindow())
		self.congcu2.triggered.connect(self.capnhatVCT)
		self.xaydungbando_DVMTR.addAction(self.congcu2)

		# Menu Update payment area
		icon = QIcon(os.path.dirname(__file__) + "/icons/difference.png")
		self.congcu5 = QAction(icon, u'Cập nhật khu vực đã có nguồn đầu tư khác', self.iface.mainWindow())
		self.congcu5.triggered.connect(self.capnhatNSK)
		self.xaydungbando_DVMTR.addAction(self.congcu5)
        
        # Menu Update Payment forest
		icon = QIcon(os.path.dirname(__file__) + "/icons/update.png")
		self.congcu4 = QAction(icon, u'Cập nhật dữ liệu chi trả', self.iface.mainWindow())
		self.congcu4.triggered.connect(self.capnhatDTCT)
		self.xaydungbando_DVMTR.addAction(self.congcu4)

		icon = QIcon(os.path.dirname(__file__) + "/icons/price.png")
		self.congcu3 = QAction(icon, u'Tính đơn giá chi trả', self.iface.mainWindow())
		self.congcu3.triggered.connect(self.capnhatDG)
		self.xaydungbando_DVMTR.addAction(self.congcu3)

		# Menu Manager Database
		icon = QIcon(os.path.dirname(__file__) + "/icons/build.png")
		self.xaydungCSDL_action = QAction(icon, u'Xây dựng cơ sở dữ liệu', self.iface.mainWindow())
		self.xaydungCSDL_action.triggered.connect(self.xaydungCSDL)
		self.q5pfes_menu.addAction(self.xaydungCSDL_action)

		# Thêm Menu Statistic
		icon = QIcon(os.path.dirname(__file__) + "/icons/statistics.png")
		self.thongkeSL = QMenu(u'Thống kê số liệu')		
		self.ifee_add_submenu(self.thongkeSL, icon)		

		icon = QIcon(os.path.dirname(__file__) + "/icons/table1.png")
		self.congcu1 = QAction(icon, u'Xuất biểu nhóm 1', self.iface.mainWindow())
		self.congcu1.triggered.connect(self.xuatbieuNhom1)
		self.thongkeSL.addAction(self.congcu1)

		icon = QIcon(os.path.dirname(__file__) + "/icons/table1.png")
		self.congcu2 = QAction(icon, u'Xuất biểu nhóm 2', self.iface.mainWindow())
		self.congcu2.triggered.connect(self.xuatbieuNhom2)
		self.thongkeSL.addAction(self.congcu2)

		icon = QIcon(os.path.dirname(__file__) + "/icons/table1.png")
		self.congcu3 = QAction(icon, u'Xuất biểu số 11 phụ lục VI NĐ-156', self.iface.mainWindow())
		self.congcu3.triggered.connect(self.xuatbieu11_156)
		self.thongkeSL.addAction(self.congcu3)

        # Menu Help
		icon = QIcon(os.path.dirname(__file__) + "/icons/guidebook.png")
		self.help = QAction(icon, u'Hướng dẫn sử dụng', self.iface.mainWindow())
		self.help.triggered[bool].connect(lambda: open_link_with_browser("https://www.youtube.com/watch?v=f4laSNw6W1M"))
		self.q5pfes_menu.addAction(self.help)
        
        # Menu About
		icon = QIcon(os.path.dirname(__file__) + "/icons/about.png")
		self.about = QAction(icon, u'Giới thiệu', self.iface.mainWindow())
		self.about.triggered.connect(self.show_about)
		self.q5pfes_menu.addAction(self.about)
			
	def unload(self):
		if self.q5pfes_menu != None:
			self.iface.mainWindow().menuBar().removeAction(self.q5pfes_menu.menuAction())
		else:
			self.iface.removePluginMenu("&ifee", self.geoprocessing_menu.menuAction())
			self.iface.removePluginMenu("&ifee", self.tool_menu.menuAction())


	##########################
	def cauhinh(self):
		dialog = CauHinh_Dlg(self.iface)
		dialog.exec_()

	def downbd(self):
		dialog = DownloadDBR_Dlg(self.iface)
		dialog.exec_()
	
	def chuanhoabd(self):
		dialog = ChuanHoaDBR_Dlg(self.iface)
		dialog.exec_()

	def xaydungCTDL(self):
		dialog = XayDungCTDL_Dlg(self.iface)
		dialog.exec_()

	def capnhatVCT(self):
		dialog = CapNhatVCT_Dlg(self.iface)
		dialog.exec_()

	def capnhatNSK(self):
		dialog = CapNhatNSK_Dlg(self.iface)
		dialog.exec_()

	def capnhatDTCT(self):
		dialog = CapNhatDTCT_Dlg(self.iface)
		dialog.exec_()

	def capnhatDG(self):
		dialog = CapNhatDG_Dlg(self.iface)
		dialog.exec_()

	def xaydungCSDL(self):
		dialog = XayDungCSDL_Dlg(self.iface)
		dialog.exec_()	

	def xuatbieuNhom1(self):
		dialog = XuatBieuNhom1_Dlg(self.iface)
		dialog.exec_()

	def xuatbieuNhom2(self):
		dialog = XuatBieuNhom2_Dlg(self.iface)
		dialog.exec_()

	def xuatbieu11_156(self):
		dialog = XuatBieu11_156_Dlg(self.iface)
		dialog.exec_()

	def show_about(self, _):
		if self._about_browser is None:
			self._about_browser = QTextBrowser()
			self._about_browser.setReadOnly(True)
			self._about_browser.setOpenExternalLinks(True)
			self._about_browser.setMinimumSize(500, 300)
            # TODO: Template terms.html first section, per subscription level
            #       Collect subscription info from self.p_client.user
			self._about_browser.setSource(
				QUrl.fromLocalFile(str(os.path.dirname(__file__) + "/forms/about.html"))
			)
			self._about_browser.setWindowModality(Qt.ApplicationModal)
		self._about_browser.show()
