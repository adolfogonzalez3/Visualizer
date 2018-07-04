
import numpy as np
from collections import deque

from PygameVisualizer.PygameBackend import PygameBackend
from multiprocessing import Process, Pipe
from imageio import imwrite, mimwrite



def run_task(pipe, width, height):
    visualizer = PygameBackend(width, height)
    while True:
        if pipe.poll(1.0):
            array = pipe.recv()
            visualizer.array_blit(array)
        visualizer.clear()

class PygameVisualizer(object):
    def __init__(self, width=512, height=512, buffer=None):
        self.buffer = deque(maxlen=buffer)
        
        self.width = width
        self.height = height

        self.pipe = None
        self.process = None
        
    def open(self):
        mine, yours = Pipe()
        self.pipe = mine
        self.process = Process(target=run_task, args=(yours, self.width, self.height), daemon=True)
        self.process.start()
        return self
        
    def blit(self, array):
        if np.any(array < 0) or np.any(255 < array):
            raise ValueError('Array values should be between 0 and 255, inclusively.')
            
        array = array.astype(np.uint8)
        self.pipe.send(array)
        self.buffer.append(array)
        
    def save(self, filename, N=None):
        '''Save an image or sequence of images from images stored in buffer.'''
        if N is None:
            imwrite(filename, self.images[-1])
        elif self.buffer < N or N < 0:
            raise RuntimeError(('N must be either None or a value between ,'
                                '1 and buffer({!s})').format(self.buffer))
        else:
            mimwrite(filename, self.images[-N:])
        
        
    def close(self):
        self.process.terminate()