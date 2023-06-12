import sys
from pygame.locals import *
import pygame
import Fighter

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
font = pygame.font.Font(None, 90)
mainClock = pygame.time.Clock()
background = pygame.image.load("backgrounds/background_bar.png").convert_alpha()
background = pygame.transform.scale(background, (800, 600))

# creating fighters
fighter1 = Fighter.Fighter(100, 350)
fighter2 = Fighter.Fighter(650, 350)


def game():
    running = True
    while running:
        screen.blit(background, (0, 0))

        fighter1.move(fighter2)
        # fighter2.move(fighter1)

        fighter1.draw(screen)
        fighter2.draw(screen)


        click = False
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
