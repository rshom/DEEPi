#! /bin/usr/env python3

'''
Network connections to DeePi
'''

import numpy as np
import io
import socket
import struct
from PIL import Image
import cv2

pi_server = "0.0.0.0"
port = 1234

pi = socket.socket()
pi.bind( (pi_server, port) )
pi.listen(0)
# ???: why 0

connection = pi.accept()[0].makefile('rb')

def pull_stream():
    while True:
        image_len = struct.unpack(
            '<L', connection.read(struct.calcsize('<L'))
        )[0]
        # ???: wat

        if not image_len:
            break
        
        image_stream = io.BytesIO()
        image_stream.write( connection.read(image_len))
        
        image_stream.seek(0)
        image = Image.open(image_stream)
        #print('Image is {0}x{0}'.format( image.size ))
        #image.verify()
        #print('Image is verified')
        cv_image = np.array(image)
        yield cv_image
        
if __name__=='__main__':
    try:
        image_stream = pull_stream()
        while True:
            cv_image = next(image_stream)
            cv2.imshow('Stream', cv_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    finally:
        connection.close()
        pi.close()

