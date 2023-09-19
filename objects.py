import pygame

class Object:
    def __init__(self, x, y, height, width):
        self.color = (255, 101, 101)
        self.rect = pygame.Rect(x, y, height, width)

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

    def jump(self):
        self.velocity.y = -7

    def update(self):
        self.velocity.y += 0.3
        self.rect.move_ip(self.velocity)
        

class Obstacle(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 75, 150)
        self.velocity = pygame.Vector2(0,0)
        self.rect.y = self.rect.y - self.rect.height

    def update(self):
        self.velocity.x = -5
        self.rect.move_ip(self.velocity)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.color, 
                         (self.rect.x, 0, self.rect.width, self.rect.height)
                         )