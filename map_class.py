import os
import pygame
import player
import enum
from pygame.locals import *

ScreenEdge = enum.Enum('ScreenEdge', 'NONE TOP BOTTOM LEFT RIGHT')

class Map(pygame.sprite.Sprite):
    def __init__(self, filename, location, scale=1, colorkey=None):
        pygame.sprite.Sprite.__init__(self)
        self.filename = filename
        self.location = location
        self.scale = scale
        self.colorkey = colorkey
        self.size = (0,0) #variable will be set when load_map is called

    def load_map(self):
        # Load image from file
        file_path = os.path.abspath(self.filename)
        map_img = pygame.image.load(file_path)

        # Scale sprite to correct size
        self.size = map_img.get_size()
        self.size = (self.size[0]*self.scale, self.size[1]*self.scale)
        sprite = pygame.transform.scale(map_img, self.size)

        # Set colorkey, i.e. color used to represent transparent pixels
        if self.colorkey is not None:
            if self.colorkey == -1:
                # Use color of top-left-most pixel as colorkey
                colorkey = map_img.get_at((0,0))
            map_img.set_colorkey(self.colorkey, pygame.RLEACCEL)

        return map_img

    """
    Built in scroll function is buggy, trying this instead.
    Undefined behavior if load_map has not been called yet
    Returns True if map will scroll, False otherwise.
    TODO: 
    - fix framerate? not sure if it's actually an issue at this point
    - fix dodge animation to make less buggy? seems to be only issue so far
    """
    def scroll_map(self, player1: player.Player):
        # Check state of player to get speed
        speed = 0;
        if player1.state == player.PlayerState.WALKING:
            speed = player1.speed
        elif player1.state == player.PlayerState.RUNNING:
            speed = player1.run_speed
        elif player1.state == player.PlayerState.DODGING:
            speed = player1.dodge_speed
        else:
            return False

        # Check direction of player movement by seeing if the location of the player
        # is at the bounds of the screen, and if so, which screen edge (top, bottom, left, right).
        # Enum for screen edge is defined at top of this file.
        current_edge = ScreenEdge.NONE
        screen = player1.screen
        #also check if player is moving in correct direction; return if not
        if player1.top <= 0 and player1.direction == player.PlayerDirection.UP:
            current_edge = ScreenEdge.TOP
        elif player1.bottom >= screen.get_height() and player1.direction == player.PlayerDirection.DOWN:
            current_edge = ScreenEdge.BOTTOM
        elif player1.left <= 0 and player1.direction == player.PlayerDirection.LEFT:
            current_edge = ScreenEdge.LEFT
        elif player1.right >= screen.get_width() and player1.direction == player.PlayerDirection.RIGHT:
            current_edge = ScreenEdge.RIGHT
        else:
            return False

        # Move map, checking bounds to make sure that scrolling stops at end of map
        offset = 20  # helps get rid of weird artifacting if player tries to move to a position outisde of the map bounds, specifically while dodging
        top_bound = 0 - offset
        bottom_bound = screen.get_height() - self.size[1] + offset
        left_bound = 0 - offset
        right_bound = screen.get_width() - self.size[0] + offset
        if speed != 0 and current_edge != ScreenEdge.NONE:
            if current_edge == ScreenEdge.TOP and self.location[1] <= top_bound:
                self.location = (self.location[0], self.location[1] + speed)
            elif current_edge == ScreenEdge.BOTTOM and self.location[1] >= bottom_bound:
                self.location = (self.location[0], self.location[1] - speed)
            elif current_edge == ScreenEdge.LEFT and self.location[0] <= left_bound:
                self.location = (self.location[0] + speed, self.location[1])
            elif current_edge == ScreenEdge.RIGHT and self.location[0] >= right_bound:
                self.location = (self.location[0] - speed, self.location[1])
            return True