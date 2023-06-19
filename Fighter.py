import pygame


class Fighter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 80, 150)
        self.vel_y = 0
        self.jumping = False
        self.health = 100
        self.attack_cooldown = 0
        self.attack_type = 'none'

    def attack_kick(self, target):
        if target.rect.x < self.rect.x:
            attacking_rect = pygame.Rect((self.rect.x - 100, self.rect.y + 100, 100, 80))
        else:
            attacking_rect = pygame.Rect((self.rect.x + 80, self.rect.y + 100, 100, 80))
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
        self.attack_cooldown = 20
        self.attack_type = 'kick'

    def attack_punch(self, target):
        if target.rect.x < self.rect.x:
            attacking_rect = pygame.Rect((self.rect.x - 80, self.rect.y + 10, 80, 100))
        else:
            attacking_rect = pygame.Rect((self.rect.x + 80, self.rect.y + 10, 80, 100))
        if attacking_rect.colliderect(target.rect):
            target.health -= 5
        self.attack_cooldown = 20
        self.attack_type = 'punch'


class Player1(Fighter):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Animations
        self.images_walking = []  # List storing walking animation images
        self.images_punch = []  # List storing punch animation images
        self.images_kick = []  # List storing kick animation images
        self.current_frame = 0  # Current animation frame
        self.animation_delay = 100  # Delay between animation frames (smaller value = faster animation)
        self.last_frame_change = pygame.time.get_ticks()  # Time of the last frame change
        self.load_images()  # Loading animation images
        self.image = self.images_walking[self.current_frame]  # Setting the initial image

    def load_images(self):
        for i in range(1, 4):
            image = pygame.image.load(f"Piskel/Player1/Walking/Walking-{i}.png").convert_alpha()
            self.images_walking.append(image)

        # Loading punch animation images
        for i in range(1, 3):
            image = pygame.image.load(f"Piskel/Player1/Attack_punch/Punch-{i}.png").convert_alpha()
            self.images_punch.append(image)

        # Loading kick animation images
        for i in range(1, 3):
            image = pygame.image.load(f"Piskel/Player1/Attack_kick/Kick-{i}.png").convert_alpha()
            self.images_kick.append(image)

    def update(self):
        # Updating animation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_change >= self.animation_delay:
            self.current_frame += 1
            if self.current_frame >= len(self.images_walking):
                self.current_frame = 0

            if self.attack_cooldown > 0:
                if self.attack_type == 'punch':
                    # Punch animation during cooldown
                    self.image = self.images_punch[self.current_frame % len(self.images_punch)]

                elif self.attack_type == 'kick':
                    # Kick animation during cooldown
                    self.image = self.images_kick[self.current_frame % len(self.images_kick)]
            else:
                self.image = self.images_walking[self.current_frame]

            self.last_frame_change = current_time

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def draw(self, surface, target):
        image_rect = self.image.get_rect(center = self.rect.center)
        if self.rect.x < target.rect.x:
            surface.blit(self.image, image_rect)
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            flipped_rect = flipped_image.get_rect(center = self.rect.center)
            surface.blit(flipped_image, flipped_rect)

    def move(self, target):
        speed = 5
        dx = 0
        dy = 0
        gravity = 2

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            dx = -speed
        if keys[pygame.K_d]:
            dx = speed

        # Staying on the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > 800:
            dx = 800 - self.rect.right
        if self.rect.bottom + dy > 550:
            dy = 550 - self.rect.bottom
            self.vel_y = 0
            self.jumping = False

        # Jump
        if self.vel_y == 0 and keys[pygame.K_w] and not self.jumping:
            self.vel_y = -30
            self.jumping = True

        # Applying gravity
        self.vel_y += gravity
        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        # Attack
        if keys[pygame.K_e] and self.attack_cooldown == 0:
            super().attack_kick(target)
        if keys[pygame.K_q] and self.attack_cooldown == 0:
            super().attack_punch(target)


class Player2(Fighter):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Animacje
        self.images_walking = []  # Lista przechowująca obrazy animacji chodzenia
        self.images_punch = []  # Lista przechowująca obrazy animacji uderzenia pięścią
        self.images_kick = []  # Lista przechowująca obrazy animacji kopnięcia
        self.current_frame = 0  # Aktualna klatka animacji
        self.animation_delay = 100  # Opóźnienie między klatkami animacji (im mniejsza wartość, tym szybsza animacja)
        self.last_frame_change = pygame.time.get_ticks()  # Czas ostatniej zmiany klatki
        self.load_images()  # Ładowanie obrazów animacji
        self.image = self.images_walking[self.current_frame]  # Ustawienie obrazu początkowego

    def load_images(self):
        for i in range(1, 4):
            image = pygame.image.load(f"Piskel/Player2/Walking/Walking-{i}.png").convert_alpha()
            self.images_walking.append(image)

        # Ładowanie obrazów animacji uderzenia pięścią
        for i in range(1, 3):
            image = pygame.image.load(f"Piskel/Player2/Attack_punch/Punch-{i}.png").convert_alpha()
            self.images_punch.append(image)

        # Ładowanie obrazów animacji kopnięcia
        for i in range(1, 3):
            image = pygame.image.load(f"Piskel/Player2/Attack_kick/Kick-{i}.png").convert_alpha()
            self.images_kick.append(image)

    def update(self):
        # Aktualizacja animacji
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_change >= self.animation_delay:
            self.current_frame += 1
            if self.current_frame >= len(self.images_walking):
                self.current_frame = 0

            if self.attack_cooldown > 0:
                if self.attack_type == 'punch':
                    # Animacja punch w trakcie cooldown
                    self.image = self.images_punch[self.current_frame % len(self.images_punch)]
                elif self.attack_type == 'kick':
                    # Animacja kopania w trakcie cooldown
                    self.image = self.images_kick[self.current_frame % len(self.images_kick)]
            else:

                self.image = self.images_walking[self.current_frame]

            self.last_frame_change = current_time

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def draw(self, surface, target):
        image_rect = self.image.get_rect(center = self.rect.center)
        if self.rect.x < target.rect.x:
            surface.blit(self.image, image_rect)
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            flipped_rect = flipped_image.get_rect(center = self.rect.center)
            surface.blit(flipped_image, flipped_rect)

    def move(self, target):
        speed = 5
        dx = 0
        dy = 0
        gravity = 2

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx = -speed
        if keys[pygame.K_RIGHT]:
            dx = speed

        # Pozostanie na ekranie
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > 800:
            dx = 800 - self.rect.right
        if self.rect.bottom + dy > 550:
            dy = 550 - self.rect.bottom
            self.vel_y = 0
            self.jumping = False

        # Skok
        if self.vel_y == 0 and keys[pygame.K_UP] and not self.jumping:
            self.vel_y = -30
            self.jumping = True

        # Zastosowanie grawitacji
        self.vel_y += gravity
        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        # Atak
        if keys[pygame.K_SPACE] and self.attack_cooldown == 0:
            super().attack_kick(target)
        if keys[pygame.K_m] and self.attack_cooldown == 0:
            super().attack_punch(target)


class HealthBar:
    def __init__(self, fighter):
        self.fighter = fighter

    def draw(self, surface):
        self.draw_health(surface)

    def draw_health(self, surface):
        health_width = int(self.fighter.rect.width * (self.fighter.health / 100))
        health_rect = pygame.Rect(self.fighter.rect.left, self.fighter.rect.top - 50, health_width, 10)
        hit_rect = pygame.Rect(self.fighter.rect.left, self.fighter.rect.top - 50, 80, 10)
        pygame.draw.rect(surface, (255, 0, 0), hit_rect)
        pygame.draw.rect(surface, (0, 255, 0), health_rect)


class LargeHealthBar:
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
