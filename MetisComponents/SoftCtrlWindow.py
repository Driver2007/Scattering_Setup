# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:39:46 2017

@author: user
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
#from Process import Process
#from NetworkHost import NetworkHost
#from MetisConfig import MetisProcesses, MetisHosts
#from collections import OrderedDict

from threading import Thread
import time
from functools import partial

class SoftCtrlWindow(QtWidgets.QMainWindow):
    def __init__(self, processes, icon_red, icon_green):
        QtWidgets.QMainWindow.__init__(self)
        self.processes = processes
        self.icon_red = QPixmap(icon_red)
        self.icon_green = QPixmap(icon_green)
        wintitle = "Metis Software Components"
        self.setWindowTitle(wintitle)
        self.main_panel = QtWidgets.QWidget(self)
        self.process_panels = []
        self.widget_groups = {}
        vbox = QtWidgets.QVBoxLayout()
        for process_refid in self.processes.keys():
            self.process_panels.append(QtWidgets.QWidget(self.main_panel))
            
            process_panel = self.process_panels[-1]
            process = self.processes[process_refid]
            running = process.is_running()
            hbox = QtWidgets.QHBoxLayout()
            hbox.setAlignment(Qt.AlignRight)
            widget_group = {}
            # -----------------------------------------------------------------
            widget_group["label"] = QtWidgets.QLabel(process.menulabel)
            hbox.addWidget(widget_group["label"])
            # -----------------------------------------------------------------
            widget_group["running"] = QtWidgets.QLabel()
            if running:
                widget_group["running"].setPixmap(self.icon_green)
            else:
                widget_group["running"].setPixmap(self.icon_red)
            hbox.addWidget(widget_group["running"])
            # -----------------------------------------------------------------
            widget_group["start"] = QtWidgets.QPushButton("Start", process_panel)
            hbox.addWidget(widget_group["start"])
            #widget_group["start"].clicked.connect(print)
            widget_group["start"].clicked.connect(partial(SoftCtrlWindow._on_start_clicked, self, process_refid))
            # -----------------------------------------------------------------
            widget_group["stop"] = QtWidgets.QPushButton("Stop", process_panel)
            hbox.addWidget(widget_group["stop"])
            widget_group["stop"].clicked.connect(partial(SoftCtrlWindow._on_stop_clicked, self, process_refid))
            # -----------------------------------------------------------------
            widget_group["log"] = QtWidgets.QPushButton("Show log", process_panel)
            hbox.addWidget(widget_group["log"])
            widget_group["log"].clicked.connect(partial(SoftCtrlWindow._on_log_clicked, self, process_refid))
            ### ---------------------------------------------------------------
            self.widget_groups[process_refid]=widget_group
            process_panel.setLayout(hbox)
            vbox.addWidget(process_panel)
            ### ---------------------------------------------------------------
        self.main_panel.setLayout(vbox)
        self.setCentralWidget(self.main_panel)
        # ---------------------------------------------------------------------
        self.upd_state = 0
        self.cancel_update_thread = False
        self.update_thread = Thread(target=self._update_thread_body)
        self.update_thread.start()
        # ---------------------------------------------------------------------
        
    def _update_thread_body(self):
        while not self.cancel_update_thread:
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
    

    def setProcessRunningStatusThreadSafe(self, refid, running):
        QtCore.QMetaObject.invokeMethod(self, "setProcessRunningStatus", QtCore.Qt.AutoConnection,
                QtCore.Q_ARG(str, refid),
                QtCore.Q_ARG(bool, running))
    
    @QtCore.pyqtSlot(str, bool)
    def setProcessRunningStatus(self, refid, running):
        pixmap = self.icon_green if running else self.icon_red
        if refid in self.widget_groups:
            self.widget_groups[refid]["running"].setPixmap(pixmap)
        #self._set_menuicon(self._processrefid_to_menuid(refid), iconobj)

    def closeEvent(self,event):
        self.closeAction()
        event.accept()
    
    def closeAction(self):
        self.cancel_update_thread = True
        self.update_thread.join()
        self.close()

    def _on_start_clicked(self, refid):
        print(refid)
        try:
            self.processes[refid].start()
        except:
            pass
    
    def _on_stop_clicked(self, refid):
        self.processes[refid].terminate()
    
    def _on_log_clicked(self, refid):
        self.processes[refid].output()