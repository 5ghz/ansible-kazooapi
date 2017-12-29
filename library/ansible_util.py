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

def run_handler(action_func=None, action_func_args=None):
    try:
        return action_func(*action_func_args)
    except Exception as e:

        # If there are any commonly known errors that we should provide more
        # context for to help the users diagnose what's wrong. Handle that here
        if "INVALID_SERVICE" in "%s" % e:
            self.msgs.append(
                "Services are defined by port/tcp relationship and named as they are in /etc/services (on most systems)")

        if len(self.msgs) > 0:
            module.fail_json(
                msg='ERROR: Exception caught: %s %s' % (e, ', '.join(self.msgs))
            )
        else:
            module.fail_json(msg='ERROR: Exception caught: %s' % e)



