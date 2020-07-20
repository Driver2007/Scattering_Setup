#!/usr/bin/env python
# -*- coding:utf-8 -*-


# ############################################################################
#  license :
# ============================================================================
#
#  File :        Keithley6485.py
#
#  Project :     Keithley 6485 Picoammeter
#
# This file is part of Tango device class.
# 
# Tango is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Tango is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Tango.  If not, see <http://www.gnu.org/licenses/>.
# 
#
#  $Author :      tnunez$
#
#  $Revision :    $
#
#  $Date :        $
#
#  $HeadUrl :     $
# ============================================================================
#            This file is generated by POGO
#     (Program Obviously used to Generate tango Object)
# ############################################################################

__all__ = ["Keithley6485", "Keithley6485Class", "main"]

__docformat__ = 'restructuredtext'

import PyTango
import sys
# Add additional import
#----- PROTECTED REGION ID(Keithley6485.additionnal_import) ENABLED START -----#

import os
import serial
import time
import threading
import pdb
#----- PROTECTED REGION END -----#	//	Keithley6485.additionnal_import

# Device States Description
# ON : 
# FAULT : 


class Keithley6485 (PyTango.Device_4Impl):
    """Class for controlling the Keithley Picoammeter Model 6485 via socket interface"""
    
    # -------- Add you global variables here --------------------------
    #----- PROTECTED REGION ID(Keithley6485.global_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	Keithley6485.global_variables

    def __init__(self, cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.debug_stream("In __init__()")
        Keithley6485.init_device(self)
        #----- PROTECTED REGION ID(Keithley6485.__init__) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Keithley6485.__init__
        
    def delete_device(self):
        self.debug_stream("In delete_device()")
        #----- PROTECTED REGION ID(Keithley6485.delete_device) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Keithley6485.delete_device

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        self.attr_Current_read = 0.0
        #----- PROTECTED REGION ID(Keithley6485.init_device) ENABLED START -----#
        #pdb.set_trace()
        self.start_measure=False
        try:
            self.keithley = serial.Serial(self.serial_port,baudrate=38400,timeout=0.1)
            self.set_state(PyTango.DevState.ON)
        except:
            self.set_state(PyTango.DevState.FAULT)
        if not 'measure' in dir(self):
            self.measure = threading.Thread(target=self.measure_loop)
            self.measure.setDaemon(True)
            self.measure.start() 
            
        #----- PROTECTED REGION END -----#	//	Keithley6485.init_device

    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")
        #----- PROTECTED REGION ID(Keithley6485.always_executed_hook) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Keithley6485.always_executed_hook

    # -------------------------------------------------------------------------
    #    Keithley6485 read/write attribute methods
    # -------------------------------------------------------------------------
    
    def read_Current(self, attr):
        self.debug_stream("In read_Current()")
        #----- PROTECTED REGION ID(Keithley6485.Current_read) ENABLED START -----#
        
        attr.set_value(self.attr_Current_read)
        
        #----- PROTECTED REGION END -----#	//	Keithley6485.Current_read
        
    def write_ZeroCheck(self, attr):
        self.debug_stream("In write_ZeroCheck()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Keithley6485.ZeroCheck_write) ENABLED START -----#

        cmd = "SYST:ZCH " + str(data)
        
        self.write(cmd)

        #----- PROTECTED REGION ID(Keithley6485.ZeroCheck_write) ENABLED START -----#
        
    def read_ZeroCorrect(self, attr):
        self.debug_stream("In read_ZeroCorrect()")
        #----- PROTECTED REGION ID(Keithley6485.ZeroCorrect_read) ENABLED START -----#
        
        answer = self.write_read("SYST:ZCOR?")
        self.attr_ZeroCorrect_read = int(answer)
        
        attr.set_value(self.attr_ZeroCorrect_read)
        
        #----- PROTECTED REGION END -----#	//	Keithley6485.ZeroCorrect_read
        
    def write_start_measure(self, attr):
        self.debug_stream("In write_start_measure()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Keithley6485.start_measure_write) ENABLED START -----#
        self.start_measure=data
        #----- PROTECTED REGION END -----#	//	Keithley6485.start_measure_write
        
    
    
            
    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")
        #----- PROTECTED REGION ID(Keithley6485.read_attr_hardware) ENABLED START -----#
    
    
    def measure_loop(self):
        while True:
            if self.start_measure==True:
                self.write("INIT")
                time.sleep(0.5)
                self.write("ABOR")
                time.sleep(0.1)
                answer=self.write_read("DATA?")
                try:
                    answer = answer.split(',')[0].replace("A", "")
                    self.attr_Current_read = round(float(answer)*10**9,4)
                except:
                    pass
                print (answer)
            time.sleep(0.1)
            
    def write(self, data):
        self.keithley.write(("%s\n" % data).encode())

    def write_read(self, data):
        self.keithley.write(("%s\n" % data).encode())
        time.sleep(0.1)
        response = self.keithley.readline()
        #print (response)
        # only the end character is sometimes not read at first try
        #if hex(ord(response[len(response)-1])) != hex(10):
        #    tmp = self.keithley.readline()
        return response
        
        
        #----- PROTECTED REGION END -----#	//	Keithley6485.read_attr_hardware


    # -------------------------------------------------------------------------
    #    Keithley6485 command methods
    # -------------------------------------------------------------------------
    

    #----- PROTECTED REGION ID(Keithley6485.programmer_methods) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	Keithley6485.programmer_methods

class Keithley6485Class(PyTango.DeviceClass):
    # -------- Add you global class variables here --------------------------
    #----- PROTECTED REGION ID(Keithley6485.global_class_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	Keithley6485.global_class_variables


    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        'serial_port':
            [PyTango.DevString, 
            "Ip Adress of the terminal server",
            [] ],
        }


    #    Command definitions
    cmd_list = {
        }


    #    Attribute definitions
    attr_list = {
        'Current':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ],
            {
                'unit': "nA",
                'format': "%e",
            } ],
        'ZeroCheck':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'max value': "1",
                'min value': "0",
                'description': "0 -> disable, 1 -> enable",
            } ],
        'start_measure':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.WRITE]],
        }


def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(Keithley6485Class, Keithley6485, 'Keithley6485')
        #----- PROTECTED REGION ID(Keithley6485.add_classes) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Keithley6485.add_classes

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed as e:
        print ('-------> Received a DevFailed exception:', e)
    except Exception as e:
        print ('-------> An unforeseen exception occured....', e)

if __name__ == '__main__':
    main()