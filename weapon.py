import pygame
import math
import imageio

class Weapon(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, weapon_sprite, speed=10):
        super().__init__()
        self.image = pygame.image.load(weapon_sprite).convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.target_pos = target_pos
        self.speed = speed

        # Calculate the direction to the target
        x_diff = target_pos[0] - start_pos[0]
        y_diff = target_pos[1] - start_pos[1]
        angle = math.atan2(y_diff, x_diff)
        self.velocity = (speed * math.cos(angle), speed * math.sin(angle))

    def update(self):
        print("Update 2")
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        print(f"x = {self.rect.x}")
        print(f"y = {self.rect.y}")

        # Check if the weapon has reached the target
        # if self.rect.collidepoint(self.target_pos):
        if ( abs(self.rect.x - self.target_pos[0]) < 10 and abs(self.rect.y >= self.target_pos[1]) < 10):
            print(f"Weapon collided on {self.target_pos}")
            self.kill()  # Remove the weapon from the sprite group