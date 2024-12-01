import pygame
from random import randrange
from consts import OBSTACLE_GAP, OBSTACLE_MINIMUM_HEIGHT

class Object:
    def __init__(self, x, y, height, width):
        self.color = (255, 101, 101)
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        pass

    def isOffscreen(self):
        # The player object is fixed to the y axis, and obstacles are fixed to the x axis
        # and move across the screen to the left. Because of this behavior, we only care if the
        # x position is less than 0. We really dont care if the bird is off screen, we will worry
        # about that in collision detection.

        # Subtract object's width from the left window boundary (0) so that the object does not
        # register as being offscreen until it is completly offscreen.
        return self.rect.x < (0 - self.rect.width)

        

class Player(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40)
        self.color = (0, 0, 255)
        self.velocity = pygame.Vector2(0,0)
        # scored_obs is a list of obstacles the player has passed,
        # score is calculated from the number of objects in the list.
        self.scored_obs = []
        self.player_image = self.load_player_image()
    
    def draw(self, screen):
        # pygame.draw.rect(self.player_image, self.color, self.rect)
        screen.blit(self.player_image, (self.rect.x, self.rect.y))

    def jump(self):
        self.velocity.y = -5

    def update(self, dt):
        self.velocity.y += 3 * dt
        self.rect.move_ip(self.velocity)
    
    @staticmethod
    def load_player_image():
        image = pygame.image.load("assets/player.gif").convert_alpha()
        image = pygame.transform.scale_by(image, 0.1)
        return image
    
    @property
    def get_score(self):
        return len(self.scored_obs)
        

class Obstacle(Object):
    def __init__(self, x, y, screen_height=None):
        h1, self.h2 = self.getRandomObstacleHeight(screen_height)
        super().__init__(x, y, height=h1, width=75)
        self.velocity = pygame.Vector2(0,0)
        self.rect.y = self.rect.y - self.rect.height
        self.obstacle2_height = 2
        self.inverse_rect = pygame.Rect(self.rect.x, 0, self.rect.width, self.h2)

    def update(self, dt):
        self.velocity.x = -50 * dt
        self.rect.move_ip(self.velocity)
        self.inverse_rect.move_ip(self.velocity)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.color, self.inverse_rect)

    def get_obstacle2_height(self, screen_height):
        # Calculates the height for the second generated obstacle
        max_combined_height = screen_height - OBSTACLE_GAP
        height = max_combined_height - self.height
        return height
    
    @staticmethod
    def getRandomObstacleHeight(screen_height):
        # The maximum combined height for the obstacles is found by subtracting
        # our screen height minus our gap size.
        max_combined_height = screen_height - OBSTACLE_GAP
        # The first height is a random number between our minimum height and maximum height,
        # defined as max_combined_height - minimum_height
        h1 = randrange(OBSTACLE_MINIMUM_HEIGHT, max_combined_height - OBSTACLE_MINIMUM_HEIGHT)
        # Our second height is the difference between our first height and our max combined height
        h2 = max_combined_height - h1
        return [h1, h2]