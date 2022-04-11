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

def getQueryParams(query):
    if not query:
        return None

    resultArray = []
    for key in query:
        resultArray.append('{}={}'.format(key, query[key]))

    return resultArray

@wallets.route('/<wallet_id>/apitoken', methods=['GET', 'POST'])
def apitoken(wallet_id):
    args = request.get_json()
    if (not wallet_id):
        return 'Invalid parameters', 400
    else:
        setAPICode(wallet_id, args['api_code'], args['api_secret'])
        print('API Code:', args['api_code'], 'API Secret:', args['api_secret'])
        return { 'result': 1 }, 200

# MISSING GET CASE
@wallets.route('/<wallet_id>/addresses', methods=['GET', 'POST'])
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

@wallets.route('/<wallet_id>/pooladdress')
def pooladdress(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    apires = makeRequest(
            wallet_id,
            'GET',
            '/v1/sofa/wallets/{}/pooladdress'.format(wallet_id)
        )
    
    if apires['statusCode']:
        return json.load(apires['result']), apires['statusCode']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/pooladdress/balance')
def pooladdressBalance(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400

    apires = makeRequest(
            wallet_id,
            'GET',
            '/v1/sofa/wallets/{}/pooladdress/balance'.format(wallet_id)
        )
    
    if apires['statusCode']:
        return json.load(apires['result']), apires['statusCode']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/collection/notifications/manual', methods=['POST'])
def collectionNotificationsManual(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    body = request.get_data()
    apires = makeRequest(
            wallet_id,
            'GET',
            '/v1/sofa/wallets/{}/collection/notifications/manual'.format(wallet_id),
            None,
            json.dumps(body)
        )
    
    if apires['statusCode']:
        return json.load(apires['result']), apires['statusCode']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/sender/transactions', methods=['POST'])
def senderTransactions(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    body = request.get_data()
    apires = makeRequest(
            wallet_id,
            'POST',
            '/v1/sofa/wallets/{}/sender/transactions'.format(wallet_id),
            None,
            json.dumps(body)
        )
    
    if apires['statusCode']:
        return json.load(apires['result']), apires['statusCode']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/sender/balance')
def senderBalance(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    apires = makeRequest(
            wallet_id,
            'GET',
            '/v1/sofa/wallets/{}/sender/balance'.format(wallet_id)
        )
    
    if apires['statusCode']:
        return json.load(apires['result']), apires['statusCode']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/apisecret')
def apiSecret(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    apires = makeRequest(
            wallet_id,
            'GET',
            '/v1/sofa/wallets/{}/apisecret'.format(wallet_id)
        )
    
    if apires['statusCode']:
        return json.load(apires['result']), apires['statusCode']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/apisecret/activate', methods=['POST'])
def apiSecretActivate(wallet_id):
    url = ''
    if not wallet_id:
        url = '/v1/sofa/wallets/readonly/apisecret/activate'
    else:
        url = '/v1/sofa/wallets/{}/apisecret/activate'.format(wallet_id)
    
    body = request.get_data()
    apires = makeRequest(
            wallet_id,
            'POST',
            url,
            None,
            json.dumps(body)
        )
    
    if apires['statusCode']:
        return json.load(apires['result']), apires['statusCode']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/notifications')
def notifications(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/notifications'.format(wallet_id)

    apires = makeRequest(
            wallet_id,
            'GET',
            url,
            getQueryParams(request.query_string)
        )
    
    if apires['statusCode']:
        return json.load(apires['result']), apires['statusCode']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/notifications/get_by_id', methods=['POST'])
def get_by_id(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/notifications/get_by_id'.format(wallet_id)

    apires = makeRequest(
            wallet_id,
            'POST',
            url,
            None,
            json.dumps(request.get_data())
        )
    
    if apires['statusCode']:
        return json.load(apires['statusCode']), apires['result']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/sender/notifications/order_id/<order_id>')
def notifications_order_id(wallet_id, order_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    if not order_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/sender/notifications/order_id/{}'.format(
            wallet_id,
            order_id
        )
    
    apires = makeRequest(
            wallet_id,
            'GET',
            url,
            None,
            None
        )
        
    if apires['statusCode']:
        return json.load(apires['statusCode']), apires['result']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/transactions')
def transactions(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/transactions'.format(wallet_id)
    
    apires = makeRequest(
            wallet_id,
            'GET',
            url,
            None,
            None
        )
    
    if apires['statusCode']:
        return json.load(apires['statusCode']), apires['result']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/blocks')
def blocks(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/blocks'.format(wallet_id)
    
    apires = makeRequest(
            wallet_id,
            'GET',
            url
        )
    
    if apires['statusCode']:
        return json.load(apires['statusCode']), apires['result']
    else:
        return json.load(apires), 400

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