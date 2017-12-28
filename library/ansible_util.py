#!/usr/bin/python

from ansible.module_utils.basic import *
import kazoo

def auth(ansible_module=None):
    auth_user = ansible_module.params.get('auth_user', None)
    auth_pass = ansible_module.params.get('auth_pass', None)
    auth_realm = ansible_module.params.get('auth_realm', None)
    base_url = ansible_module.params.get('base_url', None)
    api_key = ansible_module.params.get('api_key', None)

    if (auth_user is None and api_key is None) or (auth_pass is None and api_key is None) or (auth_realm is None
                                                                                              and api_key is None):
        ansible_module.fail_json(msg='auth_user and auth_pass and auth_realm or api_key must be defined ')

    if api_key:
        client = kazoo.Client(api_key=api_key, base_url=base_url)
    else:
        client = kazoo.Client(username=auth_user, password=auth_pass, account_name=api_key, base_url=base_url)

    return client

def run_handler():
    pass
