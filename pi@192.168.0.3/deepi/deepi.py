#! /usr/bin/env python3
'''
PiCamera implementation for deep sea applications

This is a test.
'''

# TODO: impliment logging as necessary

import io
import os
import threading
import socket
import datetime

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


    def stream_live(self, broadcast='0.0.0.0', port=3141):
        '''Continuous capture and send stream'''

        # TODO: finish implimentation of live stream <>

        # set up socket using TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # TODO: change to UDP socket <>
        client_socket.connect(( broadcast, port ))
        connection = client_socket.makefile('wb')

        try:
            # ???: learn about thread locks <>
            connection_lock = threading.Lock()
            # ???: What is the pool lock and pool list for?
            pool_lock = threading.Lock()
            pool = []

            class StreamerThread( threading.Thread ):

                def __init__( self ):
                    super().__init__()
                    self.stream = io.BytesIO()
                    self.event = threading.Event()
                    #???: learn more about threading<>
                    self.terminated = False
                    # define the socket and get it ready here
                    self.start()
                    
                def run( self ):
                    # This runs in a background thread
                    while not self.terminated:
                        # Wait for image to be written to the stream
                        if self.event.wait(1):
                        #???: what is the wait <>
                            try:
                                with connection_lock:
                                    connection.write(struct.pack('<L',self.stream.tell() ))
                                    # ???: not sure about this line
                                    connection.flush()
                                    self.stream.seek(0)
                                    connection.write( self.stream.read() )
                            finally:
                                # ???: what happens in this finally block
                                self.stream.seek(0)
                                self.stream.truncate()
                                self.event.clear()
                                with pool_lock:
                                    pool.append(self)
                        
                

        self.streamer = StreamerThread()



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
                
