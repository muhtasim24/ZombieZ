#!/usr/bin/env python3

import pygame
from pygame.locals import *
# https://stackoverflow.com/questions/10078287/how-to-import-a-python-file-in-a-parent-directory/10078468#comment17421554_10078468
import sys
sys.path.append("../")
import player


def run_test3():
	screen_width = 1920
	screen_height = 1080
	flags = pygame.SCALED | pygame.RESIZABLE
	screen = pygame.display.set_mode((screen_width, screen_height), flags)
	pygame.display.set_caption("run_test1")
	screen_center = (screen_width/2, screen_height/2) #center point of the screen
	health = 100
	damage = 2
	speed = 3
	run_speed = speed * 2  ##CHANGE THIS IF REAL RUN SPEED CALCULATION CHANGES##
	
	passed = 0
	failed = 0

	# Assert that player cannot attack while its state is "running"
	player1 = player.Player(screen_center,health,health,damage,speed,screen)
	player1.state = "running"
	retval = player1.attack_enemy() #should return False
	if retval:
		print("TEST RUN_3 FAILED: Player was able to attack while running.")
		failed += 1
	else:
		print("TEST RUN_3 PASSED!")
		passed += 1

	return (passed, failed)