import pygame
from pygame.locals import QUIT
import zombie
import player
from button import Button
from game_instance import GameInstance
import json
import re
import imageio
import numpy as np
from PIL import Image
import items

#Change by MHz to demo git. This is okay -- Hertz 
# Initialize screen
pygame.init()
info = pygame.display.Info()
flags = pygame.SCALED | pygame.RESIZABLE
screen = pygame.display.set_mode((info.current_w, info.current_h), flags)
pygame.display.set_caption('ZombieZ')
screen_center = (screen.get_width()/2, screen.get_height()/2)

def load_game():
    try:
        with open('saved_game.txt', 'r') as f:
            # Read the save file
            save_data = f.read()

            # Parse the file
            save_data = save_data.replace('\n', '')
            save_boundary = r'------game_instance\/player boundary------|------player\/enemy boundary------|------enemy\/item boundary------'
            game_save_data, player_data, enemy_data, item_data = re.split(save_boundary, save_data)
            player_data = player_data.split('--begin_player--')
            del player_data[0]
            enemy_data = enemy_data.split('--begin_enemy--')
            del enemy_data[0]
            item_data = item_data.split('--health_potion--')
            del item_data[0]

            # Create sprite groups
            all_players = pygame.sprite.Group()
            all_enemies = pygame.sprite.Group()
            all_items = pygame.sprite.Group()

            # Extract the data and add corresponding players/enemies to their sprite groups
            game_save = json.loads(game_save_data)
            for p in player_data:
                p = json.loads(p)
                tmp_player = player.Player(location=tuple(p['location']), cur_health=p['current_health'], max_health=p['max_health'], damage=p['damage'], speed=p['speed'], screen=screen, stats=p['stats'])
                all_players.add(tmp_player)
            for e in enemy_data:
                e = json.loads(e)
                tmp_enemy =  zombie.Enemy(location=tuple(e['location']), health=e['current_health'], max_health=e['max_health'], damage=e['damage'], speed=e['speed'], target=all_players.sprites()[0], scale=e['scale'], screen=screen)
                all_enemies.add(tmp_enemy)
            for i in item_data:
                i = json.loads(i)
                tmp_item = items.HealthPotion(i['location'], i['health'], all_players)
                all_items.add(tmp_item)

            return game_save, all_players, all_enemies, all_items
    except FileNotFoundError:
        return None
       



def main_menu():
    global background_image
    # Create font object
    font = pygame.font.Font(None, 60)

    # Set button size
    button_width = 250
    button_height = 80

    # Set button colors
    button_color = (255, 0, 0)
    button_highlight_color = (255, 100, 100)

    # Create new game button
    new_game_text = font.render("New Game", True, (255, 255, 255))
    new_game_rect = pygame.Rect(0, 0, button_width, button_height)
    new_game_rect.center = (screen.get_width() / 2, screen.get_height() / 2 - 100)
    new_game_text_rect=new_game_text.get_rect(center=new_game_rect.center)
    new_game_highlight = False

    # Create load game button
    load_game_text = font.render("Load Game", True, (255, 255, 255))
    load_game_rect = pygame.Rect(0, 0, button_width, button_height)
    load_game_rect.center = (screen.get_width() / 2, screen.get_height() / 2)
    load_game_text_rect=load_game_text.get_rect(center=load_game_rect.center)
    load_game_highlight = False

    # Create quit game button
    quit_game_text = font.render("Quit Game", True, (255, 255, 255))
    quit_game_rect = pygame.Rect(0, 0, button_width, button_height)
    quit_game_rect.center = (screen.get_width() / 2, screen.get_height() / 2 + 100)
    quit_game_text_rect=quit_game_text.get_rect(center=quit_game_rect.center)
    quit_game_highlight = False

    # Create clock object
    clock = pygame.time.Clock()
    logol_font = pygame.font.SysFont("arialblack", 100)
    TEXT_COL = (255,255,255)
    logo_text = logol_font.render("ZombieZ", True, TEXT_COL)
    logo_text_rect = logo_text.get_rect(center=(screen_center[0], new_game_rect.top - 100))
  
    gif_frames = []
    gif_path = "background.gif"
    gif_reader = imageio.get_reader(gif_path)
    fps = gif_reader.get_meta_data().get("fps", 10)


    for frame in gif_reader:
        pil_image = Image.fromarray(imageio.core.util.Array(frame))
        pil_image = pil_image.resize(screen.get_size())
        pygame_surface = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)
        gif_frames.append(pygame_surface)

    frame_index = 0
    animation_delay = int(900 / fps)

    

    in_menu = True
    action = None
    game=GameInstance()
    while in_menu:
        # EventQueue
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if new_game_rect.collidepoint(mouse_pos):
                    action = "New Game"
                    in_menu = False
                    

                elif load_game_rect.collidepoint(mouse_pos):
                    action = "Load Game"
                    in_menu = False
                    
                elif quit_game_rect.collidepoint(mouse_pos):
                    action = "Quit"
                    in_menu = False

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if new_game_rect.collidepoint(mouse_pos):
                    new_game_highlight = True
                else:
                    new_game_highlight = False

                if load_game_rect.collidepoint(mouse_pos):
                    load_game_highlight = True
                else:
                    load_game_highlight = False

                if quit_game_rect.collidepoint(mouse_pos):
                    quit_game_highlight = True
                else:
                    quit_game_highlight = False

        # Draw the gif
        
        background_image = gif_frames[frame_index]
        background_image = pygame.transform.scale(background_image, screen.get_size())
        background_image = background_image.convert()
        screen.blit(background_image, (0, 0))
         
        # Draw the buttons
        pygame.draw.rect(background_image, button_highlight_color if new_game_highlight else button_color, new_game_rect)
        background_image.blit(new_game_text, new_game_text_rect)
        pygame.draw.rect(background_image, button_highlight_color if load_game_highlight else button_color, load_game_rect)
        background_image.blit(load_game_text, load_game_text_rect)
        pygame.draw.rect(background_image, button_highlight_color if quit_game_highlight else button_color, quit_game_rect)
        background_image.blit(quit_game_text, quit_game_text_rect)
        background_image.blit(logo_text, logo_text_rect)
        # Update the display
        screen.blit(background_image, (0, 0))
        frame_index = (frame_index + 1) % len(gif_frames)
        pygame.display.flip()
        pygame.time.delay(animation_delay)

    # Close main menu and handle action
    if action == "New Game":
        game.start()
    elif action == "Load Game":
        loaded_data = load_game()
        if loaded_data is not None:
            game_save, all_players, all_enemies, all_items = loaded_data
            game.start(game_save=game_save, all_players=all_players, all_enemies=all_enemies, all_items=all_items)
        else:
            print("No save file found... creating New Game")
            game.start()

    elif action == "Quit":
        pygame.quit()

if __name__ == "__main__":
    main_menu()
