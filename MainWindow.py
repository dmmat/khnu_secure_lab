from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

import settings


class UiMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(558, 344)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainlabel = QtWidgets.QLabel(self.centralwidget)
        self.mainlabel.setGeometry(QtCore.QRect(10, 250, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mainlabel.setFont(font)
        self.mainlabel.setObjectName("mainlabel")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(120, 40, 241, 161))
        self.calendarWidget.setObjectName("calendarWidget")
        # MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 498, 15))
        self.menubar.setObjectName("menubar")
        # MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.mainlabel.setText(_translate("MainWindow", "TextLabel"))


class MainForm(QWidget):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        self.offline_minutes_to_end = settings.OFFLINE_TRIAL_MINUTES_LIMIT
        self.timer = None

    def setTrialStatus(self, text):
        self.ui.mainlabel.setText(text)

    def close_form(self):
        self.offline_minutes_to_end -= 1
        print('%s minutes to end trial' % self.offline_minutes_to_end)
        self.setTrialStatus('%s minutes to end trial' % self.offline_minutes_to_end)
        if not self.offline_minutes_to_end:
            self.close()

    def setOfflineTrial(self):
        print('timer init!')
        self.timer = QTimer()
        self.timer.timeout.connect(self.close_form)
        self.timer.start(60*1000)