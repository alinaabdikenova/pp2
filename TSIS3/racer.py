import pygame
import random
from persistence import add_score

WIDTH = 400
HEIGHT = 600
FPS = 60

#images will be loaded inside init_game_assets()
image_background = None
image_player = None
image_enemy = None
coin_image = None
sound_crash = None

BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)
ORANGE = (255, 150, 0)
PURPLE = (140, 0, 180)

def init_game_assets():
    global image_background, image_player, image_enemy, coin_image, sound_crash

    image_background = pygame.image.load("resources/AnimatedStreet.png")
    image_player = pygame.image.load("resources/Player.png")
    image_enemy = pygame.image.load("resources/Enemy.png")
    coin_image = pygame.image.load("resources/coin.png").convert_alpha()

    pygame.mixer.music.load("resources/background.wav")
    sound_crash = pygame.mixer.Sound("resources/crash.wav")

class Player(pygame.sprite.Sprite):
       def __init__(self, settings):
        super().__init__()

        self.original_image = image_player.copy()
        self.image = self.original_image

        color = settings["car_color"]

        if color == "red":
            self.image.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
        elif color == "green":
            self.image.fill((0, 255, 0), special_flags=pygame.BLEND_RGB_MULT)
        elif color == "blue":
            self.image.fill((0, 0, 255), special_flags=pygame.BLEND_RGB_MULT)

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10

        self.speed = 5
        self.shield = False

       def move(self):
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.rect.move_ip(-self.speed, 0)

            if keys[pygame.K_RIGHT]:
                 self.rect.move_ip(self.speed, 0)

            if self.rect.left < 0:
                self.rect.left = 0

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = speed
        self.respawn()

    def respawn(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.top = random.randint(-500, -80)

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > HEIGHT:
            self.respawn()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = coin_image
        self.weight = 1
        self.speed = 5
        self.generate()

    def generate(self):
        self.weight = random.choice([1, 2, 3])

        if self.weight == 1:
            size = 35
        elif self.weight == 2:
            size = 45
        else:
            size = 55

        self.image = pygame.transform.scale(self.base_image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.top = random.randint(-400, -50)

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > HEIGHT:
            self.generate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.type = random.choice(["barrier", "oil", "pothole"])
        self.speed = speed
        self.image = pygame.Surface((60, 30))
        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        self.type = random.choice(["barrier", "oil", "pothole"])

        if self.type == "barrier":
            self.image.fill(RED)
        elif self.type == "oil":
            self.image.fill(BLACK)
        else:
            self.image.fill(ORANGE)

        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.top = random.randint(-600, -100)

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > HEIGHT:
            self.respawn()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.kind = random.choice(["nitro", "shield", "repair"])
        self.speed = speed
        self.life_time = 6000
        self.spawn_time = pygame.time.get_ticks()
        self.image = pygame.Surface((35, 35))
        self.rect = self.image.get_rect()
        self.generate()

    def generate(self):
        self.kind = random.choice(["nitro", "shield", "repair"])

        if self.kind == "nitro":
            self.image.fill(BLUE)
        elif self.kind == "shield":
            self.image.fill(PURPLE)
        else:
            self.image.fill(GREEN)

        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.top = random.randint(-700, -100)
        self.spawn_time = pygame.time.get_ticks()

    def move(self):
        self.rect.move_ip(0, self.speed)

        now = pygame.time.get_ticks()

        if self.rect.top > HEIGHT or now - self.spawn_time > self.life_time:
            self.generate()

def game_loop(screen, clock, username, settings):
    font_small = pygame.font.SysFont("Verdana", 16)

    collected = 0
    distance = 0
    score = 0
    finish_distance = 3000

    active_power = None
    power_start_time = 0
    power_duration = 4000

    difficulty = settings["difficulty"]

    if difficulty == "easy":
        enemy_speed = 4
        obstacle_count = 1
    elif difficulty == "hard":
        enemy_speed = 7
        obstacle_count = 3
    else:
        enemy_speed = 5
        obstacle_count = 2

    player = Player(settings)

    traffic = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    powers = pygame.sprite.Group()

    for _ in range(2):
        traffic.add(TrafficCar(enemy_speed))

    for _ in range(obstacle_count):
        obstacles.add(Obstacle(enemy_speed))

    coins.add(Coin())
    powers.add(PowerUp(enemy_speed))

    if settings["sound"]:
        pygame.mixer.music.play(-1)

    while True:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        player.move()
        distance += 1

        # Difficulty scaling
        if distance % 700 == 0:
            enemy_speed += 1
            traffic.add(TrafficCar(enemy_speed))

        # Nitro effect
        if active_power == "nitro":
            player.speed = 9

            if now - power_start_time > power_duration:
                active_power = None
                player.speed = 5
        else:
            player.speed = 5

        for car in traffic:
            car.speed = enemy_speed
            car.move()

        for obstacle in obstacles:
            obstacle.speed = enemy_speed
            obstacle.move()

        for coin in coins:
            coin.move()

        for power in powers:
            power.speed = enemy_speed
            power.move()

        # Coin collision
        coin_hit = pygame.sprite.spritecollideany(player, coins)
        if coin_hit:
            collected += coin_hit.weight
            coin_hit.generate()

        # Power-up collision
        power_hit = pygame.sprite.spritecollideany(player, powers)
        if power_hit and active_power is None:
            active_power = power_hit.kind
            power_start_time = now

            if active_power == "shield":
                player.shield = True

            elif active_power == "repair":
                for obstacle in obstacles:
                    obstacle.respawn()
                active_power = None

            power_hit.generate()

        # Traffic collision
        if pygame.sprite.spritecollideany(player, traffic):
            if player.shield:
                player.shield = False
                active_power = None

                for car in traffic:
                    car.respawn()
            else:
                if settings["sound"]:
                    sound_crash.play()

                add_score(username, score, distance)
                return score, collected, distance

        # Obstacle collision
        obstacle_hit = pygame.sprite.spritecollideany(player, obstacles)

        if obstacle_hit:
            if obstacle_hit.type == "oil":
                player.speed = 2
                obstacle_hit.respawn()

            elif player.shield:
                player.shield = False
                active_power = None
                obstacle_hit.respawn()

            else:
                if settings["sound"]:
                    sound_crash.play()

                add_score(username, score, distance)
                return score, collected, distance

        score = collected * 10 + distance // 5

        # Finish
        if distance >= finish_distance:
            add_score(username, score, distance)
            return score, collected, distance

        screen.blit(image_background, (0, 0))

        for coin in coins:
            screen.blit(coin.image, coin.rect)

        for power in powers:
            screen.blit(power.image, power.rect)

        for obstacle in obstacles:
            screen.blit(obstacle.image, obstacle.rect)

        for car in traffic:
            screen.blit(car.image, car.rect)

        screen.blit(player.image, player.rect)

        info1 = font_small.render(f"Name: {username}", True, BLACK)
        info2 = font_small.render(f"Coins: {collected}", True, BLACK)
        info3 = font_small.render(f"Score: {score}", True, BLACK)
        info4 = font_small.render(f"Distance: {distance}/{finish_distance}", True, BLACK)

        screen.blit(info1, (10, 10))
        screen.blit(info2, (10, 30))
        screen.blit(info3, (10, 50))
        screen.blit(info4, (10, 70))

        if active_power:
            remaining = max(0, (power_duration - (now - power_start_time)) // 1000)
            power_text = font_small.render(f"Power: {active_power} {remaining}s", True, BLACK)
            screen.blit(power_text, (10, 90))

        if player.shield:
            shield_text = font_small.render("Shield: ON", True, BLUE)
            screen.blit(shield_text, (10, 110))

        pygame.display.flip()
        clock.tick(FPS) 

