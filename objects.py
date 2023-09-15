import pygame

class Object:
    def __init__(self, x, y, height, width):
        self.color = (255, 101, 101)
        self.rect = pygame.Rect(x, y, height, width)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        pass

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

class Obstactle(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 75, 200)
        self.velocity = pygame.Vector2(0,0)
    
    def update(self):
        self.velocity.x = -5
        self.rect.move_ip(self.velocity)