import pygame


################
# Menu Classes #
################
class Button():
    def __init__(self, screen, text, font, font_color, button_color, button_highlight_color, location, width, height):
        self.screen = screen
        self.text = font.render(text, True, font_color)
        self.button_color = button_color
        self.button_highlight_color = button_highlight_color
        self.button_rect = pygame.Rect(0, 0, width, height)
        self.button_rect.center = location
        self.text_rect = self.text.get_rect(center = self.button_rect.center)
        self.highlight = False

    def draw(self):
        pygame.draw.rect(self.screen, self.button_highlight_color if self.highlight else self.button_color, self.button_rect)
        self.screen.blit(self.text, self.text_rect)

class Text():
    def __init__(self, screen, text, font, color, location):
        self.screen = screen
        self.text = font.render(text, True, color)
        self.text_rect = self.text.get_rect(center=location)

    def draw(self):
        self.screen.blit(self.text, self.text_rect)


########
# Menu #
########
def game_over_menu(screen, stats):
    pygame.display.set_caption("Game Over Menu")

    # Compute the maximum number of digits for the player stats
    max_len = 0
    for label, stat in stats.items():
        max_len = max(len(str(stat)), max_len)

    # Create the text objects that will be displayed on the menu
    text_objects = {
        "game_over": Text(screen, text="Game Over", font=pygame.font.SysFont("arialblack",200), color=(255,0,0), location=(screen.get_width()/2, screen.get_height()*0.2)),
        "rounds": Text(screen, text=f"Rounds Survived: {format(stats['rounds'], f'0{max_len}d')}", font=pygame.font.SysFont(None, 100), color=(255,255,255), location=(screen.get_width()/2, screen.get_height()*0.35)),
        "kills": Text(screen, text=f"Enemies Killed: {format(stats['kills'], f'0{max_len}d')}", font=pygame.font.SysFont(None,100), color=(255,255,255), location=(screen.get_width()/2, screen.get_height()*0.425)),
        "dmg_taken": Text(screen, text=f"Damage Taken: {format(stats['dmg_taken'], f'0{max_len}d')}", font=pygame.font.SysFont(None,100), color=(255,255,255), location=(screen.get_width()/2, screen.get_height()*0.5)),
        "health_recovered": Text(screen, text=f"Damage Dealt: {format(stats['dmg_dealt'], f'0{max_len}d')}", font=pygame.font.SysFont(None,100), color=(255,255,255), location=(screen.get_width()/2, screen.get_height()*0.575))
    }
    
    # Align the statistics text objects
    avg_right = 0
    for label, text in text_objects.items():
        if label != 'game_over':
            avg_right += text.text_rect.right
    avg_right /= (len(text_objects)-1)
    for label, text in text_objects.items():
        if label != 'game_over':
            text.text_rect.right = avg_right

    # Create the buttons that will be displayed on the menu
    buttons = {
        "restart":  Button(screen, text="Restart Game",     font=pygame.font.Font(None,60), font_color=(255,255,255), button_color=(255,0,0), button_highlight_color=(255,100,100), location=(screen.get_width()/2, screen.get_height()*0.725), width=400, height=100),
        "quit":     Button(screen, text="Quit To Desktop",  font=pygame.font.Font(None,60), font_color=(255,255,255), button_color=(255,0,0), button_highlight_color=(255,100,100), location=(screen.get_width()/2, screen.get_height()*0.85),  width=400, height=100)
    }

    in_menu = True
    action = None
    while in_menu:
        # EventQueue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # Handle button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button_action, button in buttons.items():
                    if button.button_rect.collidepoint(mouse_pos):
                        action = button_action
                        in_menu = False

            # Highlight buttons when mouse hovers
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons.values():
                    button.highlight = button.button_rect.collidepoint(mouse_pos)
            
        # Draw Menu
        screen.fill("black")
        for text in text_objects.values():
            text.draw()
        for button in buttons.values():
            button.draw()
        pygame.display.flip()

    # Close Game Over menu and handle action
    if action == "restart":
        from game_instance import GameInstance
        game = GameInstance()
        game.start()
    elif action == "quit":
        pygame.quit()

