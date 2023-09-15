import pygame
from pygame.locals import *
 
from objects import Obstactle, Player

class App:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.width, self.height = 640, 400
        self.player_pos = None
        self.clock = None
        self.player = None
        self.dt = 0
 
    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self._running = True
        self.clock = pygame.time.Clock()
        self.player = Player(self.width / 2, self.height / 2)
        self.obstacle = Obstactle(self.width / 2 + 100, self.height - 200)
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.jump()

    def on_loop(self):
        self.player.update()
        self.obstacle.update()

    def on_render(self):
        self.screen.fill((128, 128, 255))
        self.player.draw(self.screen)
        self.obstacle.draw(self.screen)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.dt = self.clock.tick(60) / 1000

        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()