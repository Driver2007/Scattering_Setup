#!/usr/bin/env python
# -*- coding:utf-8 -*-


# ############################################################################
#  license :
# ============================================================================
#
#  File :        Quadrupole.py
#
#  Project :     Photocathode
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
#  $Author :      sergey.v.babenkov$
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

__all__ = ["Quadrupole", "QuadrupoleClass", "main"]

__docformat__ = 'restructuredtext'

import PyTango
import sys
# Add additional import
#----- PROTECTED REGION ID(Quadrupole.additionnal_import) ENABLED START -----#
import time
import threading
#----- PROTECTED REGION END -----#	//	Quadrupole.additionnal_import

# Device States Description
# No states for this device


class Quadrupole (PyTango.Device_4Impl):
    """Photocathode"""
    
    # -------- Add you global variables here --------------------------
    #----- PROTECTED REGION ID(Quadrupole.global_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	Quadrupole.global_variables

    def __init__(self, cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.debug_stream("In __init__()")
        Quadrupole.init_device(self)
        #----- PROTECTED REGION ID(Quadrupole.__init__) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Quadrupole.__init__
        
    def delete_device(self):
        self.debug_stream("In delete_device()")
        #----- PROTECTED REGION ID(Quadrupole.delete_device) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Quadrupole.delete_device

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        self.attr_X_Gate_read_read = 0.0
        self.attr_Y_Gate_read_read = 0.0
        self.attr_X_Transfer_read_read = 0.0
        self.attr_Y_Transfer_read_read = 0.0
        #----- PROTECTED REGION ID(Quadrupole.init_device) ENABLED START -----#
        
        
        if not 'pingthread' in dir(self):
            self.pingthread = threading.Thread(target=self.check_voltages)
            self.pingthread.setDaemon(True)
            self.pingthread.start()
        #----- PROTECTED REGION END -----#	//	Quadrupole.init_device

    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")
        #----- PROTECTED REGION ID(Quadrupole.always_executed_hook) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Quadrupole.always_executed_hook

    # -------------------------------------------------------------------------
    #    Quadrupole read/write attribute methods
    # -------------------------------------------------------------------------
    
    def write_X_Gate(self, attr):
        self.debug_stream("In write_X_Gate()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Quadrupole.X_Gate_write) ENABLED START -----#
        self.attr_X_Gate_read_read=data
        #----- PROTECTED REGION END -----#	//	Quadrupole.X_Gate_write
        
    def read_X_Gate_read(self, attr):
        self.debug_stream("In read_X_Gate_read()")
        #----- PROTECTED REGION ID(Quadrupole.X_Gate_read_read) ENABLED START -----#
        attr.set_value(self.attr_X_Gate_read_read)
        
        #----- PROTECTED REGION END -----#	//	Quadrupole.X_Gate_read_read
        
    def write_Y_Gate(self, attr):
        self.debug_stream("In write_Y_Gate()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Quadrupole.Y_Gate_write) ENABLED START -----#
        self.attr_Y_Gate_read_read=data
        #----- PROTECTED REGION END -----#	//	Quadrupole.Y_Gate_write
        
    def read_Y_Gate_read(self, attr):
        self.debug_stream("In read_Y_Gate_read()")
        #----- PROTECTED REGION ID(Quadrupole.Y_Gate_read_read) ENABLED START -----#
        attr.set_value(self.attr_Y_Gate_read_read)
        
        #----- PROTECTED REGION END -----#	//	Quadrupole.Y_Gate_read_read
        
    def write_X_Transfer(self, attr):
        self.debug_stream("In write_X_Transfer()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Quadrupole.X_Transfer_write) ENABLED START -----#
        self.attr_X_Transfer_read_read=data
        #----- PROTECTED REGION END -----#	//	Quadrupole.X_Transfer_write
        
    def read_X_Transfer_read(self, attr):
        self.debug_stream("In read_X_Transfer_read()")
        #----- PROTECTED REGION ID(Quadrupole.X_Transfer_read_read) ENABLED START -----#
        attr.set_value(self.attr_X_Transfer_read_read)
        
        #----- PROTECTED REGION END -----#	//	Quadrupole.X_Transfer_read_read
        
    def write_Y_Transfer(self, attr):
        self.debug_stream("In write_Y_Transfer()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Quadrupole.Y_Transfer_write) ENABLED START -----#
        self.attr_Y_Transfer_read_read=data
        #----- PROTECTED REGION END -----#	//	Quadrupole.Y_Transfer_write
        
    def read_Y_Transfer_read(self, attr):
        self.debug_stream("In read_Y_Transfer_read()")
        #----- PROTECTED REGION ID(Quadrupole.Y_Transfer_read_read) ENABLED START -----#
        attr.set_value(self.attr_Y_Transfer_read_read)
        
        #----- PROTECTED REGION END -----#	//	Quadrupole.Y_Transfer_read_read
        
    
    
            
    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")
        #----- PROTECTED REGION ID(Quadrupole.read_attr_hardware) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Quadrupole.read_attr_hardware


    # -------------------------------------------------------------------------
    #    Quadrupole command methods
    # -------------------------------------------------------------------------
    

    #----- PROTECTED REGION ID(Quadrupole.programmer_methods) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	Quadrupole.programmer_methods

class QuadrupoleClass(PyTango.DeviceClass):
    # -------- Add you global class variables here --------------------------
    #----- PROTECTED REGION ID(Quadrupole.global_class_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	Quadrupole.global_class_variables


    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        }


    #    Command definitions
    cmd_list = {
        }


    #    Attribute definitions
    attr_list = {
        'X_Gate':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'Memorized':"true"
            } ],
        'X_Gate_read':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ]],
        'Y_Gate':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'Memorized':"true"
            } ],
        'Y_Gate_read':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ]],
        'X_Transfer':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'Memorized':"true"
            } ],
        'X_Transfer_read':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ]],
        'Y_Transfer':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'Memorized':"true"
            } ],
        'Y_Transfer_read':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ]],
        }


def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(QuadrupoleClass, Quadrupole, 'Quadrupole')
        #----- PROTECTED REGION ID(Quadrupole.add_classes) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Quadrupole.add_classes

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed as e:
        print ('-------> Received a DevFailed exception:', e)
    except Exception as e:
        print ('-------> An unforeseen exception occured....', e)

if __name__ == '__main__':
    main()