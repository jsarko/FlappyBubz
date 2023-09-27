from random import randrange
from consts import OBSTACLE_GAP, OBSTACLE_MINIMUM_HEIGHT

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