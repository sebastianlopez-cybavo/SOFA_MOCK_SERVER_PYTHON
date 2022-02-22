# Copyright (c) 2018-2022 The CYBAVO developers
# All Rights Reserved.
# NOTICE: All information contained herein is, and remains
# the property of CYBAVO and its suppliers,
# if any. The intellectual and technical concepts contained
# herein are proprietary to CYBAVO
# Dissemination of this information or reproduction of this materia
# is strictly forbidden unless prior written permission is obtained
# from CYBAVO.

import sqlite3
import os

from mockserver import DB_PATH, RUNTIME_PATH, DB_INIT_PATH

def init_db():
    if (not os.path.isdir(RUNTIME_PATH)):
        os.mkdir(RUNTIME_PATH)

    db = sqlite3.connect(DB_PATH)

    with open(DB_INIT_PATH) as f:
        db.executescript(f.read())

    db.commit()
    db.close()

def getAPICode(walletID):
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    sql = 'SELECT api_code code, api_secret secret FROM mock_apicode WHERE wallet_id  = ?'
    cursor.execute(sql, (walletID, ))
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    db.close()
    return {'code': row.code, 'secret': row.secret}

def setAPICode(walletID, code, secret):
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    sql = 'REPLACE INTO mock_apicode (wallet_id, api_code, api_secret) VALUES(?, ?, ?)'
    cursor.execute(sql, (walletID, code, secret))
    db.commit()
    db.close()