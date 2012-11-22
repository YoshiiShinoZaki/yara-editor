# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yaraeditor.ui'
#
# Created: Thu Nov 22 23:32:20 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_YaraEditor(object):
    def setupUi(self, YaraEditor):
        YaraEditor.setObjectName(_fromUtf8("YaraEditor"))
        YaraEditor.resize(1117, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logo/images/logo.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        YaraEditor.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(YaraEditor)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget_3 = QtGui.QWidget(self.widget)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pathYara = QtGui.QLineEdit(self.widget_3)
        self.pathYara.setReadOnly(False)
        self.pathYara.setObjectName(_fromUtf8("pathYara"))
        self.verticalLayout_2.addWidget(self.pathYara)
        self.yaraTree = QtGui.QTreeView(self.widget_3)
        self.yaraTree.setObjectName(_fromUtf8("yaraTree"))
        self.verticalLayout_2.addWidget(self.yaraTree)
        self.horizontalLayout.addWidget(self.widget_3)
        self.yaraEdit = QtGui.QTextEdit(self.widget)
        self.yaraEdit.setObjectName(_fromUtf8("yaraEdit"))
        self.horizontalLayout.addWidget(self.yaraEdit)
        self.widget_4 = QtGui.QWidget(self.widget)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.pathMalware = QtGui.QLineEdit(self.widget_4)
        self.pathMalware.setReadOnly(False)
        self.pathMalware.setObjectName(_fromUtf8("pathMalware"))
        self.verticalLayout_3.addWidget(self.pathMalware)
        self.malwareTree = QtGui.QTreeView(self.widget_4)
        self.malwareTree.setObjectName(_fromUtf8("malwareTree"))
        self.verticalLayout_3.addWidget(self.malwareTree)
        self.horizontalLayout.addWidget(self.widget_4)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtGui.QWidget(self.centralwidget)
        self.widget_2.setMaximumSize(QtCore.QSize(16777215, 110))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.outputEdit = QtGui.QTextEdit(self.widget_2)
        self.outputEdit.setMaximumSize(QtCore.QSize(16777215, 100))
        self.outputEdit.setReadOnly(True)
        self.outputEdit.setObjectName(_fromUtf8("outputEdit"))
        self.horizontalLayout_2.addWidget(self.outputEdit)
        self.verticalLayout.addWidget(self.widget_2)
        YaraEditor.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(YaraEditor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1117, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        YaraEditor.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(YaraEditor)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        YaraEditor.setStatusBar(self.statusbar)
        self.actionNouveau = QtGui.QAction(YaraEditor)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/images/win/filenew.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionNouveau.setIcon(icon1)
        self.actionNouveau.setObjectName(_fromUtf8("actionNouveau"))
        self.actionExit = QtGui.QAction(YaraEditor)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionEnregistrer = QtGui.QAction(YaraEditor)
        self.actionEnregistrer.setObjectName(_fromUtf8("actionEnregistrer"))

        self.retranslateUi(YaraEditor)
        QtCore.QMetaObject.connectSlotsByName(YaraEditor)

    def retranslateUi(self, YaraEditor):
        YaraEditor.setWindowTitle(QtGui.QApplication.translate("YaraEditor", "Yara-Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNouveau.setText(QtGui.QApplication.translate("YaraEditor", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNouveau.setShortcut(QtGui.QApplication.translate("YaraEditor", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("YaraEditor", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("YaraEditor", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEnregistrer.setText(QtGui.QApplication.translate("YaraEditor", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEnregistrer.setShortcut(QtGui.QApplication.translate("YaraEditor", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))

import yaraeditor_rc
