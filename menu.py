import pygame
import sys
from pygame.locals import *
import button
import game

mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('Polish Brawlers')
pygame.display.set_icon(pygame.image.load('icon.png'))
screen = pygame.display.set_mode((800, 600), 0, 32)
font = pygame.font.Font(None, 90)
menu_music = pygame.mixer.Sound('Music/menu.mp3')
background = pygame.image.load("backgrounds/zabka.png").convert_alpha()
background = pygame.transform.scale(background, (800, 600))
top_image = pygame.image.load("crop.png").convert_alpha()
top_image = pygame.transform.scale(top_image, (350, 160))
speaker = pygame.image.load("speaker.png").convert_alpha()
speaker = pygame.transform.scale(speaker, (50, 50))

is_muted = False


def draw_text(text, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


start_button_image = pygame.image.load("Piskel/menu/start.png").convert_alpha()
options_button_image = pygame.image.load("Piskel/menu/options.png").convert_alpha()
credits_button_image = pygame.image.load("Piskel/menu/credits.png").convert_alpha()

start_button = button.Button(250, 230, start_button_image, 10)
options_button = button.Button(200, 360, options_button_image, 0.8)
credits_button = button.Button(200, 480, credits_button_image, 0.8)
mute_button = button.Button(700, 500, speaker, 1)
click = False


def main_menu():
    global is_muted
    selected_background = pygame.image.load("Backgrounds/background_bar.png")
    click = False
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
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def options():
    global is_muted
    running = True
    backgrounds = [
        pygame.image.load("Backgrounds/background_bar.png"),
        pygame.image.load("Backgrounds/cracovia.png"),
        pygame.image.load("Backgrounds/lech.png"),
        pygame.image.load("Backgrounds/zabka.png")
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
                    click = True
                    pos = pygame.mouse.get_pos()
                    if mute_button.rect.collidepoint(pos):
                        is_muted = not is_muted
                        if is_muted:
                            pygame.mixer.Sound.stop(menu_music)
                        else:
                            pygame.mixer.Sound.play(menu_music, loops=-1)
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

        if mute_button.draw(screen):
            is_muted = not is_muted
            if is_muted:
                pygame.mixer.Sound.stop(menu_music)
            else:
                pygame.mixer.Sound.play(menu_music, loops=-1)

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
    while running:
        screen.blit(background, (0, 0))

        draw_text('Credits', (255, 255, 255), screen, 280, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)
