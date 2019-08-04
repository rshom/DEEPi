'''PiCamera implementation for deep sea applications'''

#TODO: impliment logging as necessary

import io
import os
import threading
import socket
import datetime
import time
import struct

from picamera import PiCamera

class DEEPi(PiCamera):
    '''
    PiCamera implementation for deep sea applications.
    '''
    
    def __init__(self, diveFolder="./"):
        '''Initiate camera and lock resources'''
        PiCamera.__init__(self)
        self.diveFolder=diveFolder
        self.deployed=False
        self.last_access=0
        self.stream = None
        self.thread = None
        self.last_frame = None

    def close(self):
        '''Release all resources'''
        PiCamera.close(self)
        # TODO: check for threads and terminate/join them <>

    def update_frame(self):
        '''Continuous capture that saves the latest frame in memory.
        Any live stream applications will access this updating frame
        '''
        self.stream = io.BytesIO()
        print("starting capture")
        for _ in PiCamera.capture_continuous(self, self.stream, 'jpeg', use_video_port=True):
            #TODO: ensure splitter port and resolution are properly calibrated.
            self.stream.seek(0)
            self.last_frame =  self.stream.read()
            self.stream.seek(0)
            self.stream.truncate()
            #TODO: double check the stream stop and start process
            if ((time.time()-self.last_access)>10):
                print(time.time()-self.last_access)
                self.stream = None
                break

    def start_stream(self):
        '''Start and stop the threaded process for updating the live stream frame'''
        self.last_access=time.time()
        if self.thread is None:
            self.thread = threading.Thread(target=self.update_frame)
            self.thread.start()
        while self.last_frame is None:
            time.sleep(0)

    #TODO: impliment stop_stream

    def __enter__(self):
        '''Called whenever instance is opened using a with statement'''
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Close out anything necessary'''
        self.close()


