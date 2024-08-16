import pygame
import random
import sys

# Window settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Efects settings
pygame.mixer.init()

menu_change_effect      = pygame.mixer.Sound("media/Sons/Efects/selection_menu_change.mp3")
menu_select_effect      = pygame.mixer.Sound("media/Sons/Efects/selection_menu_select.mp3")
menu_unselect_effect    = pygame.mixer.Sound("media/Sons/Efects/selection_menu_unselect.mp3")
game_win_effect         = pygame.mixer.Sound("media/Sons/Efects/game_win.mp3")
game_over_effect        = pygame.mixer.Sound("media/Sons/Efects/game_over.mp3")
take_damage_effect      = pygame.mixer.Sound("media/Sons/Efects/take_damage.mp3")

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
    font = pygame.font.Font("media/Fonts/Press_Start_2P/PressStart2P-Regular.ttf", font_size)
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
    arrow = pygame.image.load("media/UI/introcomp_seta.png")
    arrow = pygame.transform.scale(arrow, (70, 70))

    # Load hero bg image
    hero_bg = pygame.image.load("media/UI/introcomp_menu.png")
    hero_bg = pygame.transform.scale(hero_bg, (140, 140))

    # x and y axis positions
    x_positions = [201, 457, 713, 289, 629]
    y_positions = [320, 560]
    for i, hero in enumerate(heroes):
        hero_bg = pygame.transform.scale(hero_bg, (140, 140))
        x = x_positions[i % 5]
        y = y_positions[i // 3]

        # drawingn the heroes
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
    # while the user not select 3 heroes
    while len(selected_characters) < 3:
        screen.blit(background_image, (0, 0))

        # Centralize 'IntroBattle' text
        draw_text(text='IntroBattle', color=WHITE, surface=screen,
                  x=SCREEN_WIDTH//2, y=100, font_size=40, background=True,
                  bg_color=BLACK, border=True, border_color=WHITE, border_thickness=2,
                  padding=10, alignment="center")

        # Centralize 'Select 3 Heroes:' text
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
                    menu_change_effect.play()
                    index = (index - 1) % len(heroes)
                if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    menu_change_effect.play()
                    index = (index + 1) % len(heroes)
                if event.key == pygame.K_z:
                    if heroes[index] not in selected_characters:
                        menu_select_effect.play()
                        selected_characters.append(heroes[index])
                    else:
                        menu_unselect_effect.play()
                        selected_characters.remove(heroes[index])

        clock.tick(30)

    return selected_characters

def draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action=0, selected_target=0, display_actions=True):
    """
    Draws the battle interface, including player characters, enemies, and the current turn details.

    Args:
        screen (pygame.Surface): The Pygame surface where the screen elements are drawn.
        background_image (pygame.Surface): The background image for the battle scene.
        player_characters (list): A list of player character objects to be displayed on the screen.
        enemies (list): A list of enemy objects to be displayed on the screen.
        current_char (object): The character object whose turn it is to act.
        selected_action (int, optional): Index of the selected action for the current character. Defaults to 0.
        selected_target (int, optional): Index of the selected enemy target. Defaults to 0.
        display_actions (bool, optional): Whether to display the action menu for the player characters. Defaults to True.
    """

    # Clear the screen by blitting the background image
    screen.blit(background_image, (0, 0))

    # Load and scale the arrow image
    arrow = pygame.image.load("media/UI/introcomp_seta.png")
    arrow = pygame.transform.scale(arrow, (70, 70))
    right_arrow = pygame.transform.rotate(arrow, 90)

    # Load the hero background image for the action menus
    menu_bg = pygame.image.load("media/UI/introcomp_menu.png")

    # Draw the left-side action menu background
    menu_bg = pygame.transform.scale(menu_bg, (580, 235))
    screen.blit(menu_bg, (15, SCREEN_HEIGHT - 230 - 15))

    # Draw the right-side action menu background
    menu_bg = pygame.transform.scale(menu_bg, (424, 235))
    screen.blit(menu_bg, (SCREEN_WIDTH - 424 - 15, SCREEN_HEIGHT - 230 - 15))

    # Draw player characters and highlight the current character
    for i, char in enumerate(player_characters):
        player_characters[i].position = (
            200 + (((i + 1) % 2) * 70) + player_characters[i].image.get_width() / 2,
            200 + i * 80 + player_characters[i].image.get_height() / 2
        )
        screen.blit(char.image, (200 + (((i + 1) % 2) * 70), 200 + i * 80))

        if char == current_char:
            screen.blit(arrow, (170 + (((i + 1) % 2) * 70) + char.image.get_width() // 2, 140 + i * 80))

    # Draw enemies and highlight the selected target
    for i, char in enumerate(enemies):
        char.position = (
            650 - ((i % 2) * 70) + char.image.get_width() / 2,
            200 + i * 100 + char.image.get_height() / 2
        )
        draw_text(f"{char.name}", RED, screen, x=650 - ((i % 2) * 70) + 100, y=200 + i * 100 + 30, font_size=18, alignment="topleft")
        draw_text(f"HP: {char.hp:.0f} / {char.max_hp}", RED, screen, x=650 - ((i % 2) * 70) + 100, y=200 + i * 100 + 60, font_size=18, alignment="topleft")
        screen.blit(char.image, (650 - ((i % 2) * 70), 200 + i * 100))

        if i == selected_target:
            screen.blit(arrow, (710 - ((i % 2) * 140 + char.image.get_width()) // 2, 145 + i * 90))

    # Display the current character's turn message
    draw_text(f"{current_char.name}'s turn!", WHITE, screen, x=110, y=570, font_size=18, alignment="topleft")

    # Display the action menu if display_actions is True
    if display_actions:
        # Draw all player options
        if current_char in player_characters:
            actions_name = ["Attack", "Defend", "Insight", "Skill"]
            # List of action names and their respective coordinates
            actions = [
                (actions_name[0], 110, 620),
                (actions_name[1], 360, 620),
                (actions_name[2], 110, 670),
                (actions_name[3], 360, 670)
            ]

            # Loop through the actions and display each one with an arrow indicating the selected action
            for i, (text, x, y) in enumerate(actions):
                draw_text(text, WHITE, screen, x=x, y=y, font_size=20, alignment="topleft")
                if i == selected_action:
                    screen.blit(right_arrow, (x - 60, y - 25))

    # Display the HP of player characters
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
    # creates a copy of the original enemies list
    enemies_copy = enemies.copy()
    enemies_num = len(enemies)

    clock = pygame.time.Clock()
    # sort characters by their speeds
    turn_order = sorted(player_characters + enemies, key=lambda x: x.speed, reverse=True)
    turn_index = 0
    selected_action = 0
    selected_target = None

    all_sprites_group = pygame.sprite.Group()
    
    # each iteration is a round
    while player_characters and enemies:
        current_char = turn_order[turn_index]
        
        # if is a player character then we can draw the options that he can take
        if current_char in player_characters:
            action_chosen = False
            while not action_chosen:
                selected_target = None
                draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target, display_actions=True)
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            selected_action = (selected_action - 2) % 4
                            menu_change_effect.play()
                        if event.key == pygame.K_DOWN:
                            selected_action = (selected_action + 2) % 4
                            menu_change_effect.play()
                        if event.key == pygame.K_LEFT:
                            selected_action = (selected_action - 1) % 4
                            menu_change_effect.play()
                        if event.key == pygame.K_RIGHT:
                            selected_action = (selected_action + 1) % 4
                            menu_change_effect.play()
                        if event.key == pygame.K_z:
                            menu_select_effect.play()
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
                                                menu_change_effect.play()
                                            if sub_event.key == pygame.K_DOWN:
                                                selected_target = (selected_target + 1) % len(enemies) if selected_target is not None else 0
                                                menu_change_effect.play()
                                            if sub_event.key == pygame.K_z:
                                                print(f'{current_char.name} is attacking {enemies[selected_target].name}')
                                                print(f'hp of {enemies[selected_target].name} before: {enemies[selected_target].hp}')
                                                
                                                damage = current_char.attack_target(enemies[selected_target], all_sprites_group)
                                                
                                                # Attack animation
                                                while all_sprites_group.__len__():
                                                    draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target)
                                                    all_sprites_group.update()
                                                    all_sprites_group.draw(screen)
                                                    pygame.display.flip()
                                                
                                                # After the animation is finished, we can take the damage
                                                shake_screen(screen, intensity=3, duration=50)
                                                take_damage_effect.play()
                                                enemies[selected_target].take_damage(damage)

                                                print(f'hp of {enemies[selected_target].name} after: {enemies[selected_target].hp}')
                                                if enemies[selected_target].hp == 0:
                                                    enemies.pop(selected_target)
                                                target_selected = True
                                                action_chosen = True
                                            if sub_event.key == pygame.K_x:
                                                target_selected = True
                                                menu_unselect_effect.play()
                            if selected_action == 1:  # Defend
                                print(f'{current_char.name} is defending')
                                current_char.is_defending = True
                                action_chosen = True
                            if selected_action == 2:  # Insight
                                x_selected = False
                                z_selected = False
                                while not x_selected:
                                    if selected_target is None:
                                        selected_target = 0  # Default enemy selected
                                    if not z_selected:
                                        draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target)
                                        pygame.display.flip()
                                    for sub_event in pygame.event.get():
                                        if sub_event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()
                                        if sub_event.type == pygame.KEYDOWN:
                                            if sub_event.key == pygame.K_UP:
                                                selected_target = (selected_target - 1) % len(enemies) if selected_target is not None else 0
                                                menu_change_effect.play()
                                            if sub_event.key == pygame.K_DOWN:
                                                selected_target = (selected_target + 1) % len(enemies) if selected_target is not None else 0
                                                menu_change_effect.play()
                                            if sub_event.key == pygame.K_z:
                                                menu_select_effect.play()
                                                z_selected = True
                                                draw_insights_info(screen, enemies[selected_target])
                                                pygame.display.flip()
                                            if sub_event.key == pygame.K_x:
                                                menu_unselect_effect.play()
                                                x_selected = True
                                                
                            if selected_action == 3:  # SKill
                                menu_select_effect.play()
                                if current_char.num_rounds_to_use_skill == 0:
                                    if current_char.name == "Paladin":
                                        action = current_char.paladin_protect(player_characters)
                                        draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target, display_actions=False)
                                        
                                        line1, line2, line3 = split_string_into_three_lines(action)
                                        draw_text(f"{line1}", WHITE, screen, x=110, y=630, font_size=18, alignment="topleft")
                                        draw_text(f"{line2}", WHITE, screen, x=110, y=630 + 30, font_size=18, alignment="topleft")
                                        draw_text(f"{line3}", WHITE, screen, x=110, y=630 + 60, font_size=18, alignment="topleft")

                                        pygame.display.flip()
                                        pygame.time.delay(5000)

                                    elif current_char.name == "Rogue":
                                        target_selected = False
                                        while not target_selected:
                                            if selected_target is None:
                                                selected_target = 0  # Default enemy to attack
                                            draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target, display_actions=False)
                                            pygame.display.flip()
                                            for sub_event in pygame.event.get():
                                                if sub_event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    exit()
                                                if sub_event.type == pygame.KEYDOWN:
                                                    if sub_event.key == pygame.K_UP:
                                                        selected_target = (selected_target - 1) % len(enemies) if selected_target is not None else 0
                                                        menu_change_effect.play()
                                                    if sub_event.key == pygame.K_DOWN:
                                                        selected_target = (selected_target + 1) % len(enemies) if selected_target is not None else 0
                                                        menu_change_effect.play()
                                                    if sub_event.key == pygame.K_z:
                                                    
                                                        damage, action = current_char.rogue_special_attack(enemies[selected_target], all_sprites_group)
                                                        
                                                        # Attack animation
                                                        while all_sprites_group.__len__():
                                                            draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target, display_actions=False)
                                                            
                                                            line1, line2, line3 = split_string_into_three_lines(action)
                                                            draw_text(f"{line1}", WHITE, screen, x=110, y=630, font_size=18, alignment="topleft")
                                                            draw_text(f"{line2}", WHITE, screen, x=110, y=630 + 30, font_size=18, alignment="topleft")
                                                            draw_text(f"{line3}", WHITE, screen, x=110, y=630 + 60, font_size=18, alignment="topleft")

                                                            all_sprites_group.update()
                                                            all_sprites_group.draw(screen)
                                                            pygame.display.flip()
                                                        
                                                        # After the animation is finished, we can take the damage
                                                        shake_screen(screen, intensity=3, duration=50)
                                                        take_damage_effect.play()
                                                        enemies[selected_target].take_damage(damage)

                                                        print(f'hp of {enemies[selected_target].name} after: {enemies[selected_target].hp}')
                                                        if enemies[selected_target].hp == 0:
                                                            enemies.pop(selected_target)
                                                        target_selected = True

                                    elif current_char.name == "Wizard":
                                        damages, action = current_char.wizard_spell(enemies, all_sprites_group)
                                                        
                                        # Attack animation
                                        sprites_count = all_sprites_group.__len__()
                                        while all_sprites_group.__len__():
                                            draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target, display_actions=False)
                                            
                                            line1, line2, line3 = split_string_into_three_lines(action)
                                            draw_text(f"{line1}", WHITE, screen, x=110, y=630, font_size=18, alignment="topleft")
                                            draw_text(f"{line2}", WHITE, screen, x=110, y=630 + 30, font_size=18, alignment="topleft")
                                            draw_text(f"{line3}", WHITE, screen, x=110, y=630 + 60, font_size=18, alignment="topleft")

                                            all_sprites_group.update()
                                            all_sprites_group.draw(screen)
                                            pygame.display.flip()
                                            if sprites_count > all_sprites_group.__len__():
                                                shake_screen(screen, intensity=3, duration=50)
                                                sprites_count -= 1
                                        
                                        # After the animation is finished, we can take the damage
                                        shake_screen(screen, intensity=3, duration=50)
                                        take_damage_effect.play()
                                        for i, enemy in enumerate(enemies):
                                            enemy.take_damage(damages[i])
                                            if enemies[i].hp == 0:
                                                enemies.pop(i)
                                        
                                    elif current_char.name == "Hunter":
                                        target_selected = False
                                        while not target_selected:
                                            if selected_target is None:
                                                selected_target = 0  # Default enemy to attack
                                            draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target, display_actions=False)
                                            pygame.display.flip()
                                            for sub_event in pygame.event.get():
                                                if sub_event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    exit()
                                                if sub_event.type == pygame.KEYDOWN:
                                                    if sub_event.key == pygame.K_UP:
                                                        selected_target = (selected_target - 1) % len(enemies) if selected_target is not None else 0
                                                        menu_change_effect.play()
                                                    if sub_event.key == pygame.K_DOWN:
                                                        selected_target = (selected_target + 1) % len(enemies) if selected_target is not None else 0
                                                        menu_change_effect.play()
                                                    if sub_event.key == pygame.K_z:
                                                    
                                                        damage, action = current_char.hunter_marked_shot(enemies[selected_target], all_sprites_group)
                                                        
                                                        # Attack animation
                                                        while all_sprites_group.__len__():
                                                            draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target)
                                                            
                                                            line1, line2, line3 = split_string_into_three_lines(action)
                                                            draw_text(f"{line1}", WHITE, screen, x=110, y=630, font_size=18, alignment="topleft")
                                                            draw_text(f"{line2}", WHITE, screen, x=110, y=630 + 30, font_size=18, alignment="topleft")
                                                            draw_text(f"{line3}", WHITE, screen, x=110, y=630 + 60, font_size=18, alignment="topleft")

                                                            all_sprites_group.update()
                                                            all_sprites_group.draw(screen)
                                                            pygame.display.flip()
                                                        
                                                        # After the animation is finished, we can take the damage
                                                        shake_screen(screen, intensity=3, duration=50)
                                                        take_damage_effect.play()
                                                        enemies[selected_target].take_damage(damage)

                                                        print(f'hp of {enemies[selected_target].name} after: {enemies[selected_target].hp}')
                                                        if enemies[selected_target].hp == 0:
                                                            enemies.pop(selected_target)
                                                        target_selected = True

                                    elif current_char.name == "Priest":
                                        action = current_char.priest_heal(player_characters)
                                        draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target, display_actions=False)
                                    
                                        line1, line2, line3 = split_string_into_three_lines(action)
                                        draw_text(f"{line1}", WHITE, screen, x=110, y=630, font_size=18, alignment="topleft")
                                        draw_text(f"{line2}", WHITE, screen, x=110, y=630 + 30, font_size=18, alignment="topleft")
                                        draw_text(f"{line3}", WHITE, screen, x=110, y=630 + 60, font_size=18, alignment="topleft")

                                        pygame.display.flip()
                                        pygame.time.delay(5000)

                                    current_char.reset_num_rounds_to_use_skill()
                                    action_chosen = True
                                else:
                                    action = f"You can only use the skill of this hero after {current_char.num_rounds_to_use_skill} rounds!"
                                    draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target, display_actions=False)
                                
                                    line1, line2, line3 = split_string_into_three_lines(action)
                                    draw_text(f"{line1}", WHITE, screen, x=110, y=630, font_size=18, alignment="topleft")
                                    draw_text(f"{line2}", WHITE, screen, x=110, y=630 + 30, font_size=18, alignment="topleft")
                                    draw_text(f"{line3}", WHITE, screen, x=110, y=630 + 60, font_size=18, alignment="topleft")

                                    pygame.display.flip()
                                    pygame.time.delay(5000)

                        if event.key == pygame.K_x:
                            action_chosen = True
            current_char.decrease_num_rounds_to_use_skill()
        else:
            if current_char.hp > 0:
                # Define probabilities: 70% chance for "Attack", 20% for "Defense", 10% for "Skill"
                probabilities = [0.7, 0.2, 0.1]
                options = ["Attack", "Defense", "Skill"]

                # chose a random option based on the probabilities
                chosen_option = random.choices(options, probabilities)[0]

                if chosen_option == "Attack":
                    target = random.choice(player_characters)               # chose a aleatory player hero
                    print(f'{current_char.name} is attacking {target.name}')
                    print(f'hp of {target.name} before: {target.hp}')
                    damage = current_char.attack_target(target, all_sprites_group)

                    # delay
                    pygame.time.delay(500)

                    # Attack animation
                    while all_sprites_group.__len__():
                        draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target)
                        draw_text(f"Attacking {target.name}'s!", WHITE, screen, x=110, y=670, font_size=18, alignment="topleft")
                        all_sprites_group.update()
                        all_sprites_group.draw(screen)
                        pygame.display.flip()

                    # After the animation is finished, we can take the damage
                    shake_screen(screen, intensity=3, duration=50)
                    take_damage_effect.play()
                    target.take_damage(damage)
                    print(f'hp of {target.name} after: {target.hp}')
                    
                    # if the character's hp is zero, he is dead, so we can remove him from the battle scene
                    if target.hp == 0:
                        player_characters.remove(target)

                    # draw the current action 
                    draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target)
                    draw_text(f"Attacking {target.name}'s!", WHITE, screen, x=110, y=670, font_size=18, alignment="topleft")
                    pygame.display.flip()
                    pygame.time.delay(2000)

                elif chosen_option == "Defense":
                    # draw the current action 
                    print(f'{current_char.name} is defending')
                    current_char.is_defending = True
                    draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target)
                    draw_text(f"{current_char.name}'s defending!", WHITE, screen, x=110, y=670, font_size=18, alignment="topleft")
                    pygame.display.flip()
                    pygame.time.delay(3000)

                else: #Skill
                    if current_char.name == "Necromante":
                        # Necromante tried to use his skill, but his ally is already alive, so it completes their life
                        if len(enemies) == enemies_num:
                            action = current_char.necromancer_dark_revival(enemies[1], enemies, revive=False)
                        # Necromante revives his ally
                        else:
                            enemy = enemies_copy[1]
                            action = current_char.necromancer_dark_revival(enemy, enemies, revive=True)
                        draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target, display_actions=False)
                        
                        line1, line2, line3 = split_string_into_three_lines(action)
                        draw_text(f"{line1}", WHITE, screen, x=110, y=630, font_size=18, alignment="topleft")
                        draw_text(f"{line2}", WHITE, screen, x=110, y=630 + 30, font_size=18, alignment="topleft")
                        draw_text(f"{line3}", WHITE, screen, x=110, y=630 + 60, font_size=18, alignment="topleft")

                        pygame.display.flip()
                        pygame.time.delay(5000)

                    elif current_char.name == "Caveira":
                        target = random.choice(player_characters)               # chose a aleatory player hero
                       
                        damage, action = current_char.skeleton_bone_crush(target, all_sprites_group)
                        
                        # Attack animation
                        while all_sprites_group.__len__():
                            draw_battle_interface(screen, background_image, player_characters, enemies, current_char, selected_action, selected_target)
                            
                            line1, line2, line3 = split_string_into_three_lines(action)
                            draw_text(f"{line1}", WHITE, screen, x=110, y=630, font_size=18, alignment="topleft")
                            draw_text(f"{line2}", WHITE, screen, x=110, y=630 + 30, font_size=18, alignment="topleft")
                            draw_text(f"{line3}", WHITE, screen, x=110, y=630 + 60, font_size=18, alignment="topleft")

                            all_sprites_group.update()
                            all_sprites_group.draw(screen)
                            pygame.display.flip()
                        
                        # After the animation is finished, we can take the damage
                        shake_screen(screen, intensity=3, duration=50)
                        take_damage_effect.play()
                        target.take_damage(damage)
                        
                        # if the character's hp is zero, he is dead, so we can remove him from the battle scene
                        if target.hp == 0:
                            player_characters.remove(target)
        
        # updating the character that will act
        turn_index = (turn_index + 1) % len(turn_order)
        
        # if all characters of a group are dead, then the game is finished
        if not player_characters or not enemies:
            # in this case, all players characters are dead, so it's game over
            if not player_characters:  
                game_over_effect.play()
                return "Game Over"
            # in this case, all enemies characters are dead, so it's game win
            else:
                game_win_effect.play()
                return "Win"
            break

        pygame.display.flip()
        clock.tick(30)

def finish_screen(result, screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    Displays the end screen based on the game result (win or loss) and waits for the player's action.

    Args:
        result (str): The outcome of the game, either "Win" or "Game Over".
        screen (pygame.Surface): The Pygame surface where the screen elements are drawn.
        SCREEN_WIDTH (int): The width of the game screen.
        SCREEN_HEIGHT (int): The height of the game screen.

    Returns:
        str: The player's selection, either "quit", "restart", or "menu".
    """
    
    # Fill the screen with black color
    screen.fill((0, 0, 0))
    
    # Display the result message
    if result == "Win":
        draw_text(text="YOU WIN", color=GREEN, surface=screen, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2 - 200, font_size=74, border=True, border_color=GREEN, border_thickness=2)
    else:
        draw_text(text="GAME OVER", color=RED, surface=screen, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2 - 200, font_size=74, border=True, border_color=RED, border_thickness=2)
    
    # Add menu options
    draw_text(text="Press Q to Quit", color=(255, 255, 255), surface=screen, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2 + 50, font_size=36, border=True, border_color=WHITE, border_thickness=2)
    draw_text(text="Press R to Restart", color=(255, 255, 255), surface=screen, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2 + 100, font_size=36, border=True, border_color=WHITE, border_thickness=2)
    draw_text(text="Press M for Menu", color=(255, 255, 255), surface=screen, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2 + 150, font_size=36, border=True, border_color=WHITE, border_thickness=2)

    pygame.display.flip()

    # Wait for a player action
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_select_effect.play()
                    return "quit"
                elif event.key == pygame.K_r:
                    menu_select_effect.play()
                    waiting = False
                    return "restart"
                elif event.key == pygame.K_m:
                    menu_select_effect.play()
                    waiting = False
                    return "menu"


def shake_screen(screen, intensity, duration):
    """
    Simulates a screen shake effect in Pygame.

    This function creates a shaking effect on the specified screen surface by moving it randomly for a given duration. After the effect, the screen is restored to its original state.

    Args:
        screen (pygame.Surface): The surface to apply the screen shake effect on.
        intensity (int): The intensity of the screen shake, determining the maximum displacement of the screen in pixels.
        duration (float): The duration of the screen shake effect in milliseconds.
    """
    start_time = pygame.time.get_ticks()
    # Create a copy of the screen
    copied_screen = screen.copy()

    # shakes the screen 
    while pygame.time.get_ticks() - start_time < duration:
        dx, dy = random.randint(-intensity, intensity), random.randint(-intensity, intensity)
        screen.blit(screen, (dx, dy))
        pygame.display.flip()
    
    screen.blit(copied_screen, (0, 0)) # Restore the copied screen
    pygame.display.flip()

def draw_insights_info(screen, enemie):
    """
    Displays the insight information of the current enemy on the screen.

    Args:
        screen (pygame.Surface): The Pygame surface where the screen elements are drawn.
        enemie (object): The enemy object containing attributes like name, attack, defense, and hp.
    """

    # Load and scale the menu background image for the player's action menu
    menu_bg = pygame.image.load("media/UI/introcomp_menu.png")
    
    # Draw the left-side menu background
    menu_bg = pygame.transform.scale(menu_bg, (580, 235))
    screen.blit(menu_bg, (15, SCREEN_HEIGHT - 230 - 15))

    # Draw the right-side menu background
    menu_bg = pygame.transform.scale(menu_bg, (424, 235))
    screen.blit(menu_bg, (SCREEN_WIDTH - 424 - 15, SCREEN_HEIGHT - 230 - 15))

    # Display the current turn message showing the enemy's name
    draw_text(f"{enemie.name}'s Info!", WHITE, screen, x=110, y=570, font_size=18, alignment="topleft")
    
    # Define the labels and values for the enemy's attributes
    infos_name = ["Attack: ", "Defend: ", "Life: "]
    
    # List of text items with their corresponding coordinates
    infos = [
        (infos_name[0], f"{enemie.attack:.0f}", 110, 620),
        (infos_name[1], f"{enemie.defense:.0f}", 110, 655),
        (infos_name[2], f"{enemie.hp:.0f}", 110, 690)
    ]

    # Loop through the info list and display each attribute
    for (info_name, info, x, y) in infos:
        draw_text(info_name + info, WHITE, screen, x=x, y=y, font_size=18, alignment="topleft")
    
    # Display a message prompting the player to tap 'X' to go back
    draw_text("Tap 'X' to go back!", WHITE, screen, x=650, y=570, font_size=16, alignment="topleft")

def split_string_into_three_lines(action):
    """
    Splits a given string into three approximately equal lines, ensuring that each split occurs at the nearest space.

    Args:
        action (str): The string to be split into three lines.

    Returns:
        tuple: A tuple containing three strings (line1, line2, line3) representing the split lines.
    """
    # Find the first split_index by dividing at the nearest space to one-third of the string length
    split_index1 = len(action) // 3
    while split_index1 < len(action) and action[split_index1] != ' ':
        split_index1 += 1

    # Find the second split_index by dividing at the nearest space to two-thirds of the string length
    split_index2 = 2 * len(action) // 3
    while split_index2 < len(action) and action[split_index2] != ' ':
        split_index2 += 1

    # Ensure that split indices are valid
    split_index1 = max(0, min(split_index1, len(action)))
    split_index2 = max(split_index1, min(split_index2, len(action)))

    # Split the string into three lines
    line1 = action[:split_index1].rstrip()
    line2 = action[split_index1:split_index2].strip()
    line3 = action[split_index2:].lstrip()

    return line1, line2, line3

