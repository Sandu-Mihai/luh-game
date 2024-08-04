import pygame
import os

pygame.init()
clock = pygame.time.Clock()

screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Alchimia Alcanilor")

font_title = pygame.font.Font(None, 80)
font_button = pygame.font.Font(None, 50)

menu_open = False
exit_confirm = False
player_movement_disabled = False
table_names = ["Masa 1", "Masa 2", "Masa 3", "Masa 4", "Masa 5", "Masa 6", "Masa 7", "Masa 8", "Masa 9", "Masa 10"]
table_colors = [(255, 0, 0) for _ in range(len(table_names))]

class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.hovered = False

    def draw(self, screen, text_color=(255, 255, 255), bg_color=(0, 0, 0, 1)):
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        button_surface.fill(bg_color)
        screen.blit(button_surface, (self.x, self.y))

        text_surf = font_button.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

def loading_screen():
    loading_texts = ["Se incarca", "Se incarca.", "Se incarca..", "Se incarca..."]
    for loading_text in loading_texts:
        screen.fill((0, 0, 0))
        loading_text_render = font_title.render(loading_text, True, (255, 255, 255))
        loading_text_rect = loading_text_render.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(loading_text_render, loading_text_rect)
        pygame.display.flip()
        pygame.time.delay(500)

def draw_single_button_gui(button_text):
    menu_surface = pygame.Surface((screen_width // 2, screen_height // 2 + 100))
    menu_surface.set_alpha(200)
    menu_surface.fill((255, 255, 255))

    button_width = 200
    button_height = 40
    button_x = (menu_surface.get_width() - button_width) // 2
    button_y = (menu_surface.get_height() - button_height) // 2
    button = Button(button_text, button_x, button_y, button_width, button_height)
    button.draw(menu_surface, text_color=(255, 0, 0), bg_color=(255, 0, 0, 1))

    screen.blit(menu_surface, ((screen_width - menu_surface.get_width()) // 2, (screen_height - menu_surface.get_height()) // 2))
    pygame.display.flip()

def draw_other_menu(table_number):
    menu_surface = pygame.Surface((screen_width // 2, screen_height // 2 + 100))
    menu_surface.set_alpha(200)
    menu_surface.fill((255, 255, 255))

    table_text = font_button.render(f"Cerinta pentru masa {table_number}:", True, (255, 255, 255))
    table_rect = table_text.get_rect(center=(screen_width // 2, screen_height * 0.6))
    menu_surface.blit(table_text, table_rect)

    screen.blit(menu_surface, ((screen_width - menu_surface.get_width()) // 2, (screen_height - menu_surface.get_height()) // 2))

    button_width = 200
    button_height = 40
    button_gap = 20

    yes_button = Button("Inchide", screen_width // 2 - button_width // 2, screen_height // 2 + 100, button_width, button_height)
    yes_button.draw(screen, text_color=(255, 0, 0), bg_color=(255, 0, 0, 1))

    pygame.display.flip()

    return yes_button

def draw_button(surface, text, x, y, width, height, color):
    pygame.draw.rect(surface, color, (x, y, width, height))
    font = pygame.font.Font(None, 20)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)

def draw_text(surface, text, x, y, color):
    font = pygame.font.Font(None, 20)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def draw_gui(menu_surface):
    button_width = 200
    button_height = 40
    button_padding = 10
    button_x = 50
    button_y = 50

    for i, table_name in enumerate(table_names):
        button_text = f"Cerinta {i+1}"
        button_color = (255, 0, 0, 128) if table_colors[i] == (255, 0, 0) else (0, 255, 0, 128)
        draw_button(menu_surface, button_text, button_x, button_y + i * (button_height + button_padding), button_width, button_height, button_color)

        table_name_color = (255, 0, 0) if table_colors[i] == (255, 0, 0) else (0, 255, 0)
        draw_text(menu_surface, table_name, screen_width // 2, button_y + i * (button_height + button_padding), table_name_color)

# Define global variable for exit background image
exit_background_image = None

def game_loop():
    global menu_open, exit_confirm, player_movement_disabled, exit_background_image
    menu_open = False
    exit_confirm = False
    player_movement_disabled = False
    running = True
    current_table_menu = None
    gui_visible = False

    background_image = pygame.image.load("E:/Visual Studio Code/Python Joc Chimie/background.png").convert_alpha()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    exit_background_image = pygame.image.load(os.path.join("E:/Visual Studio Code/Python Joc Chimie", "dark_oak.png")).convert_alpha()
    exit_background_image = pygame.transform.scale(exit_background_image, (screen_width // 2, screen_height // 2))
    exit_background_image.set_alpha(192)  # Setează transparența la 75%

    player_default = pygame.image.load(os.path.join("E:/Visual Studio Code/Python Joc Chimie", "player_sprite_front_1.png")).convert_alpha()
    player_left_1 = pygame.image.load(os.path.join("E:/Visual Studio Code/Python Joc Chimie", "player_sprite_left_1.png")).convert_alpha()
    player_left_2 = pygame.image.load(os.path.join("E:/Visual Studio Code/Python Joc Chimie", "player_sprite_left_2.png")).convert_alpha()
    player_right_1 = pygame.image.load(os.path.join("E:/Visual Studio Code/Python Joc Chimie", "player_sprite_right_1.png")).convert_alpha()
    player_right_2 = pygame.image.load(os.path.join("E:/Visual Studio Code/Python Joc Chimie", "player_sprite_right_2.png")).convert_alpha()
    player_front_1 = pygame.image.load(os.path.join("E:/Visual Studio Code/Python Joc Chimie", "player_sprite_default.png")).convert_alpha()

    player_width = 85
    player_height = 85

    player_x = 1500
    player_y = 900
    player_vel = 20
    player_direction = "default"
    animation_counter = 0
    player_animation = player_default
    animation_switch = False

    mese_zones = [
        [(190, 70), (580, 180)],  # 1
        [(730, 70), (1115, 180)],  # 2
        [(1270, 70), (1660, 180)],  # 3
        [(190, 300), (580, 420)],  # 4
        [(730, 300), (1115, 420)],  # 5
        [(1270, 300), (1660, 420)],  # 6
        [(190, 545), (580, 640)],  # 7
        [(730, 545), (1115, 640)],  # 8
        [(1270, 545), (1660, 640)],  # 9
        [(190, 740), (580, 860)],  # 10
    ]

    usa_barrier = [(1570, 730), (1770, 950)]

    while running:
        screen.blit(background_image, (0, 0))

        for index, mese in enumerate(mese_zones):
            # Calculăm dimensiunile mesei
            x1, y1 = mese[0]
            x2, y2 = mese[1]
            margin = 10  # Marginile interioare

            if index == 9:  # Masa 10
                if (x1+120 <= player_x <= x2-120) and (y2 <= player_y <= y2 + 10) and player_animation == player_default:
                    interact_text = font_button.render("Apasă F pentru a interacționa", True, (255, 255, 255))
                    interact_text_rect = interact_text.get_rect(center=(x1 + (x2 - x1 + 50) // 2, y2 - 50))
                    screen.blit(interact_text, interact_text_rect)
                    break
            else:  # Mesele 1-9
                if (x1+120 <= player_x <= x2-120) and (y1 - 5 <= player_y <= y1 + 5) and player_animation == player_front_1:
                    interact_text = font_button.render("Apasă F pentru a interacționa", True, (255, 255, 255))
                    interact_text_rect = interact_text.get_rect(center=(x1 + (x2 - x1 + 50) // 2, y1 - 30))
                    screen.blit(interact_text, interact_text_rect)
                    break

        # Verificăm poziția jucătorului pentru a afișa "Apasă E pentru a interacționa" doar când se apropie de tablă
        if (620 <= player_x <= 1170) and (910 <= player_y <= 930) and player_animation == player_front_1:
            interact_text = font_button.render("Apasă E pentru a interacționa", True, (255, 255, 255))
            interact_text_rect = interact_text.get_rect(center=(screen_width // 2, screen_height - 100))
            screen.blit(interact_text, interact_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not gui_visible:
                    if (620 <= player_x <= 1170) and (910 <= player_y <= 930) and player_direction == "back":
                        current_table_menu = 11
                elif event.key == pygame.K_f and not gui_visible:
                    for index, mese in enumerate(mese_zones):
                        x1, y1 = mese[0]
                        x2, y2 = mese[1]
                        if index == 9:  # Masa 10
                            if (x1 <= player_x <= x2) and (y2 + 5 <= player_y <= y2 + 15) and player_animation == player_front_1:
                                current_table_menu = index + 1
                        else:  # Mesele 1-9
                            if (x1 <= player_x <= x2) and (y1 - 15 <= player_y <= y1 - 5) and player_animation == player_front_1:
                                current_table_menu = index + 1
                elif event.key == pygame.K_ESCAPE:
                    if exit_confirm:
                        exit_confirm = False
                        player_movement_disabled = False
                    else:
                        exit_confirm = True
                        player_movement_disabled = True
                elif event.key == pygame.K_f:
                    gui_visible = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and exit_confirm:
                yes_button, no_button = draw_exit_confirm_menu()
                if yes_button.is_clicked(event.pos):
                    exit_confirm = False
                    player_movement_disabled = False
                    main_menu()
                elif no_button.is_clicked(event.pos):
                    exit_confirm = False
                    player_movement_disabled = False
        
        if gui_visible:
            menu_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            menu_surface.fill((0, 0, 0, 128))

            draw_gui(menu_surface)

            screen.blit(menu_surface, (0, 0))
            pygame.display.flip()

        keys = pygame.key.get_pressed()

        if not player_movement_disabled:
            if keys[pygame.K_w]:
                if player_y > 0 and not any(
                (masa[0][0] < player_x < masa[1][0] and masa[0][1] < player_y - player_vel < masa[1][1]) or
                (player_x < 20) or (player_x + player_width > screen_width - 20) or
                (player_y < 20) for masa in mese_zones) and not (1580 <= player_x <= 1790 and 740 <= player_y - player_vel <= 950):
                    player_y -= player_vel
                    player_direction = "front"
                    player_animation = player_default
            if keys[pygame.K_s]:
                if player_y < screen_height - player_height and not any(
                    (masa[0][0] < player_x < masa[1][0] and masa[0][1] < player_y + player_vel < masa[1][1]) or
                    (player_x <= 70) or (player_x + player_width >= screen_width - 70) or
                    (player_y + player_height > screen_height - 70) for masa in mese_zones) and not (1580 <= player_x + 10 <= 1790 and 740 <= player_y + player_vel <= 950):
                    player_y += player_vel
                    player_direction = "back"
                    player_animation = player_front_1
            if keys[pygame.K_a]:
                if player_x > 0 and not any(
                    (masa[0][0] < player_x - player_vel < masa[1][0] and masa[0][1] < player_y < masa[1][1]) or
                    (player_x - player_vel <= 35) or (player_y <= 35) or
                    (player_y + player_height > screen_height - 35) for masa in mese_zones) and not (1580 <= player_x - player_vel <= 1790 and 740 <= player_y + 10 <= 950):
                        player_x -= player_vel
                        player_direction = "left"
                        animation_switch = not animation_switch
                        if animation_switch:
                            player_animation = player_left_1
                        else:
                            player_animation = player_left_2
            if keys[pygame.K_d]:
                if player_x < screen_width - player_width and not any(
                    (masa[0][0] < player_x + player_vel < masa[1][0] and masa[0][1] < player_y < masa[1][1]) or
                    (player_x + player_width + player_vel > screen_width - 40) or
                    (player_y < 40) or (player_y + player_height > screen_height - 40) for masa in mese_zones) and not (1580 <= player_x + player_vel <= 1790 and 740 <= player_y + 10 <= 950):
                        player_x += player_vel
                        player_direction = "right"
                        animation_switch = not animation_switch
                        if animation_switch:
                            player_animation = player_right_1
                        else:
                            player_animation = player_right_2

        screen.blit(pygame.transform.scale(player_animation, (player_width, player_height)), (player_x, player_y))

        if menu_open:
            draw_table_menu()

        if exit_confirm:
            yes_button, no_button = draw_exit_confirm_menu()

        pygame.display.flip()
        clock.tick(12)
        
def draw_table_menu():
    menu_surface = pygame.Surface((screen_width // 2, screen_height // 2 + 100))
    menu_surface.set_alpha(200)
    menu_surface.fill((255, 255, 255))

    table_text = font_button.render("Alege o masă:", True, (255, 255, 255))
    table_rect = table_text.get_rect(center=(screen_width // 2, screen_height * 0.6))
    menu_surface.blit(table_text, table_rect)

    screen.blit(menu_surface, ((screen_width - menu_surface.get_width()) // 2, (screen_height - menu_surface.get_height()) // 2))

    button_width = 200
    button_height = 40
    button_gap = 20
    total_buttons_height = len(table_names) * (button_height + button_gap) - button_gap
    start_y = (menu_surface.get_height() - total_buttons_height) // 2

    for i, (table_name, color) in enumerate(zip(table_names, table_colors)):
        button_x = (screen_width - button_width) // 2
        button_y = (screen_height - menu_surface.get_height()) // 2 + start_y + i * (button_height + button_gap)
        button = Button(table_name, button_x, button_y, button_width, button_height)
        button.draw(screen, text_color=(255, 0, 0), bg_color=(255, 0, 0, 1))

    pygame.display.flip()

def draw_exit_confirm_menu():
    exit_surface = pygame.Surface((screen_width // 2, screen_height // 2), pygame.SRCALPHA)
    exit_surface.blit(exit_background_image, (0, 0))
    screen.blit(exit_surface, (screen_width // 4, screen_height // 4))

    exit_text = font_button.render("Doriți să ieșiți?", True, (255, 255, 255))
    screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, screen_height // 2 - 100))

    yes_button = Button("Da", screen_width // 2 - 110, screen_height // 2, 100, 50)
    no_button = Button("Nu", screen_width // 2 + 10, screen_height // 2, 100, 50)

    yes_button.draw(screen, text_color=(255, 255, 255), bg_color=(255, 0, 0, 1))
    no_button.draw(screen, text_color=(255, 255, 255), bg_color=(0, 255, 0, 1))

    pygame.display.flip()

    return yes_button, no_button

def main_menu():
    global menu_open 
    menu_open = False  

    background_image = pygame.image.load(r"E:/Visual Studio Code/Python Joc Chimie/background1.png").convert_alpha()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    brightness_factor = 0.4 
    for y in range(background_image.get_height()):
        for x in range(background_image.get_width()):
            color = background_image.get_at((x, y))
            new_color = (min(color[0] * brightness_factor, 255),
                         min(color[1] * brightness_factor, 255),
                         min(color[2] * brightness_factor, 255),
                         color[3])
            background_image.set_at((x, y), new_color)

    play_button = Button("Joaca", screen_width // 2 - 50, screen_height // 2, 100, 50)
    exit_button = Button("Iesi", screen_width // 2 - 50, screen_height // 1.5, 100, 50)

    while True:
        screen.blit(background_image, (0, 0))

        title_text = font_title.render("Alchimia Alcanilor", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3))
        screen.blit(title_text, title_rect)

        play_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.is_clicked(event.pos):
                    loading_screen()
                    game_loop()
                elif exit_button.is_clicked(event.pos):
                    pygame.quit()
                    return

main_menu()
