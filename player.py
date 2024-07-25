#!/usr/bin/env python3
"""
references: 
[0] https://www.pygame.org/docs/ref/surface.html#pygame.Surface.fill
[1] https://www.pygame.org/docs/ref/rect.html
[2] https://www.pygame.org/docs/ref/sprite.html
[3] https://www.pygame.org/docs/tut/tom_games4.html
[4] https://www.pygame.org/docs/tut/ChimpLineByLine.html
[5] https://docs.python.org/3/library/os.path.html
"""
import os
import pygame
from pygame.locals import *
import zombie
import json
import enum
from Sound import SoundEffects

PlayerState = enum.Enum('PlayerState', 'STILL WALKING RUNNING DODGING')
PlayerDirection = enum.Enum('PlayerDirection', "NONE UP DOWN LEFT RIGHT")
import math
import weapon

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


class Player(pygame.sprite.Sprite):
	"""
	Explanation of inputs:
		location = (x postion, y position)
		cur_health = current health of the player
		max_health = maximum health the player can have
		damage = amount of damage done to enemies when attacking
		speed = number of pixels player moves while walking.
		screen = the screen to draw to
	"""
	def __init__(self, location, cur_health, max_health, damage, speed, screen, stats=None):
		# Call parent class constructor to create Sprite for player
		pygame.sprite.Sprite.__init__(self)

		# Load sprite from image
		self.image, self.rect, self.width, self.height = load_sprite("Assets/Player.png", -1)



		#From [2]:
		# Fetch the rectangle object that has the dimensions of the image
		# Update the position of this object by setting the values of rect.x and rect.y
		self.rect = self.image.get_rect()
		# Note tht pygame starts drawing from the top left, so we need to subtract half of the width/height
		# in order for the rectangle to be centered
		self.rect.x = location[0] - self.width/2
		self.rect.y = location[1] - self.height/2

		

		# Initialize player state (an enum defined with broader scope at the top of this file) 
		# containing the current action of the player.
		self.state = PlayerState.STILL
		self.direction = PlayerDirection.NONE

		# Initialize player stats
		self.location = location
		self.cur_health = cur_health
		self.max_health = max_health
		self.damage = damage
		self.speed = speed
		self.run_speed = speed * 2
		self.dodge_speed = speed * 3
		self.screen = pygame.display.get_surface()
		if stats == None:
			self.stats = {
				'rounds': 0,
				'kills': 0,
				'dmg_taken': 0,
				'dmg_dealt': 0
			}
		else:
			self.stats = stats


		# Set bounds of sprite to make collision more precise
		self.left = self.location[0] - self.width/2
		self.right = self.location[0] + self.width/2
		self.top = self.location[1] - self.height/2
		self.bottom = self.location[1] + self.height/2

        # Variables to regulate animations
		self.original_image = self.image
		self.dodge_timer = 0
		self.dodge_stage = 0
		self.animating_dodge = False
		self.dodge_sign = 0
		self.dodge_direction = "none"
		self.angle = 0



		# Load default weapon (sword)
		self.weapon = weapon.Weapon()

		#create hitboxes
		self.hitbox = self.rect.copy()
		self.attackbox = self.rect.copy()
		self.attackbox.top = self.rect.bottom
		padding = 3
		self.attackbox.height = max(self.weapon.width,self.weapon.height) + padding

		# Need this variable to ensure that dodge only occurs once per press of the Alt key
		self.dodge_requested = False

		#Load sound effect
		self.sound_effects = SoundEffects()


	def update(self, is_dev_mode):
		self.get_input()
		self.draw_health_bar()

		# Update rect position on screen
		self.rect.x = self.location[0] - self.width/2
		self.rect.y = self.location[1] - self.height/2

		# Update bounds
		self.left = self.location[0] - self.width/2
		self.right = self.location[0] + self.width/2
		self.top = self.location[1] - self.height/2
		self.bottom = self.location[1] + self.height/2

		self.draw_weapon()
		self.update_hitbox(is_dev_mode)
		self.update_attackbox(is_dev_mode)
		
        # Animate dodge if necessary
		if self.animating_dodge:
			self.animate_dodge()

	def animate_dodge(self):
		max_stage = 10
		anim_delay = 2
		rotation = 360.0 / max_stage

		# Timer controls the speed of the animation
		if self.dodge_timer == 0:
			# Update stage
			self.dodge_stage += 1
			if self.dodge_stage > max_stage:
				self.dodge_stage = 0
				self.dodge_sign = 0
				self.animating_dodge = False
				self.dodge_requested = False
				self.dodge_direction = "none"
			# Rotate the image to match the enemy's rotation
			self.image = pygame.transform.rotate(self.original_image, self.dodge_signself.dodge_stagerotation)

		self.dodge_timer += 1

		if self.dodge_timer >= anim_delay:
			self.dodge_timer = 0

	def dodge(self, direction):
		if self.state != PlayerState.DODGING:
			self.state = PlayerState.DODGING

		# Update player location
		new_x = self.location[0]
		new_y = self.location[1]
		if direction == "up" and self.top > 0:
			new_y -= self.dodge_speed
			self.dodge_sign = 1
		elif direction == "down" and self.bottom < self.screen.get_height():
			new_y += self.dodge_speed
			self.dodge_sign = -1
		elif direction == "left" and self.left > 0:
			new_x -= self.dodge_speed
			self.dodge_sign = 1
		elif direction == "right" and self.right < self.screen.get_width():
			new_x += self.dodge_speed
			self.dodge_sign = -1
		# These edge cases make sure that dodge still animates at screen border
		elif self.top <= 0 or self.left <= 0:
			self.dodge_sign = 1
		elif self.bottom >= self.screen.get_height() or self.right >= self.screen.get_width():
			self.dodge_sign = -1
		self.location = (new_x, new_y)
		self.animating_dodge = True
		self.dodge_direction = direction



	def draw_health_bar(self):

		# Draw health bar border
		color_white = (255, 255, 255)
		border_position = (70, 20)
		border_size = (350, 28)
		border = pygame.Rect(border_position, border_size)
		pygame.draw.rect(self.screen, color_white, border)


		#Initialize some variables for the health bar and its background
		offset = 2
		bar_position = (border_position[0]+offset,border_position[1]+offset)
		bar_size = (border_size[0]-(offset*2), border_size[1]-(offset*2))
		
		# Draw health bar background
		color_red = (100, 0, 0)
		health_background = pygame.Rect(bar_position, bar_size)
		pygame.draw.rect(self.screen, color_red, health_background)

		# Draw health bar based on current health
		color_green = (0, 200, 50)
		health_percentage = self.cur_health/self.max_health
		bar_size = (bar_size[0]*health_percentage, bar_size[1])
		health_bar = pygame.Rect(bar_position, bar_size)
		pygame.draw.rect(self.screen, color_green, health_bar)
		
		# Write "HP" next to bar
		if pygame.font:
			font = pygame.font.Font(None, 36)
			text_color = (255,255,255)
			text = font.render("HP", True, text_color)
			text_pos = text.get_rect(x=20,y=20)
			self.screen.blit(text, text_pos)

	def get_input(self):
		# Check for key presses
		# get_pressed returns a sequence of bools where each index corresponds to a key
		# if the key is currently pressed down, the value at that index is True
		# This is better than checking for KEYDOWN events, since you can have an action occur
		# for the entire time that the key is pressed, rather than only when it is initially pressed
		# It should also make instances where multiple keys are being pressed easier to manage
		key_presses = pygame.key.get_pressed()
		if key_presses[K_w]:
			self.direction = PlayerDirection.UP
			if key_presses[K_LSHIFT] or key_presses[K_RSHIFT]:
				self.run("up")
			elif self.dodge_requested:
				self.dodge("up")
				#self.dodge_requested = False
			else:
				self.walk("up")
		elif key_presses[K_s]:
			self.direction = PlayerDirection.DOWN
			if key_presses[K_LSHIFT] or key_presses[K_RSHIFT]:
				self.run("down")
			elif self.dodge_requested:
				self.dodge("down")
				#self.dodge_requested = False
			else:
				self.walk("down")
		elif key_presses[K_a]:
			self.direction = PlayerDirection.LEFT
			if key_presses[K_LSHIFT] or key_presses[K_RSHIFT]:
				self.run("left")
			elif self.dodge_requested:
				self.dodge("left")
				#self.dodge_requested = False
			else:
				self.walk("left")
		elif key_presses[K_d]:
			self.direction = PlayerDirection.RIGHT
			if key_presses[K_LSHIFT] or key_presses[K_RSHIFT]:
				self.run("right")
			elif self.dodge_requested:
				self.dodge("right")
				#self.dodge_requested = False
			else:
				self.walk("right")
		elif self.animating_dodge:
			self.dodge(self.dodge_direction)
		else:
			self.state = PlayerState.STILL
			self.direction = PlayerDirection.NONE

	def walk(self, direction):
		# Update player state
		if self.state != PlayerState.WALKING:
			self.state = PlayerState.WALKING

		# Update player location
		new_x = self.location[0]
		new_y = self.location[1]
		if direction == "up" and self.top > 0:
			new_y -= self.speed
		elif direction == "down" and self.bottom < self.screen.get_height():
			new_y += self.speed
		elif direction == "left" and self.left > 0:
			new_x -= self.speed
		elif direction == "right" and self.right < self.screen.get_width():
			new_x += self.speed
		self.location = (new_x, new_y)

	def run(self, direction):
		# Update player state
		if self.state != PlayerState.RUNNING:
			self.state = PlayerState.RUNNING

		# Update player location
		new_x = self.location[0]
		new_y = self.location[1]
		if direction == "up" and self.top > 0:
			new_y -= self.run_speed
		elif direction == "down" and self.bottom < self.screen.get_height():
			new_y += self.run_speed
		elif direction == "left" and self.left > 0:
			new_x -= self.run_speed
		elif direction == "right" and self.right < self.screen.get_width():
			new_x += self.run_speed
		self.location = (new_x, new_y)
	

	def request_dodge(self):
		if not self.dodge_requested:
			self.dodge_requested = True

	def animate_dodge(self):
		max_stage = 10
		anim_delay = 2
		rotation = 360.0 / max_stage

		# Timer controls the speed of the animation
		if self.dodge_timer == 0:
			# Update stage
			self.dodge_stage += 1
			if self.dodge_stage > max_stage:
				self.dodge_stage = 0
				self.dodge_sign = 0
				self.animating_dodge = False
				self.dodge_requested = False
				self.dodge_direction = "none"
			# Rotate the image to match the enemy's rotation
			self.image = pygame.transform.rotate(self.original_image, self.dodge_sign*self.dodge_stage*rotation)

		self.dodge_timer += 1

		if self.dodge_timer >= anim_delay:
			self.dodge_timer = 0

	def dodge(self, direction):
		if self.state != PlayerState.DODGING:
			self.state = PlayerState.DODGING

		# Update player location
		new_x = self.location[0]
		new_y = self.location[1]
		if direction == "up" and self.top > 0:
			new_y -= self.dodge_speed
			self.dodge_sign = 1
		elif direction == "down" and self.bottom < self.screen.get_height():
			new_y += self.dodge_speed
			self.dodge_sign = -1
		elif direction == "left" and self.left > 0:
			new_x -= self.dodge_speed
			self.dodge_sign = 1
		elif direction == "right" and self.right < self.screen.get_width():
			new_x += self.dodge_speed
			self.dodge_sign = -1
		# These edge cases make sure that dodge still animates at screen border
		elif self.top <= 0 or self.left <= 0:
			self.dodge_sign = 1
		elif self.bottom >= self.screen.get_height() or self.right >= self.screen.get_width():
			self.dodge_sign = -1
		self.location = (new_x, new_y)
		self.animating_dodge = True
		self.dodge_direction = direction

	# Returns bool for testing purposes; True if attack is possible, False otherwise
	def attack_enemy(self, enemy_group=None):
		if self.state == PlayerState.RUNNING or self.state == PlayerState.DODGING:
			return False
		else:
			for enemy in enemy_group.sprites():
				if self.attackbox.colliderect(enemy.hitbox):
					enemy.damageSelf(self.damage)
					print(self.weapon.weapon_type)
					self.sound_effects.play_attack_sound(self.weapon)
					self.stats['dmg_dealt'] += self.damage
			return True

	# Returns bool for testing purposes; True if damage is possible, False otherwise
	def damageSelf(self, damage):
		if self.state == PlayerState.DODGING:
			return False
		else:
			self.cur_health -= damage
			self.stats['dmg_taken'] += damage
			if self.cur_health <= 0:
				DEATHEVENT = pygame.USEREVENT + 4
				pygame.event.post(pygame.event.Event(DEATHEVENT))
				self.kill()
			return True
	
	def generateSaveData(self):
		save_data = {
			"location": (self.rect.left, self.rect.top),
			"rotation": 0, # There is not player rotation at the moment - 0 is a placeholder
			"current_health": self.cur_health,
			"max_health": self.max_health,
			"damage": self.damage,
			"speed": self.speed,
			"stats": self.stats
		}
		save_data_string = "--begin_player--\n" + json.dumps(save_data) + "\n\n"
		return save_data_string


	def draw_weapon(self):
		#get the position of the weapon on the screen relative to 
		#the center of the player and according to the mouse position
		#src: https://stackoverflow.com/questions/42180159/moving-a-point-along-a-circular-path-via-mouse-motion-python-pygame
		mouse_pos = pygame.mouse.get_pos()
		weapon_pos = self.rect.midbottom
		padding = self.weapon.width/2 #needed bc images are drawn from top left corner.
		center_of_rotation = (self.rect.centerx - padding, self.rect.centery - padding)
		vector = (mouse_pos[0]-center_of_rotation[0], mouse_pos[1]-center_of_rotation[1])
		distance = (vector[0]**2 + vector[1]**2)**0.5

		if distance > 0:
			weight = 0.9 #decrement to make weapon closer to player, increment to make weapon further from player
			scalar = (max(self.width,self.height)*weight) / distance
			weapon_pos = (int(round(center_of_rotation[0] + vector[0]*scalar)), int(round(center_of_rotation[1] + vector[1]*scalar)))

		pivot = self.rect.center
		self.weapon.update(mouse_pos, pivot)
		self.screen.blit(self.weapon.image, weapon_pos)


	def update_hitbox(self, is_dev_mode):
		self.hitbox = self.rect.copy()
		if is_dev_mode:
			green = (0,255,0)
			pygame.draw.rect(surface=self.screen,color=green,rect=self.hitbox,width=2)

	def update_attackbox(self, is_dev_mode):
		#get the position of the attack hitbox on the screen relative to 
		#the center of the player and according to the mouse position
		#src: https://stackoverflow.com/questions/42180159/moving-a-point-along-a-circular-path-via-mouse-motion-python-pygame
		mouse_pos = pygame.mouse.get_pos()
		attackbox_pos = self.rect.midbottom
		padding = self.weapon.width/2 #needed bc images are drawn from top left corner.
		center_of_rotation = (self.rect.centerx - padding, self.rect.centery - padding)
		vector = (mouse_pos[0]-center_of_rotation[0], mouse_pos[1]-center_of_rotation[1])
		distance = (vector[0]**2 + vector[1]**2)**0.5

		if distance > 0:
			weight = 0.9 #decrement to make weapon closer to player, increment to make weapon further from player
			scalar = (max(self.width,self.height)*weight) / distance
			attackbox_pos = (int(round(center_of_rotation[0] + vector[0]*scalar)), int(round(center_of_rotation[1] + vector[1]*scalar)))


		#create attack rect
		self.attackbox = self.rect.copy()
		self.attackbox.topleft = attackbox_pos
		padding = 3
		self.attackbox.height = max(self.weapon.width,self.weapon.height) + padding		#too lazy to think about which one is larger lol
		self.attackbox.width = max(self.weapon.width,self.weapon.height) + padding

		if is_dev_mode:
			#show rect outline
			red = (255,0,0)
			pygame.draw.rect(surface=self.screen,color=red,rect=self.attackbox,width=2)

	
