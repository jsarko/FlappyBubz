import pygame
from pygame.locals import *
 
from objects import Obstacle, Player
from helpers import getRandomObstacleHeight

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
        self.endgame = False
        self.obstacles = []
 
    def on_init(self):
        pygame.init()
        pygame.font.init()
        self.font_large = pygame.font.SysFont("impact", 55)
        self.font_small = pygame.font.SysFont("impact", 35)
        self.screen = pygame.display.set_mode(self.size, vsync=1)
        self._running = True
        self.clock = pygame.time.Clock()
        self.player = Player(self.width / 2 - 200, self.height / 2)
        self.obstacles = []
        self.collide_list = []
        pygame.time.set_timer(pygame.USEREVENT, 3000)
 
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
                obs = Obstacle(
                    x=self.width / 2 + 300, 
                    y=self.height,
                    screen_height=self.height
                )
                self.obstacles.append(obs)
                self.collide_list += [obs.rect, obs.inverse_rect]


    def on_loop(self):
        if not self.endgame:
            self.player.update(self.dt)

            # Update obstacles
            # print(f"Obstacles: {len(self.obstacles)}")
            for obstacle in self.obstacles:
                obstacle.update(self.dt)
                # Check if obstacle is offscreen
                if obstacle.isOffscreen():
                    self.obstacles.pop(0)
                # Check if player has passed obstacle and a point should be awarded
                if (obstacle.rect.x + obstacle.rect.width) < self.player.rect.x and obstacle not in self.player.scored_obs:
                    self.player.scored_obs.append(obstacle)
                # print(f"ClosestObs: {obstacle.rect.x} / Player: {self.player.rect.x}")

            # Check for collisions
            if self.player.rect.collidelist(self.collide_list) != -1:
                self.endgame = True
            

    def on_render(self):
        if self.endgame:
            self.on_endgame()
        else:
            self.screen.fill((128, 128, 255))
            self.player.draw(self.screen)
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            
            # Display Score
            score = self.font_large.render(f"{self.player.get_score}", True, pygame.Color("black"))
            self.screen.blit(score, (15, 15))

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_endgame(self):
        self.screen.fill("white")
        msg = self.font_large.render(f'BOOM BITCH!', True, pygame.Color("black"))
        score = self.font_small.render(f"SCORE: {self.player.get_score}", True, pygame.Color("black"))
        self.screen.blit(
            msg, 
            (
                (self.width / 2) - (msg.get_width() / 2), 
                (self.height / 2) - (msg.get_height() / 2)
            )
        )
        self.screen.blit(
            score,
            (
                (self.width / 2) - (score.get_width() / 2), 
                (self.height / 2) - (score.get_height() / 2) + 50
            )
        )
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            if not self.pregame:
                self.on_loop()
           
            self.on_render()
            self.dt = 1 / self.clock.tick(120)
            # For the moment, removing the print causes
            # speed spikes intermitently.
            # print(f"dt: {self.dt}")
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()