'''PiCamera implementation for deep sea applications'''

# TODO: impliment logging as necessary

import io
import os
import threading
import socket
import datetime
import time
import struct

from picamera import PiCamera as Camera



class DEEPi(Camera):
    '''
    PiCamera implementation for deep sea applications.
    '''

    def __init__(self):
        Camera.__init__(self)


    def close(self):
        '''Release all resources'''
        camera.close()
        # TODO: check for threads and terminate/join them <>


    def capture(self, output=None, use_video_port=True):
        '''Capture image using default settings and save to timestamp.

        See capture for more options
        '''
        if output=None:
            output = datetime.datetime.utcnow().isoformat()[:-7] + '.jpeg'
            
        Camera.capture( output, use_video_port=use_video_port)


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


    def __enter__(self):
        '''Called whenever instance is opened using a with statement'''
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Close out anything necessary'''
        self.close()


