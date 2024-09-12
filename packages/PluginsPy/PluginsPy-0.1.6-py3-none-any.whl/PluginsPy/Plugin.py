#!/usr/bin/env python3

import importlib
import re
import os
import inspect

from PluginsPy.UI import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Plugin:

    def __init__(self, ui: Ui_MainWindow, MainWindow: QMainWindow):
        self.ui               = ui
        self.gridLayout       = ui.PSGridLayout
        self.MainWindow       = MainWindow

        # Plugins
        ui.PSPluginsComboBox.currentIndexChanged.connect(self.PSPluginsChanged)
        ui.PSRunPushButton.clicked.connect(self.PSRunClick)

        self.initPlugins()

    def initPlugins(self):
        self.plugins     = {}
        self.firstPlugin = ""

        for f in self.getPluginFiles("Plugins"):
            moduleFile   = f.split(".")[0]
            moduleString = moduleFile

            if moduleFile == "__init__":
                continue

            matchObj     = re.match(r'\d{4}[_]?', moduleFile)
            if matchObj:
                moduleString = moduleFile.replace(matchObj.group(0), "")

            self.plugins[moduleString] = moduleFile

            if self.firstPlugin == "":
                self.firstPlugin = moduleString
 
        self.pluginsKeys = list(self.plugins.keys())
        # self.ui.PSPluginsComboBox.addItems(self.pluginsKeys)
        self.ui.PSPluginsComboBox.addItems(self.plugins.values())
        # 下面这句会导致重复加载界面
        # self.fillePSGridLayout(self.ui.PSGridLayout, self.getClazzArgs(self.firstPlugin))

    def fillePSGridLayout(self, gridLayout: QGridLayout, keyValues: dict):
        if len(keyValues) == 0:
            return

        i = 0
        for key in keyValues.keys():
            label = QLabel(key)
            value = QLineEdit(keyValues[key])
            gridLayout.addWidget(label, i, 0, 1, 1)
            gridLayout.addWidget(value, i, 1, 1, 1)

            if "/" in keyValues[key] or "\\" in keyValues[key]:
                button = QPushButton("Select File ...")
                button.clicked.connect(self.PSPluginsArgsClicked)
                gridLayout.addWidget(button, i, 2, 1, 1)

            i += 1

    def PSPluginsArgsClicked(self):
        print("PSPluginsClicked")
        row, col = self.findWidgetPosition(self.ui.PSGridLayout)

        fileName,fileType = QFileDialog.getOpenFileName(None, "select file", os.getcwd(), "All Files(*);;Text Files(*.txt)")
        if (len(fileName) > 0):
            print(fileName)
            print(fileType)

            edit: QLineEdit = self.ui.PSGridLayout.itemAtPosition(row, col - 1).widget()
            edit.setText(fileName)


    def findWidgetPosition(self, gridLayout):
        print(gridLayout.rowCount())
        print(gridLayout.columnCount())
        for i in range(gridLayout.rowCount()):
            for j in range(gridLayout.columnCount()):
                if gridLayout.itemAtPosition(i, j) != None and (gridLayout.itemAtPosition(i, j).widget() == self.MainWindow.sender()):
                    return (i, j)

        return (-1, -1)

    def getClazzArgs(self, moduleString):
        # import file
        module   = importlib.import_module("Plugins." + self.plugins[moduleString])
        # get class
        clazz    = getattr(module, moduleString)
        # get class doc
        clazzDoc = clazz.__doc__

        # 从类注释中获取类参数及参数说明，格式@argument: argument doc
        keyValues = {}
        if clazzDoc != None:
            for arg in clazzDoc.split("\n"):
                keyValue = arg.strip().split(":")
                if len(keyValue) == 2 and keyValue[0].strip().startswith("@"):
                    key = keyValue[0].strip().replace("@", "")
                    matchObj     = re.match(r'(.*)\((.*)\)', key)
                    if matchObj:
                        keyValue = matchObj.groups()
                        keyValues[keyValue[0]] = keyValue[1]

        return keyValues

    def PSRunClick(self):
        print("PSRunClick")

        keyValues = {}
        for i in range(self.ui.PSGridLayout.rowCount()):
            if self.ui.PSGridLayout.itemAtPosition(i, 0) == None:
                continue

            key = self.ui.PSGridLayout.itemAtPosition(i, 0).widget().text()
            value = self.ui.PSGridLayout.itemAtPosition(i, 1).widget().text()
            if not os.path.exists(value):
                if "/" in value or "\\" in value:
                    print("can't find: " + value)
                    value = os.getcwd() + "/" + value

            keyValues[key] = value

        print(keyValues)

        ret = self.getClazzWithRun(self.pluginsKeys[self.ui.PSPluginsComboBox.currentIndex()], keyValues)

        if len(ret) > 0:
            self.ui.PSInfoPlainTextEdit.setPlainText(ret)

    def getClazzWithRun(self, moduleString, args):
        # import file
        module = importlib.import_module("Plugins." + self.plugins[moduleString])
        # get class
        clazz  = getattr(module, moduleString)
        # new class
        obj = clazz(args)

        ret = None
        invert_op = getattr(obj, "start", None)
        if callable(invert_op):
            print(">>> enter plugin start method")
            if len(inspect.signature(invert_op).parameters) > 0:
                ret = invert_op(args)
            else:
                ret = invert_op()
            print("<<< end plugin start method")
        
        if ret == None:
            return ""
        elif isinstance(ret, list):
            return "\n".join(ret)
        elif isinstance(ret, int) or isinstance(ret, float):
            return str(ret)
        else:
            return ret

    def PSPluginsChanged(self):
        pluginsIndex = self.ui.PSPluginsComboBox.currentIndex()

        # clear
        item_list = list(range(self.ui.PSGridLayout.count()))
        item_list.reverse()# 倒序删除，避免影响布局顺序

        for i in item_list:
            item = self.ui.PSGridLayout.itemAt(i)
            self.ui.PSGridLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

        # fill gridlayout
        self.fillePSGridLayout(self.ui.PSGridLayout, self.getClazzArgs(self.pluginsKeys[pluginsIndex]))

        print(self.pluginsKeys[pluginsIndex])

    def getFiles(self, path) :
        for (dirpath, dirnames, filenames) in os.walk(path) :
            dirpath   = dirpath
            dirnames  = dirnames
            filenames = filenames
            return filenames

        return []

    def getPluginFiles(self, dirpath):
        plugins = self.getFiles(dirpath)
        print(plugins)
        # plugins.remove("__init__.py")
        plugins.sort()

        return plugins
