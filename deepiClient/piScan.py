import concurrent.futures
import ipaddress
import socket
import sys

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

def check_addr(addr, port=__PORT):
    '''Check to see if connection is available on a address'''
    socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    socket.setdefaulttimeout(1) 
    result = socket_obj.connect_ex( (addr,port) )
    socket_obj.close()
    return result

def get_subnet(IP):
    iface = ipaddress.IPv4Interface('{}/255.255.255.0'.format(IP))
    return iface.network

def scan_network(subnet, port=__PORT):
    '''Check subnet for possible connections'''
    # TODO: impliment some kind of test to ensure the pi is operational
    ipSet = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_host = {executor.submit(check_addr, str(host), port): host for host in subnet.hosts()}
        for future in concurrent.futures.as_completed(future_to_host):
            host = future_to_host[future]
            #result = check_addr(str(host),port)
            result = future.result()
            if result == '111':
                ipSet.add(host)
    return ipSet


if __name__=='__main__':
    IP = get_ip()
    print("Client IP: {}".format(IP))
    subnet = get_subnet(IP)
    ipSet = scan_network(subnet)
    print("DEEPi IPs:")
    if not bool(ipSet):
        print("No DEEPi's found! Check configuration")
        
    for ip in ipSet:
        print(ip)
