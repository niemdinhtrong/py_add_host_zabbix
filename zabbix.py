import configparser
import json
import sys
import requests
from requests.auth import HTTPBasicAuth

def get_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config

config = get_config('setting')
addr = config['zabbix']['zabbix_addr']

class Zabbix(object):
    url = 'http://{}/zabbix/api_jsonrpc.php'.format(addr)
    print(url)
    headers = {'content-type': 'application/json'}
    
    def __init__(self, username, passwd, group, template):
        #self.url = url
        #self.header = header
        self.username = username
        self.passwd = passwd
        self.group = group
        self.template = template

    def get_aut_key(self):
        payload= {'jsonrpc': '2.0','method':'user.login','params':
                {'user':'admin','password':'zabbix'},'id':'1'}
        r = requests.post(self.url, data=json.dumps(payload), headers=self.headers,
                         verify=True, auth=HTTPBasicAuth('admin','zabbix'))
        if r.status_code != 200:
            print('problem -key')
            print(r.status_code)
            sys.exit()
            return ("Error")
        else:
            try:
                result=r.json()
                auth_key=result['result']
                return (auth_key, "Ok")
            except:
                return ("Error", "Error")

    def get_tem_id(self, auth_key):
        payload={
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": [
                        self.template,
                    ]
                }
            },
            "auth": auth_key,
            "id": 1
        }
        r = requests.post(self.url, data=json.dumps(payload),
                      headers=self.headers, verify=True,
                      auth=HTTPBasicAuth(self.username,self.passwd))
        if r.status_code != 200:
            return ("Error")
        else:
            try:
                a = r.json()['result'][0]
                print("tem: ", a['templateid'])
                return(a['templateid'], "Ok")
            except:
                return ("Error", "Error")

    def get_group_id(self, auth_key):
        payload={
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": [
                        self.group,
                    ]
                }
            },
            "auth": auth_key,
            "id": 1
        }
        r = requests.post(self.url, data=json.dumps(payload),
                      headers=self.headers, verify=True,
                      auth=HTTPBasicAuth(self.username,self.passwd))
        if r.status_code != 200:
            return ("Error")
        else:
            try:
                a = r.json()['result'][0]
                groupid = a['groupid']
                print("Group: ", groupid)
                return (groupid, "Ok")
            except:
                return ("Error", "Error")

    def add_host(self, auth_key, list_host, groupid, templateid):
        i = 0
        status_l = []
        for host in list_host:
            ip = host[1]
            name = host[0]
            payload={
                "jsonrpc": "2.0",
                "method": "host.create",
                "params": {
                    "host": name,
                    "interfaces": [
                        {
                            "type": 1,
                            "main": 1,
                            "useip": 1,
                            "ip": ip,
                            "dns": "",
                            "port": "10050"
                        }
                    ],
                    "groups": [
                        {
                            "groupid": groupid
                        }
                    ],
                    "templates": [
                        {
                            "templateid": templateid
                        }
                    ],
                },
                    "auth": auth_key,
                    "id":  i + 1
            }
            r = requests.post(self.url, data=json.dumps(payload),
                          headers=self.headers, verify=True,
                          auth=HTTPBasicAuth(self.username,self.passwd))
            print(r.json())
            if 'result' in r.json():
                status_l.append("Ok")
            else:
                status_l.append("Error")
        print(status_l)
        for status in status_l:
            if status == "Error":
                sta = "Error"
                break
            else:
                sta = "Ok"
        return sta
