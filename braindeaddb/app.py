import json
import os
import hashlib

from flask import Flask, request

from braindeaddb import config

app = Flask(__name__)

def _fname(key):
    return os.path.join(config.store, key)


def _mkkey(data):
    return hashlib.sha1(data).hexdigest()


@app.route('/', methods=['GET', 'PUT'])
def listnew():
    if request.method == 'GET':
        return json.dumps({"keys": os.listdir(config.store)})
    if request.method == 'PUT':
        key = _mkkey(request.data)
        with open(_fname(key), 'wb+') as f:
            f.write(request.data)
            return key


@app.route('/<key>', methods=['GET', 'POST', 'DELETE'])
def getset(key):
    fname = _fname(key)
    if not os.path.isfile(fname):
        return "key not found", 404

    if request.method == 'GET':
        with open(fname, 'r') as f:
            return f.read()
    if request.method == 'POST':
        # ignores ancestor for now, making it almost the same as PUT to /
        key = _mkkey(request.data)
        with open(_fname(key), 'wb+') as f:
            f.write(request.data)
            return key
    if request.method == 'DELETE':
        os.remove(fname)
        return ""
