#!/usr/bin/env python3

import os
import math
import pygame
from pygame.locals import *
from enum import Enum

#Enumeration for weapon typing
WeaponType = Enum('WeaponType', ['SWORD', 'AXE', 'LANCE', 'SAI'])

def load_sprite(name, colorkey=None, scale=1):
	# Load image from file
	file_path = os.path.abspath(name)
	sprite = pygame.image.load(file_path)

	# Scale sprite to correct size
	size = sprite.get_size()
	size = (size[0]*scale, size[1]*scale)
	sprite = pygame.transform.scale(sprite, size)

	# Set colorkey, i.e. color used to represent transparent pixels
	if colorkey is not None:
		if colorkey == -1:
			# Use color of top-left-most pixel as colorkey
			colorkey = sprite.get_at((0,0))
		sprite.set_colorkey(colorkey, pygame.RLEACCEL)

	return sprite, sprite.get_rect(), size[0], size[1]

class Weapon(pygame.sprite.Sprite):

	#File path for each weapon, should be based on what weapon player selects
	# filepath="Assets/Lance/lanceRight.png"
	# filepath="Assets/Sai/saiRight.png"
	# filepath="Assets/Axe/axeRight.png"
	sword_path="Assets/Sword/swordRight.png"

	def __init__(self, filepath=sword_path, weapon_type=WeaponType.SWORD, scale=1, colorkey=None):
		#Call parent class constructor to create Sprite for weapon
		pygame.sprite.Sprite.__init__(self)

		# Load sprite from image
		self.image, self.rect, self.width, self.height = load_sprite(filepath, colorkey, scale)

		self.weapon_type = weapon_type

		# Animation variables
		self.anim_timer = 0
		self.angle = 0
		self.og_image = self.image
	
	def update(self, mouse_pos, pivot):
		self.lookAt(mouse_pos)
		self.animate(mouse_pos, pivot)
		#print(self.weapon_type)

	def lookAt(self, mouse_pos):
		if not self.rect.collidepoint(mouse_pos):
 			# Calculate direction vector
			dx = mouse_pos[0] - self.rect.centerx
			dy = mouse_pos[1] - self.rect.centery
			vec = pygame.math.Vector2(dx, dy)

			# Calculate look at rotation
			angle = math.degrees(math.atan2(dy, dx))
			self.angle = angle

	def animate(self, mouse_pos, pivot):
		if not (self.rect.collidepoint(mouse_pos)):
			# The purpose of the animation timer is to control the speed of the animation
			if self.anim_timer == 0:
				# Rotate the image
				self.image = pygame.transform.rotate(self.og_image, -self.angle)
				self.rect.center = pivot

			self.anim_timer += 1

			anim_delay = 5
			if self.anim_timer >= anim_delay:
				self.anim_timer = 0