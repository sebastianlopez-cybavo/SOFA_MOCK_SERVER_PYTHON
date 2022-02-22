# Copyright (c) 2018-2022 The CYBAVO developers
# All Rights Reserved.
# NOTICE: All information contained herein is, and remains
# the property of CYBAVO and its suppliers,
# if any. The intellectual and technical concepts contained
# herein are proprietary to CYBAVO
# Dissemination of this information or reproduction of this materia
# is strictly forbidden unless prior written permission is obtained
# from CYBAVO.

from string import ascii_letters
from random import randint

def randomString(length):
    r = ''
    charset = ascii_letters + '0123456789'

    for i in range(length):
        r = r + charset[randint(0, len(charset))]
    
    return r