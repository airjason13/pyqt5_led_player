import netifaces
from socket import *
from global_def import *

def get_routingGateway():
    routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
    return routingGateway
def get_routingNicName():
    routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]
    return routingNicName

def get_routingIPAddr():
    for interface in netifaces.interfaces():
        if interface == get_routingNicName():
            # print netifaces.ifaddresses(interface)
            routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            try:
                routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                # TODO(Guodong Ding) Note: On Windows, netmask maybe give a wrong result in 'netifaces' module.
                routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
            except KeyError:
                pass

    print("routingIPAddr:", routingIPAddr)
    return routingIPAddr

def send_broadcast(socket, data, bc_port=broadcast_port):
    socket.sendto(data, ('<broadcast>', bc_port))