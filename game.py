import pygame
import random
from character import Character

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Font
pygame.font.init()
font = pygame.font.Font("IntroBattle/media/Fonts/Press_Start_2P/PressStart2P-Regular.ttf", 16)

def draw_text(text, font, color, surface, x, y):
    """
    Draws text on the given surface.

    Args:
        text (str): The text to be drawn.
        font (pygame.font.Font): The font used to render the text.
        color (tuple): The color of the text.
        surface (pygame.Surface): The surface on which to draw the text.
        x (int): The x-coordinate of the text's top-left corner.
        y (int): The y-coordinate of the text's top-left corner.
    """
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def draw_heroes(screen, heroes, selected_index):
    """
    Draws the hero images on the screen.

    Args:
        screen (pygame.Surface): The game screen where the heroes are drawn.
        heroes (list): A list of hero characters.
        selected_index (int): The index of the currently selected hero.
    """
    x_positions = [50, 250, 450]
    y_positions = [200, 400]
    for i, hero in enumerate(heroes):
        x = x_positions[i % 3]
        y = y_positions[i // 3]
        if i == selected_index:
            pygame.draw.rect(screen, RED, (x-5, y-5, 110, 110), 3)
        screen.blit(hero.image, (x, y))
        draw_text(hero.name, font, BLACK, screen, x, y + 110)

def selection_screen(screen, heroes):
    """
    Displays the character selection screen and allows the player to select characters.

    Args:
        screen (pygame.Surface): The game screen where the selection screen is displayed.
        heroes (list): A list of available hero characters.

    Returns:
        list: A list of selected hero characters.
    """
    selected_characters = []
    index = 0
    clock = pygame.time.Clock()
    while len(selected_characters) < 3:
        screen.fill(WHITE)
        draw_text('Select 3 characters:', font, BLACK, screen, 20, 20)
        
        draw_heroes(screen, heroes, index)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    index = (index - 1) % len(heroes)
                if event.key == pygame.K_DOWN:
                    index = (index + 1) % len(heroes)
                if event.key == pygame.K_z:
                    if heroes[index] not in selected_characters:
                        selected_characters.append(heroes[index])

        clock.tick(30)
    
    return selected_characters

def battle(screen, player_characters, enemies):
    """
    Simulates a battle between the player's characters and the enemies.

    Args:
        screen (pygame.Surface): The game screen where the battle is displayed.
        player_characters (list): A list of the player's characters.
        enemies (list): A list of enemy characters.
    """
    clock = pygame.time.Clock()
    turn_order = sorted(player_characters + enemies, key=lambda x: x.speed, reverse=True)
    turn_index = 0

    while player_characters and enemies:
        screen.fill(WHITE)
        
        # Draw player's characters
        for i, char in enumerate(player_characters):
            screen.blit(char.image, (100, 300 + i * 150))
            draw_text(f'{char.name} HP: {char.hp:.2f}/{char.max_hp}', font, BLACK, screen, 100, 270 + i * 150)
        
        # Draw enemies
        for i, char in enumerate(enemies):
            screen.blit(char.image, (500, 300 + i * 150))
            draw_text(f'{char.name} HP: {char.hp:.2f}/{char.max_hp}', font, BLACK, screen, 500, 270 + i * 150)
        
        # Draw battle interface
        current_char = turn_order[turn_index]
        if current_char in player_characters:
            draw_text(f"{current_char.name}'s turn. Choose an action:", font, BLACK, screen, 50, 50)
            draw_text('1. Attack', font, BLACK, screen, 50, 100)
            draw_text('2. Defend', font, BLACK, screen, 50, 140)
            pygame.display.flip()

            action_chosen = False
            while not action_chosen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            action_chosen = 'attack'
                        if event.key == pygame.K_2:
                            action_chosen = 'defend'
                
                clock.tick(30)

            if action_chosen == 'attack':
                enemy_index = 0
                choosing_target = True
                while choosing_target:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                enemy_index = (enemy_index - 1) % len(enemies)
                            if event.key == pygame.K_DOWN:
                                enemy_index = (enemy_index + 1) % len(enemies)
                            if event.key == pygame.K_z:
                                current_char.attack_target(enemies[enemy_index])
                                if enemies[enemy_index].hp == 0:
                                    enemies.pop(enemy_index)
                                choosing_target = False

                    screen.fill(WHITE)
                    for i, char in enumerate(player_characters):
                        screen.blit(char.image, (100, 300 + i * 150))
                        draw_text(f'{char.name} HP: {char.hp:.2f}/{char.max_hp}', font, BLACK, screen, 100, 270 + i * 150)
                    for i, char in enumerate(enemies):
                        screen.blit(char.image, (500, 300 + i * 150))
                        draw_text(f'{char.name} HP: {char.hp:.2f}/{char.max_hp}', font, BLACK, screen, 500, 270 + i * 150)
                        if i == enemy_index:
                            pygame.draw.rect(screen, RED, (500, 300 + i * 150, 100, 100), 3)
                    pygame.display.flip()
                    clock.tick(30)

            if action_chosen == 'defend':
                current_char.is_defending = True
        
        else:
            if current_char.hp > 0:
                if random.choice([True, False]):
                    target = random.choice(player_characters)
                    current_char.attack_target(target)
                    if target.hp == 0:
                        player_characters.remove(target)
                else:
                    current_char.is_defending = True
        
        turn_index = (turn_index + 1) % len(turn_order)
        
        if not player_characters or not enemies:
            break

        pygame.display.flip()
        clock.tick(30)
