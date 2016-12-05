from PyQt5.QtWidgets import QMessageBox

CREDENTIALS_FILE_PATH = 'crd.key'
HOST = "http://localhost:5000"
TRIAL_FILE_PATH = '/'
TRIAL_DAY_LIMIT = 30
OFFLINE_TRIAL_MINUTES_LIMIT = 30


def error_msg(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle("Error")
    return msg.exec_()


def info_msg(text, details=False):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    if details:
        msg.setDetailedText(details)
    msg.setWindowTitle("Information")
    return msg.exec_()
