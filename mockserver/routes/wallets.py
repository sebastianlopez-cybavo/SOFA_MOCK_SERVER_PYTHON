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
    
@wallets.route('/<wallet_id>/addresses/invalid-deposit')
def invalid_deposit(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/addresses/invalid-deposit'.format(wallet_id)
    
    apires = makeRequest(
            wallet_id,
            'GET',
            url
        )
    
    if apires['statusCode']:
        return json.load(apires['statusCode']), apires['result']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/info')
def info(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/info'.format(wallet_id)
    
    apires = makeRequest(
            wallet_id,
            'GET',
            url
        )
    
    if apires['statusCode']:
        return json.load(apires['statusCode']), apires['result']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/addresses/verify', methods=['POST'])
def verify(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/addresses/verify'.format(wallet_id)
    
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

@wallets.route('/<wallet_id>/autofee', methods=['POST'])
def autofee(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/autofee'.format(wallet_id)
    
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

@wallets.route('/<wallet_id>/receiver/balance')
def balance(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/receiver/balance'.format(wallet_id)
    
    apires = makeRequest(
            wallet_id,
            'GET',
            url
        )
    
    if apires['statusCode']:
        return json.load(apires['statusCode']), apires['result']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/vault/balance')
def vaultbalance(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/vault/balance'.format(wallet_id)
    
    apires = makeRequest(
            wallet_id,
            'GET',
            url
        )
    
    if apires['statusCode']:
        return json.load(apires['statusCode']), apires['result']
    else:
        return json.load(apires), 400

# TODO THIS IS DIFFERENT
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

@wallets.route('/withdrawal/callback', methods=['POST'])
def withdrawal_callback():
    print('withdrawal/callback -> ', request.get_data())
    return 'OK', 200

@wallets.route('/<wallet_id>/addresses/contract_txid')
def contract_txid(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/addresses/contract_txid'.format(wallet_id)
    
    apires = makeRequest(
            wallet_id,
            'GET',
            url
        )
    
    if apires['statusCode']:
        return json.load(apires['statusCode']), apires['result']
    else:
        return json.load(apires), 400
    
@wallets.route('/<wallet_id>/sender/transactions/acl', methods=['POST'])
def sendertransactions(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/sender/transactions/acl'.format(wallet_id)
    
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

@wallets.route('/<wallet_id>/sender/notifications/manual', methods=['POST'])
def sendernotifications(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/sender/notifications/manual'.format(wallet_id)
    
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

@wallets.route('/<wallet_id>/refreshsecret', methods=['POST'])
def refreshsecret(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/refreshsecret'.format(wallet_id)
    
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

# TODO add post and delete
@wallets.route('/<wallet_id>/sender/whitelist')
def senderwhitelist(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/sender/whitelist'.format(wallet_id)
    
    apires = makeRequest(
            wallet_id,
            'GET',
            url,
            getQueryParams(request.query_string),
            None
        )
    
    if apires['statusCode']:
        return json.load(apires['statusCode']), apires['result']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/sender/whitelist/config')
def whitelist_config(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/sender/whitelist/config'.format(wallet_id)
    
    apires = makeRequest(
            wallet_id,
            'GET',
            url,
            getQueryParams(request.query_string),
            None
        )
    
    if apires['statusCode']:
        return json.load(apires['statusCode']), apires['result']
    else:
        return json.load(apires), 400

@wallets.route('/<wallet_id>/sender/whitelist/check', methods=['POST'])
def whitelist_check(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/sender/whitelist/check'.format(wallet_id)
    
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

@wallets.route('/<wallet_id>/addresses/label', methods=['POST'])
def addresses_label(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/addresses/label'.format(wallet_id)
    
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

@wallets.route('/<wallet_id>/addresses/get_labels', methods=['POST'])
def addresses_get_labels(wallet_id):
    if not wallet_id:
        errorMessage = json.dumps({'error': 'Invalid parameters'})
        return errorMessage, 400
    
    url = '/v1/sofa/wallets/{}/addresses/get_labels'.format(wallet_id)
    
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

@wallets.route('/readonly/walletlist')
def readonlywalletlist():
    url = '/v1/sofa/wallets/readonly/walletlist'
    
    apires = makeRequest(
            0,
            'GET',
            url,
            getQueryParams(request.query_string),
            None
        )
    
    if apires['statusCode']:
        return json.load(apires['statusCode']), apires['result']
    else:
        return json.load(apires), 400