# Copyright (c) 2018-2022 The CYBAVO developers
# All Rights Reserved.
# NOTICE: All information contained herein is, and remains
# the property of CYBAVO and its suppliers,
# if any. The intellectual and technical concepts contained
# herein are proprietary to CYBAVO
# Dissemination of this information or reproduction of this materia
# is strictly forbidden unless prior written permission is obtained
# from CYBAVO.

from flask import Flask
import json

app = Flask(__name__)

f = open('./conf/mockserver.conf.json')
cfg = json.load(f)
f.close()
DB_PATH = cfg['db_path']
RUNTIME_PATH = cfg['runtime_path']
DB_INIT_PATH = cfg['db_init_path']

from .routes.wallets import wallets

app.register_blueprint(wallets, url_prefix = '/v1/mock/wallets')

from .models import init_db

init_db()