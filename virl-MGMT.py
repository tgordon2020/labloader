import os
from utils import deviceip
from time import sleep


# update gig0/0 configuration for OOBM
def gig00(ip):
    for i,v in enumerate(device_config):
        if "interface GigabitEthernet0/1\n" in v:
            gig00_index = i-1
        else:
            pass
    
    gig = ("!\n",
        "interface GigabitEthernet0/0\n"
        " description MGMT\n",
        " no switchport\n",
        " vrf forwarding MGMT\n",
        f" ip address {ip} 255.255.255.0\n",
        " duplex auto\n",
        " speed auto\n",)

    for y in reversed(gig):
        device_config.insert(gig00_index,y)


# insert VRF def in config
def hostname():
    for i,v in enumerate(device_config):
        if "hostname" in v:
            hostname_index = i+1
        else:
            pass
    device_config.insert(hostname_index,"!\nvrf definition MGMT\n !\n address-family ipv4\n exit-address-family\n!\n")

# insert http client device and VRF default route
def httpclient():
    for i,v in enumerate(device_config):
        if "line con 0" in v:
            linecon0_index = i
        else:
            pass
    device_config.insert(linecon0_index,"!\nip http client source-interface GigabitEthernet0/0\nip route vrf MGMT 0.0.0.0 0.0.0.0 172.16.0.1\nno cdp log mismatch duplex\n")

# insert VTY config for mgmt
def vty04():
    for i,v in enumerate(device_config):
        if "vty" in v:
            vty_index = i
            while vty_index < len(device_config):
                device_config.pop(vty_index)

    vty_config = ("line vty 0 4\n",
                  " privilege level 15\n",
                  " password password\n",
                  " login\n",
                  " transport input all\n",
                  "!\n",
                  "end\n")

    for y in reversed(vty_config):
        device_config.insert(vty_index,y)


# change interfaces from gigX to gig0/X
def fixgig():
    for i,v in enumerate(device_config):
        if "GigabitEthernet1" in v:
            v = v.replace("GigabitEthernet", "GigabitEthernet0/")
            device_config.pop(i)
            device_config.insert(i,v)
        elif "GigabitEthernet2" in v:
            v = v.replace("GigabitEthernet", "GigabitEthernet0/")
            device_config.pop(i)
            device_config.insert(i,v)
        elif "GigabitEthernet3" in v:
            v = v.replace("GigabitEthernet", "GigabitEthernet0/")
            device_config.pop(i)
            device_config.insert(i,v)
        else:
            pass 

def domainname(domain):
    for i,v in enumerate(device_config):
        if "domain lookup" in v:
            device_config.insert(i+1,f"ip domain name {domain}\n")
        else:
            pass



for x in os.listdir("topologies"):
    for y in os.listdir(f"topologies/{x}"):
        if "txt" in y:
            device_ip = deviceip(y.split(".")[0])

            # Attempt to open file as utf-16
            try:
                with open(f"topologies/{x}/{y}", "r", encoding='utf-16') as config:
                    device_config = config.readlines()
            except:
                pass
            
            # Attempt to open file as ascii
            try:
                with open(f"topologies/{x}/{y}", "r", encoding='ascii') as config:
                    device_config = config.readlines()
            except:
                pass

            # Check if gig0/x exists.  If not fix the gigx interface names
            if "interface GigabitEthernet0/1\n" in device_config:
                pass
            else:
                fixgig()

            #Check for gig0/0.  If exists check if it has correct config.  If not exist create, if not correct fix
            if "interface GigabitEthernet0/0\n" in device_config:
                if " vrf forwarding MGMT\n" in device_config:
                    pass
                else:
                    print(f"interface Gig0/0 exists, but not configured in {x}/{y}")
                    print(f"Removing bad Gig0/0 config in {x}/{y}")
                    for i,v in enumerate(device_config):
                        if v == "interface GigabitEthernet0/0\n":
                            start_index = i
                        if v == "interface GigabitEthernet0/1\n":
                            end_index = i - 1
                    iteration = end_index - start_index
                    for z in range(iteration):
                        device_config.pop(start_index)
                    gig00(device_ip)
            else:
                try:
                    gig00(device_ip)
                except:
                    print(f"issues adding gig0/0 mgmt interface in topologies/{x}/{y}, manually edit file") 

            if "vrf definition MGMT\n" in device_config:
                pass
            else:
                try:
                    hostname()
                except:
                    print(f"issues adding MGMT vrf to to toplogies/{x}/{y}, manually edit file")
    
            if " line vty 0 4\n" in device_config:
                pass
            else:
                try:
                    vty04()
                except:
                    print(f"issues adding VTY 0 4 config to topologies/{x}/{y}")

            if "ip http client source-interface GigabitEthernet0/0\n" in device_config:
                pass
            else:
                try:
                    httpclient()
                except:
                    print(f"issues adding http client and VRF route to topologies/{x}/{y}")
            

            if f"ip domain name {x}\n" in device_config:
                pass
            else:
                try:
                    domainname(x)
                except:
                    print(f"issues adding domain name {x} to {y}")

            with open(f"topologies/{x}/{y}", "w", encoding='ascii') as config_update:
                config_update.writelines(device_config)

