import unittest
import zabbix
import main

class TestZabbix(unittest.TestCase):
    config = zabbix.get_config('setting')
    username = config['zabbix']['zabbix_username']
    passwd = config['zabbix']['zabbix_password']
    group = config['zabbix']['group_name']
    template = config['zabbix']['template_name']
    list_host = main.get_host('hosts')
    zapi = zabbix.Zabbix(username, passwd, group, template)

    def test_get_key(self):
        a1, a2 = self.zapi.get_aut_key()
        self.assertEqual(a2, "Ok")

    def test_tem_id(self):
        a1, a2 = self.zapi.get_tem_id("9f01bf795a0fddcea5d9ed8b3864a581")
        self.assertEqual(a2, "Ok")

    def test_group_id(self):
        a1, a2 = self.zapi.get_group_id("9f01bf795a0fddcea5d9ed8b3864a581")
        self.assertEqual(a2, "Ok")