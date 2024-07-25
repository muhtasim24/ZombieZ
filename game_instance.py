import os
import pygame
from pygame.locals import *
import random
import json

import zombie
import player
import pause
import map_class
import inventory
import items


class GameInstance():

    def spawn_enemy(self):
        # Generate Random Spawn Location
        width, height = self.screen.get_size()
        p1_width = self.player1.rect.width
        p1_height = self.player1.rect.height
        spawn_locations = [
            (random.randint(0, width), -p1_height), # Top of Screen
            (random.randint(0, width), height),     # Bottom of Screen
            (-p1_width, random.randint(0, height)), # Left Side of Screen
            (width, random.randint(0, height))      # Right Side of Screen    
        ]
        random_location = random.choice(spawn_locations)

        # Spawn the boss enemies
        if self.spawn_boss and self.spawned_bosses < self.boss_quantity:
            self.spawned_enemies += 1
            self.spawned_bosses += 1

            enemy = zombie.Enemy(location=random_location, health=(self.enemy_stats['current_health'] * 5), max_health=(self.enemy_stats['max_health'] * 5), damage=(self.enemy_stats['damage'] * 2), speed=(self.enemy_stats['speed'] * 0.5), target=self.player1, scale=2, screen=self.screen)
            self.all_enemies.add(enemy)

        # Spawn the regular enemies
        elif self.spawned_enemies < self.max_enemies and (self.killed_round_enemies + self.spawned_enemies) < self.max_round_enemies:
            self.spawned_enemies += 1
            
            enemy = zombie.Enemy(location=random_location, health=self.enemy_stats['current_health'], max_health=self.enemy_stats['max_health'], damage=self.enemy_stats['damage'], speed=self.enemy_stats['speed'], target=self.player1, scale=1, screen=self.screen)
            self.all_enemies.add(enemy)



    def draw_round(self):
        font = pygame.font.Font(None, size=250)
        round_text = font.render(str(self.round), True, (255, 0, 0))
        text_width = round_text.get_width()
        padding = 25
        round_text_pos = round_text.get_rect(x = self.screen.get_width() - text_width - padding, y = 0)
        self.screen.blit(round_text, round_text_pos)

    def reset_round(self):
        self.resetting_round = False

        # Update player stats
        self.player1.stats['rounds'] += 1

        # Reset round variables
        self.killed_round_enemies = 0
        self.max_round_enemies = min(self.max_round_enemies + 5, self.max_max_round_enemies)
        self.spawned_bosses = 0
        self.spawn_boss = False

        # Every other round, buff the enemy stats
        if self.round % 2 == 1:
            self.enemy_stats['current_health'] = min(self.enemy_stats['current_health'] + 10, self.max_enemy_stats['current_health'])
            self.enemy_stats['max_health'] = min(self.enemy_stats['max_health'] + 10, self.max_enemy_stats['max_health'])
            self.enemy_stats['damage'] = min(self.enemy_stats['damage'] + 5, self.max_enemy_stats['damage'])
            self.enemy_stats['speed'] = min(self.enemy_stats['speed'] + 0.5, self.max_enemy_stats['speed'])

        # Every 5 rounds, increase the maximum number of enemies allowed to be spawned in and spawn a boss
        if self.round % 5 == 0:
            self.max_enemies = min(self.max_enemies + 2, self.max_max_enemies)
            self.spawn_boss = True

        # Every 10 rounds increase the number of bosses spawened
        if self.round % 10 == 0:
            self.boss_quantity += 1



    def start(self, game_save=None, all_players:pygame.sprite.Group=None, all_enemies:pygame.sprite.Group=None, all_items:pygame.sprite.Group=None):
        # Variable used for developer only options (hitbox outlining, etc.)
        self.is_dev_mode = False
        
        # Initialize screen
        pygame.init()
        info = pygame.display.Info()
        flags = pygame.SCALED | pygame.RESIZABLE
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), flags)
        pygame.display.set_caption('ZombieZ')
        screen_center = (self.screen.get_width()/2, self.screen.get_height()/2)

        # Fill background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        color = (20,20,20)  #dark gray
        self.background.fill(color)

        # Put map on background
        """
        We need to draw the map somewhere other than the top-left corner of the
        screen in order to test the up and left directions independently of
        other directions for map scrolling.
        Drawing the map in the negative direction from the top-left corner of
        the screen roughly centers the map.
        (It's 6am and I don't care to do the exact math tbh but half of the
        screen dimenstions is good enough to test scrolling)
        -- Matt
        """
        map_location = (-screen_center[0],-screen_center[1])  
        self.map_obj = map_class.Map(filename="Assets/Map.png",location=map_location)
        self.map_surface = self.map_obj.load_map()
        self.background.blit(self.map_surface, self.map_obj.location)
        self.background = self.background.convert()

        # Create clock object
        self.clock = pygame.time.Clock()

        # Create enemy events
        self.ENEMY_SPAWN_EVENT = pygame.USEREVENT + 1
        self.ENEMY_DEATH_EVENT = pygame.USEREVENT + 2
        self.RESET_ROUND_EVENT = pygame.USEREVENT + 3

        # Create player events
        self.PLAYER_DEATH_EVENT = pygame.USEREVENT + 4
        self.MAIN_MENU_EVENT = pygame.USEREVENT + 5

        # LOAD the game_instance save data
        if game_save == None: # New Game
            # Create enemy variables for spawning system
            self.round = 1
            self.max_enemies = 5
            self.max_max_enemies = 15
            self.spawned_enemies = 0
            self.killed_round_enemies = 0
            self.max_round_enemies = 5
            self.max_max_round_enemies = 50
            self.spawn_boss = False
            self.spawned_bosses = 0
            self.boss_quantity = 1
            self.spawn_rate = 1000 # ms per spawn
            self.enemy_stats = {
                'current_health': 10,
                'max_health': 10,
                'damage': 1,
                'speed': 2,
            }
            self.max_enemy_stats = {
                'current_health': 1000,
                'max_health': 1000,
                'damage': 50,
                'speed': 10,
            }
            self.resetting_round = False
        else:
            self.loadSaveData(game_save)

        # LOAD the player save data
        if all_players == None: # New Game
            # Create player sprite group
            self.all_players = pygame.sprite.Group()
            
            # Create player
            self.player1 = player.Player(location=screen_center, cur_health=100, max_health=100, damage=10, speed=5, screen=self.screen)
            self.all_players.add(self.player1)
        else:
            self.all_players = all_players
            self.player1 = all_players.sprites()[0]

        # LOAD the enemy save data
        if all_enemies == None: # New Game
            # Create enemy sprite group
            self.all_enemies = pygame.sprite.Group()
        else:
            self.all_enemies = all_enemies
        
        # LOAD the item save data
        if all_items == None: # New Game
            # Create item sprite group
            self.all_items = pygame.sprite.Group()
        else:
            self.all_items = all_items

        # Reset the round if not done so in the save
        if self.resetting_round:
                self.reset_round()

        # Start the enemy spawner
        pygame.time.set_timer(self.ENEMY_SPAWN_EVENT, self.spawn_rate)

        # Start the game loop
        self.game_loop()
            

    def game_loop(self):
        game_ongoing = True
        action = None
        while game_ongoing:
            # EventQueue
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                
                # Player Controls
                elif event.type == KEYDOWN:
                    if event.key == K_LALT or event.key == K_RALT:
                        self.player1.request_dodge()   
                    elif event.key == K_ESCAPE:
                        game_paused = True
                        pause.paused(game=self, player_sprites=self.all_players, enemy_sprites=self.all_enemies, item_sprites=self.all_items)
                        break
                    elif event.key == K_F12:
                        self.is_dev_mode = not self.is_dev_mode
                    elif event.key == K_i:
                        inventory.inventory(self.player1)
                elif event.type == MOUSEBUTTONDOWN:
                    self.player1.attack_enemy(self.all_enemies)
                elif event.type == self.PLAYER_DEATH_EVENT:
                    action = 'game_over'
                    game_ongoing = False
                elif event.type == self.MAIN_MENU_EVENT:
                    action = 'main_menu'
                    game_ongoing = False
                
                # Enemy Events
                elif event.type == self.ENEMY_SPAWN_EVENT:
                    self.spawn_enemy()
                elif event.type == self.ENEMY_DEATH_EVENT:
                    # Update player stats
                    self.player1.stats['kills'] += 1

                    # Random chance of spawning health potion
                    chance = random.uniform(0, 1)
                    potion_drop_rate = 0.1
                    potion_spawn_point = event.dict['item_spawn_point']
                    potion_health_value = 10
                    if chance <= potion_drop_rate:
                        tmp_item = items.HealthPotion(potion_spawn_point, potion_health_value, self.all_players)
                        self.all_items.add(tmp_item)

                    self.spawned_enemies -= 1
                    self.killed_round_enemies += 1
                    if self.killed_round_enemies == self.max_round_enemies:
                        self.round += 1
                        delay = 3000 # ms before next round spawns
                        self.resetting_round = True
                        pygame.time.set_timer(self.RESET_ROUND_EVENT, delay, 1)
                elif event.type == self.RESET_ROUND_EVENT:
                    self.reset_round()

            #Check if player moved offscreen; if so, scroll the map
            is_scrolling = self.map_obj.scroll_map(self.player1)
            if is_scrolling:
                self.background.blit(self.map_surface, self.map_obj.location)
                self.background = self.background.convert()

            # Update the background (must be updated BEFORE anything else)
            self.screen.blit(self.background, (0, 0))


            # Draw and update all sprites (enemies)
            self.all_enemies.update(self.is_dev_mode)
            self.all_players.update(self.is_dev_mode)
            self.all_enemies.draw(self.screen)
            self.all_players.draw(self.screen)

            self.all_items.update()
            self.all_items.draw(self.screen)

            # Draw the round number
            self.draw_round()

            # Update the display
            pygame.display.flip()

            # Lock the framerate at 60 fps
            self.clock.tick(60)
        
        # Stop game loop and handle action
        if action == 'main_menu':
            from main import main_menu
            main_menu()
        elif action == 'game_over':
            # Delete the save data
            save_file_path = os.path.dirname(__file__) + "/saved_game.txt"
            if os.path.exists(save_file_path):
                os.remove(save_file_path)

            # Go to game over screen
            from game_over import game_over_menu
            game_over_menu(self.screen, self.player1.stats)


    def generateSaveData(self):
        save_data = {
            "round": self.round,
            "max_enemies": self.max_enemies,
            "max_max_enemies": self.max_max_enemies,
            "spawned_enemies": self.spawned_enemies,
            "killed_round_enemies": self.killed_round_enemies,
            "max_round_enemies": self.max_round_enemies,
            "max_max_round_enemies": self.max_max_round_enemies,
            "spawn_rate": self.spawn_rate,
            "enemy_stats": self.enemy_stats,
            "max_enemy_stats": self.max_enemy_stats,
            "spawn_boss": self.spawn_boss,
            "spawned_bosses": self.spawned_bosses,
            "boss_quantity": self.boss_quantity,
            "resetting_round": self.resetting_round
        }
        save_data_string = json.dumps(save_data) + "\n\n"
        return save_data_string
    
    def loadSaveData(self, saveData):
        self.round = saveData['round']
        self.max_enemies = saveData['max_enemies']
        self.max_max_enemies = saveData['max_max_enemies']
        self.spawned_enemies = saveData['spawned_enemies']
        self.killed_round_enemies = saveData['killed_round_enemies']
        self.max_round_enemies = saveData['max_round_enemies']
        self.max_max_round_enemies = saveData['max_max_round_enemies']
        self.spawn_rate = saveData['spawn_rate']
        self.enemy_stats = saveData['enemy_stats']
        self.max_enemy_stats = saveData['max_enemy_stats']
        self.spawn_boss = saveData['spawn_boss']
        self.spawned_bosses = saveData['spawned_bosses']
        self.boss_quantity = saveData['boss_quantity']
        self.resetting_round = saveData['resetting_round']

