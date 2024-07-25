import pygame
import os
import math
import player
import json

class item():
    def __init__(self, itemName, imageName):
        self.itemName = itemName
        self.image = pygame.image.load(os.path.dirname(__file__) + imageName)

test_item = item("gun", "/ima")