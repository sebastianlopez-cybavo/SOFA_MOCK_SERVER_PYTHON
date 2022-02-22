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
from hashlib import sha256

merchant = Blueprint('merchant', __name__)

@merchant.route('/<merchant_id>/apitoken', methods=['GET', 'POST'])
def apitoken(merchant_id):
    args = request.get_json()
    if (not merchant_id):
        return 'Invalid parameters', 400
    else:
        setAPICode(merchant_id, args['api_code'], args['api_secret'])
        print('API Code:', args['api_code'], 'API Secret:', args['api_secret'])
        return { 'result': 1 }, 200