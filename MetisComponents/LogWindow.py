# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 14:39:15 2017

@author: martin
"""

from PyQt5 import QtGui, QtCore, QtWidgets

class LogWindow(QtWidgets.QMainWindow):
    def __init__(self, processobj=None, title=None):
        QtWidgets.QMainWindow.__init__(self)
        
        self.pobj = processobj
        wintitle = "Log"
        if self.pobj!=None:
            wintitle = "Log " + self.pobj.name
        self.setWindowTitle(wintitle)
        self.widget = QtWidgets.QWidget(self)
        self.textarea = QtWidgets.QPlainTextEdit(self._logbuf_to_message(), self.widget)
        self.textarea.setReadOnly(True)
        #self.textarea.resize(600, 480)        
        self.textarea.setStyleSheet("background-color: rgb(235,235,235);")
        self.textarea.setStyleSheet('font: 11pt "Courier";')
        self.bu_update = QtWidgets.QPushButton("Update", self.widget)
        self.bu_update.clicked.connect(self._on_update_clicked)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.bu_update)
        vbox.addWidget(self.textarea)
        self.widget.setLayout(vbox)
        self.setCentralWidget(self.widget)
        
        
    
    def _logbuf_to_message(self):
        if self.pobj==None:
            return ""
        logbuf = self.pobj.get_output()
        if logbuf==None:
            logbuf = ""
        elif type(logbuf)==type([]):
            logbuf = '\n'.join(logbuf)
        linesmsg = " (" + str(self.pobj.outlines) + " lines max)"
        header = "Terminal messages from " + self.pobj.name + linesmsg + ":\n"
        logbuf = header + logbuf
        return logbuf
    
    def _on_update_clicked(self):
        self.textarea.setPlainText(self._logbuf_to_message())

