import os
import pickle

import flask
from flask import Flask, request

from Credentials import Credentials
from Trials import Trials

app = Flask(__name__)
CREDENTIALS_FILE_PATH = 'credentials_v1.0.obj'
TRIAL_KEYS_FILE_PATH = 'trials.obj'
KEYS = []
TRIAL_KEYS = []


@app.route('/create_key', methods=['POST'])
def create_key():
    email = request.form.get('email')
    uuid = request.form.get('uuid')
    exist_credential = find_credential(email, uuid)
    if exist_credential:
        credential = exist_credential
    else:
        credential = Credentials(email, uuid)
        KEYS.append(credential)
        with open(CREDENTIALS_FILE_PATH, 'wb') as file:
            pickle.dump(KEYS, file)
            file.close()

    return flask.jsonify(**credential.to_dic())


@app.route('/auth', methods=['POST'])
def auth():
    email = request.form.get('email')
    key = request.form.get('key')
    uuid = request.form.get('uuid')
    exist_credential = find_credential(email, uuid, key)
    if exist_credential:
        return flask.jsonify(exist_credential.to_dic())
    else:
        return flask.jsonify({'error': 'key or email incorrect :<'}), 400


@app.route('/check_trial', methods=['post'])
def trial():
    uid = request.form.get('uid')
    trial_key = find_trial(Trials(uid).uid)
    if not trial_key:
        trial_key = Trials(uid)
        TRIAL_KEYS.append(trial_key)
        with open(TRIAL_KEYS_FILE_PATH, 'wb') as file:
            pickle.dump(TRIAL_KEYS, file)
            file.close()
    return flask.jsonify(trial_key.to_dic())


def find_credential(email, uuid, key=None):
    if key:
        return next((x for x in KEYS if x.email == email and x.key == key), None)
    else:
        machine_uuid = '-'.join(uuid.__str__().split('-')[1:5])
        return next((x for x in KEYS if x.email == email and x.uid == machine_uuid), None)


def find_trial(uid: object) -> object:
    return next((x for x in TRIAL_KEYS if x.uid == uid), None)


if __name__ == '__main__':
    if os.path.exists(CREDENTIALS_FILE_PATH):
        KEYS = pickle.load(open(CREDENTIALS_FILE_PATH, 'rb'))
    if os.path.exists(TRIAL_KEYS_FILE_PATH):
        TRIAL_KEYS = pickle.load(open(TRIAL_KEYS_FILE_PATH, 'rb'))
    app.run()
