# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yaraeditor.ui'
#
# Created: Thu Nov 22 17:07:36 2012
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
        self.centralwidget = QtGui.QWidget(YaraEditor)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.treeYara = QtGui.QTreeWidget(self.widget)
        self.treeYara.setMinimumSize(QtCore.QSize(200, 0))
        self.treeYara.setMaximumSize(QtCore.QSize(200, 16777215))
        self.treeYara.setObjectName(_fromUtf8("treeYara"))
        self.treeYara.headerItem().setText(0, _fromUtf8("1"))
        self.treeYara.header().setVisible(False)
        self.horizontalLayout.addWidget(self.treeYara)
        self.yaraEdit = QtGui.QTextEdit(self.widget)
        self.yaraEdit.setObjectName(_fromUtf8("yaraEdit"))
        self.horizontalLayout.addWidget(self.yaraEdit)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtGui.QWidget(self.centralwidget)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(611, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(self.widget_2)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addWidget(self.widget_2)
        YaraEditor.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(YaraEditor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1117, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFichier = QtGui.QMenu(self.menubar)
        self.menuFichier.setObjectName(_fromUtf8("menuFichier"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        YaraEditor.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(YaraEditor)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        YaraEditor.setStatusBar(self.statusbar)
        self.actionNouveau = QtGui.QAction(YaraEditor)
        self.actionNouveau.setObjectName(_fromUtf8("actionNouveau"))
        self.actionQuitter = QtGui.QAction(YaraEditor)
        self.actionQuitter.setObjectName(_fromUtf8("actionQuitter"))
        self.actionEnregistrer = QtGui.QAction(YaraEditor)
        self.actionEnregistrer.setObjectName(_fromUtf8("actionEnregistrer"))
        self.menuFichier.addAction(self.actionNouveau)
        self.menuFichier.addAction(self.actionEnregistrer)
        self.menuFichier.addAction(self.actionQuitter)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(YaraEditor)
        QtCore.QMetaObject.connectSlotsByName(YaraEditor)

    def retranslateUi(self, YaraEditor):
        YaraEditor.setWindowTitle(QtGui.QApplication.translate("YaraEditor", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("YaraEditor", "Appliquer sur la base", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFichier.setTitle(QtGui.QApplication.translate("YaraEditor", "Fichier", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("YaraEditor", "?", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNouveau.setText(QtGui.QApplication.translate("YaraEditor", "Nouveau", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNouveau.setShortcut(QtGui.QApplication.translate("YaraEditor", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuitter.setText(QtGui.QApplication.translate("YaraEditor", "Quitter", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuitter.setShortcut(QtGui.QApplication.translate("YaraEditor", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEnregistrer.setText(QtGui.QApplication.translate("YaraEditor", "Enregistrer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEnregistrer.setShortcut(QtGui.QApplication.translate("YaraEditor", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))

