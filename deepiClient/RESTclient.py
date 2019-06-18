'''Send HTTP requests to DEEPi'''

import requests

__IP = '127.0.0.1'
__PORT = 5000

__BASE_URL = 'http://{}:{}'.format(__IP,__PORT)

def get_status(ip,port):
    '''Standard GET request will return status as JSON'''
    r = requests.get('http://{}:{}/status'.format(ip,port))
    return r.json()
    
    
def send_command(cmd, ip=__IP, port=__PORT):
    url = 'http://{}:{}/cmd'.format(ip,port)
    payload = {'cmd':cmd}
    print(payload)
    print(url)
    r = requests.post(url, json=payload)
    print(r.text)
    if r.status_code != 200:
        print("ERROR: {}".format(r.status_code))
    else:
        return r.json()

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

if __name__=='__main__':
    addr, port = "192.168.0.3", __PORT
              
    command_prompt(addr, port)

    

                      
