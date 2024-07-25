#!/usr/bin/env python3

import pygame
from pygame.locals import *
# https://stackoverflow.com/questions/10078287/how-to-import-a-python-file-in-a-parent-directory/10078468#comment17421554_10078468
import sys
sys.path.append("../")
import player


def walk_test2():

	screen_width = 1920
	screen_height = 1080
	flags = pygame.SCALED | pygame.RESIZABLE
	screen = pygame.display.set_mode((screen_width, screen_height), flags)
	pygame.display.set_caption("walk_test1")
	screen_center = (screen_width/2, screen_height/2) #center point of the screen
	health = 100
	damage = 2
	speed = 3
	
	passed = 0
	failed = 0

	# Assert that player location moves up on the screen the correct distance
	player_up = player.Player(screen_center,health,health,damage,speed,screen)
	old_location = player_up.location
	player_up.walk("up")
	new_location = player_up.location
	if old_location[1] - new_location[1] != speed:
		print("TEST WALK_2W FAILED: Player position did not move correct distance upwards.")
		failed += 1
	else:
		print("TEST WALK_2W PASSED!")
		passed += 1

	# Assert that player location moves down on the screen the correct distance
	player_down = player.Player(screen_center,health,health,damage,speed,screen)
	old_location = player_down.location
	player_down.walk("down")
	new_location = player_down.location
	if new_location[1] - old_location[1] != speed:
		print("TEST WALK_2S FAILED: Player position did not move correct distance downwards.")
		failed += 1
	else:
		print("TEST WALK_2S PASSED!")
		passed += 1

	# Assert that player location moves left on the screen the correct distance
	player_left = player.Player(screen_center,health,health,damage,speed,screen)
	old_location = player_left.location
	player_left.walk("left")
	new_location = player_left.location
	if old_location[0] - new_location[0] != speed:
		print("TEST WALK_2A FAILED: Player position did not move correct distance to the left.")
		failed += 1
	else:
		print("TEST WALK_2A PASSED!")
		passed += 1

	# Assert that player location moves right on the screen the correct distance
	player_right = player.Player(screen_center,health,health,damage,speed,screen)
	old_location = player_right.location
	player_right.walk("right")
	new_location = player_right.location
	if new_location[0] - old_location[0] != speed:
		print("TEST WALK_2D FAILED: Player position did not move correct distance to the right.")
		failed += 1
	else:
		print("TEST WALK_2D PASSED!")
		passed += 1

	return (passed, failed)
