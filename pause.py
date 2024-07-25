import pygame
import button
import zombie
import player

pygame.init()


info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h))

pygame.display.set_caption("In Game")


#define fonts
font = pygame.font.Font(None, 60)



#while game is in session



#while game is in session
def inGame():
    pygame.display.set_caption("In Game")
    while True:
        print("loop: pause menuS")
        screen.fill("black")
        
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Pause")
                    paused()
        pygame.display.update()


def paused(game, player_sprites, enemy_sprites, item_sprites):
    pygame.display.set_caption("Paused Menu")

    # Logo
    title_font = pygame.font.SysFont("arialblack", 60)
    TEXT_COL = (255,255,255)
    logo_text=title_font.render("ZombieZ", True, TEXT_COL)
    logo_text_rect=logo_text.get_rect(center=(screen.get_width()/2, screen.get_width() * 0.1))

    #button size
    button_width = 250
    button_height = 80
    button_color = (255, 0, 0)
    button_highlight_color = (255, 100,100)

    #create pause menu buttons
    resumeBtn_text = font.render("Resume", True, (255, 255, 255))
    resumeBtn_rect = pygame.Rect(0, 0, button_width, button_height)
    resumeBtn_rect.center = (screen.get_width() / 2, screen.get_height() / 2 - 100)
    resumeBtn_text_rect = resumeBtn_text.get_rect(center = resumeBtn_rect.center)
    resumeBtn_highlight = False

    saveBtn_text = font.render("Save Game", True, (255, 255, 255))
    saveBtn_rect = pygame.Rect(0, 0, button_width, button_height)
    saveBtn_rect.center = (screen.get_width() / 2, screen.get_height() / 2)
    saveBtn_text_rect = saveBtn_text.get_rect(center = saveBtn_rect.center)
    saveBtn_highlight = False

    mainMenuBtn_text = font.render("Main Menu", True, (255, 255, 255))
    mainMenuBtn_rect = pygame.Rect(0, 0, button_width, button_height)
    mainMenuBtn_rect.center = (screen.get_width() / 2, screen.get_height() / 2 + 100)
    mainMenuBtn_text_rect = mainMenuBtn_text.get_rect(center = mainMenuBtn_rect.center)
    mainMenuBtn_highlight = False
    frame_path="lastframe.jpg"
    lastframe = pygame.image.load(frame_path)

    background_image=lastframe
    background_image = pygame.transform.scale(background_image, (screen.get_size()))

    #add ZombieZ logo to pause menu
    logo_image = pygame.image.load("logo.jpeg")
    logo_image = pygame.transform.scale(logo_image, (screen.get_width() / 7, screen.get_width() /7))
    logo_rect = logo_image.get_rect(bottomright=screen.get_rect().bottomright)
    background_image.blit(logo_image, logo_rect)

    game_paused = True
    action = None
    while game_paused:
        screen.fill((139, 0, 0))

        # draw buttons onto the screen

        
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if resumeBtn_rect.collidepoint(mouse_pos):
                    action = "resume"
                    game_paused = False
                elif saveBtn_rect.collidepoint(mouse_pos):
                    action = "save"
                    save_game(game, player_sprites, enemy_sprites, item_sprites)     
                elif mainMenuBtn_rect.collidepoint(mouse_pos):
                    action = "main_menu"
                    game_paused = False
                    
                    
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if resumeBtn_rect.collidepoint(mouse_pos):
                    resumeBtn_highlight = True
                else: 
                    resumeBtn_highlight = False
                
                if saveBtn_rect.collidepoint(mouse_pos):
                    saveBtn_highlight = True
                else:
                    saveBtn_highlight = False
                
                if mainMenuBtn_rect.collidepoint(mouse_pos):
                    mainMenuBtn_highlight = True
                else:
                    mainMenuBtn_highlight = False

        #Draw the buttons 
        pygame.draw.rect(background_image, button_highlight_color if resumeBtn_highlight else button_color, resumeBtn_rect)
        background_image.blit(resumeBtn_text,resumeBtn_text_rect )

        pygame.draw.rect(background_image, button_highlight_color if saveBtn_highlight else button_color, saveBtn_rect)
        background_image.blit(saveBtn_text, saveBtn_text_rect)
        
        pygame.draw.rect(background_image, button_highlight_color if mainMenuBtn_highlight else button_color, mainMenuBtn_rect)
        background_image.blit(mainMenuBtn_text, mainMenuBtn_text_rect)
        background_image.blit(logo_text, logo_text_rect)
        screen.blit(background_image,(0,0))

        pygame.display.flip()

    # Close Pause Menu and handle action
    if action == "resume":
        return
    elif action == "main_menu":
        MAIN_MENU_EVENT = pygame.USEREVENT + 5
        pygame.event.post(pygame.event.Event(MAIN_MENU_EVENT))
        return

def save_game(game, player_sprites, enemy_sprites, item_sprites):
    with open('saved_game.txt', 'w') as file:
        # SAVE THE GAME INSTANCE DATA
        from game_instance import GameInstance
        file.write(game.generateSaveData())

        file.write('------game_instance/player boundary------\n\n') # For Parsing - marks the split between the game_instance and the player data

        # SAVE THE PLAYER DATA
        for players in player_sprites.sprites():
            file.write(players.generateSaveData())
        
        file.write('------player/enemy boundary------\n\n') # For Parsing - marks the split between player and enemy data

        # SAVE THE ENEMY DATA
        for enemy in enemy_sprites.sprites():
            file.write(enemy.generateSaveData())

        file.write('------enemy/item boundary------\n\n') # For Parsing - marks the split between enemy and item data

        # SAVE THE ITEM DATA
        for item in item_sprites.sprites():
            file.write(item.generateSaveData())





"""def main_menu():
    pygame.display.set_caption("Main Menu")
    
    while True:
        screen.fill("black")
        draw_text("THIS IS THE MAIN MENU", font, TEXT_COL, 180, 200)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()"""


# inGame()