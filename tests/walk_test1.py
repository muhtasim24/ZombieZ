#!/usr/bin/env python3

import pygame
from pygame.locals import *
# https://stackoverflow.com/questions/10078287/how-to-import-a-python-file-in-a-parent-directory/10078468#comment17421554_10078468
import sys
sys.path.append("../")
import player


def walk_test1():

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
	# Assert that player location moves towards the top of 
	# the screen (y == 0) when player.walk("up") is called
	player_up = player.Player(screen_center,health,health,damage,speed,screen)
	old_location = player_up.location
	player_up.walk("up")
	new_location = player_up.location
	if new_location[1] > old_location[1]:
		print("TEST WALK_1W FAILED: Player position did not move towards top of screen.")
		failed += 1
	elif new_location[0] != old_location[0]:
		print("TEST WALK_1W FAILED: Player moved in x direction when it shouldn't have.")
		failed += 1
	else:
		print("TEST WALK_1W PASSED!")
		passed += 1

	# Assert that player location moves towards the bottom of
	# the screen (y == screen_height) when player.walk("down") is called
	player_down = player.Player(screen_center,health,health,damage,speed,screen)
	old_location = player_down.location
	player_down.walk("down")
	new_location = player_down.location
	if new_location[1] < old_location[1]:
		print("TEST WALK_1S FAILED: Player position did not move towards bottom of screen.")
		failed += 1
	elif new_location[0] != old_location[0]:
		print("TEST WALK_1S FAILED: Player moved in x direction when it shouldn't have.")
		failed += 1
	else:
		print("TEST WALK_1S PASSED!")
		passed += 1

	# Assert that player location moves towards the left side of
	# the screen (x == 0) when player.walk("left") is called
	player_left = player.Player(screen_center,health,health,damage,speed,screen)
	old_location = player_left.location
	player_left.walk("left")
	new_location = player_left.location
	if new_location[0] > old_location[0]:
		print("TEST WALK_1A FAILED: Player position did not move towards left of screen.")
		failed += 1
	elif new_location[1] != old_location[1]:
		print("TEST WALK_1A FAILED: Player moved in y direction when it shouldn't have.")
		failed += 1
	else:
		print("TEST WALK_1A PASSED!")
		passed += 1

	# Assert that player location moves towards the right side of
	# the screen (x == screen_width) when player.walk("right") is called
	player_right = player.Player(screen_center,health,health,damage,speed,screen)
	old_location = player_right.location
	player_right.walk("right")
	new_location = player_right.location
	if new_location[0] < old_location[0]:
		print("TEST WALK_1D FAILED: Player position did not move towards right of screen.")
		failed += 1
	elif new_location[1] != old_location[1]:
		print("TEST WALK_1D FAILED: Player moved in y direction when it shouldn't have.")
		failed += 1
	else:
		print("TEST WALK_1D PASSED!")
		passed += 1

	return (passed, failed)
