
from PygameVisualizer.PygameBackend import PygameBackend
from multiprocessing import Process, Pipe



def run_task(pipe, width, height):
    visualizer = PygameBackend(width, height)
    while True:
        if pipe.poll(1.0):
            array = pipe.recv()
            visualizer.array_blit(array)
        visualizer.clear()

class PygameVisualizer(object):
    def __init__(self, width=512, height=512):
        mine, yours = Pipe()
        self.pipe = mine
        self.process = Process(target=run_task, args=(yours, width, height), daemon=True)
        self.process.start()
        
    def blit(self, array):
        self.pipe.send(array)
        
    def close(self):
        self.process.terminate()