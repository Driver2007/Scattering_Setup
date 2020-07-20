from Process import ProcessConfig
from NetworkHost import NetworkHost

p_tdc = ProcessConfig(
    name       = "tdc",
    startcmds  = ["unbuffer ./launch_tdc"],
    wdir       = "/home/user/build/TangoServers/TDC",
    startuplvl = 0,
    outlines   = 200,
    stdin_pipe = False,
    envdict    = {}
)
 
p_iseg = ProcessConfig(
    name       = "ISEG",
    startcmds  = ["unbuffer ./launch_iseg"],
    wdir       = "/home/user/build/TangoServers/KMicLensLogic",
    startuplvl = 0,
    outlines   = 200,
    stdin_pipe = False,
    envdict    = {}
)
p_hel = ProcessConfig(
    name       = "Helicity",
    startcmds  = ["unbuffer ./launch_hel"],
    wdir       = "/home/user/build/TangoServers/Helicity",
    startuplvl = 0,
    outlines   = 200,
    stdin_pipe = False,
    envdict    = {}
)

p_keithley = ProcessConfig(
    name       = "keithley",
    startcmds  = ["unbuffer ./launch_Keithley"],
    wdir       = "/home/user/build/TangoServers/Keithley",
    startuplvl = 0,
    outlines   = 200,
    stdin_pipe = False,
    envdict    = {}
)


host_pic884          = NetworkHost(host='192.168.3.110', label="Hexapod Motor Controller")
host_hvps     = NetworkHost(host='192.168.3.109', label="HV Power Supply")
host_fug             = NetworkHost(host='192.168.3.120', label="FuG Netzteil 30kV")
host_multimodcrate = NetworkHost(host='192.168.3.130', label="Multimodule Crate")
#host_crate_hv_cs_dac = NetworkHost(host='192.168.3.160', label="Deflektor- & MCP-Module")

#MetisProcesses = [p_epicspic884, p_smaractmcs, p_smaractmcs_presets, p_fug, p_hv, p_currentsrc, p_dac, p_kmiclens, p_tdc]
MetisProcesses = [p_tdc,p_iseg,p_hel,p_keithley]
#MetisHosts = [host_pic884, host_multimodcrate, host_fug]
MetisHosts = [host_pic884]
