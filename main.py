import sys
import os
import json

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QTabBar,
                             QFrame, QStackedLayout, QTabWidget, QShortcut, QKeySequenceEdit,
                             QSplitter)

from PyQt5.QtGui import QIcon, QWindow, QImage, QKeySequence
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *


class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        self.selectAll()


class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Browser")
        # to open at a specific size
        self.setBaseSize(1366, 768)
        self.setMinimumSize(1366, 768)
        self.CreateApp()
        self.setWindowIcon(QIcon("logo.png"))


    def CreateApp(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create Tabs
        self.tabbar = QTabBar(movable=True, tabsClosable=True)
        self.tabbar.tabCloseRequested.connect(self.CloseTab)
        self.tabbar.tabBarClicked.connect(self.SwitchTab)

        self.tabbar.setCurrentIndex(0)
        self.tabbar.setDrawBase(False)
        self.tabbar.setLayoutDirection(Qt.LeftToRight)
        self.tabbar.setElideMode(Qt.ElideLeft)
        self.shortcutNewTab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcutNewTab.activated.connect(self.AddTab)

        self.shortcutReload = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcutReload.activated.connect(self.ReloadPage)

        # Keep track of tabs
        self.tabCount = 0

        # contains every widget in the tab
        self.tabs = []

        # Set up all Buttons with their methods
        self.Toolbar = QWidget()
        self.Toolbar.setObjectName("Toolbar")
        self.ToolbarLayout = QHBoxLayout()
        self.addressbar = AddressBar()
        self.AddTabButton = QPushButton("+")
        self.BackButton = QPushButton("<")

        self.BackButton.clicked.connect(self.GoBack)

        self.ForwardButton = QPushButton(">")
        self.ReloadButton = QPushButton("R")
        self.ReloadButton.clicked.connect(self.ReloadPage)
        self.ForwardButton.clicked.connect(self.GoForward)
        self.addressbar.returnPressed.connect(self.BrowseTo)
        self.AddTabButton.clicked.connect(self.AddTab)

        # Build Toolbars
        self.Toolbar.setLayout(self.ToolbarLayout)
        self.ToolbarLayout.addWidget(self.BackButton)
        self.ToolbarLayout.addWidget(self.ForwardButton)
        self.ToolbarLayout.addWidget(self.ReloadButton)
        self.ToolbarLayout.addWidget(self.addressbar)
        self.ToolbarLayout.addWidget(self.AddTabButton)




        # Set main view
        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)

        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.Toolbar)
        self.layout.addWidget(self.container)
        self.setLayout(self.layout)

        self.AddTab()

        self.show()

    def CloseTab(self, i):
        self.tabbar.removeTab(i)

    def AddTab(self):
        i = self.tabCount

        self.tabs.append(QWidget())
        self.tabs[i].layout = QVBoxLayout()
        self.tabs[i].layout.setContentsMargins(0, 0, 0, 0)

        self.tabs[i].setObjectName("tab " + str(i))

        # Open webview
        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("http://google.com"))

        self.tabs[i].content1 = QWebEngineView()
        self.tabs[i].content1.load(QUrl.fromUserInput("http://google.com"))

        self.tabs[i].content.titleChanged.connect(lambda: self.SetTabContent(i, "title"))
        self.tabs[i].content.iconChanged.connect(lambda: self.SetTabContent(i, "icon"))
        self.tabs[i].content.urlChanged.connect(lambda: self.SetTabContent(i, "url"))

        # Add webview to tabs layout
        self.tabs[i].splitview = QSplitter()
        self.tabs[i].layout.addWidget(self.tabs[i].splitview)

        self.tabs[i].splitview.addWidget(self.tabs[i].content)
        self.tabs[i].splitview.addWidget(self.tabs[i].content1)

        # set top level tab from [] to layout
        self.tabs[i].setLayout(self.tabs[i].layout)

        # add tab to top level stackedwidget
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])

        # Set the tab at top of screen
        # Set tabData to tab<#> So it knows what self.tabs(#) it needs to control
        self.tabbar.addTab("New Tab")
        self.tabbar.setTabData(i, {"object": "tab " + str(i), "initial": i})
        '''
            self.tabs[i].objectName = tab1
            self.tabbar.tabData(i)["object"] = tab1
        '''


        self.tabbar.setCurrentIndex(i)
        self.tabCount += 1

    def SwitchTab(self, i):
        if self.tabbar.tabData(i):
            tab_data = self.tabbar.tabData(i)
            print(tab_data)
            tab_content = self.tabs[i]
            print(tab_content)
            self.container.layout.setCurrentWidget(tab_content)
            new_url = tab_content.content.url().toString()
            self.addressbar.setText(new_url)

    def BrowseTo(self):
        text = self.addressbar.text()
        print(text)
        i = self.tabbar.currentIndex()
        print(i)
        tab = self.tabbar.tabData(i)
        print(tab)
        # wv = self.findChild(QWidget, tab).content
        if "http" not in text:
            if "." not in text:
                url = "https://google.com/#q=" + text
            else:
                url = "http://" + text
        else:
            url = text
        self.tabs[i].content.load(QUrl.fromUserInput(url))

    def SetTabContent(self, i, type):
        print("im here")
        tab_name = self.tabs[i].objectName()
        print(tab_name)
        count = 0
        running = True

        current_tab = self.tabbar.tabData(self.tabbar.currentIndex())["object"]

        if current_tab == tab_name and type == "url":
            new_url = self.tabs[i].content.url().toString()
            self.addressbar.setText(new_url)
            return False


        while running:
            tab_data_name = self.tabbar.tabData(count)
            print(tab_data_name)

            if count >= 99:
                running = False

            if tab_name == tab_data_name["object"]:
                if type == "title":
                    print("im in here")
                    newTitle = self.tabs[i].content.title()
                    self.tabbar.setTabText(count, newTitle)
                    running = False
                elif type == "icon":
                    newIcon= self.tabs[i].content.icon()
                    self.tabbar.setTabIcon(count, newIcon)
                    running = False

            else:
                count += 1

    def GoBack(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.tabs[activeIndex].content
        tab_content.back()
        pass

    def GoForward(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.tabs[activeIndex].content
        tab_content.forward()
        pass

    def ReloadPage(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.tabs[activeIndex].content
        tab_content.reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = "667"
    window = App()

    with open("main.css", "r") as style:
        app.setStyleSheet(style.read())

    sys.exit(app.exec_())





