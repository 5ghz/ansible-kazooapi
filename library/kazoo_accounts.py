#!/usr/bin/python

from ansible.module_utils.basic import *
import kazoo
#import ansible_util

class kazoo_helper(object):
    @classmethod
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
            client = kazoo.Client(username=auth_user, password=auth_pass, account_name=auth_realm, base_url=base_url)
        client.authenticate()
        return client

    @classmethod
    def run_handler(action_func=None, action_func_args=None, ansible_module=None):
        msgs = []

        try:
            return action_func(action_func_args)
        except Exception as e:
            # If there are any commonly known errors that we should provide more
            # context for to help the users diagnose what's wrong. Handle that here
            if "INVALID_SERVICE" in "%s" % e:
                msgs.append("/etc/services (on most systems)")

            if len(msgs) > 0:
                ansible_module.fail_json(msg='ERROR: Exception caught: %s %s' % (e, ', '.join(msgs)))
            else:
                ansible_module.fail_json(msg='ERROR: Exception caught: %s' % e)

class acoount_operation(kazoo_helper):
    def __init__(self, ansible_module=None):
        self.client = self.auth(ansible_module)
        self.ansible_module = ansible_module
        desired_state = ansible_module.params['state']

        if (ansible_module.params['account_name'] is not None):
            account_data['name'] = ansible_module.params['account_name']

        if (ansible_module.params['timezone'] is not None):
            account_data['timezone'] = ansible_module.params['timezone']

        if (ansible_module.params['call_restriction'] is not None):
            account_data['call_restriction'] = ansible_module.params['call_restriction']

        if (ansible_module.params['caller_id'] is not None):
            account_data['caller_id'] = ansible_module.params['caller_id']

        if (ansible_module.params['dial_plan'] is not None):
            account_data['dial_plan'] = ansible_module.params['dial_plan']

        if (ansible_module.params['music_on_hold'] is not None):
            account_data['music_on_hold'] = ansible_module.params['music_on_hold']

        if (ansible_module.params['preflow'] is not None):
            account_data['preflow'] = ansible_module.params['preflow']

        if (ansible_module.params['ringtones'] is not None):
            account_data['ringtones'] = ansible_module.params['ringtones']

        if (ansible_module.params['notifications'] is not None):
            account_data['notifications'] = ansible_module.params['notifications']

        if (ansible_module.params['is_reseller'] is not None):
            account_data['is_reseller'] = ansible_module.params['is_reseller']

        if (ansible_module.params['wnm_allow_additions'] is not None):
            account_data['wnm_allow_additions'] = ansible_module.params['wnm_allow_additions']

        if (ansible_module.params['enabled'] is not None):
            account_data['enabled'] = ansible_module.params['enabled']

        if (ansible_module.params['billing_mode'] is not None):
            account_data['billing_mode'] = ansible_module.params['billing_mode']

        if (ansible_module.params['item_id'] is not None):
            item_id = ansible_module.params['item_id']

            #pass

    def account_operation(self, ansible_module=None):



def main():
    account_data = {}
    item_id = None

    fields = {
        "auth_user": {"required": False, "type": "str"},
        "auth_pass": {"required": False, "type": "str"},
        "auth_realm": {"required": False, "type": "str"},
        "base_url": {"required": True, "type": "str"},
        "api_key": {"required": False, "type": "str"},
        "item_id": {"required": False, "type": "str"},
        "state": { "choices" : ['enabled', 'disabled', 'update'], "required": True},
        "account_name": {"required": False, "type": "str"},
        "timezone": {"required": False, "type": "str"},
        "call_restriction": {"required": False, "type": "str"},
        "caller_id": {"required": False, "type": "str"},
        "dial_plan": {"required": False, "type": "str"},
        "music_on_hold": {"required": False, "type": "str"},
        "preflow": {"required": False, "type": "str"},
        "ringtones": {"required": False, "type": "str"},
        "notifications": {"required": False, "type": "str"},
        "is_reseller": {"required": False, "type": "str"},
        "wnm_allow_additions": {"required": False, "type": "str"},
        "superduper_admin": {"required": False, "type": "str"},
        "enabled": {"required": False, "type": "str"},
        "billing_mode": {"required": False, "type": "str"}
    }

    ansible_module = AnsibleModule(argument_spec=fields, supports_check_mode=True)

   # client = auth(ansible_module)

    if desired_state=='enabled':
        res=run_handler(action_func=client.create_account, action_func_args=account_data,
                        ansible_module=ansible_module)
    elif desired_state=='disabled':
        res=run_handler(client.delete_account, item_id, ansible_module=ansible_module)
    elif desired_state=='update':
        res = run_handler(client.update_account, item_id, ansible_module=ansible_module)

    #response = {"hello": "world"}
    response={"hello": res}
    ansible_module.exit_json(changed=False, meta=response)


if __name__ == '__main__':
    main()