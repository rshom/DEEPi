'''PiCamera implementation for deep sea applications'''

# TODO: impliment logging as necessary

import io
import os
import threading
import socket
import datetime
import time
import struct

from picamera import PiCamera


def genName():
    while True:
        timeStamp = datetime.datetime.utcnow().isoformat()
        yield timeStamp[:-7].replace('-','').replace(':','')


class DEEPi(PiCamera):
    '''
    PiCamera implementation for deep sea applications.
    '''

    def __init__(self, diveFolder="./"):
        PiCamera.__init__(self)
        self.diveFolder=diveFolder
        
        self.streaming=False
        self.deployed=False
        self.frame=None
        self.last_access=0

    def close(self):
        '''Release all resources'''
        PiCamera.close()
        # TODO: check for threads and terminate/join them <>

    def status(self):
        return {'closed':PiCamera.closed,
                'recording':PiCamera.recording,
                'streaming':bool(self.streaming),
                'deployed':self.deployed
                }

    def capture(self, output=next(genName()), use_video_port=True):
        '''Capture image using default settings and save to timestamp.
        See capture for more options
        '''

        PiCamera.capture( output+'.jpeg', use_video_port=use_video_port)


    def record_videos( self, vid_length=6000 ):
        '''Record and save split video files to dive folder'''

        class RecorderThread( threading.Thread ):

            def __init__(self):
                super().__init__()
                # TODO: set up to record
                self.start()

            def run(self):
                PiCamera.start_recording(next(genName)+'.h264')
                while PiCamera.recording==True:
                    PiCamera.wait_recording(vid_length)
                    PiCamera.split_recording(next(genName)+'.h264')


    def frames():
        stream = io.BytesIO()
        for _ in PiCamera.capture_continuous(stream, 'jpeg',
                                             use_video_port=True,
                                             resize=(720,480),
                                             splitter_port=3):
            stream.seek(0)
            self.frame = stream.read()
            yield
            self.event.set()
            stream.seek(0)
            stream.truncate()
            time.sleep(0)
            if time.time() - self.last_access > 10:
                break


            

    def stream(self):
        
        if self.streaming is None:
            self.last_access = time.time()
            self.streaming = threading.Thread(target=self.frames)
            self.streaming.start()
            

    def __enter__(self):
        '''Called whenever instance is opened using a with statement'''
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Close out anything necessary'''
        self.close()


