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
    textobj = font.render(text, 1, color)
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
    click = False
    pygame.mixer.Sound.play(menu_music, loops=-1)
    while True:
        screen.blit(background, (0, 0))
        screen.blit(top_image, (205, 30))

        if start_button.draw(screen):
            game.game()
        if options_button.draw(screen):
            options()
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
    while running:
        screen.blit(background, (0, 0))
        draw_text('Options', (255, 255, 255), screen, 280, 20)

        if mute_button.draw(screen):
            is_muted = not is_muted
            if is_muted:
                menu_music.stop()
            else:
                pygame.mixer.Sound.play(menu_music, loops=-1)

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

        pygame.display.update()
        mainClock.tick(60)


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
