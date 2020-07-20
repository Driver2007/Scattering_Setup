"""This module contains drivers for the following equipment from FUG:

* MCP 140-1250. Voltage supply
"""

import time
import serial

# Code translations constants
Error_codes = {
    'E0': 'No error, standard response on each command',
    'E1': 'no data available, Customer tried to read data from GPIB but there were no data prepared. (IBIG50 sent command ~T2 to ADDA)',
    'E2': 'unknown register type, No valid register type after >',
    'E4': 'invalid argument, The argument of the command was rejected. i.e. malformed number',
    'E5': 'argument out of range, i.e. setvalue higher than type value',
    'E6': 'register is read only, Some registers can only be read but not written to. (i.e. monitor registers)',
    'E7': 'Receive Overflow, Command string was longer than 50 characters.',
    'E8': 'EEPROM is write protected, Write attempt to calibration data while the write protection switch was set to write protected.',
    'E9': 'address error, A non addressed command was sent to ADDA while it was in addressable mode (and vice versa).',
    'E10': 'unknown SCPI command, This SCPI command is not implemented',
    'E11': 'not allowed Trigger-on-Talk, Not allowed attempt to Trigger-on-Talk (~T1) while ADDA was in addressable mode.',
    'E12': 'invalid argument in ~Tn command, Only ~T1 and ~T2 is implemented.',
    'E13': 'invalid N-value, Register >K8 contained an invalid value. Error code is output on an attempt to query data with ? or ~T1',
    'E14': 'register is write only, Some registers can only be write to (i.e. >H0)',
    'E15': 'string too long, i.e. serial number string too long during calibration',
    'E16': 'wrong checksum, checksum over command string was not correct, refer also to 3.4'
}


class MCP(object):

    """
    :var ETX: End text (Ctrl-c), chr(3), \\x15
    :var CR: Carriage return, chr(13), \\r
    :var LF: Line feed, chr(10), \\n
    :var ENQ: Enquiry, chr(5), \\x05
    :var ACK: Acknowledge, chr(6), \\x06
    :var NAK: Negative acknowledge, chr(21), \\x15
    """

    ETX = chr(3)  # \x03
    CR = chr(13)
    LF = chr(10)
    ENQ = chr(5)  # \x05
    ACK = chr(6)  # \x06
    NAK = chr(21)  # \x15

    def __init__(self, port, baudrate=9600):
        """Initialize internal variables and serial connection

        :param port: The COM port to open. See the documentation for
            `pyserial <http://pyserial.sourceforge.net/>`_ for an explanation
            of the possible value. The default value is '/dev/ttyUSB0'.
        :type port: str or int
        :param baudrate: 9600, 19200, 38400 where 9600 is the default
        :type baudrate: int
        """
        # The serial connection should be setup with the following parameters:
        # 1 start bit, 8 data bits, No parity bit, 1 stop bit, no hardware
        # handshake. These are all default for Serial and therefore not input
        # below
        self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        
    def serial_close(self):
        serial.close()
        

    def _cr_lf(self, string):
        """Pad carriage return and line feed to a string

        :param string: String to pad
        :type string: str
        :returns: the padded string
        :rtype: str
        """
        return string + self.CR + self.LF

    def _send_command(self, command):
        """Send a command and check if it is positively acknowledged

        :param command: The command to send
        :type command: str
        :raises IOError: if the negative acknowledged or a unknown response
            is returned
        """
        self.serial.write(self._cr_lf(command))

    def _get_data(self):
        """Get the data that is ready on the device

        :returns: the raw data
        :rtype:str
        """
        #self.serial.write(self.ENQ)
        data = self.serial.readline()
        return data.rstrip(self.LF).rstrip(self.CR)

    def check_test(self):
        """Return Manufacturer, Type and Serial number of the unit"""
        self._send_command('>CFN ?')
        return self._get_data()

    def set_output_on(self):

        self._send_command("OUTPut ON")
    def set_output_off(self):

        self._send_command("OUTPut OFF")
    def set_remote_on(self):

        self._send_command("POWer:STAGe:AFTer:REMote ON")
    def set_remote_off(self):

        self._send_command("REMote OFF")

    def ask_array(self):

        self._send_command("MEAS:ARR?")
        response=self._get_data()
        return response

    def set_voltage_fil(self, value):

        self._send_command("VOLT "+str(value))

class FUG_MCP(MCP):
    """Driver for the TPG 261 dual channel measurement and control unit"""

    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        """Initialize internal variables and serial connection

        :param port: The COM port to open. See the documentation for
            `pyserial <http://pyserial.sourceforge.net/>`_ for an explanation
            of the possible value. The default value is '/dev/ttyUSB0'.
        :type port: str or int
        :param baudrate: 9600, 19200, 38400 where 9600 is the default
        :type baudrate: int
        """
        super(FUG_MCP, self).__init__(port=port, baudrate=baudrate)
