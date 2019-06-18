'''
Commands for DEEPi system
'''

#import deepi



threads = []

# TODO: impliment actual status dictionary
status = {"ip":'0.0.0.0',
          "port": 3000,
          "threads": threads
}

# TODO: update status function that checks actual status of camera at the end of everfunciton
# perhaps a decorator


# TODO: implement logging and threading here

# TODO: implement actual commands

def deploy():
    '''Run a customizable deployment script'''
    report = "Deploying"
    return report

def stream():
    '''Live stream video to the any client'''
    # TODO: impliment a UDP server to stream
    report = "Streaming"
    return report

def capture():
    '''Take a picture as soon as possible'''
    report = "Snapping pic"
    return report

def record( split_time=None ):
    '''Record and save video in chunks'''
    report = "Recording with splits every: {} seconds".format(split_time/1000)
    return report

def status():
    report = status
    return str(report)

def command_prompt():

    print("Welcome to the DEEPi command line interface")
    # TODO: impliment some kind of help menu

    while True:
        command = input("> ")
        if command == 'exit()':
            break
        try:
            report = eval(command)
            print(report)
        except:
            print("Invalid command")
            print()
            raise


if __name__=='__main__':
    command_prompt()
