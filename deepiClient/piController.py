import socket
import sys

__PORT = 3000

def sync_time(addr, port=__PORT):
    # TODO: sync time function
    return

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

        if command

        response = send_command(command, addr, port)
        print("Rcvd from {}:{}".format(addr,port))
        print(response)


if __name__=='__main__':
    addr, port = "localhost", __PORT
              
    command_prompt(addr, port)
