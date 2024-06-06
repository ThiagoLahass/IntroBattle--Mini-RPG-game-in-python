import pygame
import random

# Window settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Efects settings
pygame.mixer.init()
menu_change_efect = pygame.mixer.Sound("IntroBattle/media/Sons/Efects/selection_menu_change.mp3")
menu_select_efect = pygame.mixer.Sound("IntroBattle/media/Sons/Efects/selection_menu_select.mp3")
menu_unselect_efect = pygame.mixer.Sound("IntroBattle/media/Sons/Efects/selection_menu_unselect.mp3")

# Font
pygame.font.init()

import pygame

def draw_text(text, color, surface, x, y, font_size=16, background=False, bg_color=(0, 0, 0), border=False, border_thickness=2, border_color=(0, 0, 0), padding=5, alignment="center"):
    """
    Draws text on the given surface with specified options.

    Args:
        text (str): The text to be drawn.
        color (tuple): The color of the text.
        surface (pygame.Surface): The surface on which to draw the text.
        x (int): The x-coordinate for the text position.
        y (int): The y-coordinate for the text position.
        font_size (int): The size of the font.
        background (bool): Whether to fill the background with a color.
        bg_color (tuple): The color to fill the background (default is black).
        border (bool): Whether to draw a border around the text.
        border_thickness (int): The thickness of the border (default is 2).
        border_color (tuple): The color of the border (default is black).
        padding (int): The padding between the text and the background border (default is 5).
        alignment (str): The alignment of the text ("center" or "topleft").
    """
    font = pygame.font.Font("IntroBattle/media/Fonts/Press_Start_2P/PressStart2P-Regular.ttf", font_size)
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()

    # Set the position based on alignment
    if alignment == "center":
        text_rect.center = (x, y)
    elif alignment == "topleft":
        text_rect.topleft = (x, y)
    else:
        raise ValueError("Invalid alignment option. Choose 'center' or 'topleft'.")

    if background:
        pygame.draw.rect(surface, bg_color, (text_rect.left - padding, text_rect.top - padding, text_rect.width + 2 * padding, text_rect.height + 2 * padding))

    if border:
        pygame.draw.rect(surface, border_color, (text_rect.left - padding, text_rect.top - padding, text_rect.width + 2 * padding, text_rect.height + 2 * padding), border_thickness)

    surface.blit(text_obj, text_rect)

def draw_heroes(screen, heroes, selected_index, selected_heroes):
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

        if(hero in selected_heroes):
            text_color = BLUE
        draw_text(hero.name, text_color, screen, scaled_center_x, scaled_center_y + 105, int(14*scale))


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
                  x=SCREEN_WIDTH//2, y=100, font_size=40, background=True,
                  bg_color=BLACK, border=True, border_color=WHITE, border_thickness=2,
                  padding=10, alignment="center")

        # Centralize o texto 'Select 3 Heroes:'
        draw_text(text="Select 3 Heroes (tap 'Z'):", color=WHITE, surface=screen,
                  x=SCREEN_WIDTH//2, y=220, font_size=22,
                  background=True, bg_color=RED, 
                  border=True, border_thickness=1, border_color=WHITE,
                  alignment="center")

        draw_heroes(screen, heroes, index, selected_characters)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                    menu_change_efect.play()
                    index = (index - 1) % len(heroes)
                if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    menu_change_efect.play()
                    index = (index + 1) % len(heroes)
                if event.key == pygame.K_z:
                    if heroes[index] not in selected_characters:
                        menu_select_efect.play()
                        selected_characters.append(heroes[index])
                    else:
                        menu_unselect_efect.play()
                        selected_characters.remove(heroes[index])

        clock.tick(30)

    return selected_characters

def draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action=0, selected_target=0):
    # Clear screen
    screen.blit(background_image, (0, 0))

    # Load arrow image
    arrow = pygame.image.load("IntroBattle/media/UI/introcomp_seta.png")
    arrow = pygame.transform.scale(arrow, (70, 70))
    right_arrow = pygame.transform.rotate(arrow, 90)

    # Load hero bg image
    menu_bg = pygame.image.load("IntroBattle/media/UI/introcomp_menu.png")

    # Actions menu for player characters
    menu_bg = pygame.transform.scale(menu_bg, (580, 235))
    screen.blit(menu_bg, (15 ,SCREEN_HEIGHT - 230 - 15))

    menu_bg = pygame.transform.scale(menu_bg, (424, 235))
    screen.blit(menu_bg, (SCREEN_WIDTH - 424 - 15 ,SCREEN_HEIGHT - 230 - 15 ))
    
    # Draw player characters
    for i, char in enumerate(player_characters):
        screen.blit(char.image, (200 + (((i+1) % 2) * 70), 200 + i * 80 ))
    
    # Draw enemies
    for i, char in enumerate(enemies):
        screen.blit(char.image, (650 - ((i % 2) * 70), 200 + i * 100))
        
        if i == selected_target:
            screen.blit(arrow, (710 - ((i % 2) * 140 + char.image.get_width()) // 2, 145 + i * 90))
    
    # Current turn message
    draw_text(f"{current_char.name}'s turn", WHITE, screen, x=110, y=570, font_size=18, alignment="topleft")

    if current_char in player_characters:
        actions_name = ["Attack", "Defend", "Insight", "Skill"]
        # Lista de textos e suas respectivas coordenadas
        actions = [
            (actions_name[0], 110, 620),
            (actions_name[1], 360, 620),
            (actions_name[2], 110, 670),
            (actions_name[3], 360, 670)
        ]

        for i, (text, x, y) in enumerate(actions):
            draw_text(text, WHITE, screen, x=x, y=y, font_size=20, alignment="topleft")
            if i == selected_action:
                screen.blit(right_arrow, (x - 60, y - 25))
    
    # Player characters' HP
    for i, char in enumerate(player_characters):
        draw_text(f'{char.name} {char.hp:.0f} / {char.max_hp}', WHITE, screen, 650, 570 + i * 50, font_size=18, alignment="topleft")


def battle(screen, background_image, player_characters, enemies):
    """
    Simulates a battle between the player's characters and the enemies.

    Args:
        screen (pygame.Surface): The game screen where the battle is displayed.
        background_image (pygame.Surface): The background image for the battle screen.
        player_characters (list): A list of the player's characters.
        enemies (list): A list of enemy characters.

    Returns:
        str: The result of the game, "Win" or "Game Over".
    """
    clock = pygame.time.Clock()
    turn_order = sorted(player_characters + enemies, key=lambda x: x.speed, reverse=True)
    turn_index = 0
    selected_action = 0
    selected_target = None
    
    while player_characters and enemies:
        screen.blit(background_image, (0, 0))
        
        current_char = turn_order[turn_index]
        
        if current_char in player_characters:
            action_chosen = False
            while not action_chosen:
                selected_target = None
                draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target)
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            selected_action = (selected_action - 2) % 4
                        if event.key == pygame.K_DOWN:
                            selected_action = (selected_action + 2) % 4
                        if event.key == pygame.K_LEFT:
                            selected_action = (selected_action - 1) % 4
                        if event.key == pygame.K_RIGHT:
                            selected_action = (selected_action + 1) % 4
                        if event.key == pygame.K_z:
                            if selected_action == 0:  # Attack
                                target_selected = False
                                while not target_selected:
                                    if selected_target is None:
                                        selected_target = 0  # Default enemy to attack
                                    draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target)
                                    pygame.display.flip()
                                    for sub_event in pygame.event.get():
                                        if sub_event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()
                                        if sub_event.type == pygame.KEYDOWN:
                                            if sub_event.key == pygame.K_UP:
                                                selected_target = (selected_target - 1) % len(enemies) if selected_target is not None else 0
                                            if sub_event.key == pygame.K_DOWN:
                                                selected_target = (selected_target + 1) % len(enemies) if selected_target is not None else 0
                                            if sub_event.key == pygame.K_z:
                                                current_char.attack_target(enemies[selected_target])
                                                if enemies[selected_target].hp == 0:
                                                    enemies.pop(selected_target)
                                                target_selected = True
                                                action_chosen = True
                                            if sub_event.key == pygame.K_x:
                                                target_selected = True
                            if selected_action == 1:  # Defend
                                current_char.is_defending = True
                                action_chosen = True
                        if event.key == pygame.K_x:
                            action_chosen = True
        else:
            if current_char.hp > 0:
                if random.choice([True, False]):    # If true enemie attacks
                    target = random.choice(player_characters)   # chose a aleatory player hero
                    current_char.attack_target(target)
                    if target.hp == 0:
                        player_characters.remove(target)
                else:                               # Else, it defends
                    current_char.is_defending = True
        
        turn_index = (turn_index + 1) % len(turn_order)
        
        if not player_characters or not enemies:
            if not player_characters:
                return "Game Over"
            else:
                return "Win"
            break

        pygame.display.flip()
        clock.tick(30)