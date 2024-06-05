import pygame
from character import Character
from game import selection_screen, battle, draw_text

# Initialize Pygame
pygame.init()

# Music settings
pygame.mixer.music.load("IntroBattle\media\Sons\music.wav")
pygame.mixer.music.play()

# Window settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("IntroBattle RPG")

# Defining player characters
heroes = [
    Character("Paladino", 200, 30, 20, 10, "IntroBattle/media/Personagens/paladino.png"),
    Character("Wizard", 120, 40, 10, 20, "IntroBattle/media/Personagens/wizard.png"),
    Character("Hunter", 150, 35, 15, 25, "IntroBattle/media/Personagens/hunter.png"),
    Character("Rogue", 100, 20, 10, 30, "IntroBattle/media/Personagens/rogue.png")
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
    player_characters = selection_screen(screen, heroes)

    # Battle
    battle(screen, player_characters, enemies)

    # Game Over
    screen.fill((0, 0, 0))
    draw_text("Game Over", pygame.font.Font(None, 74), (255, 0, 0), screen, 400, 300)
    pygame.display.flip()
    pygame.time.wait(3000)

if __name__ == "__main__":
    main()

# Quit Pygame
pygame.quit()
