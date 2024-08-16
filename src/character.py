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

    def __init__(self, name, hp, attack, defense, speed, image_path, weapon_sprite, weapon_speed, skills=None, num_rounds_to_use_skill=3):
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
        self.num_rounds_to_use_skill = num_rounds_to_use_skill
        self.position = (0, 0)
        self.skills = skills if skills else []

    def decrease_num_rounds_to_use_skill(self):
        """
        Decreases the number of rounds remaining before the character can use their skill again.

        This method decreases the `num_rounds_to_use_skill` attribute by 1, but only if it is greater than 0.
        """
        
        # Check if there are rounds left before the skill can be used
        if self.num_rounds_to_use_skill > 0:
            # Decrease the number of rounds by 1
            self.num_rounds_to_use_skill -= 1


    def reset_num_rounds_to_use_skill(self):
        """
        Resets the number of rounds required before the character can use their skill.

        This method sets the `num_rounds_to_use_skill` attribute back to the initial value of 3 rounds.
        """
        
        # Reset the number of rounds to the default value (3)
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
        Attacks the target character, dealing damage based on the attacker's attack and the target's defense.
        Also creates and launches a weapon towards the target.

        Args:
            target (Character): The target character who will receive the attack.
            all_sprites_group (pygame.sprite.Group): The group of all sprites where the weapon associated with the attack will be added.

        Returns:
            float: The amount of damage dealt to the target.
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
        Deals damage to all enemies in the list.

        The function iterates through a list of enemies, applying damage to each one and collecting the damage values.

        Args:
            enemies (list[Character]): A list of enemy characters to be damaged.
            all_sprites_group (pygame.sprite.Group): The group of all sprites where the weapon associated with the spell will be added.

        Returns:
            tuple:
                - damages (list[float]): A list of damage values dealt to each enemy.
                - action (str): A description of the spell action performed.
        """
        damages = []
        for enemy in enemies:
            damage = self.attack_target(enemy, all_sprites_group)
            damages.append(damage)
        
        action = f'{self.name} is dealing damage to all enemies!'

        return damages, action

    def paladin_protect(self, allies):
        """
        Increases the defense of all allies by 5 points.

        The function iterates through a list of allies, increasing each ally's defense attribute by 5 points.

        Args:
            allies (list[Character]): A list of ally characters whose defense will be increased.

        Returns:
            str: A description of the defense boost action performed.
        """
        for ally in allies:
            ally.defense += 5

        action = f'{self.name} is increasing +5 defense points of all allies!'

        return action

    def priest_heal(self, allies):
        """
        Heals all allies by 50% of the Priest's maximum health.

        The function iterates through a list of allies, increasing each ally's health by 50% of the Priest's maximum health. If the healing amount exceeds the ally's maximum health, their health is capped at the maximum.

        Args:
            allies (list[Character]): A list of ally characters to be healed.

        Returns:
            str: A description of the healing action performed.
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
        Executes the Hunter's marked shot, increasing the damage dealt to the target.

        The damage is increased by 30%.

        Args:
            target (Character): The target character who will receive the attack and have their defense reduced.
            all_sprites_group (pygame.sprite.Group): The group of all sprites where the weapon associated with the attack will be added.

        Returns:
            tuple:
                - damage (float): The total amount of damage dealt to the target, including the increased damage from the marked shot.
                - action (str): A description of the marked shot attack and its effects.
        """
        damage = self.attack_target(target, all_sprites_group) * 1.3
        target.defense -= 5

        action = f'{self.name} is attacking {target.name} with +30% damage and taking 5 defense points of him!'

        return damage, action

    def rogue_special_attack(self, target, all_sprites_group):
        """
        Executes the Rogue's special attack, dealing extra damage based on the target's lost health.

        The extra damage is calculated as 30% of the target's lost health.

        Args:
            target (Character): The target character who will receive the damage.
            all_sprites_group (pygame.sprite.Group): The group of all sprites where the weapon associated with the attack will be added.

        Returns:
            tuple:
                - damage (float): The total amount of damage dealt to the target, including extra damage from lost health.
                - action (str): A description of the special attack performed.
        """
        lost_health = target.max_hp - target.hp
        damage = self.attack_target(target, all_sprites_group) + (lost_health * 0.3)

        action = f'{self.name} attack {target.name} with +30% extra damage of his lost health!'

        return damage, action

    def skeleton_bone_crush(self, target, all_sprites_group):
        """
        Executes the Bone Crush attack, dealing significant damage to a single target.

        This attack deals more than 50% additional damage compared to the character's regular attack value.

        Args:
            target (Character): The target character to whom the damage will be applied.
            all_sprites_group (pygame.sprite.Group): The group of all sprites where the weapon associated with the attack will be added.

        Returns:
            tuple:
                - damage (float): The amount of damage dealt to the target.
                - action (str): A description of the attack action performed.
        """
        damage = self.attack_target(target, all_sprites_group) * 1.5

        action = f'{self.name} is attacking {target.name} with +50% damage!'

        return damage, action

    def necromancer_dark_revival(self, ally, enemies, revive=True):
        """
        Revives a fallen ally or restores an ally's health to full.

        Args:
            ally (Character): The ally to revive or restore health to.
            enemies (list): List of enemy characters.
            revive (bool, optional): Whether to revive a fallen ally (True) or restore health to a living ally (False). Default is True.

        Returns:
            str: A string describing the action performed.
        """
        if revive:
            enemies.append(ally)  # Add the revived ally to the list of enemies
            ally.hp = ally.max_hp  # Set the ally's health to full
            action = f"{self.name} is reviving {ally.name}!"  # Action message for reviving
        else:
            ally.hp = ally.max_hp  # Restore the ally's health to full
            action = f"{self.name} is restoring {ally.name}'s health!"  # Action message for health restoration

        return action  # Return the action message
