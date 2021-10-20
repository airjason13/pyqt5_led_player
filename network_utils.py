import netifaces
from socket import *
from global_def import *
import platform

def get_routingGateway():
    try:
        routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
    except:
        return None
    return routingGateway
def get_routingNicName():
    try:
        routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]
    except:
        return None
    return routingNicName

def get_routingIPAddr():
    routingIPAddr = ""
    for interface in netifaces.interfaces():
        if interface == get_routingNicName():
            # print netifaces.ifaddresses(interface)
            routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            try:
                routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                # TODO(Guodong Ding) Note: On Windows, netmask maybe give a wrong result in 'netifaces' module.
                routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
            except KeyError:
                return None
                #pass
    if routingIPAddr is not None:
        print("routingIPAddr:", routingIPAddr)

    return routingIPAddr

def send_broadcast(socket, data, bc_port=broadcast_port):
    socket.sendto(data, ('<broadcast>', bc_port))

def is_interface_up(interface):
    addr = netifaces.ifaddresses(interface)
    return netifaces.AF_INET in addr

def get_wireless_interface():
    wireless_interface = ""

    if platform.processor().startswith("x86_64") is True:
        #print("x86_64 ")
        wireless_interface = "wlp3s0"
    else:
        #print("platform processor: ", platform.processor())
        wireless_interface = "wlan0"


    return wireless_interface