import pygame

class Character:
    def __init__(self, name, hp, attack, defense, speed, image_path):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.is_defending = False

    def take_damage(self, damage):
        '''
        
        '''
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack_target(self, target):
        damage = self.attack * (50 / (50 + target.defense))
        if target.is_defending:
            damage /= 2
            target.is_defending = False
        target.take_damage(damage)
