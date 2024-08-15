import pygame
import weapon

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
        skills (list): The list of skills the character has.
    """

    def __init__(self, name, hp, attack, defense, speed, image_path, weapon_sprite, weapon_speed, skills=None):
        """
        Initializes a Character object.

        Args:
            name (str): The name of the character.
            hp (int): The health points of the character.
            attack (int): The attack power of the character.
            defense (int): The defense power of the character.
            speed (int): The speed of the character.
            image_path (str): The file path of the character's image.
            weapon_sprite (str): The file path of the weapon's image.
            skills (list): The list of skills the character has.
        """
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.weapon_speed = weapon_speed
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.weapon_sprite = weapon_sprite
        self.is_defending = False
        self.num_rounds_to_use_skill = 3
        self.position = (0, 0)
        self.skills = skills if skills else []

    def decrease_num_rounds_to_use_skill(self):
        if self.num_rounds_to_use_skill > 0:
            self.num_rounds_to_use_skill -= 1

    def reset_num_rounds_to_use_skill(self):
        self.num_rounds_to_use_skill = 3

    def take_damage(self, damage):
        """
        Reduces the character's health points by the specified damage amount.

        Args:
            damage (float): The amount of damage to be taken.
        """
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack_target(self, target, all_sprites_group):
        """
        Attacks the target character, causing damage based on the attacker's attack and the target's defense.
        Also launches a weapon towards the target.

        Args:
            target (Character): The target character to be attacked.
            all_sprites_group (pygame.sprite.Group): The group of all sprites for adding the weapon.
        """
        # Create and shoot the weapon
        character_weapon = weapon.Weapon(start_pos=self.position, target_pos=target.position, weapon_sprite=self.weapon_sprite, speed=self.weapon_speed)
        all_sprites_group.add(character_weapon)
        print(character_weapon)
        print(all_sprites_group)

        # Calculate damage
        defense_value = target.defense
        if target.is_defending:
            defense_value *= 2
            target.is_defending = False
        
        damage = self.attack * (50 / (50 + defense_value))

        # Apply damage to the target
        return damage

    def reset_hp(self):
        self.hp = self.max_hp

    # Skill methods
    def wizard_spell(self, enemies, all_sprites_group):
        """
        Deals damage to all enemies.

        Args:
            enemies (list): List of enemy characters.
            all_sprites_group (pygame.sprite.Group): The group of all sprites for adding the weapon.
        """
        damages = []
        for enemy in enemies:
            damage = self.attack_target(enemy, all_sprites_group)
            damages.append(damage)
        
        action = f'{self.name} is dealing damage to all enemies!'

        return damages, action

    def paladin_protect(self, allies):
        """
        Increases defense with 5 points of all allies.

        Args:
            allies (list): List of ally characters.
        """
        for ally in allies:
            ally.defense += 5

        action = f'{self.name} is increasing +5 defense points of all allies!'

        return action

    def priest_heal(self, allies):
        """
        Heals all ally in 50% of his life.

        Args:
            ally (Character): The ally to heal.
        """
        for ally in allies:
            heal_amount = ally.max_hp * 0.5
            ally.hp += heal_amount
            if ally.hp > ally.max_hp:
                ally.hp = ally.max_hp

        action = f'{self.name} is increasing hp of all allies in +50% of his max hp!'

        return action
    
    def hunter_marked_shot(self, target, all_sprites_group):
        """
        Marks a target, increasing the damage done to that target and decreasing its defense value by 5 points.

        Args:
            target (Character): The target character.
            all_sprites_group (pygame.sprite.Group): The group of all sprites for adding the weapon.
        """
        damage = self.attack_target(target, all_sprites_group) * 1.3
        target.defense -= 5

        action = f'{self.name} is attacking {target.name} with +30% damage and taking 5 defense points of him!'

        return damage, action

    def rogue_special_attack(self, target, all_sprites_group):
        """
        Deals extra damage based on the target's lost health (lost health * 0.3).
        
        Args:
            target (Character): The target character.
            all_sprites_group (pygame.sprite.Group): The group of all sprites for adding the weapon.
        """
        lost_health = target.max_hp - target.hp
        damage = self.attack_target(target, all_sprites_group) + (lost_health * 0.3)

        action = f'{self.name} attack {target.name} with +30% extra damage of his lost health!'

        return damage, action

    def skeleton_bone_crush(self, target, all_sprites_group):
        """
        Deals significant damage (more 50% of his attack value) to a single target.

        Args:
            target (Character): The target character.
            all_sprites_group (pygame.sprite.Group): The group of all sprites for adding the weapon.
        """
        damage = self.attack_target(target, all_sprites_group) * 1.5

        action = f'{self.name} is attacking {target.name} with +50% damage!'

        return damage, action

    def necromancer_dark_revival(self, ally, enemies):
        """
        Revives a fallen ally with full health.

        Args:
            ally (Character): The ally to revive.
            enemies (list): List of enemy characters.
        """
        enemies.append(ally)
        ally.hp = ally.max_hp

        action = f'{self.name} is reliving {ally.name}!'

        return action