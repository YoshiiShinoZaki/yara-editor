# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rules_generator.ui'
#
# Created: Sun Dec  2 12:09:53 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DialogGenerator(object):
    def setupUi(self, DialogGenerator):
        DialogGenerator.setObjectName(_fromUtf8("DialogGenerator"))
        DialogGenerator.resize(728, 507)
        self.verticalLayout = QtGui.QVBoxLayout(DialogGenerator)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(DialogGenerator)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget_3 = QtGui.QWidget(self.widget)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widget_4 = QtGui.QWidget(self.widget_3)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.widget_4)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.btnBrowseNewFile = QtGui.QToolButton(self.widget_4)
        self.btnBrowseNewFile.setObjectName(_fromUtf8("btnBrowseNewFile"))
        self.horizontalLayout_3.addWidget(self.btnBrowseNewFile)
        self.verticalLayout_2.addWidget(self.widget_4)
        self.listFiles = QtGui.QListWidget(self.widget_3)
        self.listFiles.setObjectName(_fromUtf8("listFiles"))
        self.verticalLayout_2.addWidget(self.listFiles)
        self.horizontalLayout.addWidget(self.widget_3)
        self.treeWidget = QtGui.QTreeWidget(self.widget)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.treeWidget.header().setVisible(False)
        self.horizontalLayout.addWidget(self.treeWidget)
        self.widget_5 = QtGui.QWidget(self.widget)
        self.widget_5.setObjectName(_fromUtf8("widget_5"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget_5)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.widget_6 = QtGui.QWidget(self.widget_5)
        self.widget_6.setObjectName(_fromUtf8("widget_6"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget_6)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.widget_6)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.btnBrowseNewFamily = QtGui.QToolButton(self.widget_6)
        self.btnBrowseNewFamily.setObjectName(_fromUtf8("btnBrowseNewFamily"))
        self.horizontalLayout_4.addWidget(self.btnBrowseNewFamily)
        self.verticalLayout_3.addWidget(self.widget_6)
        self.listFilesFamily = QtGui.QListWidget(self.widget_5)
        self.listFilesFamily.setObjectName(_fromUtf8("listFilesFamily"))
        self.verticalLayout_3.addWidget(self.listFilesFamily)
        self.horizontalLayout.addWidget(self.widget_5)
        self.verticalLayout.addWidget(self.widget)
        self.buttonBox = QtGui.QDialogButtonBox(DialogGenerator)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogGenerator)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogGenerator.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogGenerator.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogGenerator)

    def retranslateUi(self, DialogGenerator):
        DialogGenerator.setWindowTitle(QtGui.QApplication.translate("DialogGenerator", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogGenerator", "Other Malware (False positive)", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowseNewFile.setText(QtGui.QApplication.translate("DialogGenerator", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DialogGenerator", "Same Family", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowseNewFamily.setText(QtGui.QApplication.translate("DialogGenerator", "...", None, QtGui.QApplication.UnicodeUTF8))

