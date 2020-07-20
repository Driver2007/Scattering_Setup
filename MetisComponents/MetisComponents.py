#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 15:36:41 2017

@author: mellguth
"""

LOGWINDOW_W = 600
LOGWINDOW_H = 480

#import sys
#import os
from PyQt5 import QtGui, QtCore, QtWidgets
from Process import Process
from LogWindow import LogWindow
from SoftCtrlWindow import SoftCtrlWindow
#from NetworkHost import NetworkHost
from MetisConfig import MetisProcesses, MetisHosts
from collections import OrderedDict

import os
import sys
import time
from threading import Thread

SCRIPT_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))

###############################################################################
class MetisAppIndicator_Process:
    def __init__(self, process_config_obj=None):
        self.menulabel = process_config_obj.name
        self.submenu = None
        self.pobj = Process(process_config_obj) if process_config_obj!=None else None
        #self.startuplvl = 0
        #self.name = ""
        #if self.pobj!=None:
            #self.startuplvl = self.pobj.startuplvl
            #self.name = self.pobj.name
    
    def start(self):
        if self.pobj!=None:
            self.pobj.start()
        
    def output(self):
        if self.pobj!=None:
            self.logwin = LogWindow(self.pobj)
            self.logwin.resize(LOGWINDOW_W, LOGWINDOW_H)
            self.logwin.show()
        
    
    def terminate(self):
        if self.pobj!=None:
            self.pobj.terminate()

    def kill(self):
        if self.pobj!=None:
            self.pobj.kill()
    
    def is_running(self):
        if self.pobj==None:
            return False
        return self.pobj.running()
        
    
###############################################################################
###   MAIN CLASS   ############################################################
###############################################################################
class MetisAppIndicator(QtWidgets.QApplication):
    def __init__(self, iconfile):
        QtWidgets.QApplication.__init__(self, [])
        self.icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(iconfile), self)
        self.menu = QtWidgets.QMenu()
        self.menuitems = {}
        
        self.hosts = OrderedDict()
        self.processes = OrderedDict()
        
        self.icon_green = QtGui.QIcon(os.path.join(SCRIPT_PATH, 'GreenIcon.svg'))
        self.icon_red = QtGui.QIcon(os.path.join(SCRIPT_PATH, 'RedIcon.svg'))
        # test case
        #self.addHostEntry("host1", "Host 1", "192.168.2.100", False)
        #self.addProcessEntry("proc1", "Process 1", True)
        #self.rebuild_menu()
        # install application indicator icon
        self.icon.setContextMenu(self.menu)
        self.icon.show()
        self.upd_state = 0
        self.cancel_update_thread = False
        self.update_thread = Thread(target=self._update_thread_body)
        self.update_thread.start()
        #self.timer = QtCore.QTimer()
        #self.timer.timeout.connect(self.do_updates)
        #self.timer.start(1000)
        
        
    ###########################################################################
    ###   Host Entries   ######################################################
    ###########################################################################
    def clearHostEntries(self):
        pass
    
    def addHostEntry(self, refid, networkhost_object):
        if refid in self.hosts:
            print("Warning! addHostEntry(...) called with existing refid! Entry will be replaced")
        self.hosts[refid] = networkhost_object
    
    
    def setHostConnectedStatusThreadSafe(self, refid, connected):
        QtCore.QMetaObject.invokeMethod(self, "setHostConnectedStatus", QtCore.Qt.AutoConnection,
                QtCore.Q_ARG(str, refid),
                QtCore.Q_ARG(bool, connected))
    
    @QtCore.pyqtSlot(str, bool)
    def setHostConnectedStatus(self, refid, connected):
        #if refid in self.hosts:
        #    self.hosts[refid].connected = connected
        iconobj = self.icon_green if connected else self.icon_red
        self._set_menuicon(self._hostrefid_to_menuid(refid), iconobj)
    
    def _hostrefid_to_menuid(self, hostrefid):
        return 'host_' + hostrefid
    
    def _menuid_to_hostrefid(self, menuid):
        if menuid.startswith('host_'):
            return menuid[5:]
    
    ###########################################################################
    ###   Process Entries   ###################################################
    ###########################################################################
    def clearProcessEntries(self):
        pass
    
    def addProcessEntry(self, refid, process_config_obj):
        if refid in self.processes:
            print("Warning! addProcessEntry(...) called with existing refid! Entry will be replaced")
        p = MetisAppIndicator_Process(process_config_obj)
        self.processes[refid] = p
    
    
    def setProcessRunningStatusThreadSafe(self, refid, running):
        QtCore.QMetaObject.invokeMethod(self, "setProcessRunningStatus", QtCore.Qt.AutoConnection,
                QtCore.Q_ARG(str, refid),
                QtCore.Q_ARG(bool, running))
    
    @QtCore.pyqtSlot(str, bool)
    def setProcessRunningStatus(self, refid, running):
        iconobj = self.icon_green if running else self.icon_red
        self._set_menuicon(self._processrefid_to_menuid(refid), iconobj)
        
    def _processrefid_to_menuid(self, process_refid):
        return 'p_' + process_refid
    
    def _menuid_to_processrefid(self, menuid):
        return menuid[2:]
    
    ###########################################################################
    ###   General   ###########################################################
    ###########################################################################
    def _set_menuicon(self, menuid, iconobj):
        if type(iconobj)!=type(QtGui.QIcon()):
            print("_set_menuicon(...) called with non-QIcon-object")
            return
        if menuid in self.menuitems:
            self.menuitems[menuid].setIcon(iconobj)
            #pass
    
    def rebuild_menu(self):
        self.menu.clear()
        self.menuitems = {}
        # add network host entries
        self.menu.addSeparator()
        self.menu.addAction("--- Network devices: ---")
        for host_refid in self.hosts.keys():
            host = self.hosts[host_refid]
            menuid = self._hostrefid_to_menuid(host_refid)
            iconobj = self.icon_green if host.connected else self.icon_red
            self.menuitems[menuid] = self.menu.addAction(iconobj, host.label)
        # add process entries
        self.menu.addSeparator()
        self.menu.addAction("--- Software components: ---")
        self.menu.addAction("Start all", self._start_all_processes)
        self.menu.addAction("Stop all", self._stop_all_processes)
        self.menu.addAction("Software Control...", self._software_control)
        for process_refid in self.processes.keys():
            process = self.processes[process_refid]
            menuid = self._processrefid_to_menuid(process_refid)
            iconobj = self.icon_green if process.is_running() else self.icon_red
            process.menu = self.menu.addMenu(process.menulabel)
            #process.menu = QtWidgets.QMenu(process.menulabel)
            #self.menuitems[menuid].setIcon(iconobj)
            process.menu.addAction("Start", process.start)
            process.menu.addAction("Read Messages", process.output)
            process.menu.addSeparator()
            process.menu.addAction("Terminate", process.terminate)
            self.menuitems[menuid] = process.menu
            #self.menu.addMenu(process.menu)
            #process.menu.addAction("Kill", process.kill)
            
        # add quit entry
        self.menu.addSeparator()
        self.menu.addAction("Quit", self.on_quit)
        self.icon.setContextMenu(self.menu)

    def _update_thread_body(self):
        while not self.cancel_update_thread:
            if (self.upd_state % 30)==1 and not self.cancel_update_thread: # ping after one second, then twice a minute
                for hostid in self.hosts:
                    if self.cancel_update_thread:
                        break
                    if self.hosts[hostid].ping():
                        self.setHostConnectedStatusThreadSafe(hostid, True)
                    else:
                        self.setHostConnectedStatusThreadSafe(hostid, False)
            if (self.upd_state % 3)==2 and not self.cancel_update_thread: # check after 2 seconds, then every 3 seconds
                for processid in self.processes:
                    if self.cancel_update_thread:
                        break
                    if self.processes[processid].is_running():
                        self.setProcessRunningStatusThreadSafe(processid, True)
                    else:
                        self.setProcessRunningStatusThreadSafe(processid, False)
            self.upd_state = (self.upd_state + 1) % 3600
            time.sleep(1.0)
    
    def _start_all_processes(self):
        plist = [self.processes[pkey] for pkey in self.processes if self.processes[pkey].pobj!=None]
        plist.sort(key=lambda x: x.pobj.startuplvl)        
        #print("Processes sorted by startup level")
        previous_startuplvl = 0
        for p in plist:
            #if p.pobj == None:
            #    continue
            if not p.pobj.running():
                #print("Starting {pname}".format(pname=p.pobj.name))
                if previous_startuplvl != p.pobj.startuplvl:
                    time.sleep(2.0)
                    previous_startuplvl = p.pobj.startuplvl
                p.pobj.start()
                time.sleep(0.5)
            
    
    def _stop_all_processes(self):
        plist = [self.processes[pkey] for pkey in self.processes if self.processes[pkey].pobj!=None]
        plist.sort(key=lambda x: x.pobj.startuplvl, reverse=True)
        for p in plist:
            #if p.pobj == None:
            #    continue
            if p.pobj.running():
                #print("Terminating {pname}".format(pname=p.pobj.name))
                p.pobj.terminate()
                time.sleep(0.5)
        
    def _software_control(self):
        self.softctrl_win = SoftCtrlWindow(self.processes, os.path.join(SCRIPT_PATH, 'RedIcon.svg'), os.path.join(SCRIPT_PATH, 'GreenIcon.svg'))
        self.softctrl_win.show()
        #self.softctrl_win.resize(250,150)
        #self.softctrl_win.setWindowTitle("Main Window")
            
    def on_quit(self):
        plist = [self.processes[pkey] for pkey in self.processes if self.processes[pkey].pobj!=None]
        any_process_running = False
        for p in plist:
            if p.pobj.running():
                any_process_running = True
        if any_process_running:
            QtWidgets.QMessageBox.information(None, "Cannot close indicator app", "Cannot close indicator app when software components are still running!")
            return
        # todo: warn about running processes
        #
        # really shut down
        self.cancel_update_thread = True
        self.update_thread.join()
        try:
            self.softctrl_win.closeAction()
        except:
            pass
        self.quit()
    

if __name__ == "__main__":
    APP = MetisAppIndicator(os.path.join(SCRIPT_PATH, 'MetisCtrlIcon.svg'))
    for idx, h in enumerate(MetisHosts):
        APP.addHostEntry("{i}".format(i=idx), h)
    for idx, p in enumerate(MetisProcesses):
        APP.addProcessEntry("{i}".format(i=idx), p)
    APP.rebuild_menu()
    APP.setQuitOnLastWindowClosed(False)
    APP.exec_()
