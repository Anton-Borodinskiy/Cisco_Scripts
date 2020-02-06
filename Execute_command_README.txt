Script with multiprocessing wich allow you execute command on device and write it to file.

Start script and send next info to it:
Username
Password
Enable password
Enter hosts (You can put many lines)
Enter command to execute on device

Example of usage(Also you will have 2 files in script directory Success.txt and Bad.txt):
PycharmProjects\Main>python Execute_command.py
Login: admin
Password:
Cisco enable password:
Enter hosts(Put empty sting to end!):
CISCO-CAT

Enter command to execute on device: show ver
Host CISCO-CAT result:
Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version 15.0(2)SE8, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2015 by Cisco Systems, Inc.
Compiled Thu 14-May-15 02:39 by prod_rel_team

ROM: Bootstrap program is C2960 boot loader
BOOTLDR: C2960 Boot Loader (C2960-HBOOT-M) Version 15.0(2r)EZ1, RELEASE SOFTWARE (fc2)

CISCO-CAT uptime is 3 years, 5 weeks, 6 days, 21 hours, 2 minutes
System returned to ROM by power-on
System restarted at 21:33:56 MSK Tue Dec 20 2016
System image file is "flash:/c2960-lanbasek9-mz.150-2.SE8/c2960-lanbasek9-mz.150-2.SE8.bin"


This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

Configuration register is 0xF
Writing to files
