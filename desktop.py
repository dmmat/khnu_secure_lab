import datetime
import json
import os
import pickle
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

from PyQt5.QtWidgets import QApplication

import settings
from LoginForm import LoginForm
from MainWindow import MainForm

ACTIVATION_KEY = ''



def main():
    app = QApplication(sys.argv)
    form = LoginForm()
    if os.path.exists(settings.CREDENTIALS_FILE_PATH):
        ACTIVATION_KEY = pickle.load(open(settings.CREDENTIALS_FILE_PATH, 'rb'))
        try:
            with urllib.request.urlopen('%s/auth' % settings.HOST, ACTIVATION_KEY) as r:
                success = json.loads(r.read().decode('utf-8'))
                form = MainForm()
                form.setTrialStatus('Activated - %s ' % success['email'])
        except urllib.error.HTTPError:
            settings.error_msg("Error: Invalid credentials")
    else:
        try:
            trial_data = bytes(urllib.parse.urlencode({'uid': uuid.uuid1()}).encode())
            with urllib.request.urlopen('%s/check_trial' % settings.HOST, trial_data) as r:
                success = json.loads(r.read().decode('utf-8'))
                ended_at = datetime.datetime.strptime(success['ended_at'], "%Y-%m-%dT%H:%M:%S.%f")
                days = ended_at - datetime.datetime.now()
                if days.days:
                    form.setTrialPeriod(days.days)
                else:
                    return settings.error_msg('trial end (')
        except urllib.error.HTTPError and urllib.error.URLError:
            print('error')
            settings.error_msg('cannot connect to server! %s minutes trial!' % settings.OFFLINE_TRIAL_MINUTES_LIMIT)
            form = MainForm()
            form.setOfflineTrial()
            form.setTrialStatus('%s minutes trial' % settings.OFFLINE_TRIAL_MINUTES_LIMIT)
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
