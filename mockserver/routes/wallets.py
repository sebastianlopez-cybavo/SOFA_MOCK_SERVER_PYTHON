# Copyright (c) 2018-2022 The CYBAVO developers
# All Rights Reserved.
# NOTICE: All information contained herein is, and remains
# the property of CYBAVO and its suppliers,
# if any. The intellectual and technical concepts contained
# herein are proprietary to CYBAVO
# Dissemination of this information or reproduction of this materia
# is strictly forbidden unless prior written permission is obtained
# from CYBAVO.

from flask import Blueprint, request
from mockserver.models import setAPICode, getAPICode
from mockserver.helper.apicaller import makeRequest
from hashlib import sha256
import json

wallets = Blueprint('wallets', __name__)

# TODO Add function getQueryParams

@wallets.route('/<wallet_id>/apitoken', methods=['GET', 'POST'])
def apitoken(wallet_id):
    args = request.get_json()
    if (not wallet_id):
        return 'Invalid parameters', 400
    else:
        setAPICode(wallet_id, args['api_code'], args['api_secret'])
        print('API Code:', args['api_code'], 'API Secret:', args['api_secret'])
        return { 'result': 1 }, 200

@wallets.route('/<wallet_id>/addresses', methods = ['GET', 'POST'])
def addresses(wallet_id):
    args = request.get_json()
    if (not wallet_id):
        return 'Invalid parameters', 400
    apires = makeRequest(
            wallet_id, 
            'POST', 
            '/v1/sofa/wallets/{}/addresses'.format(wallet_id),
            None,
            args
        )
    return json.dumps(apires), 200

@wallets.route('/callback', methods=['POST'])
def callback():
    wallet_id = request.args.get('wallet_id')
    APICode = getAPICode(wallet_id)
    if (not APICode):
        return 'Unknown wallet ID', 400
    else:
        checksum = sha256('abcd')
        return checksum, 200
        # TODO callback from wallets.js