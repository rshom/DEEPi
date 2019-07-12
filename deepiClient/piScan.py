import concurrent.futures
import ipaddress
import socket
import sys
import TCPclient

import RESTclient

__PORT = 3000

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_subnet(IP=get_ip()):
    iface = ipaddress.IPv4Interface('{}/255.255.255.0'.format(IP))
    return iface.network

def tcp_check(addr, port=__PORT):
    '''Check to see if connection is available on a address'''
    '''
    socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    socket.setdefaulttimeout(1) 
    result = socket_obj.connect_ex( (addr,port) )
    socket_obj.close()
    '''
    try:
        result = TCPclient.send_command('status()',addr,port)
        return True
    except:
        return False

def rest_check(addr,port):
    '''Check for a DEEPi REST server on address'''
    try:
        result = RESTclient.get_status(addr,port)
        return True
    except:
        return False


def scan_net(subnet, server_style='REST', port=__PORT):
    '''Check subnet for possible connections'''
    # TODO: impliment some kind of test to ensure the pi is operational
    ipSet = set()
    
    if server_style=='REST':
        cmd = rest_check
        port = 3000
    elif server_style=='TCP':
        cmd = tcp_check
        port = 3000
    else:
        print("Incorrect server type")

    with concurrent.futures.ThreadPoolExecutor(max_workers=255) as executor:
        future_to_host = {executor.submit(cmd, str(host), port): host for host in subnet.hosts()}
        for future in concurrent.futures.as_completed(future_to_host):
            host = future_to_host[future]
            #result = check_addr(str(host),port)
            result = future.result()
            if result:
                ipSet.add(host)
    '''
    for host in subnet.hosts():
        result = rest_check(host,port)
        print('{}: {}'.format(host,result))
        ipSet.add(host)
    '''
    return ipSet


def piScan():
    IP = get_ip()
    print("Client IP: {}".format(IP))
    subnet = get_subnet(IP)
    print("subnet")
    ipSet = scan_net(subnet)
    print("DEEPi IPs:")
    if not bool(ipSet):
        print("No DEEPi's found! Check configuration")
        
    '''
    for ip in ipSet:
        RESTclient.sync_time(IP,5000)
    '''
    return ipSet
