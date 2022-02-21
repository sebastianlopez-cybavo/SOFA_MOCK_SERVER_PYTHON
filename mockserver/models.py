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

    connection = sqlite3.connect(DB_PATH)

    with open(DB_INIT_PATH) as f:
        connection.executescript(f.read())

    connection.commit()
    connection.close()

def setAPICode(param1, param2, param3):
    pass