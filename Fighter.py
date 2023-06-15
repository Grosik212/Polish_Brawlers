import pygame
import game


class Fighter:
        def __init__(self, x, y):
            self.rect = pygame.Rect((x, y, 80, 180))
            self.vel_y = 0
            self.jumping = False
            self.health = 100
            self.attack_cooldown = 0

            # Cooldown
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1

        def draw(self, surface):
            pygame.draw.rect(surface, (255, 0, 0), self.rect)


        def attack_kick(self, surface, target):
            attacking_rect = pygame.Rect((self.rect.x + 80, self.rect.y + 100, 100, 80))
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
            self.attack_cooldown = 10


        def attack_punch(self, surface, target):
            attacking_rect = pygame.Rect((self.rect.x + 80, self.rect.y + 10, 80, 100))
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
            if attacking_rect.colliderect(target.rect):
                target.health -= 5
            self.attack_cooldown = 10


class Player1(Fighter):
    def __init__(self, x, y):
        super().__init__(x, y)

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

        # Stay on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > 800:
            dx = 800 - self.rect.right
        if self.rect.bottom + dy > 550:
            dy = 550 - self.rect.bottom
            self.vel_y = 0
            self.jumping = False

        # Jump
        if self.vel_y == 0 and key[pygame.K_w] and not self.jumping:
            self.vel_y = -30
            self.jumping = True

        # Apply gravity
        self.vel_y += gravity
        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        # Attack
        if key[pygame.K_e] and self.attack_cooldown == 0:
            super().attack_kick(game.screen, target)
        if key[pygame.K_q] and self.attack_cooldown == 0:
            super().attack_punch(game.screen, target)


class Player2(Fighter):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self, target):
        speed = 5
        dx = 0
        dy = 0
        gravity = 2


        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = -speed
        if key[pygame.K_RIGHT]:
            dx = speed

        # Stay on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > 800:
            dx = 800 - self.rect.right
        if self.rect.bottom + dy > 550:
            dy = 550 - self.rect.bottom
            self.vel_y = 0
            self.jumping = False

        # Jump
        if self.vel_y == 0 and key[pygame.K_UP] and not self.jumping:
            self.vel_y = -30
            self.jumping = True

        # Apply gravity
        self.vel_y += gravity
        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        # Attack
        if key[pygame.K_SPACE] and self.attack_cooldown == 0:
            super().attack_kick(game.screen, target)
        if key[pygame.KMOD_ALT] and self.attack_cooldown == 0:
            super().attack_punch(game.screen, target)


class HealthBar:
    def __init__(self, x, y, fighter):
        self.rect = pygame.Rect(x, y, 80, 10)
        self.fighter = fighter

    def draw(self, surface):
        self.draw_health(surface)

    def draw_health(self, surface):
        health_width = int(self.fighter.rect.width * (self.fighter.health / 100))
        health_rect = pygame.Rect(self.fighter.rect.left, self.fighter.rect.top - 20, health_width, 10)
        hit_rect = pygame.Rect(self.fighter.rect.left, self.fighter.rect.top - 20, 80, 10)
        pygame.draw.rect(surface, (255, 0, 0), hit_rect)
        pygame.draw.rect(surface, (0, 255, 0), health_rect)


class LargeHealthBar():
    def __init__(self, x, y, fighter):
        self.rect = pygame.Rect(x, y, 250, 20)
        self.fighter = fighter

    def draw(self, surface):
        self.draw_health(surface)
        self.draw_health_text(surface)

    def draw_health(self, surface):
        health_width = int(self.rect.width * (self.fighter.health / 100))
        health_rect = pygame.Rect(self.rect.left, self.rect.top, health_width, self.rect.height)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        pygame.draw.rect(surface, (0, 255, 0), health_rect)

    def draw_health_text(self, surface):
        health_text = f"{self.fighter.health}/100"
        font = pygame.font.Font(None, 24)
        text_surface = font.render(health_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        surface.blit(text_surface, text_rect)

