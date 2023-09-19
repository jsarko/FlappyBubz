import pygame
from pygame.locals import *
 
from objects import Obstacle, Player

class App:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.width, self.height = 640, 400
        self.player_pos = None
        self.clock = None
        self.player = None
        self.dt = 0
        self.pregame = True
        self.obstacles = []
 
    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self._running = True
        self.clock = pygame.time.Clock()
        self.player = Player(self.width / 2 - 200, self.height / 2)
        self.obstacles = []
        pygame.time.set_timer(pygame.USEREVENT, 1500)
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if self.pregame:
                self.pregame = False
            elif event.key == pygame.K_SPACE:
                self.player.jump()
        # All events that start once pregame ends
        elif not self.pregame:
            if event.type == pygame.USEREVENT:
                self.obstacles.append(
                    Obstacle(self.width / 2 + 300, self.height)
                )


    def on_loop(self):
        self.player.update()

        # Update obstacles
        for obstacle in self.obstacles:
            obstacle.update()

        # Check if obstacle is offscreen
        if len(self.obstacles) > 0:
            if self.obstacles[-1].isOffscreen():
                self.obstacles.pop()
        
        # Check for collisions
        if self.player.rect.collidelist(self.obstacles) != -1:
            pass
            

    def on_render(self):
        self.screen.fill((128, 128, 255))
        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            if not self.pregame:
                self.on_loop()
            self.on_render()
            self.dt = self.clock.tick(60) / 1000

        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()