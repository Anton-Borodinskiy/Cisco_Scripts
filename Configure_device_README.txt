Script with multiprocessing wich allow you to configure cisco devices(All congifuration will apply and write to devices)

Start script and send next info to it:
Username
Password
Enable password
Enter hosts (You can put many lines)
Enter and check commadns(You can put many lines)


Example of using script:
PycharmProjects\Main>python Configure_device.py
Login: admin
Password:
Cisco enable password:
Enter hosts(Put empty sting to end!):
10.10.10.10

Enter command to execute on device(Line by line, for end send empty string):
snmp-server contact Anton Borodinsky

Your commands:
snmp-server contact Anton Borodinsky
Check if commands correct, put Y/N to continue: y
Start execute
Host 10.15.254.219 result:
config term
Configuration session is locked. The lock will be cleared once you exit out of configuration mode.
Enter configuration commands, one per line.  End with CNTL/Z.
Cisco_switch-1(config)#snmp-server contact Anton Borodinsky
Cisco_switch-1(config)#end
Cisco_switch-1#
Writing to files

