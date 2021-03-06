# check_oceanstor

Nagios plugin for monitoring Huawei OceanStor storage devices using the API

Commands implemented
- check_oceanstor_alarms.py: Checks for active alarms
- check_oceanstor_filesystems.py: Checks free space on filesystems
- check_oceanstor_diskdomains.py: Checks free space on diskdomains
- check_oceanstor_storagepools.py: Checks free space on storagepools
- check_oceanstor_health.py: Performs various checks against the main components (Enclosure, Controller, Disk, Eth Ports, FC Ports)

Just an small subset of what is possible is implemented, but it's what we need.
EVERYTHING on an OceanStor can be done using the API. If not convinced,
connect the browser to the device and fire up developer tools. You will see
the browser is using the API for doing the job.

Google "Huawei OceanStor REST API" for the documentation

Feel free to fork and extend

## Examples

* Check the general health with minimal output.
```
check_oceanstor_health.py -H <ADDRESS> -u <USER> -p <PWD> -s <SYSTEM_ID>
OK: 81/81 components are healthy.
```

* Check the general health with full output.
```
check_oceanstor_health.py -H <ADDRESS> -u <USER> -p <PWD> -s <SYSTEM_ID> -f
OK: 81/81 components are healthy.  </br>Enclosure XXXX reported status NORMAL. </br>Enclosure XXXX reported status NORMAL. </br>Controller 0A reported status NORMAL. </br>Controller 0B reported status NORMAL. </br>Disk CTE0.0 reported status NORMAL. </br>Disk CTE0.1 reported status NORMAL. </br>Disk CTE0.2 reported status NORMAL. </br>Disk CTE0.3 reported status NORMAL. </br>Disk CTE0.4 reported status NORMAL. </br>Disk CTE0.5 reported status NORMAL. </br>Disk CTE0.6 reported status NORMAL. </br>Disk CTE0.7 reported status NORMAL. </br>Disk CTE0.8 reported status NORMAL. </br>Disk CTE0.9 reported status NORMAL. </br>Disk CTE0.10 reported status NORMAL. </br>Disk CTE0.11 reported status NORMAL. </br>Disk CTE0.12 reported status NORMAL. </br>Disk CTE0.13 reported status NORMAL. </br>Disk CTE0.14 reported status NORMAL. </br>Disk CTE0.15 reported status NORMAL. </br>Disk CTE0.16 reported status NORMAL. </br>Disk CTE0.17 reported status NORMAL. </br>Disk CTE0.18 reported status NORMAL. </br>Disk CTE0.19 reported status NORMAL. </br>Disk CTE0.20 reported status NORMAL. </br>Disk CTE0.21 reported status NORMAL. </br>Disk CTE0.22 reported status NORMAL. </br>Disk CTE0.23 reported status NORMAL. </br>Disk CTE0.24 reported status NORMAL. </br>Disk CTE0.25 reported status NORMAL. </br>Disk CTE0.26 reported status NORMAL. </br>Disk CTE0.27 reported status NORMAL. </br>Disk CTE0.28 reported status NORMAL. </br>Disk CTE0.29 reported status NORMAL. </br>Disk CTE0.30 reported status NORMAL. </br>Disk CTE0.31 reported status NORMAL. </br>Disk CTE0.32 reported status NORMAL. </br>Disk CTE0.33 reported status NORMAL. </br>Disk CTE0.34 reported status NORMAL. </br>Disk CTE0.35 reported status NORMAL. </br>Disk DAE010.0 reported status NORMAL. </br>ETH Port CTE0.A.IOM0.P0 reported status NORMAL. </br>ETH Port CTE0.A.IOM0.P1 reported status NORMAL. </br>ETH Port CTE0.A.IOM0.P2 reported status NORMAL. </br>ETH Port CTE0.A.IOM0.P3 reported status NORMAL. </br>ETH Port CTE0.A.P0 reported status NORMAL. </br>ETH Port CTE0.A.P1 reported status NORMAL. </br>ETH Port CTE0.A.MGMT reported status NORMAL. </br>ETH Port CTE0.A.MAINTENANCE reported status NORMAL. </br>ETH Port CTE0.B.IOM0.P0 reported status NORMAL. </br>ETH Port CTE0.B.IOM0.P1 reported status NORMAL. </br>ETH Port CTE0.B.IOM0.P2 reported status NORMAL. </br>ETH Port CTE0.B.IOM0.P3 reported status NORMAL. </br>ETH Port CTE0.B.P0 reported status NORMAL. </br>ETH Port CTE0.B.P1 reported status NORMAL. </br>ETH Port CTE0.B.MGMT reported status NORMAL. </br>ETH Port CTE0.B.MAINTENANCE reported status NORMAL. </br>ETH Port DAE010.A.P0 reported status NORMAL. </br>ETH Port DAE010.A.P1 reported status NORMAL. </br>ETH Port DAE010.A.P2 reported status NORMAL. </br>ETH Port DAE010.A.P3 reported status NORMAL. </br>ETH Port DAE010.B.P0 reported status NORMAL. </br>ETH Port DAE010.B.P1 reported status NORMAL. </br>ETH Port DAE010.B.P2 reported status NORMAL. </br>ETH Port DAE010.B.P3 reported status NORMAL. </br>FC Port CTE0.A.IOM1.P0 reported status NORMAL. </br>FC Port CTE0.A.IOM1.P1 reported status NORMAL. </br>FC Port CTE0.A.IOM1.P2 reported status NORMAL. </br>FC Port CTE0.A.IOM1.P3 reported status NORMAL. </br>FC Port CTE0.A.IOM2.P0 reported status NORMAL. </br>FC Port CTE0.A.IOM2.P1 reported status NORMAL. </br>FC Port CTE0.A.IOM2.P2 reported status NORMAL. </br>FC Port CTE0.A.IOM2.P3 reported status NORMAL. </br>FC Port CTE0.B.IOM1.P0 reported status NORMAL. </br>FC Port CTE0.B.IOM1.P1 reported status NORMAL. </br>FC Port CTE0.B.IOM1.P2 reported status NORMAL. </br>FC Port CTE0.B.IOM1.P3 reported status NORMAL. </br>FC Port CTE0.B.IOM2.P0 reported status NORMAL. </br>FC Port CTE0.B.IOM2.P1 reported status NORMAL. </br>FC Port CTE0.B.IOM2.P2 reported status NORMAL. </br>FC Port CTE0.B.IOM2.P3 reported status NORMAL.
```

* Check one filesystem, including space used for "Data Protection", aka snapshots.
```
check_oceanstor_filesystems.py -H <ADDRESS> -u <USER> -p <PWD> -s <SYSTEM_ID>  -n <NAME> -w 70 -c 90 -W 1 -C 1
OK: [NAME] OK
OK: filesystem NAME: size: 11264GB, used:  7259GB, pctused: 64.45% Snapshots reserved:  2253GB, used:     0GB, pctused:  0.00%
| 'NAME'=64.45% 'NAME_snapshots'= 0.00%
```

* Check all filesystems with name starting with "FS"
```
check_oceanstor_filesystems.py -H <ADDRESS> -u <USER> -p <PWD> -s <SYSTEM_ID> -n FS* -w 70 -c 90

OK: [ FSname0 FSname1 FSname2 FSname3 FSname4 FSname5 FSname6 FSname7 FSname8 FSname9] OK
OK: filesystem FSname0: size: 11264GB, used:  7550GB, pctused: 67.03% Snapshots reserved:  2253GB, used:     0GB, pctused:  0.00%
OK: filesystem FSname1: size: 11264GB, used:  7527GB, pctused: 66.82% Snapshots reserved:  2253GB, used:     0GB, pctused:  0.00%
OK: filesystem FSname2: size: 11264GB, used:  7723GB, pctused: 68.57% Snapshots reserved:  2253GB, used:     0GB, pctused:  0.00%
OK: filesystem FSname3: size: 11264GB, used:  7662GB, pctused: 68.02% Snapshots reserved:  2253GB, used:     0GB, pctused:  0.00%
OK: filesystem FSname4: size: 11264GB, used:  7705GB, pctused: 68.40% Snapshots reserved:  2253GB, used:     0GB, pctused:  0.00%
OK: filesystem FSname5: size: 11264GB, used:  6985GB, pctused: 62.01% Snapshots reserved:  2253GB, used:     0GB, pctused:  0.00%
OK: filesystem FSname6: size: 11264GB, used:  7247GB, pctused: 64.34% Snapshots reserved:  2253GB, used:     0GB, pctused:  0.00%
OK: filesystem FSname7: size: 11264GB, used:     0GB, pctused:  0.00% Snapshots reserved:  2253GB, used:     0GB, pctused:  0.00%
OK: filesystem FSname8: size: 11264GB, used:     0GB, pctused:  0.00% Snapshots reserved:  2253GB, used:     0GB, pctused:  0.00%
OK: filesystem FSname9: size: 11264GB, used:     0GB, pctused:  0.00% Snapshots reserved:  2253GB, used:     0GB, pctused:  0.00%
| 'FSname0'=67.03% 'FSname0_snapshots'= 0.00% 'FSname1'=66.82% 'FSname1_snapshots'= 0.00% 'FSname2'=68.57% 'FSname2_snapshots'= 0.00% 'FSname3'=68.02% 'FSname3_snapshots'= 0.00% 'FSname4'=68.40% 'FSname4_snapshots'= 0.00% 'FSname5'=62.01% 'FSname5_snapshots'= 0.00% 'FSname6'=64.34% 'FSname6_snapshots'= 0.00% 'FSname7'= 0.00% 'FSname7_snapshots'= 0.00% 'FSname8'= 0.00% 'FSname8_snapshots'= 0.00% 'FSname9'= 0.00% 'FSname9_snapshots'= 0.00%
```

* Check for alarms. The plugin returns all active alarms, with serverity
```
check_oceanstor_alarms.py -H <ADDRESS> -u <USER> -p <PWD> -s <SYSTEM_ID>
OK: no alarms found | alarms=0

```


* Performance data graph from a filesystem
![Filesystem usage](images/filesystem_performance.png?raw=true "Filesystem usage")

* Status of a Diskdomain
![DiskDomain Usage](images/diskdomain_status.png?raw=true "Diskdomain status")

Author:

   Toni Comerma

   CCMA, SA
