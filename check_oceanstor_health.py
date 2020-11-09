#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Check the overall health of an OceanStor storage device using API."""
#
#
# Toni Comerma
# October 2017
# Marc Lueckert - 09.11.2020
#
# Changes:
# - Python3 ready, argparse instead of getopts..
# - Add overall health check
#
# TODO:
#   https port number (8088) as parameter
#   better handling of exception situations in general

from enum import Enum
import sys
import argparse
import signal
import atexit
from OceanStor import OceanStor

class NagiosStatusCodes(Enum):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3


def signal_handler(signal, frame):
    """Handle timeouts, exiting with a nice message."""
    print('UNKNOWN: Timeout contacting device or Ctrl+C')
    sys.exit(NagiosStatusCodes.UNKNOWN)

def main():
    parser = argparse.ArgumentParser('Check Oceanstor Health')
    parser.add_argument('-H', type=str, metavar='host',
                        required=True, help='IP or DNS address')
    parser.add_argument('-s', type=str, metavar='system',
                        required=True, help='System_id of the OceanStor')
    parser.add_argument('-u', type=str, metavar='username',
                        required=True, help='Username to log into')
    parser.add_argument('-p', type=str, metavar='password',
                        required=True, help='Password')
    parser.add_argument('-t', type=int, default=10,
                        metavar='timeout', help='timeout in seconds')
    parser.add_argument('-f', action='store_true',
                        help='Report all components (OK, CRITICAL, UNKNOWN)')

    args = parser.parse_args()
    """Do the checking."""
    # Parametres
    host = args.H
    system_id = args.s
    username = args.u
    password = args.p
    timeout = args.t
    fulloutput = args.f

    # Handle timeout
    signal.alarm(timeout)

    os = OceanStor(host, system_id, username, password, timeout)
    
    try:
        os.login()
    except Exception as e:
        print("CRITICAL: Login failed: {0}".format(e))
        sys.exit(NagiosStatusCodes.CRITICAL)

    # cleaup if logged in
    atexit.register(os.logout)

    # Checking...
    text = ""
    status = ""
    criticals = 0
    unknowns = 0
    oks = 0
    loops = 0
    result_list = list()
    try:
        result_list.append(os.check_component_health(
            'enclosure', 'Enclosure', identifier='SERIALNUM'))
        result_list.append(os.check_component_health(
            'controller', 'Controller', identifier='ID'))
        result_list.append(os.check_component_health('disk', 'Disk'))
        result_list.append(os.check_component_health('eth_port', 'ETH Port'))
        result_list.append(os.check_component_health('fc_port', 'FC Port'))
    except Exception as e:
        print("CRITICAL: Exception while accessing the device: {0}".format(e))
        sys.exit(NagiosStatusCodes.CRITICAL)

    for ret in result_list:
        for i in ret:
            if int(i[0]) == 1:
                oks += 1
                status = "NORMAL"
            elif int(i[0]) == 0:
                unknowns += 1
                status = "UNKNOWN"
            elif int(i[0]) == 2:
                criticals += 1
                status = "FAULTY"

            if fulloutput or status != "NORMAL":
                text = "{0} </br>{1} {2} reported status {3}.".format(
                    text, i[2], i[1], status)
            loops += 1

    if criticals != 0:
        print(
            "CRITICAL: {0}/{1} components reported FAULTY. {2}".format(criticals, loops, text))
        sys.exit(NagiosStatusCodes.CRITICAL)
    elif unknowns != 0:
        print(
            "UNKNOWN: {0}/{1} components reported UNKNOWN. {2}".format(criticals, loops, text))
        sys.exit(NagiosStatusCodes.UNKNOWN)
    else:
        print("OK: {0}/{1} components are healthy. {2}".format(oks, loops, text))
        sys.exit(NagiosStatusCodes.OK)


####################################################
# Crida al programa principal
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGALRM, signal_handler)
    main()
