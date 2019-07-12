'''Send HTTP requests to DEEPi'''

import time
import requests

__PORT = 5000

def get_status(addr,port):
    '''Standard GET request will return status as JSON'''
    r = requests.get('http://{}:{}/status'.format(addr,port))
    return r.json()
    
def send_command(cmd, addr, port=__PORT):
    url = 'http://{}:{}/cmd'.format(addr,port)
    payload = {'cmd':cmd}
    r = requests.post(url, json=payload)
    if r.status_code != 200:
        print("ERROR: {}".format(r.status_code))
    else:
        return r.json()

def command_prompt( addr, port=__PORT ):
    '''Open a simplified command prop to send commands'''
    print("Welcome to the DEEPi command line interface")
    print("Currently configured for {}:{}".format(addr,port))
    # TODO: impliment some kind of help menu
    # TODO: impliment a way to change ADDR or scan for DEEPi on network
    while True:
        command = input("> ")

        if command == 'exit()':
            break

        response = send_command(command, addr, port)
        print()
        print()
        print("Rcvd from {}:{}".format(addr,port))
        print(response)
        print()

def sync_time( addr, port=__PORT):
    '''Send current time to pi and tell it to sync itself'''
    # TODO: impliment a more accurate time sync
    cmd = 'set_time("{}")'.format(time.asctime())
    send_command( cmd, addr, port )


if __name__=='__main__':
    addr, port = "192.168.0.3", __PORT
    sync_time(addr,port)
    command_prompt(addr, port)

    

                      
