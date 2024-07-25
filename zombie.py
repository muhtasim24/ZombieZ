import pygame
import os
import math
import player
import json
import random
import items

class Enemy(pygame.sprite.Sprite):

    screen = pygame.display.get_surface()

    def __init__(self, location, health, max_health, damage, speed, target, scale=1, screen=pygame.display.get_surface()):
        pygame.sprite.Sprite.__init__(self)
        self.anim_images = [pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_0.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_1.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_2.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_3.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_4.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_5.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_6.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_7.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_8.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_9.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_10.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_11.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_12.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_13.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_14.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_15.png"),
                            pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-idle_16.png")]
        self.attack_anim_images = [pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-attack_0.png"),
                                   pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-attack_1.png"),
                                   pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-attack_2.png"),
                                   pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-attack_3.png"),
                                   pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-attack_4.png"),
                                   pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-attack_5.png"),
                                   pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-attack_6.png"),
                                   pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-attack_7.png"),
                                   pygame.image.load(os.path.dirname(__file__) + "/Assets/Zombie/skeleton-attack_8.png")]
        self.attack_anim_ongoing = False
        self.scaleImages(scale)
        self.attack_anim_stage = 0
        self.anim_stage = 0
        self.anim_timer = 0
        self.image = self.anim_images[self.anim_stage]
        self.scale = scale
        self.angle = 0

        self.rect = self.image.get_rect()
        self.rect.left = location[0]
        self.rect.top = location[1]  

        self.health: int = health
        self.maxHealth: int = max_health 
        self.damage = damage
        self.speed = speed
        self.target: player.Player = target

        self.next_update_time = 0
        self.screen = screen

        self.hitbox = self.rect.copy()

    def update(self, is_dev_mode):
        # This code allows the enemy update function to be dependent on time rather than framerate
        current_time = pygame.time.get_ticks()
        frame_delay = 10 # FPS is locked at 60 in main.py (this delay is 0.16667 sec)
        if current_time > self.next_update_time:
            self.next_update_time = current_time + frame_delay

            target_location = self.target.rect.center
            
            self.lookAt(target_location)
            self.moveTo(target_location)
            
            self.attack(target_location, 10)

            self.animate(target_location)

            self.drawHealthBar()
            
            self.update_hitbox(is_dev_mode)

    
    def moveTo(self, target_location):
        if not self.rect.collidepoint(target_location):
            # Calculate unit direction vector
            dx = target_location[0] - self.rect.centerx
            dy = target_location[1] - self.rect.centery
            vec = pygame.math.Vector2(dx, dy)
            if vec.length() == 0:
                return        
            unit_vec = vec.normalize()

            # Step towards target
            self.rect.left += (unit_vec.x * self.speed)
            self.rect.top += (unit_vec.y * self.speed)

    def lookAt(self, target_location):
        if not self.rect.collidepoint(target_location):
            # Calculate direction vector
            dx = target_location[0] - self.rect.centerx
            dy = target_location[1] - self.rect.centery
            vec = pygame.math.Vector2(dx, dy)

            # Calculate look at rotation
            angle = math.degrees(math.atan2(dy, dx))
            self.angle = angle

    def attack(self, target_location, damage):
        if self.rect.collidepoint(target_location) or self.attack_anim_ongoing:
            self.attack_anim_ongoing = True
            # The purpose of the animation timer is to control the speed of the animation
            if self.anim_timer == 0:
                # Update the image to the next in the animation array
                self.attack_anim_stage += 1
                if self.attack_anim_stage >= len(self.attack_anim_images):
                    # Animation Completed - Reset and damage player
                    self.attack_anim_ongoing = False
                    self.attack_anim_stage = 0
                    if self.rect.collidepoint(target_location):
                        self.target.damageSelf(damage)
                    return
                    
                # Rotate the image to match the enemy's rotation
                self.image = pygame.transform.rotate(self.attack_anim_images[self.attack_anim_stage], -self.angle)
        
            self.anim_timer += 1

            anim_delay = 5
            if self.anim_timer >= anim_delay:
                self.anim_timer = 0
    
    def drawHealthBar(self):
        # Draw healthbar background
        color_white = (255, 255, 255)
        # healthbar_background = pygame.Rect(self.rect.left + 35, self.rect.top, 200, 10)
        healthbar_background = pygame.Rect(0, 0, 200, 10)
        healthbar_background.centerx = self.rect.centerx
        healthbar_background.centery = self.rect.top
        pygame.draw.rect(self.screen, color_white, healthbar_background)

        # Draw healthbar
        color_red = (255, 0, 0)
        healthbar = healthbar_background.copy()
        healthbar.width = (self.health / self.maxHealth) * healthbar_background.width
        pygame.draw.rect(self.screen, color_red, healthbar)

    def damageSelf(self, damage):
        self.health -= damage
        if self.health <= 0:
            # Manage the number of enemies spawned in & set the item drop location
            DEATHEVENT = pygame.USEREVENT + 2
            event_data = {"item_spawn_point": self.rect.center}
            pygame.event.post(pygame.event.Event(DEATHEVENT, event_data))
            self.kill()

    def animate(self, target_location):
        if not (self.rect.collidepoint(target_location) or self.attack_anim_ongoing):
            # The purpose of the animation timer is to control the speed of the animation
            if self.anim_timer == 0:
                # Update the image to the next in the animation array
                self.anim_stage += 1
                if self.anim_stage >= len(self.anim_images):
                    self.anim_stage = 0
                # Rotate the image to match the enemy's rotation
                self.image = pygame.transform.rotate(self.anim_images[self.anim_stage], -self.angle)
        
            self.anim_timer += 1

            anim_delay = 5
            if self.anim_timer >= anim_delay:
                self.anim_timer = 0

    def scaleImages(self, scale):
        # Scale Idle/Walking Animation images
        default_idle_size = (120.5, 111)
        idle_scale_size = tuple(size * scale for size in default_idle_size)
        self.anim_images = [pygame.transform.scale(image, idle_scale_size) for image in self.anim_images]

        # Scale attack animation images
        default_attack_size = (159, 147)
        attack_scale_size = tuple(size * scale for size in default_attack_size)
        self.attack_anim_images = [pygame.transform.scale(image, attack_scale_size) for image in self.attack_anim_images]

    def generateSaveData(self):
        save_data = {
            "location": (self.rect.left, self.rect.top),
            "rotation": self.angle,
            "scale": self.scale,
            "current_health": self.health,
            "max_health": self.maxHealth,
            "damage": self.damage,
            "speed": self.speed
        }
        save_data_string = "--begin_enemy--\n" + json.dumps(save_data) + "\n\n"
        return save_data_string

    def update_hitbox(self, is_dev_mode):
        self.hitbox = self.rect.copy()
        if is_dev_mode:
            yellow = (255,255,0)
            pygame.draw.rect(surface=self.screen,color=yellow,rect=self.rect,width=2)

