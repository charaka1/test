# Copyright (c) The University of Edinburgh, 2014.
#
import tool
import json
import random
from datetime import datetime
from pymongo import MongoClient

EVE_ENTRY_POINT = 'http://localhost:5000'
MONGO_DB_URI = 'mongodb://user:user@localhost:27017/apitest'
ADMIN_USERNAME = 'adminuser'
ADMIN_SECRET = 'letmein'
USER_USERNAME = 'user'
USER_SECRET = 'secret'

def delete_accounts():
    mongo_client=MongoClient(MONGO_DB_URI)
    db = mongo_client.apitest
    db.accounts.drop()
    print "Accounts deleted"

def create_admin_user():
    mongo_client = MongoClient(MONGO_DB_URI)
    admin_account = {'firstname': 'User',
                  'lastname': 'Admin',
                  'username': ADMIN_USERNAME,
                  'email': 'admin@example.com',
                  'secret': ADMIN_SECRET,
                  'roles': ['admin', 'user']}
    db = mongo_client.apitest
    account_id = db.accounts.insert(admin_account)
    print "Admin account created id=", account_id

def get_accounts():
    message = ''
    response = tool.performGet('accounts', message)
    print "GET 'accounts' status:", response.status_code
    if response.status_code == 200:
        print json.dumps(response.json(), indent=2, sort_keys=True)
    else:
        print "Getting accounts failed"

def get_experiments():
    message = ''
    response = tool.performGet('experiments', message)
    print "GET 'experiments' status:", response.status_code
    if response.status_code == 200:
        print json.dumps(response.json(), indent=2, sort_keys=True)
    else:
        print "Getting experiments failed"

def get_events():
    message = ''
    response = tool.performGet('events', message)
    print "GET 'events' status:", response.status_code
    if response.status_code == 200:
        print json.dumps(response.json(), indent=2, sort_keys=True)
    else:
        print "Getting events failed"

def delete_experiments():
    message = '';
    response = tool.performDelete('experiments', message)
    if response.status_code == 200:
        print "DELETEd 'experiments' OK:", response.status_code
    else:
        print "Failed to delete 'experiments', status:", response.status_code

def delete_events():
    message = '';
    response = tool.performDelete('events', message)
    if response.status_code == 200:
        print "DELETEd 'events' OK:", response.status_code
    else:
        print "Failed to delete 'events', status:", response.status_code

def post_accounts():
    accounts = [
        {
            'firstname': 'Jeremy',
            'lastname': 'Nowell',
            'username': 'jnowell',
            'email': 'jeremy@epcc.ed.ac.uk',
            'secret': 'letmein',
            'roles': ['user']
        },
        {
            'firstname': 'Test',
            'lastname': 'User',
            'username': USER_USERNAME,
            'email': 'testuser@example.com',
            'secret': USER_SECRET,
            'roles': ['user']
        },
    ]

    response = tool.performPost('accounts', json.dumps(accounts))
    print "POST 'accounts' status:", response.status_code

    valids = []
    if response.status_code == 201:
        response_json = response.json()
        for account in response_json:
            if account['_status'] == "OK":
                valids.append(account['_id'])

    return valids

def post_experiments(ids):
    experiments = []
    for i in range(5):
        now = datetime.utcnow().replace(microsecond=0).strftime('%a, %d %b %Y %H:%M:%S GMT')
        experiments.append(
            {
                'name': 'Experiment Name #%d' % i,
                'description': 'Description #%d' %i,
                'date': now,
                'owner': random.choice(ids),
            }
        )

    response = tool.performPost('experiments', json.dumps(experiments))
    print "POST 'experiments' status:", response.status_code

if __name__ == '__main__':
    # Direct Mongo operations
    tool = tool.Tool()
    delete_accounts()
    create_admin_user()
    get_accounts()
    ids = post_accounts()
    get_accounts()
    delete_experiments()
    delete_events()
    get_experiments()
    post_experiments(ids)
    get_experiments()
    get_events()
