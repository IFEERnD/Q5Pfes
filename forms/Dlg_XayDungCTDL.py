# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dlg_XayDungCTDL.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_XayDungCTDL(object):
    def setupUi(self, Dialog_XayDungCTDL):
        Dialog_XayDungCTDL.setObjectName("Dialog_XayDungCTDL")
        Dialog_XayDungCTDL.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_XayDungCTDL)
        self.buttonBox.setGeometry(QtCore.QRect(40, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog_XayDungCTDL)
        self.label.setGeometry(QtCore.QRect(20, 30, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog_XayDungCTDL)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog_XayDungCTDL)
        self.label_3.setGeometry(QtCore.QRect(20, 170, 251, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.widget = QtWidgets.QWidget(Dialog_XayDungCTDL)
        self.widget.setGeometry(QtCore.QRect(20, 50, 361, 25))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)
        self.widget1 = QtWidgets.QWidget(Dialog_XayDungCTDL)
        self.widget1.setGeometry(QtCore.QRect(20, 120, 361, 25))
        self.widget1.setObjectName("widget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget1)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.widget2 = QtWidgets.QWidget(Dialog_XayDungCTDL)
        self.widget2.setGeometry(QtCore.QRect(20, 190, 361, 25))
        self.widget2.setObjectName("widget2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget2)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_3.addWidget(self.lineEdit_3, 0, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_3.addWidget(self.pushButton_3, 0, 1, 1, 1)

        self.retranslateUi(Dialog_XayDungCTDL)
        self.buttonBox.accepted.connect(Dialog_XayDungCTDL.accept)
        self.buttonBox.rejected.connect(Dialog_XayDungCTDL.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_XayDungCTDL)

    def retranslateUi(self, Dialog_XayDungCTDL):
        _translate = QtCore.QCoreApplication.translate
        Dialog_XayDungCTDL.setWindowTitle(_translate("Dialog_XayDungCTDL", "v5PFES - Xây dựng cấu trúc dữ liệu"))
        self.label.setText(_translate("Dialog_XayDungCTDL", "Chọn lớp bản đồ hiện trạng rừng (.shp)"))
        self.label_2.setText(_translate("Dialog_XayDungCTDL", "Chọn danh sách lưu vực (.xlsx)"))
        self.label_3.setText(_translate("Dialog_XayDungCTDL", "Chọn thu mục chứa lớp bản đồ đầu ra  (.shp)"))
        self.pushButton.setText(_translate("Dialog_XayDungCTDL", "..."))
        self.pushButton_2.setText(_translate("Dialog_XayDungCTDL", "..."))
        self.pushButton_3.setText(_translate("Dialog_XayDungCTDL", "..."))

