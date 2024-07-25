import pygame.mixer
from weapon import Weapon
class SoundEffects:
    def __init__(self):
        # Initialize Pygame mixer module
        pygame.mixer.init()

        # Load sound effects for each weapon
        self.sword_attack_sound = pygame.mixer.Sound('sword_attack.wav')
        self.axe_attack_sound = pygame.mixer.Sound('axe_sound.wav')
        self.sai_attack_sound = pygame.mixer.Sound('sai_sound.wav')
        self.lance_attack_sound = pygame.mixer.Sound('lance_sound.wav')
       
    # Play the sound effect for the specified weapon
    def play_attack_sound(self, weapon):
        if weapon.weapon_type == weapon.weapon_type.SWORD:
            self.sword_attack_sound.play()
            print("attacking!")
        elif weapon.weapon_type==weapon.weapon_type.AXE:
            self.axe_attack_sound.play()
            print("attacking!")
        elif weapon.weapon_type==weapon.weapon_type.SAI:
            self.sai_attack_sound.play()
            print("attacking!")
        elif weapon.weapon_type==weapon.weapon_type.LANCE:
            self.lance_attack_sound.play()
            print("attacking!")

        else:
            # If an invalid weapon is specified, do nothing
            pass
    
    def play_ability_cast_sound(self,weapon):
        if weapon == 'sword':
            self.dragonblade_cast_sound.play()
        #for other abilities
        else:
            # If an invalid weapon is specified, do nothing
            pass

    def play_ability_end_sound(self,weapon):
        if weapon == 'sword':
            self.dragonblade_within_sound.play()
        #for other abilities
        else:
            # If an invalid weapon is specified, do nothing
            pass
    
    def play_ability_within_sound(self,weapon):
        if weapon == 'sword':
            self.dragonblade_within_sound.play()
        #for other abilities
        else:
            # If an invalid weapon is specified, do nothing
            pass

    
    
