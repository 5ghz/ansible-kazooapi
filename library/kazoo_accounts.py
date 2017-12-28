#!/usr/bin/python

from ansible.module_utils.basic import *
import kazoo
import ansible_util


def main():
    account_data = {}
    item_id = None

    fields = {
        "auth_user": {"required": False, "type": "str"},
        "auth_pass": {"required": False, "type": "str"},
        "auth_realm": {"required": False, "type": "str"},
        "base_url": {"required": True, "type": "str"},
        "api_key": {"required": False, "type": "str"},
        "account_id": {"required": False, "type": "str"},
        "item_id": {"required": False, "type": "str"},
        "state": { "choices" : ['enabled', 'disabled'], "required": True},
        "name": {"required": False, "type": "str"},
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
    account_id = ansible_module.params['account_id']

    desired_state = ansible_module.params['state']

    if (ansible_module.params['name'] is None):
        account_data['name'] = ansible_module.params['name']

    if (ansible_module.params['timezone'] is None):
        account_data['timezone'] = ansible_module.params['timezone']

    if (ansible_module.params['call_restriction'] is None):
        account_data['call_restriction'] = ansible_module.params['call_restriction']

    if (ansible_module.params['caller_id'] is None):
        account_data['caller_id'] = ansible_module.params['caller_id']

    if (ansible_module.params['dial_plan'] is None):
        account_data['dial_plan'] = ansible_module.params['dial_plan']

    if (ansible_module.params['music_on_hold'] is None):
        account_data['music_on_hold'] = ansible_module.params['music_on_hold']

    if (ansible_module.params['preflow'] is None):
        account_data['preflow'] = ansible_module.params['preflow']

    if (ansible_module.params['ringtones'] is None):
        account_data['ringtones'] = ansible_module.params['ringtones']

    if (ansible_module.params['notifications'] is None):
        account_data['notifications'] = ansible_module.params['notifications']

    if (ansible_module.params['is_reseller'] is None):
        account_data['is_reseller'] = ansible_module.params['is_reseller']

    if (ansible_module.params['wnm_allow_additions'] is None):
        account_data['wnm_allow_additions'] = ansible_module.params['wnm_allow_additions']

    if (ansible_module.params['enabled'] is None):
        account_data['enabled'] = ansible_module.params['enabled']

    if (ansible_module.params['billing_mode'] is None):
        account_data['billing_mode'] = ansible_module.params['billing_mode']

    if (ansible_module.params['item_id'] is None):
        item_id = ansible_module.params['item_id']

    client = ansible_util.auth(ansible_module)

    if account_id is None:
        account_id = client.account_id

    if desired_state=='enabled':
        client.create_account(account_id, account_data)
    else:
        client.delete_account(account_id, item_id)


    response = {"hello": "world"}
    module.exit_json(changed=False, meta=response)


if __name__ == '__main__':
    main()
