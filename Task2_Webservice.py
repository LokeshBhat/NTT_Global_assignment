
""" Task 2, Webservice/API """

import paramiko
import json
import time
import os
import regex
from flask import Flask
import json

# SSH parameter declaration
host = "127.0.0.1"
port = "10020"
username = "user1"
password = "admin"

# SSH connection establishment
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

# Running the required command
c = ssh.invoke_shell()
c.send('show running-config\r\n')

time.sleep(2)  # wait for the server to respond

result = c.recv(9999)
result = result.decode("utf-8")

with open('file.txt', 'w', encoding='utf-8') as file:
    file.write(result)

with open('file.txt', 'r') as file:
    result = file.read()

os.remove("file.txt")

# parsing the data in required format
reg = r'!\ninterface.*?\n!'
match = regex.finditer(reg, result, regex.DOTALL, overlapped=True)
res_list = []  # List to store the parsed data

for i in match:
    d = {}
    z = i.group()
    z = z[2:-2].split('\n')

    for j in z:
        l = j.split()
        if len(l) == 2:
            d[l[0]] = l[1]
        if l[0] == 'ip':
            d['ip address'] = l[2]
            d['subnet'] = l[3]
        if len(l) == 1:
            d[l[0]] = "Yes"
        if len(l) > 4:
            s = ' '.join(l[1:])
            d[l[0]] = s.replace("\"", '')
        if len(l) == 3:
            d['ip address'] = 'no ip address'

    res_list.append(d)

# Storing the information that is suitable for printing in a tabular format
keys = []
for i in res_list:
    for j in i:
        if j not in keys:
            keys.append(j)

        # print(res_list)
for i in res_list:
    for j in keys:
        i.setdefault(j, 'None')

new_res_list = []
for i in res_list:
    d = {}
    for j in keys:
        d[j] = i[j]
    new_res_list.append(d)

# Web service using Flask
app = Flask(__name__)


# End point to return all blocks
@app.route('/interface')
def index():
    print('\nreturning all blocks')
    return json.dumps(str(new_res_list))


# End point to return a particular block
@app.route('/interface/<interface>/')
def spec_interface(interface):
    interface = interface.replace('_', '/')
    print('\nreturning a single block')
    output_dict = [x for x in new_res_list if x['interface'] == interface]
    return json.dumps(str(output_dict))


app.run(debug=True)


