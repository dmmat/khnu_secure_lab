import json
import pickle
import urllib.error
import urllib.parse
import urllib.request
import uuid

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget

import settings
from MainWindow import MainForm


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("LoginForm")
        MainWindow.resize(558, 344)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 287, 274))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.email = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.email.setObjectName("email")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.email)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.key = QtWidgets.QTextEdit(self.formLayoutWidget)
        self.key.setObjectName("key")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.key)
        self.activate = QtWidgets.QPushButton(self.formLayoutWidget)
        self.activate.setObjectName("activate")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.activate)
        self.day_count = QtWidgets.QLCDNumber(self.centralWidget)
        self.day_count.setGeometry(QtCore.QRect(330, 100, 81, 61))
        self.day_count.setStyleSheet("color: rgb(211, 0, 3);")
        self.day_count.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.day_count.setSmallDecimalPoint(False)
        self.day_count.setDigitCount(2)
        self.day_count.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.day_count.setProperty("intValue", 30)
        self.day_count.setObjectName("day_count")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(410, 110, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(28)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.trial = QtWidgets.QPushButton(self.centralWidget)
        self.trial.setGeometry(QtCore.QRect(370, 170, 161, 31))
        self.trial.setObjectName("trial")

        self.create_account = QtWidgets.QPushButton(self.centralWidget)
        self.create_account.setGeometry(QtCore.QRect(310, 20, 235, 22))
        self.create_account.setObjectName("create_account")

        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(300, 130, 256, 10))
        self.label_3.setObjectName("label_3")
        # MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 558, 15))
        self.menuBar.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.menuBar.setObjectName("menuBar")
        self.menuSecure_lab = QtWidgets.QMenu(self.menuBar)
        self.menuSecure_lab.setObjectName("menuSecure_lab")
        # MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        # MainWindow.setStatusBar(self.statusBar)
        self.menuBar.addAction(self.menuSecure_lab.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "secure lab v1.0"))
        self.label.setText(_translate("MainWindow", "email"))
        self.label_2.setText(_translate("MainWindow", "key"))
        self.activate.setText(_translate("MainWindow", "Activate"))
        self.label_4.setText(_translate("MainWindow", "days left"))
        self.trial.setText(_translate("MainWindow", "Trial"))
        self.create_account.setText(_translate("MainWindow", "create account"))
        self.label_3.setText(_translate("MainWindow", "OR"))
        self.menuSecure_lab.setTitle(_translate("MainWindow", "secure lab"))


class LoginForm(QWidget):
    def __init__(self, parent=None):
        super(LoginForm, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.MainForm = None
        self.trial_days = None

    def setTrialPeriod(self, days):
        self.trial_days = days
        self.ui.day_count.setProperty("intValue", days)

    @pyqtSlot()
    def on_create_account_clicked(self):
        if not self.ui.email.text():
            settings.error_msg('enter email!')
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('You need pay!')
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.setWindowTitle("Pay")
            ret = msg.exec_()
            if ret == QMessageBox.Ok:
                data = {
                    'email': self.ui.email.text(),
                    'uuid': uuid.uuid1()
                }
                data = bytes(urllib.parse.urlencode(data).encode())
                try:
                    with urllib.request.urlopen('%s/create_key' % settings.HOST, data) as r:
                        success = r.read().decode('utf-8')
                        success = json.loads(success)
                    settings.info_msg('thank to use this app! CLICK SHOW DETAILS AND SAVE YOUR KEY', success['key'])

                except urllib.error.HTTPError:
                    settings.error_msg("Error: Invalid credentials")


    @pyqtSlot()
    def on_activate_clicked(self):
        data = {
            'email': self.ui.email.text(),
            'key': self.ui.key.toPlainText(),
            'uuid': uuid.uuid1()
        }
        data = bytes(urllib.parse.urlencode(data).encode())
        try:
            with urllib.request.urlopen('%s/auth' % settings.HOST, data) as r:
                success = r.read().decode('utf-8')
            print(success)
            with open(settings.CREDENTIALS_FILE_PATH, 'wb') as file:
                pickle.dump(data, file)
                file.close()
            self.MainForm = MainForm()
            self.MainForm.setTrialStatus("ACTIVATED VERSION")
            self.MainForm.show()
            self.close()
        except urllib.error.HTTPError:
            settings.error_msg("Error: Invalid credentials")
            print('error')

    @pyqtSlot()
    def on_trial_clicked(self):
        self.close()
        self.MainForm = MainForm()
        self.MainForm.setTrialStatus("TRIAL %s DAY(S) LEFT!" % self.trial_days)
        self.MainForm.show()
        # self.hide()
