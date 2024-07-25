import pygame
import os
import json

class Item (pygame.sprite.Sprite):
    def __init__(self, players, location, image, scale):
        pygame.sprite.Sprite.__init__(self)
        
        self.players = players

        original_size = (image.get_width(), image.get_height())
        scale_size = tuple(size * scale for size in original_size)
        self.image = pygame.transform.scale(image, scale_size)

        self.rect = self.image.get_rect()
        self.rect.center = location
    
    def onPickup(self, player):
        self.kill()
    
    def update(self):
        for player in self.players:
            if player.rect.collidepoint(self.rect.center):
                self.onPickup(player)

class HealthPotion(Item):
    def __init__(self, location, health, players):
        potion_image = pygame.image.load(os.path.dirname(__file__) + "/Assets/Items/health_potion.png")
        Item.__init__(self, players, location, potion_image, 0.1)
        self.health = health

    def onPickup(self, player):
        player.cur_health = min(player.cur_health + self.health, player.max_health)
        self.kill()

    def generateSaveData(self):
        save_data = {
            "location": self.rect.center,
            "health": self.health
        }
        save_data_string = "--health_potion--\n" + json.dumps(save_data) + "\n\n"
        return save_data_string
    

