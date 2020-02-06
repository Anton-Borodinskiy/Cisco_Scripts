#!/usr/bin/python3.6
from netmiko import ConnectHandler
from netmiko.ssh_autodetect import SSHDetect
from getpass import getpass
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import re

def Detect_device_type(host_to_connect):
    myrouter = {
        'device_type': 'autodetect',
        'host': host_to_connect,
        'username': Username,
        'password': Password,
    }
    connection = SSHDetect(**myrouter)
    best_match = connection.autodetect()
    if best_match == None:
        best_match = "cisco_ios"
    return best_match

def Execute_command(host_to_connect):
    try:
        myrouter = {
            'device_type': Detect_device_type(host_to_connect),
            'host': host_to_connect,
            'username': Username,
            'password': Password,
            'secret': Enable
        }
        connection = ConnectHandler(**myrouter)
        output = []
        if "cisco_ios" in myrouter["device_type"]:
            connection.enable()
            terminal = connection.send_command("terminal length 0")
            routes = connection.send_command("show ip route vrf * connected")
            routes = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{2}", routes)
            for k in range(len(routes)):
                if "/32" in routes[k]:
                    continue
                elif "Null0" in routes[k]:
                    continue
                else:
                    routes_str = "show ip route vrf * " + routes[k]
                    routes_str = routes_str[:-3]
                    interface = connection.send_command(routes_str).split("\n")
                    for t in range(len(interface)):
                        if "directly connected," in interface[t]:
                            interface = interface[t]
                            break
                    interface = interface.strip().split(" ")[-1]
                    if "." in interface:
                        interface = interface.replace("GigabitEthernet", "Gi").strip()
                        description = connection.send_command("show interfaces description | include " + interface).strip().split(" up ")[-1].strip()
                    else:
                        description = connection.send_command("show interfaces " + interface + " description").strip().split(" up ")[-1].strip()
                    output.append([routes[k], interface, description, host_to_connect])
        elif "huawei" in myrouter["device_type"]:
            routes = connection.send_command("display ip interface brief").strip()
            for k in range(100):
                routes = routes.replace("  ", " ")
            routes = routes.split("\n")
            for k in range(len(routes)):
                if "Interface" in routes[k]:
                    continue
                elif "unassigned" in routes[k]:
                    continue
                elif "MEth" in routes[k]:
                    continue
                elif "/" in routes[k]:
                    routes[k] = routes[k].split(" ")
                    interface = routes[k][0]
                    network = routes[k][1]
                    description = connection.send_command("display interface description " + interface).strip().split("   ")[-1].strip()
                    if "up" == description or "down" == description:
                        # print("No desc " + interface)
                        vlan_num = re.findall(r'\d+', interface)
                        description = connection.send_command("display vlan " + vlan_num[0]).strip().split("disable")[-1].strip()
                        # print("DESC FROM VLAN " + interface + ": " + description + " " + host_to_connect)
                    output.append([network, interface, description, host_to_connect])


            # print(routes)
        elif "cisco_nxos" in myrouter["device_type"]:
            routes = connection.send_command("show ip route direct vrf all")
            routes = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{2}", routes)
            for k in range(len(routes)):
                if "/32" in routes[k]:
                    continue
                else:
                    routes_k = routes[k][:-3]
                    routes_str = "show ip route vrf all " + routes_k + " direct"
                    interface = connection.send_command(routes_str).split("\n")
                    for t in range(len(interface)):
                        if "*via" in interface[t]:
                            interface = interface[t]
                            break
                    interface = interface.strip().split(",")[1].strip()
                    description = connection.send_command("show interface " + interface + " description").strip().split("   ")[-1].strip()
                    output.append([routes[k], interface, description, host_to_connect])
        connection.disconnect()
        return output
    except:
        not_connected = "Not connected " + host_to_connect
        print(not_connected)
        return not_connected


#Pool size
pool = ThreadPool(16)

#Main data
Username = input("Login: ")
Password = getpass(prompt="Password: ")
Enable = getpass(prompt="Cisco enable password: ")

hosts = []
host = " "
print("Enter hosts(Put empty sting to end!):")

while host != "":
    host = input("")
    if host == "":
        continue
    else:
        hosts.append(host)

#Start Pool
results = pool.map(Execute_command, hosts)
print(results)
print("Writing to files")
success_results = open("Success.txt", "w")
bad_results = open("Bad.txt", "w")
for res in results:
    if "Not connected" in res:
        bad_results.write(res)
        bad_results.write("\n")
    else:
        for deep_res in res:
            print(deep_res)
            success_results.write(deep_res[0])
            success_results.write(" | ")
            success_results.write(deep_res[1])
            success_results.write(" | ")
            success_results.write(deep_res[2])
            success_results.write(" | ")
            success_results.write(deep_res[3])
            success_results.write("\n")
success_results.close()
bad_results.close()
