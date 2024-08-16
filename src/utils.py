import pygame

pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Utils")

def resize_image(image, scale):
    new_width = int(image.get_width() * scale)
    new_height = int(image.get_height() * scale)
    resized_image = pygame.transform.scale(image, (new_width, new_height))
    return resized_image

def rotate_image(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    return rotated_image

# Carregar a imagem do sprite
sprite_path = "media/Weapons/orb.png"
sprite = pygame.image.load(sprite_path).convert_alpha()
angle = 180
scale = 0.5

# new_image = rotate_image(sprite, angle)
new_image = resize_image(sprite, scale)

pygame.image.save(new_image, sprite_path)
