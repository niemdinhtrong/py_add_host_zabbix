import unittest
import zabbix
from main import get_host

class TestZabbix(unittest.TestCase):
    config = zabbix.get_config('setting')
    username = config['zabbix']['zabbix_username']
    passwd = config['zabbix']['zabbix_password']
    group = config['zabbix']['group_name']
    template = config['zabbix']['template_name']
    list_host = get_host('hosts')
    key = "9f01bf795a0fddcea5d9ed8b3864a581"
    zapi = zabbix.Zabbix(username, passwd, group, template)

    def test_get_key(self):
        a1, a2 = self.zapi.get_aut_key()
        self.assertEqual(a2, "Ok")

    def test_tem_id_ok(self):
        a1, a2 = self.zapi.get_tem_id(self.key)
        self.assertEqual(a2, "Ok")

    def test_tem_id_er(self):
        a1, a2 = self.zapi.get_tem_id("1235")
        self.assertEqual(a2, "Error")

    def test_group_id_ok(self):
        a1, a2 = self.zapi.get_group_id(self.key)
        self.assertEqual(a2, "Ok")
    
    def test_group_id_er(self):
        a1, a2 = self.zapi.get_group_id("adfgg")
        self.assertEqual(a2, "Error")
    
    def test_add_host_ok(self):
        a1 = self.zapi.add_host(self.key, self.list_host, 2, 10001)
        self.assertEqual(a1, "Ok")

    def test_add_host_er(self):
        a1 = self.zapi.add_host("adfgg", self.list_host, 2, 10001)
        self.assertEqual(a1, "Error")