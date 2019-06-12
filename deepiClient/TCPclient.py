import ipaddress
import socket
import sys
import concurrent.futures

__PORT = 3000


def send_command(command, addr, port=__PORT):
    '''Send command to a paticular DEEPi'''
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((addr,port))
        sock.sendall(bytes(command, "utf-8"))
        
        response = sock.recv(1024)
        
    except ConnectionRefusedError as err:
        return err

    except:
        print("Unexpected Error!: Check logs.")
        raise

    else:
        sock.close()
        return response.decode("utf-8")
    
    finally:
        sock.close()


# TODO: send command to all

def command_prompt( addr, port=__PORT ):
    '''Open a simplified command prop to send commands'''
    print("Welcome to the DEEPi command line interface")
    print("Currently configured for {}:{}".format(addr,port))
    # TODO: impliment some kind of help menu
    # TODO: impliment a way to change IP or scan for DEEPi on network
    while True:
        command = input("> ")

        if command == 'exit()':
            break

        response = send_command(command, addr, port)
        print("Rcvd from {}:{}".format(addr,port))
        print(response)

def check_addr(addr, port=__PORT):
    '''Check to see if connection is available on a address'''
    socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    socket.setdefaulttimeout(1) 
    result = socket_obj.connect_ex( (addr,port) )
    socket_obj.close()
    return result
    

def scan_network(mask='192.168.0.0/24', port=__PORT):
    '''Check subnet for possible connections'''
    # TODO: impliment some kind of test to ensure the pi is operational
    subnet = ipaddress.ip_network(mask)
    ipSet = set()
    import time
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_host = {executor.submit(check_addr, str(host), port): host for host in subnet.hosts()}
        for future in concurrent.futures.as_completed(future_to_host):
            host = future_to_host[future]
            print("Checking {}:{}".format(host, port))
            #result = check_addr(str(host),port)
            result = future.result()
            if result == '111':
                ipSet.add(host)
            print("{}:{}".format(host,result))
    print(ipSet)
    print(time.time()-start)
    return ipSet

def sync_time(addr, port=__PORT):
    # TODO: sync time function
    return
        


if __name__=='__main__':
    addr, port = "localhost", __PORT
              
    command_prompt(addr, port)
