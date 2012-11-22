#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author:       Ivan Fontarensky
@license:      GNU General Public License 3.0
@contact:      ivan.fontarensky_at_gmail.com
"""


import os, sys
import string
import pickle
import logging

from yara.constante import *
from yara.core.highlighter import *

from PyQt4 import *
from PyQt4.QtCore import (QObject, Qt, SIGNAL, SLOT)


# Set the log configuration
logging.basicConfig( \
                filename=LOG_FILE, \
                level=logging.DEBUG, \
                format='%(asctime)s %(levelname)s - %(message)s', \
                datefmt='%d/%m/%Y %H:%M:%S', \
               )
logger = logging.getLogger(NAME)


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Controlleur:
    index=-1
    def __init__(self,application,ui,mainwindow):

        self.app = application
        self.ui_yaraeditor = ui
        self.mainwindow = mainwindow

        #Create our YaraHighlighter derived from QSyntaxHighlighter
        yaraEdit = self.ui_yaraeditor.yaraEdit
        highlighter = YaraHighlighter(yaraEdit.document())
        
        # Load Menu contextuel
        self.ui_yaraeditor.treeYara.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.app.connect(self.ui_yaraeditor.treeYara, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"), self.load_menu_context)
        self.app.connect(self.ui_yaraeditor.treeYara, QtCore.SIGNAL("itemSelectionChanged()"),self.change_text)

        # File
        self.app.connect(self.ui_yaraeditor.actionEnregistrer,SIGNAL("triggered()"),self.save_item)
        
        self.load_tree_yara()
        

    def action_add_item(self):
        """
        Add item
        """
        yara = add_yara(YARA_NAME_DEFAULT,YARA_CODE_DEFAULT)
        if yara != None:
            self.add_item_in_tree(yara)

 
    def action_del_item(self):
        """
        Add item
        """   
        tree = self.ui_yaraeditor.treeYara
        item  = tree.currentItem()
        yara = get_yara(_id=str(item.text(10)))[0]
        self.del_item_in_tree(yara)
        
        
    def add_item_in_tree(self,yara):
        """
        Add item
        """   
        tree = self.ui_yaraeditor.treeYara
        item = QtGui.QTreeWidgetItem(tree)
        item.setText(0,QtGui.QApplication.translate("MainWindow", yara._name, None, QtGui.QApplication.UnicodeUTF8))
        item.setText(10,QtGui.QApplication.translate("MainWindow", str(yara.id), None, QtGui.QApplication.UnicodeUTF8))
   
    def del_item_in_tree(self,yara):
        """
        Delete this item recursively
        """
        tree = self.ui_yaraeditor.treeYara
        item  = tree.currentItem()
        tree.removeItemWidget(item,0)
        del_yara(_id=yara.id)
        tree.clear()
        self.load_tree_yara()
        
    def change_text(self):
        """
        Set text on yara
        """
        item  = self.ui_yaraeditor.treeYara.currentItem()
        yara = get_yara(_id=int(item.text(10)))[0]
        self.set_text(yara._data)

    def set_text(self,text):
        """
        Set text on yara
        """
        yaraEdit = self.ui_yaraeditor.yaraEdit
        
        yaraEdit.setPlainText(text.replace(' { ','\n{ ').replace(' }',' }\n'))

    def get_text(self):
        """
        Set text on yara
        """
        yaraEdit = self.ui_yaraeditor.yaraEdit
        return str(yaraEdit.toPlainText())

    def load_menu_context(self, point):

        items = self.ui_yaraeditor.treeYara.selectedItems()

        # On définie le menu contextuel.
        menu=QtGui.QMenu()

        action_del=menu.addAction("Delete yara file")
        self.app.connect(action_del, QtCore.SIGNAL("triggered()"), self.action_del_item)

        action_add=menu.addAction("Add new yara")
        self.app.connect(action_add, QtCore.SIGNAL("triggered()"), self.action_add_item)


        # Il reste à lier chaque clic sur le menu à une action réelle via un SLOT.
        menu.exec_(QtGui.QCursor.pos())
        
    def load_tree_yara(self):
        """
        """
        self.ui_yaraeditor.treeYara.clear()

            
    def save_item(self):
        """
        """
        item  = self.ui_yaraeditor.treeYara.currentItem()


# vim:ts=4:expandtab:sw=4
