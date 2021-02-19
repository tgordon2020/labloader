from flask import Flask,request,render_template
from utils import devicelist
from utils import deviceip
from time import sleep
from collections import defaultdict
import json
from netmiko import ConnectHandler

progress = 0
progressbar = 0

devices = devicelist("topologies")

lab_names = {}
for k,v in devices.items():
    lab_names[k]=(k.replace("."," ").replace("virl","")).upper()
status = defaultdict(list)
app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

@app.route("/lab", methods=["GET"])
def lab():
    status = []
    return render_template("lab.html", content=lab_names)

@app.route("/labs", methods=["GET","POST"])
def labs():
    if request.method == "POST":
        lab = request.form['lab']
        for key,value in status.items():
            print(key,"--",value)
        loadlab(lab)
        return render_template("labs.html", content=status, progbar=progressbar)
    else:
        return render_template("labs.html", content=status, progbar=progressbar)

def loadlab(topology):
    global status
    global progress
    global progressbar
    status = defaultdict(list)
    progressbar = 0
    progress = 0
    for node in devices[topology]:
        print(len(devices[topology]))
        print(f"node {node}")
        print(f"deviceip {deviceip(node)}")
        device = {'device_type': 'cisco_ios_telnet',
                  'host': deviceip(node),
                  'password': 'password'}
        try:
            net_connect = ConnectHandler(**device)
            status[node].append(f"Connected to device {node}")
            progressbar += 1
            status[node].append(f"Attempting to revert to base config")
            progressbar += 1
            net_connect.send_command('config replace nvram:startup-config force',expect_string=r'Rollback Done')
            progressbar += 1
            status[node].append(f"Successfully reverted to base config")
            progressbar += 1
            status[node].append(f"Attempting to load {topology}")
            progressbar += 1
            net_connect.send_command(f'copy http://172.16.0.100/{topology}/{node}.txt system:running-config',expect_string=r"Destination filename")
            progressbar += 1
            net_connect.send_command('\n', expect_string=r'#')
            progressbar += 1
            status[node].append(f"Successfully loaded lab {topology} on {node}")
            progressbar += 1
            progress += 1
            progressbar = int((progress / len(devices[topology])) * 100)
            print (progressbar)
            net_connect.disconnect()
        except:
            status[node].append(f"Unable to load {topology}")
            net_connect.disconnect()
        





if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
