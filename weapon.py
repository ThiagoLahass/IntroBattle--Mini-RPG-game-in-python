import pygame
import math

class Weapon(pygame.sprite.Sprite):
    """
    A class representing a projectile weapon in the game.

    Attributes:
        velocity (tuple[float, float]): The velocity vector of the weapon, determined by its speed and the direction towards the target position.
        image (pygame.Surface): The rotated image of the weapon, based on the angle towards the target.
        rect (pygame.Rect): The rectangular area that defines the weapon's position and dimensions, centered at the start position.
        target_pos (tuple[int, int]): The (x, y) coordinates of the target position.
        speed (int or float): The speed at which the weapon travels towards the target.
    """
    def __init__(self, start_pos, target_pos, weapon_sprite, speed=10):
        """
        Initializes a Weapon object.

        Args:
            start_pos (tuple[int, int]): The starting (x, y) position of the weapon.
            target_pos (tuple[int, int]): The (x, y) coordinates of the target position where the weapon is aimed.
            weapon_sprite (str): The file path to the sprite image of the weapon.
            speed (int or float): The speed at which the weapon moves towards the target. Default is 10.
        """
        super().__init__()
        # Calculate the direction to the target
        x_diff = target_pos[0] - start_pos[0]
        y_diff = target_pos[1] - start_pos[1]
        angle = math.atan2(y_diff, x_diff)
        self.velocity = (speed * math.cos(angle), speed * math.sin(angle))
        weapon_surface = pygame.image.load(weapon_sprite).convert_alpha()
        self.image = rotated_sprite(weapon_surface, math.degrees(-angle))
        self.rect = self.image.get_rect(center=start_pos)
        self.target_pos = target_pos
        self.speed = speed

    def update(self):
        """
        Updates the position of the Weapon object based on its velocity.

        This method moves the weapon by updating its position using its velocity vector and checks if the weapon has reached its target position. If the weapon is within a certain distance of the target, it is removed from the sprite group.
        """
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        print(f"x = {self.rect.x}")
        print(f"y = {self.rect.y}")

        # Check if the weapon has reached the target
        if ( abs(self.rect.x - self.target_pos[0]) < 30 and abs(self.rect.y >= self.target_pos[1]) < 30):
            print(f"Weapon collided on {self.target_pos}")
            self.kill()  # Remove the weapon from the sprite group
    
# Função para rotacionar e desenhar o sprite
def rotated_sprite(image, angle):
    """
    Rotates a given sprite image by a specified angle.

    Args:
        image (pygame.Surface): The image surface to be rotated.
        angle (float): The angle (in degrees) by which the image will be rotated.

    Returns:
        pygame.Surface: The rotated image surface.
    """
    rotated_image = pygame.transform.rotate(image, angle)
    return rotated_image