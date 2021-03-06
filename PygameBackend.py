
import pygame

class PygameBackend(object):
    def __init__(self, width=512, height=512):
        pygame.init()
        self.dims = width, height
        self.screen = pygame.display.set_mode((width, height))
        
    def array_blit(self, array, position=(0, 0)):
        surface = pygame.surfarray.make_surface(array)
        scaled_surface = pygame.transform.scale(surface, self.dims)
        self.screen.blit(scaled_surface, position)
        pygame.display.update()
        
    def clear(self):
        pygame.event.clear()
        
    
    