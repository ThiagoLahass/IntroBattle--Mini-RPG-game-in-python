import pygame
from character import Character
from game import selection_screen, battle, draw_text

# Initialize Pygame
pygame.init()

# Music settings
pygame.mixer.music.load("IntroBattle/media/Sons/rpg-city.mp3")
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Window settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("IntroBattle RPG")

# Load background image
background_image = pygame.image.load("IntroBattle/media/Background/background2.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# The wizard image is inverted, so we need to change it
# Load the image
image_path = "IntroBattle/media/Personagens/wizard.png"
image = pygame.image.load(image_path)
# Flip horizontally
inverted_image = pygame.transform.flip(image, True, False)
# Save the inverted image (optional)
pygame.image.save(inverted_image, "IntroBattle/media/Personagens/wizard_inverted.png")

# Defining player characters
heroes = [
    Character("Paladin", 200, 30, 20, 10, "IntroBattle/media/Personagens/paladino.png"),
    Character("Rogue", 100, 20, 10, 30, "IntroBattle/media/Personagens/rogue.png"),
    Character("Wizard", 120, 40, 10, 20, "IntroBattle/media/Personagens/wizard_inverted.png"),
    Character("Hunter", 150, 35, 15, 25, "IntroBattle/media/Personagens/hunter.png"),
    Character("Priest", 150, 35, 15, 25, "IntroBattle/media/Personagens/priest.png"),
]

# Defining enemy characters
enemies = [
    Character("Necromante", 180, 25, 20, 5, "IntroBattle/media/Personagens/necromante.png"),
    Character("Caveira", 300, 50, 30, 8, "IntroBattle/media/Personagens/caveira.png")
]

def main():
    """
    Main function to run the game.
    """
    # Character selection
    player_characters = selection_screen(screen, background_image, heroes)

    # Battle
    battle(screen, background_image, player_characters, enemies)

    # Game Over
    screen.fill((0, 0, 0))
    draw_text("Game Over", pygame.font.Font("IntroBattle/media/Fonts/Press_Start_2P/PressStart2P-Regular.ttf", 74), (255, 0, 0), screen, 200, 300)
    pygame.display.flip()
    pygame.time.wait(3000)

    pygame.quit()

if __name__ == "__main__":
    main()
