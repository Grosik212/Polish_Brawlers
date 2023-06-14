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
fighter1 = Fighter.Player1(100, 350)
fighter2 = Fighter.Player2(650, 350)

health_bar1 = Fighter.HealthBar(100, 380, fighter1)
health_bar2 = Fighter.HealthBar(600, 380, fighter2)


large_health_bar1 = Fighter.LargeHealthBar(50, 50, fighter1)
large_health_bar2 = Fighter.LargeHealthBar(500, 50, fighter2)
def game():
    running = True
    while running:
        screen.blit(background, (0, 0))

        fighter1.move(fighter2)
        # fighter2.move(fighter1)

        fighter1.draw(screen)
        fighter2.draw(screen)

        health_bar1.draw(screen)
        health_bar2.draw(screen)

        large_health_bar1.draw(screen)
        large_health_bar2.draw(screen)

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
