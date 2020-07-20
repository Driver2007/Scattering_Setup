# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 13:32:12 2017

@author: mellguth
"""

import subprocess


class NetworkHost:
    def __init__(self, host="", label="", connected=False):
        if ' ' in host:
            print("Invalid host specification: {hoststr}".format(hoststr=host))
        self.host = host
        self.label = label
        self.connected = connected

    def ping(self):
        """ uses linux ping command to test reachability of a host
        this has the advantage that it works with user rights (the
        ping command has a setuid bit to be able to open a raw socket) """
        ret = subprocess.call(["timeout", "0.5", "ping", "-c", "1", "{host}".format(host=self.host)],
                              shell=False,
                              stdout=open('/dev/null', 'w'),
                              stderr=subprocess.STDOUT)
        if ret == 0:
            self.connected = True
        else:
            self.connected = False
        return self.connected            
