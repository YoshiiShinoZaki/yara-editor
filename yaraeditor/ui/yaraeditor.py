# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yaraeditor.ui'
#
# Created: Fri Nov 23 17:37:06 2012
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
        self.MainWidget = QtGui.QWidget(self.centralwidget)
        self.MainWidget.setObjectName(_fromUtf8("MainWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.MainWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widgetYara = QtGui.QWidget(self.MainWidget)
        self.widgetYara.setMaximumSize(QtCore.QSize(305, 16777215))
        self.widgetYara.setObjectName(_fromUtf8("widgetYara"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widgetYara)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pathYara = QtGui.QLineEdit(self.widgetYara)
        self.pathYara.setMaximumSize(QtCore.QSize(300, 16777215))
        self.pathYara.setReadOnly(False)
        self.pathYara.setObjectName(_fromUtf8("pathYara"))
        self.verticalLayout_2.addWidget(self.pathYara)
        self.yaraTree = QtGui.QTreeView(self.widgetYara)
        self.yaraTree.setMaximumSize(QtCore.QSize(300, 16777215))
        self.yaraTree.setObjectName(_fromUtf8("yaraTree"))
        self.verticalLayout_2.addWidget(self.yaraTree)
        self.horizontalLayout.addWidget(self.widgetYara)
        self.widgetEditor = QtGui.QWidget(self.MainWidget)
        self.widgetEditor.setObjectName(_fromUtf8("widgetEditor"))
        self.horizontalLayout.addWidget(self.widgetEditor)
        self.widgetMalware = QtGui.QWidget(self.MainWidget)
        self.widgetMalware.setMaximumSize(QtCore.QSize(305, 16777215))
        self.widgetMalware.setObjectName(_fromUtf8("widgetMalware"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widgetMalware)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.pathMalware = QtGui.QLineEdit(self.widgetMalware)
        self.pathMalware.setMaximumSize(QtCore.QSize(300, 16777215))
        self.pathMalware.setReadOnly(False)
        self.pathMalware.setObjectName(_fromUtf8("pathMalware"))
        self.verticalLayout_3.addWidget(self.pathMalware)
        self.malwareTree = QtGui.QTreeView(self.widgetMalware)
        self.malwareTree.setMaximumSize(QtCore.QSize(300, 16777215))
        self.malwareTree.setObjectName(_fromUtf8("malwareTree"))
        self.verticalLayout_3.addWidget(self.malwareTree)
        self.horizontalLayout.addWidget(self.widgetMalware)
        self.verticalLayout.addWidget(self.MainWidget)
        self.widgetOutput = QtGui.QWidget(self.centralwidget)
        self.widgetOutput.setMaximumSize(QtCore.QSize(16777215, 110))
        self.widgetOutput.setObjectName(_fromUtf8("widgetOutput"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widgetOutput)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.outputEdit = QtGui.QTextEdit(self.widgetOutput)
        self.outputEdit.setMaximumSize(QtCore.QSize(16777215, 100))
        self.outputEdit.setReadOnly(True)
        self.outputEdit.setObjectName(_fromUtf8("outputEdit"))
        self.horizontalLayout_2.addWidget(self.outputEdit)
        self.verticalLayout.addWidget(self.widgetOutput)
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
