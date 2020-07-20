# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 12:31:20 2017

@author: Martin Ellguth
"""

SHELL_CMD = "/bin/bash"

import subprocess
import tempfile
import os
import signal
#import stat
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
from threading import Thread
from RingBuffer import RingBuffer

        
class ProcessConfig:
    def __init__(self, name="", startcmds=[], wdir="", startuplvl=0, outlines=1000, stdin_pipe=False, envdict={}):
        """
        name is a short descriptive name for the user interface
        startcmds is a list of commands to be executed
        wdir is the working directory
        outlines is the maximum of stdout/stderr lines that are kept as history
        stdin_pipe = True causes a stdin pipe to be opened
        envdict allows for adding environment variables to the process environment
        """
        self.name = name
        self.startcmds = startcmds
        self.wdir = wdir
        self.startuplvl = startuplvl
        self.outlines = outlines
        self.stdin_pipe = False
        self.envdict = envdict

class Process:
    """ Represents a Process that can be launched, monitored and killed """
    def __init__(self, process_config_obj=None):
        if process_config_obj!=None and type(process_config_obj)==type(ProcessConfig()):
            self.name = process_config_obj.name
            self.startcmds = process_config_obj.startcmds
            self.wdir = process_config_obj.wdir
            self.outlines = process_config_obj.outlines
            self.outbuffer = RingBuffer(self.outlines)
            self.stdin_pipe = process_config_obj.stdin_pipe
            self.envdict = process_config_obj.envdict
            self.startuplvl = process_config_obj.startuplvl
            ###
        self.retcode = None
        self.subproc = None
        self.started = False
        self.tmpfpath = None
        self.stdout_queue = None
        self.stdout_thread = None
            
    
    def start(self):
        if self.started:
            return
        tmpfhandle, self.tmpfpath = tempfile.mkstemp()
        tmpf = os.fdopen(tmpfhandle, 'w')
        tmpf.write('#!{shellcmd}\n'.format(shellcmd=SHELL_CMD))
        tmpf.write('trap "exit" INT TERM\n')
        tmpf.write('trap "kill 0" EXIT\n')
        tmpf.write('cd "{path}"\n'.format(path=self.wdir))
        if type(self.startcmds)==type([]):
            for l in self.startcmds:
                if not l.endswith(' $'):
                    l = l + ' $'
                tmpf.write(l+"\n")
        elif type(self.startcmds)==type(""):
            bgmode = ' $' if not self.startcmds.endswith(' $') else ''
            tmpf.write(self.startcmds+bgmode+"\n")
        tmpf.write('sleep infinity\n')
        tmpf.close()
        #tmpf = open(self.tmpfpath, "r")
        #for l in tmpf:
        #    print("{l}".format(l=l))
        #tmpf.close()
        stdin_arg = subprocess.PIPE if self.stdin_pipe else None
        env_arg = dict(os.environ)
        env_arg.update(self.envdict)
        try:
            self.subproc = subprocess.Popen([SHELL_CMD, self.tmpfpath], bufsize=0, preexec_fn=os.setpgrp,
                                            stdin=stdin_arg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            cwd=self.wdir, env=env_arg)
        except OSError:
            print("Process.start(): subprocess.Popen(...) raised OSError")
            return
        self.stdout_queue = Queue()
        self.stdout_thread = Thread(target=self._enqueue_stdout, args=(self.subproc.stdout, self.stdout_queue))
        self.stdout_thread.daemon = True
        self.stdout_thread.start()
        self.started = True
    
    def _update_out_buffer(self):
        if not self.started:
            return
        pollresult = self.subproc.poll()
        if pollresult!=None:
            self.retcode = pollresult
        while True:
            try:
                line = self.stdout_queue.get_nowait()
            except Empty:
                break
            if (len(line)>0 and line[-1]=='\n'):
                line = line[:-1]
            self.outbuffer.append(line)
    
    def terminate(self):
        if not self.started:
            return
        os.killpg(os.getpgid(self.subproc.pid), signal.SIGTERM)
        self.started = False
    
    def kill(self):
        if not self.started:
            return
        os.killpg(os.getpgid(self.subproc.pid), signal.SIGKILL)
        self.started = False
    
    def terminated(self):
        return self.retcode!=None
    
    def running(self):
        return self.started and not self.terminated()
        
    def return_code(self):
        return self.retcode
    
    def get_output(self):
        if not self.started:
            return
        self._update_out_buffer()
        return self.outbuffer.get()
    
    def send(self, input_data):
        if not self.started:
            return
        stdoutdata, stderrdata = self.subproc.communicate(input_data)
        pollresult = self.subproc.poll()
        if pollresult!=None:
            self.retcode = pollresult
            return
        lines = stdoutdata.split('\n')
        for l in lines:
            self.outbuffer.append(l)

    def _enqueue_stdout(self, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line.decode("utf-8"))
        out.close()