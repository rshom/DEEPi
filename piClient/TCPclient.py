import socket
import sys

def send_command(command, HOST, PORT=3000):
    '''Send command to a paticular DEEPi'''
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((HOST,PORT))
        sock.sendall(bytes(command, "utf-8"))
        
        response = sock.recv(1024)
        
        return response.decode("utf-8")

    except ConnectionRefusedError as err:
        return err

    except:
        print("Unexpected Error!: Check logs.")
        raise

    finally:
        sock.close()


# TODO: send command to all

def command_prompt( HOST, PORT=3000 ):
    print("Welcome to the DEEPi command line interface")
    print("Currently configured for {}:{}".format(HOST,PORT))
    # TODO: impliment some kind of help menu
    # TODO: impliment a way to change IP or scan for DEEPi on network
    while True:
        command = input("> ")

        if command == 'exit()':
            break

        response = send_command(command, HOST, PORT)
        print("Rcvd from {}:{}".format(HOST,PORT))
        print(response)

if __name__=='__main__':
    HOST, PORT = "localhost", 3000

    command_prompt(HOST, PORT)
