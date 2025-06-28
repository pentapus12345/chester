import pygame

class Game(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.init()

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            return False
        return True