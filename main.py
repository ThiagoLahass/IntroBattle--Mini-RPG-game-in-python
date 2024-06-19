import pygame
from character import Character
from game import selection_screen, battle, finish_screen
import game

# Initialize Pygame
pygame.init()

# Music settings
pygame.mixer.music.load("media/Sons/Musics/rpg-city.mp3")
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Window settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("IntroBattle RPG")

# Load background image
background_image = pygame.image.load("media/Background/background2.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# The wizard image is inverted, so we need to change it
# Load the image
image_path = "media/Personagens/wizard.png"
image = pygame.image.load(image_path)
# Flip horizontally
inverted_image = pygame.transform.flip(image, True, False)
# Save the inverted image (optional)
pygame.image.save(inverted_image, "media/Personagens/wizard_inverted.png")

# Defining player characters
heroes = [
    Character(name="Paladin",   hp=50, attack=30, defense=20, speed=10, image_path="media/Personagens/paladino.png", weapon_sprite="media/Weapons/holy_lance.png", weapon_speed=10),
    Character(name="Rogue",     hp=50, attack=20, defense=10, speed=30, image_path="media/Personagens/rogue.png", weapon_sprite="media/Weapons/knife.png", weapon_speed=10),
    Character(name="Wizard",    hp=50, attack=40, defense=10, speed=20, image_path="media/Personagens/wizard_inverted.png", weapon_sprite="media/Weapons/fireball_blue.png", weapon_speed=10),
    Character(name="Hunter",    hp=50, attack=35, defense=15, speed=25, image_path="media/Personagens/hunter.png", weapon_sprite="media/Weapons/arrow.png", weapon_speed=10),
    Character(name="Priest",    hp=50, attack=35, defense=15, speed=25, image_path="media/Personagens/priest.png", weapon_sprite="media/Weapons/fireball_pink.png", weapon_speed=10),
]

# Defining enemy characters
enemies = [
    Character(name="Necromante",    hp=100, attack=25, defense=20, speed=5, image_path="media/Personagens/necromante_inverted.png", weapon_sprite="media/Weapons/orb.png", weapon_speed=10),
    Character(name="Caveira",       hp=100, attack=50, defense=30, speed=8, image_path="media/Personagens/skeleton_inverted.png", weapon_sprite="media/Weapons/skull.png", weapon_speed=10)
]

def main():
    """
    Main function to run the game.
    """
    quit = False
    restart = False
    menu = True

    while(True):
        if quit:
            print("Quiting...")
            pygame.quit()
            break
        elif restart:
            print("Restarting...")
            # restarting the characters
            for character in enemies:
                character.reset_hp()
            for character in player_characters:
                character.reset_hp()
            enemies_temp = enemies.copy()
            player_characters_temp = player_characters.copy()
            # Battle
            result = battle(screen, background_image, player_characters_temp, enemies_temp)
        elif menu:
            print("Menu...")
            # restarting the characters
            for character in enemies:
                character.reset_hp()
            for character in heroes:
                character.reset_hp()
            enemies_temp = enemies.copy()
            heroes_temp = heroes.copy()
            # Character selection
            player_characters = selection_screen(screen, background_image, heroes_temp)
            player_characters_temp = player_characters.copy()
            # Battle
            result = battle(screen, background_image, player_characters_temp, enemies_temp)
            print(f"'{result}'")

        option = finish_screen(result=result, screen=screen, SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT)
        if(option == "quit"):
            quit = True
            restart = False
            menu = False
        elif(option == "restart"):
            restart = True
            menu = False
            quit = False
        elif(option == "menu"):
            menu = True
            restart = False
            quit = False

    pygame.quit()

if __name__ == "__main__":
    main()
