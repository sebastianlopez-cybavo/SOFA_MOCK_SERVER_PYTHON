# Copyright (c) 2018-2022 The CYBAVO developers
# All Rights Reserved.
# NOTICE: All information contained herein is, and remains
# the property of CYBAVO and its suppliers,
# if any. The intellectual and technical concepts contained
# herein are proprietary to CYBAVO
# Dissemination of this information or reproduction of this materia
# is strictly forbidden unless prior written permission is obtained
# from CYBAVO.

import math, json
from datetime import datetime
from hashlib import sha256
from urllib import response
from randstr import randomString
from mockserver import API_SERVER_URL
from ..models import getAPICode

def buildChecksum(params, secret, t, r, postData):
    params.append('t={}'.format(t))
    params.append('r={}'.format(r))
    params.sort()
    params.append('secret={}'.format(secret))
    h = sha256()
    h.update(('&'.join(params)).encode('utf-8'))
    return h.hexdigest()

def tryParseJSON(s):
    try:
        o = json.dumps(json.loads(s))
        if (o and type(o) == 'object'):
            return o
    except:
        return s

def doRequest():
    pass

def makeRequest(targetID, method, api, params, postData):
    if (targetID < 0 or method == '' or api == ''):
        return {'Error': 'Invalid parameters'}

    r = randomString(8)
    t = math.floor(datetime.utcnow().timestamp() / 1000)
    url = '{}{}?t={}&r={}'.format(API_SERVER_URL, api, t, r)

    if params:
        url += '&{}'.format('&'.join(params))
    apiCodeObj = getAPICode(targetID)

    if (not apiCodeObj):
        print('Unable to find api code/secret of id {}'.format(targetID))
        return 'Unable to find api code/secret of id {}'.format(targetID), 400

    options = {
        method: '',
        'headers': {
            'X-API-CODE': apiCodeObj['code'],
            'X-CHECKSUM': buildChecksum(params, apiCodeObj['secret'], t, r, postData),
            'User-Agent': 'nodejs'
        },
    }

    if (method == 'POST' or method == 'DELETE'):
        options['headers']['ContentType'] = 'application/json'

    try:
        result = doRequest(url, options, postData)
        resp = tryParseJSON(result)
        print('Response -> ', json.dumps(json.loads(resp)) if resp else '')
        return resp 
    except BaseException:
        resp = tryParseJSON(BaseException)
        print('Response -> ', json.dumps(json.loads(resp)) if resp else '')
        return resp
