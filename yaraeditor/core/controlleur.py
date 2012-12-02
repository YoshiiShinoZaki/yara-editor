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
import sys, os, re, traceback
from yaraeditor.constante import *
from yaraeditor.core.highlighter import *
from yaraeditor.core.codeeditor import *
from yaraeditor.core.ytreewidget import *

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
        self.setupEditorActions()
        self.setupPropertiesActions()

        self.yaraTree = self.ui_yaraeditor.yaraTree
        self.malwareTree = self.ui_yaraeditor.malwareTree
        self.outputEdit = self.ui_yaraeditor.outputEdit
        self.pathYaraEdit = self.ui_yaraeditor.pathYara
        self.pathMalwareEdit = self.ui_yaraeditor.pathMalware
        self.treeMalwareProperties = self.ui_yaraeditor.treeMalwareProperties
        self.treeMalwareStrings = self.ui_yaraeditor.treeMalwareStrings


        highlighter = OutputHighlighter(self.outputEdit.document())

        


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
        #self.malwareTree.setSelectionMode( QtGui.QAbstractItemView.MultiSelection ) 

        #self.treeMalwareStrings.setDragDropMode(self.treeMalwareStrings.DragDrop)
        self.treeMalwareStrings.setDragEnabled(True)

        #self.treeMalwareStrings.setDropIndicatorShown(True)

        self.malwareTree.setContextMenuPolicy(Qt.CustomContextMenu);
        self.malwareTree.customContextMenuRequested.connect(self.menuContextTree)

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

        self.actionInspector = QtGui.QAction(
                "&Inspector", self.mainwindow, toggled=self.ui_yaraeditor.dockWidgetInspector.setVisible)
        self.actionInspector.setCheckable(True)
        self.actionInspector.setChecked(True)

        menu.addAction(self.actionInspector)

    def setupYaraActions(self):
        tb = QtGui.QToolBar(self.mainwindow)
        tb.setWindowTitle("Yara Actions")
        self.mainwindow.addToolBar(tb)

        menu = QtGui.QMenu("&Yara", self.mainwindow)
        self.mainwindow.menuBar().addMenu(menu)
        iconExec = QtGui.QIcon()
        iconExec.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/images/win/exec.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExecuteYara = QtGui.QAction(
                QtGui.QIcon.fromTheme('yara-execute',iconExec),
                "&Execute", self.mainwindow, shortcut=QtGui.QKeySequence(Qt.Key_F5),
                triggered=self.yaraExecute)
        tb.addAction(self.actionExecuteYara)
        menu.addAction(self.actionExecuteYara)

        self.actionGenerateRules = QtGui.QAction(
                "&Generate Rules", self.mainwindow, triggered=self.yaraRulesGenerator)
        menu.addAction(self.actionGenerateRules)

    def setupHelpActions(self):
        helpMenu = QtGui.QMenu("Help", self.mainwindow)
        self.mainwindow.menuBar().addMenu(helpMenu)
        helpMenu.addAction("About", self.about)
        helpMenu.addAction("About &Qt", QtGui.qApp.aboutQt)        

    def setupEditorActions(self):
        self.ui_yaraeditor.horizontalLayout = QtGui.QHBoxLayout(self.ui_yaraeditor.widgetEditor)
        self.ui_yaraeditor.horizontalLayout.setMargin(0)
        self.ui_yaraeditor.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))        
        self.ui_yaraeditor.yaraEdit = CodeEditor(self.ui_yaraeditor.widgetEditor)
        self.ui_yaraeditor.yaraEdit.setObjectName(_fromUtf8("yaraEdit"))
        self.ui_yaraeditor.horizontalLayout.addWidget(self.ui_yaraeditor.yaraEdit)    
        self.ui_yaraeditor.widgetEditor.setAcceptDrops(True)

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

    def setupPropertiesActions(self):
        self.ui_yaraeditor.verticalLayout_7 = QtGui.QVBoxLayout(self.ui_yaraeditor.tab_strings)
        self.ui_yaraeditor.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.ui_yaraeditor.treeMalwareStrings = YTreeWidget(self.ui_yaraeditor.tab_strings)
        self.ui_yaraeditor.treeMalwareStrings.setHeaderHidden(True)
        self.ui_yaraeditor.treeMalwareStrings.setObjectName(_fromUtf8("treeMalwareStrings"))
        self.ui_yaraeditor.verticalLayout_7.addWidget(self.ui_yaraeditor.treeMalwareStrings)
        


    def about(self):
        QtGui.QMessageBox.about(self.mainwindow, "About", 
                """
                Yara-Editor Version (%s)
                Editor for Yara rules
                %s
                """ % (VERSION,AUTHOR))

    def clipboardDataChanged(self):
        self.actionPaste.setEnabled(
                len(QtGui.QApplication.clipboard().text()) != 0)

    def menuContextTree(self, point):

        # On définie le menu contextuel.
        menu=QtGui.QMenu()

        action_inspect_malware=menu.addAction("Inspect")
        QtCore.QObject.connect(action_inspect_malware, QtCore.SIGNAL("triggered()"), self.inspect_malware)

        action_generate_rules=menu.addAction("Generate Rules")
        QtCore.QObject.connect(action_generate_rules, QtCore.SIGNAL("triggered()"), self.yaraRulesGenerator)

        # Il reste à lier chaque clic sur le menu à une action réelle via un SLOT.
        menu.exec_(QtGui.QCursor.pos())

    def inspect_malware(self):
        logger.debug('inspect_malware() :')
        self.treeMalwareProperties.clear()
        self.treeMalwareStrings.clear()
        for index in self.malwareTree.selectedIndexes():
            fileInfo = self.modelMalware.fileInfo(index)
            self.add_element(self.treeMalwareProperties,"Name",fileInfo.fileName())
            self.add_element(self.treeMalwareProperties,"Path",fileInfo.filePath())
            self.add_element(self.treeMalwareProperties,"Size",str(fileInfo.size()))
            fi = open(str(fileInfo.filePath()),'r')
            data = fi.read()
            fi.close()
            sha1 = QtCore.QCryptographicHash.hash(data,QtCore.QCryptographicHash.Sha1).toHex()  
            md5 = QtCore.QCryptographicHash.hash(data,QtCore.QCryptographicHash.Md5).toHex()  
            self.add_element(self.treeMalwareProperties,"MD5",str(md5))
            self.add_element(self.treeMalwareProperties,"SHA1",str(sha1))

            for s in self.get_strings(data):
                self.add_element(self.treeMalwareStrings,str(s))
            
    def add_element(self,tree,name,value=""):
        item = QtGui.QTreeWidgetItem(tree)
        item.setText(0,name)
        if value!="":
            item.setText(1,value)

    def remove_element(self,tree,name):
        findings = tree.findItems(name,Qt.MatchCaseSensitive)
        for f in findings:
            index = tree.indexOfTopLevelItem(f)
            tree.takeTopLevelItem(index)


    def get_strings(self,data,length_min=7):
        strings = list()
        for m in re.finditer("([\x20-\x7e]{3,})", data):
            if len(m.group(1))> length_min:
                strings.append(m.group(1))
        return strings

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

        self.add_message_output("Compilation...")
        yara_script = str(self.yaraEdit.document().toPlainText())

        modelIndexList = self.malwareTree.selectionModel().selectedIndexes();
        try:
            rules = yara.compile(source=yara_script)
        except yara.SyntaxError, e:
            report = "Error : Exception occured in : \n%s" % (str(e))
            self.add_message_output(report)
            return

        pathes = set()

        [pathes.add(str(self.modelMalware.filePath(index))) for index in modelIndexList]

        self.add_message_output("Execution...")
        found=0
        for path_malware in pathes:
            try:  

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
                                    found+=1
                else:
                    matches = self.check_yara(rules,path_malware)
                    if len(matches)>0:
                        for m in matches:
                            report = "Signature match : %s : %s" % (m,path_malware)
                            found+=1
                            self.add_message_output(report)

            except Exception, e:
                report = "Error : Exception occured in : \n%s\n%s" % (str(e),traceback.format_exc())
                logging.error("Exception occured in yaraExecute(): %s" % (str(e)))
                logging.debug(traceback.format_exc())
                self.add_message_output(report)

        self.add_message_output("Finish : %d match" % found)

    def check_yara(self,rules,path):
        try:
            matches = rules.match(path)
            return matches
        except Exception, e:
            logging.error("Exception occured when using yara: %s\n%s" % (str(e),traceback.format_exc()))
        return []

    def add_message_output(self, message):
        import datetime
        cursor = self.outputEdit.textCursor()
        codec = QtCore.QTextCodec.codecForHtml(message)
        unistr = codec.toUnicode(message)

        cursor.movePosition(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
        self.outputEdit.setTextCursor(cursor)
        timestamp = str(datetime.datetime.now())
        self.outputEdit.insertPlainText("["+timestamp+"] "+message+"\n")


    def yaraRulesGenerator(self):
        from yaraeditor.ui.rules_generator import *
        self.dialog_generator = QtGui.QDialog()
        self.ui_generator=Ui_DialogGenerator()
        self.ui_generator.setupUi(self.dialog_generator)

        self.app.connect(self.ui_generator.btnBrowseMalware,SIGNAL("clicked()"),self.generator_open_malware)
        self.app.connect(self.ui_generator.btnBrowseNewFile,SIGNAL("clicked()"),self.generator_add_file)
        self.app.connect(self.ui_generator.listFiles, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"), self.generator_menuContextTree)
        self.ui_generator.listFiles.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        if self.dialog_generator.exec_():
            rules = self.generator_generate_rules()
            self.yaraEdit.setPlainText(rules)

            


    def generator_generate_rules(self):
        count = self.ui_generator.treeWidget.topLevelItemCount()
        set_strings = set()
        set_condition = set()
        for i in range(0,count):
            item = self.ui_generator.treeWidget.topLevelItem(i)
            condition = "$str%d" % i
            value = "\t%s=\"%s\""%(condition,item.text(0))
            set_strings.add(value)
            set_condition.add(condition)

        rules = TEMPLATE_YARA
        rules = rules.replace("###STRINGS###","\n".join(set_strings))
        rules = rules.replace("###CONDITION###","\t(%s)" % " or ".join(set_condition))
        return rules

    def generator_open_malware(self,path=""):

        if path == "":
            path = QtGui.QFileDialog.getOpenFileName(self.mainwindow, "Open File","","*")
        if path =="":
            return 

        self.ui_generator.treeWidget.clear()
        self.ui_generator.editPathMalware.setText(path)
        self.generator_update()


    def generator_add_file(self,path=""): 
        if path == "":
            pathes = QtGui.QFileDialog.getOpenFileNames(self.mainwindow, "Open File","","All (*.*)")
        if pathes == None:
            return 

        for path in pathes:
            item = QtGui.QListWidgetItem(path)
            self.ui_generator.listFiles.addItem(item)
        self.generator_update()            


    def generator_update(self):
        path_malware = self.ui_generator.editPathMalware.text() 
        self.generator_add_string(path_malware)

        count = self.ui_generator.listFiles.count()
        for index in range(0,count):
            item = self.ui_generator.listFiles.item(index)
            self.generator_remove_string(item.text())


    def generator_remove_file(self,path=""): 
        items = self.ui_generator.listFiles.selectedItems()
        for item in items:
            index = self.ui_generator.listFiles.row(item)
            self.ui_generator.listFiles.takeItem(index)
        self.generator_update()
        
    def generator_add_string(self,malware):
        f = open(malware,'r')
        data = f.read()
        f.close()
        for s in self.get_strings(data):
            if '"' not in s and '\\' not in s:
                self.add_element(self.ui_generator.treeWidget,str(s))

    def generator_remove_string(self,malware):
        f = open(malware,'r')
        data = f.read()
        f.close()
        for s in self.get_strings(data):
            self.remove_element(self.ui_generator.treeWidget,str(s))

    def generator_menuContextTree(self, point):
        # On définie le menu contextuel.
        menu=QtGui.QMenu()

        action_delete=menu.addAction("Remove")
        QtCore.QObject.connect(action_delete, QtCore.SIGNAL("triggered()"), self.generator_remove_file)

        # Il reste à lier chaque clic sur le menu à une action réelle via un SLOT.
        menu.exec_(QtGui.QCursor.pos())



# vim:ts=4:expandtab:sw=4
