import pygame
import random
import json
from db import get_personal_best

WIDTH = 600
HEIGHT = 600
CELL = 30
FPS = 60

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
DARK_RED = (120, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)
PURPLE = (130, 0, 180)
YELLOW = (230, 230, 0)
ORANGE = (255, 140, 0)


def load_settings():
    with open("settings.json", "r", encoding="utf-8") as file:
        return json.load(file)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def same_position(a, b):
    return a.x == b.x and a.y == b.y


def draw_grid(screen):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_background(screen):
    screen.fill(WHITE)


class Snake:
    def __init__(self, color):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

        self.score = 0
        self.level = 1
        self.alive = True

        self.color = tuple(color)

        self.base_delay = 200
        self.move_delay = 200
        self.last_move_time = pygame.time.get_ticks()

        self.shield = False

    def move(self):
        # Move snake body
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        # Move head
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def check_wall_collision(self):
        head = self.body[0]

        if head.x < 0 or head.x >= WIDTH // CELL or head.y < 1 or head.y >= HEIGHT // CELL:
            if self.shield:
                self.shield = False
                head.x = max(0, min(head.x, WIDTH // CELL - 1))
                head.y = max(1, min(head.y, HEIGHT // CELL - 1))
            else:
                self.alive = False

    def check_self_collision(self):
        head = self.body[0]

        for segment in self.body[1:]:
            if same_position(head, segment):
                if self.shield:
                    self.shield = False
                else:
                    self.alive = False

    def check_obstacle_collision(self, obstacles):
        head = self.body[0]

        for block in obstacles:
            if same_position(head, block):
                if self.shield:
                    self.shield = False
                else:
                    self.alive = False

    def draw(self, screen):
        head = self.body[0]

        pygame.draw.rect(
            screen,
            RED,
            (head.x * CELL, head.y * CELL, CELL, CELL)
        )

        for segment in self.body[1:]:
            pygame.draw.rect(
                screen,
                self.color,
                (segment.x * CELL, segment.y * CELL, CELL, CELL)
            )

    def grow(self):
        head = self.body[0]
        self.body.append(Point(head.x, head.y))

    def shorten(self, count):
        for _ in range(count):
            if len(self.body) > 1:
                self.body.pop()

        if len(self.body) <= 1:
            self.alive = False

    def update_level_and_speed(self):
        old_level = self.level
        self.level = 1 + self.score // 3

        self.base_delay = max(70, 200 - self.level * 15)
        self.move_delay = self.base_delay

        return self.level > old_level


class Food:
    def __init__(self):
        self.pos = Point(9, 9)
        self.weight = 1
        self.spawn_time = pygame.time.get_ticks()
        self.life_time = 8000
        self.generate([], [])

    def generate(self, snake_body, obstacles):
        self.weight = random.choice([1, 2, 3])

        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(1, HEIGHT // CELL - 1)

            in_snake = any(same_position(self.pos, s) for s in snake_body)
            in_obstacle = any(same_position(self.pos, o) for o in obstacles)

            if not in_snake and not in_obstacle:
                break

        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.life_time

    def draw(self, screen):
        if self.weight == 1:
            color = GREEN
            size = CELL
        elif self.weight == 2:
            color = BLUE
            size = CELL - 4
        else:
            color = PURPLE
            size = CELL - 8

        offset = (CELL - size) // 2

        pygame.draw.rect(
            screen,
            color,
            (
                self.pos.x * CELL + offset,
                self.pos.y * CELL + offset,
                size,
                size
            )
        )


class PoisonFood:
    def __init__(self):
        self.pos = Point(5, 5)
        self.spawn_time = pygame.time.get_ticks()
        self.life_time = 8000
        self.generate([], [])

    def generate(self, snake_body, obstacles):
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(1, HEIGHT // CELL - 1)

            in_snake = any(same_position(self.pos, s) for s in snake_body)
            in_obstacle = any(same_position(self.pos, o) for o in obstacles)

            if not in_snake and not in_obstacle:
                break

        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.life_time

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            DARK_RED,
            (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL)
        )


class PowerUp:
    def __init__(self):
        self.pos = Point(7, 7)
        self.kind = random.choice(["speed", "slow", "shield"])
        self.spawn_time = pygame.time.get_ticks()
        self.life_time = 8000
        self.active = True
        self.generate([], [])

    def generate(self, snake_body, obstacles):
        self.kind = random.choice(["speed", "slow", "shield"])
        self.active = True

        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(1, HEIGHT // CELL - 1)

            in_snake = any(same_position(self.pos, s) for s in snake_body)
            in_obstacle = any(same_position(self.pos, o) for o in obstacles)

            if not in_snake and not in_obstacle:
                break

        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.life_time

    def draw(self, screen):
        if not self.active:
            return

        if self.kind == "speed":
            color = ORANGE
        elif self.kind == "slow":
            color = BLUE
        else:
            color = PURPLE

        pygame.draw.rect(
            screen,
            color,
            (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL)
        )


def generate_obstacles(snake_body, count):
    obstacles = []

    while len(obstacles) < count:
        block = Point(
            random.randint(0, WIDTH // CELL - 1),
            random.randint(2, HEIGHT // CELL - 1)
        )

        head = snake_body[0]

        # Do not place obstacle near snake head
        near_head = abs(block.x - head.x) <= 2 and abs(block.y - head.y) <= 2
        in_snake = any(same_position(block, s) for s in snake_body)
        duplicate = any(same_position(block, o) for o in obstacles)

        if not near_head and not in_snake and not duplicate:
            obstacles.append(block)

    return obstacles


def draw_obstacles(screen, obstacles):
    for block in obstacles:
        pygame.draw.rect(
            screen,
            BLACK,
            (block.x * CELL, block.y * CELL, CELL, CELL)
        )


def game_loop(screen, clock, username):
    settings = load_settings()

    snake = Snake(settings["snake_color"])
    food = Food()
    poison = PoisonFood()
    power = PowerUp()

    obstacles = []

    food.generate(snake.body, obstacles)
    poison.generate(snake.body, obstacles)
    power.generate(snake.body, obstacles)

    personal_best = get_personal_best(username)

    font = pygame.font.SysFont(None, 30)
    small_font = pygame.font.SysFont(None, 24)

    active_power = None
    power_start = 0
    power_duration = 5000

    running = True

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if snake.alive and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx, snake.dy = 1, 0
                elif event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx, snake.dy = -1, 0
                elif event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx, snake.dy = 0, 1
                elif event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx, snake.dy = 0, -1

        if snake.alive:
            # Active power-up timer
            if active_power == "speed":
                snake.move_delay = max(40, snake.base_delay - 70)

                if current_time - power_start > power_duration:
                    active_power = None
                    snake.move_delay = snake.base_delay

            elif active_power == "slow":
                snake.move_delay = snake.base_delay + 120

                if current_time - power_start > power_duration:
                    active_power = None
                    snake.move_delay = snake.base_delay

            # Move snake by timer
            if current_time - snake.last_move_time > snake.move_delay:
                snake.move()

                snake.check_wall_collision()
                snake.check_self_collision()
                snake.check_obstacle_collision(obstacles)

                head = snake.body[0]

                # Normal food collision
                if same_position(head, food.pos):
                    snake.score += food.weight
                    snake.grow()

                    new_level = snake.update_level_and_speed()

                    if new_level and snake.level >= 3:
                        obstacles = generate_obstacles(snake.body, snake.level + 2)

                    food.generate(snake.body, obstacles)

                # Poison food collision
                if same_position(head, poison.pos):
                    snake.shorten(2)
                    poison.generate(snake.body, obstacles)

                # Power-up collision
                if power.active and same_position(head, power.pos):
                    active_power = power.kind
                    power_start = current_time
                    power.active = False

                    if active_power == "shield":
                        snake.shield = True
                        active_power = None

                snake.last_move_time = current_time

            # Food timers
            if food.is_expired():
                food.generate(snake.body, obstacles)

            if poison.is_expired():
                poison.generate(snake.body, obstacles)

            # Power-up timer on field
            if power.active and power.is_expired():
                power.generate(snake.body, obstacles)

            # Spawn new power-up if no power-up on field and no speed/slow active
            if not power.active and active_power is None:
                if random.randint(1, 200) == 1:
                    power.generate(snake.body, obstacles)

            # Draw
            draw_background(screen)

            if settings["grid"]:
                draw_grid(screen)

            draw_obstacles(screen, obstacles)
            food.draw(screen)
            poison.draw(screen)
            power.draw(screen)
            snake.draw(screen)

            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 35))

            score_text = small_font.render(f"Score: {snake.score}", True, WHITE)
            level_text = small_font.render(f"Level: {snake.level}", True, WHITE)
            best_text = small_font.render(f"Best: {personal_best}", True, WHITE)

            screen.blit(score_text, (5, 8))
            screen.blit(level_text, (130, 8))
            screen.blit(best_text, (240, 8))

            if active_power:
                remaining = max(0, (power_duration - (current_time - power_start)) // 1000)
                power_text = small_font.render(f"Power: {active_power} {remaining}s", True, WHITE)
                screen.blit(power_text, (360, 8))

            if snake.shield:
                shield_text = small_font.render("Shield", True, WHITE)
                screen.blit(shield_text, (500, 8))

        else:
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    return snake.score, snake.level, personal_best