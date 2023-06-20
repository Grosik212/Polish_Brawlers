import sys
from pygame.locals import *
import pygame
import Fighter


pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
font = pygame.font.Font(None, 90)
mainClock = pygame.time.Clock()

def game_over(winner):
    if winner == 1:
        text = font.render("Player 1 wins!", True, (255, 255, 255))
    else:
        text = font.render("Player 2 wins!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()


def show_controls(screen, selected_background):
    font_cont = pygame.font.Font(None, 26)
    selected_background = pygame.transform.scale(selected_background, (800, 600))
    screen.blit(selected_background, (0, 0))
    player1_controls = font_cont.render("Player 1 Controls: A - Left, D - Right, W - Jump, E - Kick, Q - Punch", True, (255, 255, 255))
    player2_controls = font_cont.render("Player 2 Controls: LEFT - Left, RIGHT - Right, UP - Jump, SPACE - Kick, m - Punch", True, (255, 255, 255))

    player1_controls_rect = player1_controls.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    player2_controls_rect = player2_controls.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    background_color = (0, 0, 0)
    padding = 10
    player1_bg_rect = player1_controls_rect.inflate(padding * 2, padding * 2)
    player2_bg_rect = player2_controls_rect.inflate(padding * 2, padding * 2)

    pygame.draw.rect(screen, background_color, player1_bg_rect)
    pygame.draw.rect(screen, background_color, player2_bg_rect)

    underline_thickness = 2
    pygame.draw.rect(screen, (255, 255, 255), player1_bg_rect, underline_thickness)
    pygame.draw.rect(screen, (255, 255, 255), player2_bg_rect, underline_thickness)

    screen.blit(player1_controls, player1_controls_rect)
    screen.blit(player2_controls, player2_controls_rect)

    pygame.display.flip()
    pygame.time.wait(7000)


def game(selected_background):
    selected_background = pygame.transform.scale(selected_background, (800, 600))
    show_controls(screen, selected_background)
    running = True
    game_paused = False

    # creating fighters
    fighter1 = Fighter.Player1(100, 350)
    fighter2 = Fighter.Player2(650, 350)

    while running:
        screen.blit(selected_background, (0, 0))

        if not game_paused:
            fighter1.draw(screen, fighter2)
            fighter2.draw(screen, fighter1)

            fighter1.move(fighter2)
            fighter2.move(fighter1)

            fighter1.update()
            fighter2.update()

            Fighter.HealthBar(fighter1).draw(screen)
            Fighter.HealthBar(fighter2).draw(screen)

            Fighter.LargeHealthBar(50, 50, fighter1).draw(screen)
            Fighter.LargeHealthBar(500, 50, fighter2).draw(screen)

            if fighter1.health <= 0:
                game_over(2)
            if fighter2.health <= 0:
                game_over(1)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit ()
                    sys.exit ()

            if event.type == KEYDOWN:
                if event.key == K_p:
                    game_paused = not game_paused

        if game_paused:
            pause_text = font.render("Game Paused", True, (255, 255, 255))
            pause_text_rect = pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(pause_text, pause_text_rect)

        pygame.display.flip()
        mainClock.tick(60)
