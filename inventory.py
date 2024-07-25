import pygame
import button
import zombie
import player
import weapon

pygame.init()


info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h))

pygame.display.set_caption("In Game")

lancePath="Assets/Lance/lanceRight.png"
saiPath="Assets/Sai/saiRight.png"
axePath="Assets/Axe/axeRight.png"
swordPath="Assets/Sword/swordRight.png"
#define fonts
font = pygame.font.SysFont("arialblack", 40)

title_font = pygame.font.SysFont("arialblack", 60)
TEXT_COL = (255,255,255)

def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x,y))



#while game is in session
def inGame():
    pygame.display.set_caption("In Game")
    while True:

        screen.fill("black")
        draw_text("GAME IS RUNNING", font, TEXT_COL, 180, 200)
        draw_text("PRESS I TO OPEN INVENTORY", font, TEXT_COL, 140, 300)

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    inventory()

        pygame.display.update()


def inventory(player1: player.Player):
    game_paused = True
    selected_slot = None
    # Define inventory slot dimensions
    slot_width, slot_height = 80, 80

    # Define inventory size
    inventory_width, inventory_height = 8, 2

    # Create inventory surface
    inventory_surface = pygame.Surface((inventory_width * slot_width, inventory_height * slot_height))
    inventory_surface_topleft = (info.current_w/2 - inventory_width*slot_width/2, info.current_h/2 - inventory_height*slot_height/2 - 150)

    # Create inventory slot rects
    slot_rects = []
    for i in range(inventory_width):
        for j in range(inventory_height):
            x = i * slot_width
            y = j * slot_height
            slot_rects.append(pygame.Rect(x, y, slot_width, slot_height))

    # Create button rects
    button_rects = [
        pygame.Rect(inventory_surface_topleft[0], inventory_surface_topleft[1], slot_width, slot_height), # Sword
        pygame.Rect(inventory_surface_topleft[0] + slot_width, inventory_surface_topleft[1], slot_width, slot_height), # Lance
        pygame.Rect(inventory_surface_topleft[0], inventory_surface_topleft[1] + slot_height, slot_width, slot_height), # Axe
        pygame.Rect(inventory_surface_topleft[0] + slot_width, inventory_surface_topleft[1] + slot_height, slot_width, slot_height) # Sai
    ]

    # Define item images
    item_images = []
    item_images.append(pygame.image.load("Assets/Sword/sword.png").convert_alpha()) # example item image
    item_images.append(pygame.image.load("Assets/Axe/axe.png").convert_alpha()) # example item image
    item_images.append(pygame.image.load("Assets/Lance/lance.png").convert_alpha()) # example item image
    item_images.append(pygame.image.load("Assets/Sai/sai.png").convert_alpha()) # example item image


    # Define inventory list
    inventory = [0,1,2,3] # for more weapons


    #load button images
    resume_img = pygame.image.load("Pause_Feature/Menu_Images/button_resume.png").convert_alpha()

    #button size
    btn_size = (200,100)

    resumeScaled = pygame.transform.scale(resume_img, btn_size)

    #create button instances
    resume_button = button.Button(304, 500, resumeScaled, 1)
    resume_button.rect.centerx = info.current_w/2

    image_size = (35, 65) 
    while game_paused:
        screen.fill((139, 0, 0))

        # draw buttons onto the screen
        resume_button.draw(screen)

        # Draw inventory slots onto inventory surface and blit item images onto the slots
        
 # Draw inventory slots onto inventory surface and blit item images onto the slots
        for i, slot_rect in enumerate(slot_rects):
            if i < len(inventory):
                item_image = item_images[inventory[i]]
                item_rect = item_image.get_rect()
                item_rect.center = slot_rect.center
                scaled_image = pygame.transform.scale(item_image, image_size)
                scaled_rect = scaled_image.get_rect(center=item_rect.center)
                inventory_surface.blit(scaled_image, (scaled_rect.left - 15, scaled_rect.top))
            if i == selected_slot:
                pygame.draw.rect(inventory_surface, (255, 0,0), slot_rect, 1)
        # Draw all the other slot borders first
        for i, slot_rect in enumerate(slot_rects):
            if i != selected_slot:
                pygame.draw.rect(inventory_surface, (255, 255, 255), slot_rect, 1)

        # Draw inventory surface onto screen
        screen.blit(inventory_surface, inventory_surface_topleft)


        draw_text("Inventory", title_font, TEXT_COL, 570, 50)


        # handle events
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if button_rects[0].collidepoint(mouse_pos):
                    player1.weapon = weapon.Weapon(filepath=swordPath,weapon_type=weapon.WeaponType.SWORD)
                
                if button_rects[1].collidepoint(mouse_pos):
                    player1.weapon = weapon.Weapon(filepath=lancePath,weapon_type=weapon.WeaponType.LANCE)

                if button_rects[2].collidepoint(mouse_pos):
                    player1.weapon = weapon.Weapon(filepath=axePath,weapon_type=weapon.WeaponType.AXE)

                if button_rects[3].collidepoint(mouse_pos):
                    player1.weapon = weapon.Weapon(filepath=saiPath,weapon_type=weapon.WeaponType.SAI)

                if resume_button.rect.collidepoint(mouse_pos):
                    game_paused = False
             # add this line to print the selected slot after handling events



        pygame.display.update()





# inGame()

