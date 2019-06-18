'''
Custom server for sending requests to DEEPi system
'''

import socketserver
import controller

class RequestHandler(socketserver.BaseRequestHandler):
    '''
    Accept requests from piClient to perform pre-set commands
    '''

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        # TODO: impliment logging
        cmd = (self.data).decode("utf-8")

        print("{} wrote: {}".format(self.client_address[0], cmd))
        # TODO: send commands to handler that has dictionary of funcitons
        # TODO: log any commands recieved
        try:
            test = eval("controller.{}".format(cmd))
            self.request.sendall(bytes(test,"utf-8"))

        except AttributeError as err:
            # TODO: log the error here
            self.request.sendall(bytes("ERROR! No such command: {}".format(cmd),"utf-8"))

        # TODO: add more known exceptions

        except:
            # TODO: log the error here
            self.request.sendall(bytes("Unexpected error!","utf-8"))
            raise

def start_server( HOST, PORT):
    '''Starts the server to wait for commands'''
    # TODO: log start and finish
    server = socketserver.TCPServer((HOST,PORT), RequestHandler)
    server.serve_forever()

if __name__ == "__main__": 
    HOST, PORT = "0.0.0.0", 3000
    print("Starting server on {}:{}".format(HOST,PORT))
    try:
        start_server(HOST,PORT)
    except:
        raise
    finally:
        print("Closing")
