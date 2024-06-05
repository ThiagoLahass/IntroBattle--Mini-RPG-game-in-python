import pygame
import random

# Window settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Font
pygame.font.init()

def draw_text(text, color, surface, center_x, center_y, font_size=16, background=False, bg_color=(0, 0, 0), border=False, border_thickness=2, border_color=(0, 0, 0), padding=5):
    """
    Draws text on the given surface with specified options.

    Args:
        text (str): The text to be drawn.
        color (tuple): The color of the text.
        surface (pygame.Surface): The surface on which to draw the text.
        center_x (int): The x-coordinate of the text's center.
        center_y (int): The y-coordinate of the text's center.
        font_size (int): The size of the font.
        background (bool): Whether to fill the background with a color.
        bg_color (tuple): The color to fill the background (default is black).
        border (bool): Whether to draw a border around the text.
        border_thickness (int): The thickness of the border (default is 2).
        border_color (tuple): The color of the border (default is black).
        padding (int): The padding between the text and the background border (default is 5).
    """
    font = pygame.font.Font("IntroBattle/media/Fonts/Press_Start_2P/PressStart2P-Regular.ttf", font_size)
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    
    # Calculate the top-left position based on center and text size
    text_rect.center = (center_x, center_y)

    if background:
        pygame.draw.rect(surface, bg_color, (text_rect.left - padding, text_rect.top - padding, text_rect.width + 2 * padding, text_rect.height + 2 * padding))

    if border:
        pygame.draw.rect(surface, border_color, (text_rect.left - padding, text_rect.top - padding, text_rect.width + 2 * padding, text_rect.height + 2 * padding), border_thickness)

    surface.blit(text_obj, text_rect)

def draw_heroes(screen, heroes, selected_index):
    """
    Draws the hero images on the screen with scaling for the selected hero.

    Args:
        screen (pygame.Surface): The game screen where the heroes are drawn.
        heroes (list): A list of hero characters.
        selected_index (int): The index of the currently selected hero.
    """

    # Load arrow image
    arrow = pygame.image.load("IntroBattle/media/UI/introcomp_seta.png")
    arrow = pygame.transform.scale(arrow, (70, 70))

    # Load hero bg image
    hero_bg = pygame.image.load("IntroBattle/media/UI/introcomp_menu.png")
    hero_bg = pygame.transform.scale(hero_bg, (140, 140))

    x_positions = [201, 457, 713, 289, 629]
    y_positions = [320, 560]
    for i, hero in enumerate(heroes):
        hero_bg = pygame.transform.scale(hero_bg, (140, 140))
        x = x_positions[i % 5]
        y = y_positions[i // 3]

        if i == selected_index:
            # Increase size for selected hero
            scale = 1.4
            hero_image = pygame.transform.scale(hero.image, (int(hero.image.get_width() * scale), int(hero.image.get_height() * scale)))
            hero_bg = pygame.transform.scale(hero_bg, (int(hero_bg.get_width() * scale), int(hero_bg.get_height() * scale)))
            # Calculate central position for scaled image
            scaled_center_x = x + hero.image.get_width() * scale / 2 - 10
            scaled_center_y = y + hero.image.get_height() * scale / 2
            screen.blit(hero_bg, (scaled_center_x - 35 - hero_image.get_width() / 2, scaled_center_y - 35 - hero_image.get_height() / 2))
            screen.blit(hero_image, (scaled_center_x - hero_image.get_width() / 2, scaled_center_y - hero_image.get_height() / 2))
            text_color = RED  # Color for selected hero's text
            screen.blit(arrow, (scaled_center_x-40, scaled_center_y-150))
        else:
            scale = 1.2
            hero_image = pygame.transform.scale(hero.image, (int(hero.image.get_width() * scale), int(hero.image.get_height() * scale)))
            hero_bg = pygame.transform.scale(hero_bg, (int(hero_bg.get_width() * scale), int(hero_bg.get_height() * scale)))
            # Calculate central position for scaled image
            scaled_center_x = x + hero.image.get_width() * scale / 2
            scaled_center_y = y + hero.image.get_height() * scale / 2
            screen.blit(hero_bg, (scaled_center_x - 25 - hero_image.get_width() / 2, scaled_center_y - 25 - hero_image.get_height() / 2))
            screen.blit(hero_image, (scaled_center_x - hero_image.get_width() / 2, scaled_center_y - hero_image.get_height() / 2))
            text_color = WHITE  # Default text color

        draw_text(hero.name, text_color, screen, scaled_center_x, scaled_center_y + 100)


def selection_screen(screen, background_image, heroes):
    """
    Displays the character selection screen and allows the player to select characters.

    Args:
        screen (pygame.Surface): The game screen where the selection screen is displayed.
        background_image (pygame.Surface): The background image for the selection screen.
        heroes (list): A list of available hero characters.

    Returns:
        list: A list of selected hero characters.
    """
    selected_characters = []
    index = 0
    clock = pygame.time.Clock()
    while len(selected_characters) < 3:
        screen.blit(background_image, (0, 0))

        # Centralize o texto 'IntroBattle'
        draw_text(text='IntroBattle', color=WHITE, surface=screen,
                  center_x=SCREEN_WIDTH//2, center_y=100,
                  font_size=40, background=True, bg_color=BLACK, border=True,
                  border_color=WHITE, border_thickness=2, padding=10)

        # Centralize o texto 'Select 3 Heroes:'
        draw_text(text='Select 3 Heroes:', color=WHITE, surface=screen,
                  center_x=SCREEN_WIDTH//2, center_y=220, font_size=22,
                  background=True, bg_color=RED, border=True, border_thickness=1, border_color=WHITE)

        draw_heroes(screen, heroes, index)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                    index = (index - 1) % len(heroes)
                if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    index = (index + 1) % len(heroes)
                if event.key == pygame.K_z:
                    if heroes[index] not in selected_characters:
                        selected_characters.append(heroes[index])

        clock.tick(30)

    return selected_characters


def battle(screen, background_image, player_characters, enemies):
    """
    Simulates a battle between the player's characters and the enemies.

    Args:
        screen (pygame.Surface): The game screen where the battle is displayed.
        background_image (pygame.Surface): The background image for the battle screen.
        player_characters (list): A list of the player's characters.
        enemies (list): A list of enemy characters.
    """
    clock = pygame.time.Clock()
    turn_order = sorted(player_characters + enemies, key=lambda x: x.speed, reverse=True)
    turn_index = 0

    while player_characters and enemies:
        screen.blit(background_image, (0, 0))
        
        # Draw player's characters
        for i, char in enumerate(player_characters):
            screen.blit(char.image, (100, 300 + i * 150))
            draw_text(f'{char.name} HP: {char.hp:.2f}/{char.max_hp}', BLACK, screen, 100, 270 + i * 150)
        
        # Draw enemies
        for i, char in enumerate(enemies):
            screen.blit(char.image, (500, 300 + i * 150))
            draw_text(f'{char.name} HP: {char.hp:.2f}/{char.max_hp}', BLACK, screen, 500, 270 + i * 150)
        
        # Draw battle interface
        current_char = turn_order[turn_index]
        if current_char in player_characters:
            draw_text(f"{current_char.name}'s turn. Choose an action:", BLACK, screen, 50, 50)
            draw_text('1. Attack', BLACK, screen, 50, 100)
            draw_text('2. Defend', BLACK, screen, 50, 140)
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
                        draw_text(f'{char.name} HP: {char.hp:.2f}/{char.max_hp}', BLACK, screen, 100, 270 + i * 150)
                    for i, char in enumerate(enemies):
                        screen.blit(char.image, (500, 300 + i * 150))
                        draw_text(f'{char.name} HP: {char.hp:.2f}/{char.max_hp}', BLACK, screen, 500, 270 + i * 150)
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
