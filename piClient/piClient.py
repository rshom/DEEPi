'''
Network connections to DeePi
'''

import numpy as np
import io
import socket
import struct
from PIL import Image
import cv2

class CamStream:

    def __init__(self, pi_addr, port):
        self.pi = socket.socket()
        self.pi.bind( (pi_addr, port) )
        self.pi.listen(0)
        self.port = port
        # ???: why 0

        self.connection = self.pi.accept()[0].makefile('rb')

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()
        self.pi.close()        

    def pull_stream(self):

        while True:
            image_len = struct.unpack(
                '<L', self.connection.read(struct.calcsize('<L'))
            )[0]
            # ???: wat
            
            if not image_len:
                break
            
            image_stream = io.BytesIO()
            image_stream.write( self.connection.read(image_len))
            
            image_stream.seek(0)
            image = Image.open(image_stream)
            #print('Image is {0}x{0}'.format( image.size ))
            #image.verify()
            #print('Image is verified')
            cv_image = np.array(image)
            yield cv_image
        
def catch_stream( port ):
    '''Live stream from a single camera'''
    with CamStream('0.0.0.0',port) as cam:
        image_stream = cam.pull_stream()
        while True:
            try:
                cv_image = next(image_stream)
                cv2.imshow('{}'.format(cam.port), cv_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except:
                break
            

def stereo_stream( portLeft, portRight ):
    '''Stream images together'''
    with CamStream('0.0.0.0', portLeft) as camLeft, CamStream('0.0.0.0', portRight) as camRight:
        streamLeft = camLeft.pull_stream()
        streamRight = camRight.pull_stream()
        while True:
            try:
                imageRight = next(streamRight)
                imageLeft = next(streamLeft)
                cv_image = np.concatenate( (imageLeft, imageRight), axis=1 )
                #cv_image = cv2.cvtColor(imageLeft, cv2.COLOR_BGR2GRAY) - cv2.cvtColor(imageRight, cv2.COLOR_BGR2GRAY)
                cv2.imshow('Stereo Stream', cv_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except:
                break
    
    
if __name__=='__main__':
    #stereo_stream( 1235,1234 )
    catch_stream( 1234 )
