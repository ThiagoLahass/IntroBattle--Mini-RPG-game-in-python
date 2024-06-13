import pygame

class Character:
    """
    A class representing a character in the game.

    Attributes:
        name (str): The name of the character.
        hp (int): The current health points of the character.
        max_hp (int): The maximum health points of the character.
        attack (int): The attack power of the character.
        defense (int): The defense power of the character.
        speed (int): The speed of the character.
        image (pygame.Surface): The image representing the character.
        is_defending (bool): Whether the character is defending in the current turn.
    """

    def __init__(self, name, hp, attack, defense, speed, image_path):
        """
        Initializes a Character object.

        Args:
            name (str): The name of the character.
            hp (int): The health points of the character.
            attack (int): The attack power of the character.
            defense (int): The defense power of the character.
            speed (int): The speed of the character.
            image_path (str): The file path of the character's image.
        """
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
        """
        Reduces the character's health points by the specified damage amount.

        Args:
            damage (float): The amount of damage to be taken.
        """
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack_target(self, target):
        """
        Attacks the target character, causing damage based on the attacker's attack and the target's defense.

        Args:
            target (Character): The target character to be attacked.
        """
        damage = self.attack * (50 / (50 + target.defense))
        if target.is_defending:
            damage /= 2
            target.is_defending = False
        target.take_damage(damage)

    def reset_hp(self):
        self.hp = self.max_hp