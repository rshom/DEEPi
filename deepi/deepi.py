#! /usr/bin/env python3

'''
PiCamera implementation for deep sea applications
'''

# TODO: impliment logging as necessary

import io
import os
import threading
import socket
import datetime
import time
import struct

import picamera

class DeePi( picamera.PiCamera ):
    '''
    PiCamera implementation for deep sea applications.
    '''
    def __init__(self):
        super().__init__()
        #TODO: set up socket looking for command from topside <>
        
        # set up a dive folder to save all dive files in
        diveDtg = datetime.datetime.utcnow().isoformat()
        self.divefolder = '/home/pi/{}/'.format( diveDtg[:-10].replace('-','').replace(':','') )
        try:
            os.mkdir( self.divefolder )
            #TODO: first check if it exists <>
        except:
            print("Unable to create dive folder: using current directory instead")
            #TODO: log error correctly <>
            self.divefolder = ''


        # TODO: add a command accepter thread <>


    def __enter__(self):
        '''Called whenever instance is opened using a with statement'''
        pass


    def __exit__(self):
        self.close()


    def close(self):
        '''Release all resources'''
        super().close()
        # TODO: check for threads and terminate/join them <>


    def stream_live(self, broadcast='192.168.0.100', port=1234):
        '''Continuous capture and send stream'''

        client = socket.socket()
        client.connect( (broadcast, port) )

        connection = client.makefile('wb')

        try:
            self.resolution = (640, 480)
            start = time.time()
            stream = io.BytesIO()
            for _ in self.capture_continuous(stream, 'jpeg'):
                connection.write(struct.pack('<L', stream.tell()))
                # ???: wat
                connection.flush()
                stream.seek(0)
                connection.write(stream.read())
                # ???: wat

                if time.time()-start > 30:
                    break

                stream.seek(0)
                stream.truncate()

            connection.write(struct.pack('<L', 0))

        finally:
            connection.close()
            client.close()


    def capture_image(self):
        '''Capture image using default settings and save to timestamp. See capture for more options'''

        filename = self.divefolder + datetime.datetime.utcnow().isoformat()[:-7] + '.jpeg'
        super().capture( filename, use_video_port=True)

    def record_videos( self, vid_length=6000 ):
        '''Record and save split video files to dive folder'''

        class RecorderThread( threading.Thread ):

            def __init__(self):
                super().__init__()
                # TODO: set up to record
                self.start()

            def run(self):
                # TODO: record to disk
                pass

