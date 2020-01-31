#!/usr/bin/python3.6
from netmiko import ConnectHandler
from getpass import getpass
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

def Execute_command(host_to_connect):
    try:
        myrouter = {
            'device_type': 'cisco_ios',
            'host': host_to_connect,
            'username': Username,
            'password': Password,
            'secret': Enable,
            'global_delay_factor': 3,
        }
        connection = ConnectHandler(**myrouter)
        # Enter enable mode
        connection.enable()
        # Send empty string to ensure enable mode
        send_empty = connection.send_command(" \n ")
        # Set terminal len
        terminal = connection.send_command("terminal length 0 \n")
        # Get command result
        command_result = connection.send_config_set(Commands)
        write = connection.send_command("write")
        output = "Host " + host_to_connect + " result:\n" + command_result
        print(output)
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
Commands = []
while True:
    Command = " "
    print("Enter command to execute on device(Line by line, for end send empty string): ")
    while Command != "":
        Command = input("")
        if Command == "":
            continue
        else:
            Commands.append(Command.strip())
    print("Your commands:")
    for i in range(len(Commands)):
        print(Commands[i])
    Check_command = input("Check if commands correct, put Y/N to continue: ")
    if Check_command == "y" or Check_command == "Y":
        break
    else:
        continue
print("Start execute")

#Start Pool
results = pool.map(Execute_command, hosts)
print("Writing to files")
success_results = open("Success.txt", "w")
bad_results = open("Bad.txt", "w")
for i in range(len(results)):
    if "Not connected " in results[i]:
        bad_results.write(results[i])
        bad_results.write("\n")
    else:
        success_results.write(results[i])
        success_results.write("\n")
success_results.close()
bad_results.close()
