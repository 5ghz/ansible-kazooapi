#!/usr/bin/python

from ansible.module_utils.basic import *
import kazoo


class KazooHelper(object):
    @classmethod
    def auth(cls, auth_module=None):
        auth_user = auth_module.params.get('auth_user', None)
        auth_pass = auth_module.params.get('auth_pass', None)
        auth_realm = auth_module.params.get('auth_realm', None)
        base_url = auth_module.params.get('base_url', None)
        api_key = auth_module.params.get('api_key', None)
        if (auth_user is None and api_key is None) or (auth_pass is None and api_key is None) or (auth_realm is None
                                                                                                  and api_key is None):
            auth_module.fail_json(msg='auth_user and auth_pass and auth_realm or api_key must be defined ')
        if api_key:
            client = kazoo.Client(api_key=api_key, base_url=base_url)
        else:
            client = kazoo.Client(username=auth_user, password=auth_pass, account_name=auth_realm, base_url=base_url)
        client.authenticate()
        return client

    @classmethod
    def run_handler(cls, action_func=None, ansible_module=None):
        msgs = []

        try:
            return action_func()
        except Exception as e:
            if len(msgs) > 0:
                ansible_module.fail_json(msg='ERROR: Exception caught: %s %s' % (e, ', '.join(msgs)))
            else:
                ansible_module.fail_json(msg='ERROR: Exception caught: %s' % e)


class AccountOperation(KazooHelper):
    def __init__(self, ansible_module=None):
        self.client = KazooHelper.auth(auth_module=ansible_module)
        self.ansible_module = ansible_module
        self.account_data = {}

        if ansible_module.params['state'] is None:
            module.fail_json(msg='State is missing')

        if ansible_module.params['account_name'] is not None:
            self.account_data['name'] = ansible_module.params['account_name']

        if ansible_module.params['state'] is not None:
            self.account_data['state'] = ansible_module.params['state']

        if ansible_module.params['timezone'] is not None:
            self.account_data['timezone'] = ansible_module.params['timezone']

        if ansible_module.params['call_restriction'] is not None:
            self.account_data['call_restriction'] = ansible_module.params['call_restriction']

        if ansible_module.params['caller_id'] is not None:
            self.account_data['caller_id'] = ansible_module.params['caller_id']

        if ansible_module.params['dial_plan'] is not None:
            self.account_data['dial_plan'] = ansible_module.params['dial_plan']

        if ansible_module.params['music_on_hold'] is not None:
            self.account_data['music_on_hold'] = ansible_module.params['music_on_hold']

        if ansible_module.params['preflow'] is not None:
            self.account_data['preflow'] = ansible_module.params['preflow']

        if ansible_module.params['ringtones'] is not None:
            self.account_data['ringtones'] = ansible_module.params['ringtones']

        if ansible_module.params['notifications'] is not None:
            self.account_data['notifications'] = ansible_module.params['notifications']

        if ansible_module.params['is_reseller'] is not None:
            self.account_data['is_reseller'] = ansible_module.params['is_reseller']

        if ansible_module.params['wnm_allow_additions'] is not None:
            self.account_data['wnm_allow_additions'] = ansible_module.params['wnm_allow_additions']

        if ansible_module.params['enabled'] is not None:
            self.account_data['enabled'] = ansible_module.params['enabled']

        if ansible_module.params['billing_mode'] is not None:
            self.account_data['billing_mode'] = ansible_module.params['billing_mode']

        if ansible_module.params['account_id'] is not None:
            self.account_id = ansible_module.params['account_id']

    def create_account(self):
        data = self.client.create_account(self.account_data)
        return data, True

    def update_account(self):
        if (hasattr(self, 'account_id') and not self.account_id) or (not hasattr(self, 'account_id')):
            self.ansible_module.fail_json(msg="No account_id")
        data = self.client.get_account(self.account_id)
        data['data'].update(self.account_data)
        data = self.client.update_account(self.account_id, data['data'])
        return data, True

    def delete_account(self):
        if (hasattr(self, 'account_id') and not self.account_id) or (not hasattr(self, 'account_id')):
            self.ansible_module.fail_json(msg="No account_id")
        data = self.client.delete_account(self.account_id)
        return data, True


def main():

    fields = {
        "auth_user": {"required": False, "type": "str"},
        "auth_pass": {"required": False, "type": "str"},
        "auth_realm": {"required": False, "type": "str"},
        "base_url": {"required": True, "type": "str"},
        "api_key": {"required": False, "type": "str"},
        "account_id": {"required": False, "type": "str"},
        "state": {"choices": ['enabled', 'disabled', "update"], "required": True},
        "account_name": {"required": False, "type": "str"},
        "account_realm": {"required": False, "type": "str"},
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
    account = AccountOperation(ansible_module)

    if account.account_data['state'] == 'enabled':
        (data, chand) = account.run_handler(action_func=account.create_account, ansible_module=ansible_module)
        if chand:
            ansible_module.exit_json(changed=chand, meta=data['data'])

    elif account.account_data['state'] == 'disabled':
        (data, chand) = account.run_handler(account.delete_account, ansible_module=ansible_module)
        if chand:
            ansible_module.exit_json(changed=chand, meta='delete account')

    elif account.account_data['state'] == 'update':
        (data, chand) = account.run_handler(account.update_account, ansible_module=ansible_module)
        if chand:
            ansible_module.exit_json(changed=chand, meta=data['data'])


if __name__ == '__main__':
    main()
