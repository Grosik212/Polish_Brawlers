import pygame
import game

class Fighter():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.attacking = False
        self.jumping = False

    def move(self, target):
        speed = 5
        dx = 0
        dy = 0
        gravity = 2

        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -speed
        if key[pygame.K_d]:
            dx = speed


        #stay on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > 800:
            dx = 800 - self.rect.right
        if self.rect.bottom + dy > 550:
            dy = 550 - self.rect.bottom
            self.vel_y = 0
            self.jumping = False

        #jump
        if self.vel_y == 0 and key[pygame.K_w] and not self.jumping:
            self.vel_y = -30
            self.jumping = True


        #apply gravity
        self.vel_y += gravity

        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        #attack
        if key[pygame.K_SPACE] and not self.attacking:
            self.attack_kick(game.screen, target)
        if key[pygame.K_q] and not self.attacking:
            self.attack_punch(game.screen, target)

    def attack_kick(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect((self.rect.x + 80, self.rect.y + 100, 100, 80))
        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10

    def attack_punch(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect((self.rect.x + 80, self.rect.y + 10, 80, 100))
        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
        if attacking_rect.colliderect(target.rect):
            target.health -= 5


    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)