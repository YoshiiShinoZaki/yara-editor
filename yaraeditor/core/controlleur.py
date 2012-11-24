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
from yaraeditor.core.highlighter import *
from yaraeditor.core.codeeditor import *

from PyQt4 import *
from PyQt4.QtCore import (QObject, Qt, QDir, SIGNAL, SLOT)



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

if sys.platform.startswith('darwin'):
    rsrcPath = ":/images/mac"
else:
    rsrcPath = ":/images/win"

class Controlleur:
    index=-1
    def __init__(self,application,ui,mainwindow,fileName=None,config=None):

        self.app = application
        self.ui_yaraeditor = ui
        self.mainwindow = mainwindow
        self.config = config

        mainwindow.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.setupFileActions()
        self.setupEditActions()
        self.setupViewActions()
        self.setupYaraActions()
        self.setupHelpActions()

        self.yaraTree = self.ui_yaraeditor.yaraTree
        self.malwareTree = self.ui_yaraeditor.malwareTree
        self.outputEdit = self.ui_yaraeditor.outputEdit
        self.pathYaraEdit = self.ui_yaraeditor.pathYara
        self.pathMalwareEdit = self.ui_yaraeditor.pathMalware


        highlighter = OutputHighlighter(self.outputEdit.document())

        self.setupEditorActions()


        self.path_yara=config.get(CONF_PREFERENCE, CONF_PATH_YARA)
        self.path_malware=config.get(CONF_PREFERENCE, CONF_PATH_MALWARE)
        self.pathYaraEdit.setText(self.path_yara)
        self.pathMalwareEdit.setText(self.path_malware)



        self.modelYara = QtGui.QDirModel()
        self.yaraTree.setModel(self.modelYara)
        self.yaraTree.setAnimated(False)
        self.yaraTree.setIndentation(20)
        self.yaraTree.setSortingEnabled(True)
        self.yaraTree.setColumnHidden(1,True)
        self.yaraTree.setColumnHidden(2,True)
        self.yaraTree.setColumnHidden(3,True)
        self.yaraTree.setRootIndex( self.modelYara.index(self.path_yara) );


        self.mainwindow.connect(self.yaraTree, SIGNAL('itemDoubleClicked'), self.treeOpenFile) 

        self.modelMalware = QtGui.QDirModel()
        self.malwareTree.setModel(self.modelMalware)
        self.malwareTree.setAnimated(False)
        self.malwareTree.setIndentation(20)
        self.malwareTree.setSortingEnabled(True)
        self.malwareTree.setColumnHidden(1,True)
        self.malwareTree.setColumnHidden(2,True)
        self.malwareTree.setColumnHidden(3,True)
        self.malwareTree.setRootIndex( self.modelMalware.index(self.path_malware) );
        self.malwareTree.setSelectionMode( QtGui.QAbstractItemView.MultiSelection )       

        QtCore.QObject.connect(self.yaraTree, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")),self.treeOpenFile)
        QtCore.QObject.connect(self.pathYaraEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.changeYaraPath)
        QtCore.QObject.connect(self.pathMalwareEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.changeMalwarePath)

        if not self.load(fileName):
            self.fileNew()


    def setupFileActions(self):
        tb = QtGui.QToolBar(self.mainwindow)
        tb.setWindowTitle("File Actions")
        self.mainwindow.addToolBar(tb)

        menu = QtGui.QMenu("&File", self.mainwindow)
        self.mainwindow.menuBar().addMenu(menu)

        self.actionNew = QtGui.QAction(
                QtGui.QIcon.fromTheme('document-new',
                        QtGui.QIcon(rsrcPath + '/filenew.png')),
                "&New", self.mainwindow, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.New, triggered=self.fileNew)
        tb.addAction(self.actionNew)
        menu.addAction(self.actionNew)

        self.actionOpen = QtGui.QAction(
                QtGui.QIcon.fromTheme('document-open',
                        QtGui.QIcon(rsrcPath + '/fileopen.png')),
                "&Open...", self.mainwindow, shortcut=QtGui.QKeySequence.Open,
                triggered=self.fileOpen)
        tb.addAction(self.actionOpen)
        menu.addAction(self.actionOpen)
        menu.addSeparator()

        self.actionSave = QtGui.QAction(
                QtGui.QIcon.fromTheme('document-save',
                        QtGui.QIcon(rsrcPath + '/filesave.png')),
                "&Save", self.mainwindow, shortcut=QtGui.QKeySequence.Save,
                triggered=self.fileSave, enabled=False)
        tb.addAction(self.actionSave)
        menu.addAction(self.actionSave)

        self.actionSaveAs = QtGui.QAction("Save &As...", self.mainwindow,
                priority=QtGui.QAction.LowPriority,
                shortcut=QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_S,
                triggered=self.fileSaveAs)
        menu.addAction(self.actionSaveAs)
        menu.addSeparator()
 
        self.actionPrint = QtGui.QAction(
                QtGui.QIcon.fromTheme('document-print',
                        QtGui.QIcon(rsrcPath + '/fileprint.png')),
                "&Print...", self.mainwindow, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Print, triggered=self.filePrint)
        tb.addAction(self.actionPrint)
        menu.addAction(self.actionPrint)

        self.actionPrintPreview = QtGui.QAction(
                QtGui.QIcon.fromTheme('fileprint',
                        QtGui.QIcon(rsrcPath + '/fileprint.png')),
                "Print Preview...", self.mainwindow,
                shortcut=QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_P,
                triggered=self.filePrintPreview)
        menu.addAction(self.actionPrintPreview)

        self.actionPrintPdf = QtGui.QAction(
                QtGui.QIcon.fromTheme('exportpdf',
                        QtGui.QIcon(rsrcPath + '/exportpdf.png')),
                "&Export PDF...", self.mainwindow, priority=QtGui.QAction.LowPriority,
                shortcut=QtCore.Qt.CTRL + QtCore.Qt.Key_D,
                triggered=self.filePrintPdf)
        tb.addAction(self.actionPrintPdf)
        menu.addAction(self.actionPrintPdf)
        menu.addSeparator()

        self.actionQuit = QtGui.QAction("&Quit", self.mainwindow,
                shortcut=QtGui.QKeySequence.Quit, triggered=self.mainwindow.close)
        menu.addAction(self.actionQuit)

    def setupEditActions(self):
        tb = QtGui.QToolBar(self.mainwindow)
        tb.setWindowTitle("Edit Actions")
        self.mainwindow.addToolBar(tb)

        menu = QtGui.QMenu("&Edit", self.mainwindow)
        self.mainwindow.menuBar().addMenu(menu)

        self.actionUndo = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-undo',
                        QtGui.QIcon(rsrcPath + '/editundo.png')),
                "&Undo", self.mainwindow, shortcut=QtGui.QKeySequence.Undo)
        tb.addAction(self.actionUndo)
        menu.addAction(self.actionUndo)

        self.actionRedo = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-redo',
                        QtGui.QIcon(rsrcPath + '/editredo.png')),
                "&Redo", self.mainwindow, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Redo)
        tb.addAction(self.actionRedo)
        menu.addAction(self.actionRedo)
        menu.addSeparator()

        self.actionCut = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-cut',
                        QtGui.QIcon(rsrcPath + '/editcut.png')),
                "Cu&t", self.mainwindow, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Cut)
        tb.addAction(self.actionCut)
        menu.addAction(self.actionCut)

        self.actionCopy = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-copy',
                        QtGui.QIcon(rsrcPath + '/editcopy.png')),
                "&Copy", self.mainwindow, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Copy)
        tb.addAction(self.actionCopy)
        menu.addAction(self.actionCopy)

        self.actionPaste = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-paste',
                        QtGui.QIcon(rsrcPath + '/editpaste.png')),
                "&Paste", self.mainwindow, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Paste,
                enabled=(len(QtGui.QApplication.clipboard().text()) != 0))
        tb.addAction(self.actionPaste)
        menu.addAction(self.actionPaste)

    def setupViewActions(self):
        menu = QtGui.QMenu("&View", self.mainwindow)
        self.mainwindow.menuBar().addMenu(menu)

        self.actionYaraBrowser = QtGui.QAction(
                "&Yara Browser", self.mainwindow, toggled=self.ui_yaraeditor.dockWidgetYara.setVisible)
        self.actionYaraBrowser.setCheckable(True)
        self.actionYaraBrowser.setChecked(True)
        menu.addAction(self.actionYaraBrowser)

        self.actionMalwareBrowser = QtGui.QAction(
                "&Malware Browser", self.mainwindow, toggled=self.ui_yaraeditor.dockWidgetMalware.setVisible)
        self.actionMalwareBrowser.setCheckable(True)
        self.actionMalwareBrowser.setChecked(True)

        menu.addAction(self.actionMalwareBrowser)

    def setupYaraActions(self):
        tb = QtGui.QToolBar(self.mainwindow)
        tb.setWindowTitle("Yara Actions")
        self.mainwindow.addToolBar(tb)

        menu = QtGui.QMenu("&Yara", self.mainwindow)
        self.mainwindow.menuBar().addMenu(menu)

        self.actionExecuteYara = QtGui.QAction(
                QtGui.QIcon.fromTheme('yara-execute',
                        QtGui.QIcon(rsrcPath + '/exec.png')),
                "&Execute", self.mainwindow, shortcut=QtGui.QKeySequence(Qt.Key_F5),
                triggered=self.yaraExecute)

        tb.addAction(self.actionExecuteYara)
        menu.addAction(self.actionExecuteYara)

    def setupHelpActions(self):
        helpMenu = QtGui.QMenu("Help", self.mainwindow)
        helpMenu.addAction("About", self.about)
        helpMenu.addAction("About &Qt", QtGui.qApp.aboutQt)        

    def setupEditorActions(self):
        self.ui_yaraeditor.horizontalLayout = QtGui.QHBoxLayout(self.ui_yaraeditor.widgetEditor)
        self.ui_yaraeditor.horizontalLayout.setMargin(0)
        self.ui_yaraeditor.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))        
        self.ui_yaraeditor.yaraEdit = CodeEditor(self.ui_yaraeditor.widgetEditor)
        self.ui_yaraeditor.yaraEdit.setObjectName(_fromUtf8("yaraEdit"))
        self.ui_yaraeditor.horizontalLayout.addWidget(self.ui_yaraeditor.yaraEdit)    

        #Create our YaraHighlighter derived from QSyntaxHighlighter
        self.yaraEdit = self.ui_yaraeditor.yaraEdit
        highlighter = YaraHighlighter(self.yaraEdit.document())

        self.yaraEdit.document().modificationChanged.connect(
                self.actionSave.setEnabled)
        self.yaraEdit.document().modificationChanged.connect(
                self.mainwindow.setWindowModified)
        self.yaraEdit.document().undoAvailable.connect(
                self.actionUndo.setEnabled)
        self.yaraEdit.document().redoAvailable.connect(
                self.actionRedo.setEnabled)
        self.mainwindow.setWindowModified(self.yaraEdit.document().isModified())
        self.actionSave.setEnabled(self.yaraEdit.document().isModified())
        self.actionUndo.setEnabled(self.yaraEdit.document().isUndoAvailable())
        self.actionRedo.setEnabled(self.yaraEdit.document().isRedoAvailable())
        self.actionUndo.triggered.connect(self.yaraEdit.undo)
        self.actionRedo.triggered.connect(self.yaraEdit.redo)
        self.actionCut.setEnabled(False)
        self.actionCopy.setEnabled(False)
        self.actionCut.triggered.connect(self.yaraEdit.cut)
        self.actionCopy.triggered.connect(self.yaraEdit.copy)
        self.actionPaste.triggered.connect(self.yaraEdit.paste)
        self.yaraEdit.copyAvailable.connect(self.actionCut.setEnabled)
        self.yaraEdit.copyAvailable.connect(self.actionCopy.setEnabled)
        QtGui.QApplication.clipboard().dataChanged.connect(
                self.clipboardDataChanged)

    def about(self):
        QtGui.QMessageBox.about(self, "About", 
                "Editor for Yara rules")

    def clipboardDataChanged(self):
        self.actionPaste.setEnabled(
                len(QtGui.QApplication.clipboard().text()) != 0)

    def maybeSave(self):
        if not self.yaraEdit.document().isModified():
            return True

        ret = QtGui.QMessageBox.warning(self.mainwindow, "Application",
                "The document has been modified.\n"
                "Do you want to save your changes?",
                QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                        QtGui.QMessageBox.Cancel)

        if ret == QtGui.QMessageBox.Save:
            return self.fileSave()

        if ret == QtGui.QMessageBox.Cancel:
            return False

        return True

    def setCurrentFileName(self, fileName=''):
        self.fileName = fileName
        self.yaraEdit.document().setModified(False)

        if not fileName:
            shownName = 'untitled.yara'
        else:
            shownName = QtCore.QFileInfo(fileName).fileName()

        self.mainwindow.setWindowTitle(self.mainwindow.tr("%s[*] - %s" % (shownName, "Rich Text")))
        self.mainwindow.setWindowModified(False)

    def fileNew(self):
        if self.maybeSave():
            self.yaraEdit.clear()
            self.setCurrentFileName()

    def fileOpen(self):
        fn = QtGui.QFileDialog.getOpenFileName(self.mainwindow, "Open File...", "",
                "Yara files (*.yara);;All Files (*)")

        if fn:
            self.load(fn)

    def fileSave(self):
        if not self.fileName:
            return self.fileSaveAs()

        f = open(self.fileName, 'w')
        f.write(str(self.yaraEdit.document().toPlainText()))
        f.close()
        self.yaraEdit.document().setModified(False)
        self.modelYara.refresh()
        self.yaraTree.setRootIndex( self.modelYara.index(self.path_yara) );
        return True

    def fileSaveAs(self):
        fn = QtGui.QFileDialog.getSaveFileName(self.mainwindow, "Save as...", self.path_yara,
                "Yara files (*.yara);;HTML-Files (*.htm *.html);;All Files (*)")

        if not fn:
            return False

        lfn = fn.lower()
        if not lfn.endswith(('.yara', '.htm', '.html')):
            # The default.
            fn += '.yara'

        self.setCurrentFileName(fn)
        return self.fileSave()

    def filePrint(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        dlg = QtGui.QPrintDialog(printer, self.mainwindow)

        if self.yaraEdit.textCursor().hasSelection():
            dlg.addEnabledOption(QtGui.QAbstractPrintDialog.PrintSelection)

        dlg.setWindowTitle("Print Document")

        if dlg.exec_() == QtGui.QDialog.Accepted:
            self.yaraEdit.print_(printer)

        del dlg

    def filePrintPreview(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        preview = QtGui.QPrintPreviewDialog(printer, self.mainwindow)
        preview.paintRequested.connect(self.printPreview)
        preview.exec_()

    def printPreview(self, printer):
        self.yaraEdit.print_(printer)

    def filePrintPdf(self):
        fn = QtGui.QFileDialog.getSaveFileName(self.mainwindow, "Export PDF", None,
                "PDF files (*.pdf);;All Files (*)")

        if fn:
            if QtCore.QFileInfo(fn).suffix().isEmpty():
                fn += '.pdf'

            printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
            printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            printer.setOutputFileName(fileName)
            self.yaraEdit.document().print_(printer)

    def load(self, f):
        if not QtCore.QFile.exists(f):
            return False

        fh = QtCore.QFile(f)
        if not fh.open(QtCore.QFile.ReadOnly):
            return False

        data = fh.readAll()
        codec = QtCore.QTextCodec.codecForHtml(data)
        unistr = codec.toUnicode(data)

        if QtCore.Qt.mightBeRichText(unistr):

            doc = QtGui.QTextDocument()
            doc.setHtml(unistr)
            text = doc.toPlainText()

            unistr = text

        self.yaraEdit.setPlainText(unistr)

        self.setCurrentFileName(f)
        return True

    def treeOpenFile(self,index):
        self.load( self.modelYara.filePath(index) )

    def changeYaraPath(self,path):
        if QDir(path).exists():
            self.path_yara = path
            self.yaraTree.setRootIndex( self.modelYara.index(self.path_yara) );
            
            
            self.config.set(CONF_PREFERENCE, CONF_PATH_YARA,self.path_yara)
            self.save_config()


    def changeMalwarePath(self,path):
        if QDir(path).exists():
            self.path_malware = path
            self.malwareTree.setRootIndex( self.modelMalware.index(self.path_malware) );
            
            self.config.set(CONF_PREFERENCE, CONF_PATH_MALWARE,self.path_malware)
            self.save_config()

    def save_config(self):
        config_path = os.path.join(CONF_PATH,CONF_FILE)
        config_file = open(config_path, 'w')
        self.config.write(config_file)
        config_file.close()

    def yaraExecute(self):
        import yara
        self.outputEdit.clear()
        report = set()
        ret = ""

        yara_script = str(self.yaraEdit.document().toPlainText())

        modelIndexList = self.malwareTree.selectionModel().selectedIndexes();
        try:
            rules = yara.compile(source=yara_script)
        except yara.SyntaxError, e:
            report = "Error : Exception occured in : \n%s" % (str(e))
            self.add_message_output(report)
            return


        for index in modelIndexList:
            try:  
                path_malware = str(self.modelMalware.filePath(index))

                if os.path.isdir(path_malware): 
                    for root, dirs, files in os.walk(path_malware):
                        set_report = set()
                        for i in files:
                            n = os.path.join(root, i)
                            matches = self.check_yara(rules,n)
                            if len(matches)>0:
                                for m in matches:
                                    report = "Signature match : %s : %s" % (m,n)
                                    self.add_message_output(report)
                else:
                    matches = self.check_yara(rules,path_malware)
                    if len(matches)>0:
                        for m in matches:
                            report = "Signature match : %s : %s" % (m,path_malware)
                            self.add_message_output(report)

            except Exception, e:
                report = "Error : Exception occured in : \n%s\n%s" % (str(e),traceback.format_exc())
                logging.error("Exception occured in yaraExecute(): %s" % (str(e)))
                logging.debug(traceback.format_exc())
                self.add_message_output(report)

    def check_yara(self,rules,path):
        try:
            matches = rules.match(path)
            return matches
        except Exception, e:
            logging.error("Exception occured when using yara: %s\n%s" % (str(e),traceback.format_exc()))
        return []

    def add_message_output(self, message):
        cursor = self.outputEdit.textCursor()
        codec = QtCore.QTextCodec.codecForHtml(message)
        unistr = codec.toUnicode(message)

        cursor.movePosition(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
        self.outputEdit.setTextCursor(cursor)
        self.outputEdit.insertPlainText(message+"\n")



# vim:ts=4:expandtab:sw=4
