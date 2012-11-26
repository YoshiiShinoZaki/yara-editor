#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author:       Ivan Fontarensky
@license:      GNU General Public License 3.0
@contact:      ivan.fontarensky_at_gmail.com
"""



import string
import pickle
import logging
import sys, os, traceback
from yaraeditor.constante import *

from PyQt4 import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import (QObject, Qt, QDir, SIGNAL, SLOT)


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = str

class YTreeWidget(QtGui.QTreeWidget):
    index=-1

    def __init__(self, parent):
        super(YTreeWidget, self).__init__(parent)
        self.setDragEnabled(True)
 

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/pubmedrecord"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def startDrag(self, event):
        text = self.selectedItems()[0].text(0)
        value = "\t$str=\"%s\""%text
        mimeData = QtCore.QMimeData()
        mimeData.setData("text/plain", value)
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        result = drag.start(Qt.MoveAction)

    def mouseMoveEvent(self, event):
        self.startDrag(event)

# vim:ts=4:expandtab:sw=4
