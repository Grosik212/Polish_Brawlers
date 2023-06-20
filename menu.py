import pygame
import sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN
from button import Button
import game

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Polish Brawlers')
pygame.display.set_icon(pygame.image.load('Graphics/icon.png'))

background = pygame.image.load("Graphics/backgrounds/zabka.png").convert_alpha()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
top_image = pygame.image.load("Graphics/crop.png").convert_alpha()
top_image = pygame.transform.scale(top_image, (350, 160))
speaker = pygame.image.load("Graphics/speaker.png").convert_alpha()
speaker = pygame.transform.scale(speaker, (50, 50))

font = pygame.font.Font(None, 90)

menu_music = pygame.mixer.Sound('Music/menu.mp3')

start_button_image = pygame.image.load("Graphics/Piskel/menu/start.png").convert_alpha()
options_button_image = pygame.image.load("Graphics/Piskel/menu/options.png").convert_alpha()
credits_button_image = pygame.image.load("Graphics/Piskel/menu/credits.png").convert_alpha()

start_button = Button(250, 230, start_button_image, 10)
options_button = Button(200, 360, options_button_image, 0.8)
credits_button = Button(200, 480, credits_button_image, 0.8)
mute_button = Button(700, 500, speaker, 1)
is_muted = False


def draw_text(text, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def handle_event(event):
    global is_muted
    if event.type == MOUSEBUTTONDOWN:
        if mute_button.rect.collidepoint(event.pos):
            is_muted = not is_muted
            if is_muted:
                pygame.mixer.Sound.stop(menu_music)
            else:
                pygame.mixer.Sound.play(menu_music, loops=-1)


def options():
    running = True
    backgrounds = [
        pygame.image.load("Graphics/Backgrounds/background_bar.png"),
        pygame.image.load("Graphics/Backgrounds/cracovia.png"),
        pygame.image.load("Graphics/Backgrounds/lech.png"),
        pygame.image.load("Graphics/Backgrounds/zabka.png")
    ]
    selected_background = backgrounds[0]
    thumbnail_size = (200, 150)
    thumbnail_padding = 50
    num_columns = 2
    num_rows = 2
    total_thumbnails = num_columns * num_rows
    start_x = (screen.get_width() - (thumbnail_size[0] + thumbnail_padding) * num_columns) // 2
    start_y = (screen.get_height() - (thumbnail_size[1] + thumbnail_padding) * num_rows) // 2

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    handle_event(event)
                    pos = pygame.mouse.get_pos()
                    for i in range(total_thumbnails):
                        col = i % num_columns
                        row = i // num_columns
                        x = start_x + col * (thumbnail_size[0] + thumbnail_padding)
                        y = start_y + row * (thumbnail_size[1] + thumbnail_padding)
                        thumbnail_rect = pygame.Rect(x, y, thumbnail_size[0], thumbnail_size[1])
                        if thumbnail_rect.collidepoint(pos):
                            selected_background = backgrounds[i]
                            running = False

        screen.blit(background, (0, 0))
        draw_text('Options', (255, 255, 255), screen, 280, 20)

        mute_button.draw(screen)

        for i in range(total_thumbnails):
            col = i % num_columns
            row = i // num_columns
            x = start_x + col * (thumbnail_size[0] + thumbnail_padding)
            y = start_y + row * (thumbnail_size[1] + thumbnail_padding)

            thumbnail_rect = pygame.Rect(x, y, thumbnail_size[0], thumbnail_size[1])
            thumbnail = pygame.transform.scale(backgrounds[i], thumbnail_size)
            screen.blit(thumbnail, (x, y))
            if thumbnail_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (0, 255, 0), thumbnail_rect, 5)
            else:
                pygame.draw.rect(screen, (255, 255, 255), thumbnail_rect, 5)

        pygame.display.flip()

    return selected_background


def credits():
    running = True
    font_cont = pygame.font.Font(None, 100)
    padding = 10
    background_color = (0, 0, 0)
    credits_text = font_cont.render("Credits", True, (255, 255, 255))
    credits_text_rect = credits_text.get_rect(center=(screen.get_width() // 2, 50))
    credits_bg_rect = credits_text_rect.inflate(padding * 2, padding * 2)
    text1 = font_cont.render("Game made by:", True, (255, 255, 255))
    text1_rect = text1.get_rect(center=(screen.get_width() // 2, 200))
    text1_bg_rect = text1_rect.inflate(padding * 2, padding * 2)
    text2 = font_cont.render("Bartosz Grosicki", True, (255, 255, 255))
    text2_rect = text2.get_rect(center=(screen.get_width() // 2, 300))
    text2_bg_rect = text2_rect.inflate(padding * 2, padding * 2)
    while running:
        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, background_color, credits_bg_rect)
        screen.blit(credits_text, credits_text_rect)
        pygame.draw.rect(screen, background_color, text1_bg_rect)
        screen.blit(text1, text1_rect)
        pygame.draw.rect(screen, background_color, text2_bg_rect)
        screen.blit(text2, text2_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()


def main_menu():
    selected_background = pygame.image.load("Graphics/Backgrounds/background_bar.png")
    pygame.mixer.Sound.play(menu_music, loops=-1)
    while True:
        screen.blit(background, (0, 0))
        screen.blit(top_image, (205, 30))

        if start_button.draw(screen):
            game.game(selected_background)
        if options_button.draw(screen):
            selected_background = options()
        if credits_button.draw(screen):
            credits()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    handle_event(event)

        pygame.display.update()

