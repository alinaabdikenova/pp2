import pygame
from color_palette import *
import random

pygame.init() # initializes all the pygame sub-modules

WIDTH = 600
HEIGHT = 600
CELL = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.SysFont(None, 36)

image_game_over = font.render("Game Over", True, colorRED)
image_game_over_rect = image_game_over.get_rect(center = (WIDTH // 2, HEIGHT // 2))
sc_rect = image_game_over.get_rect(center = ( WIDTH // 2, HEIGHT // 2 + 30))


def draw_grid_chess():
    # draw chess-style background
    colors = [colorWHITE, colorGRAY]

    for i in range(HEIGHT // 2):
        for j in range(WIDTH // 2):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        #direction of snake movement 
        self.dx = 1
        self.dy = 0

        self.score = 0
        self.level = 1
        self.alive = True

        self.move_delay = 200
        self.last_move_time = pygame.time.get_ticks()

    def move(self):
        #move body segments
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        #move head
        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # checks the right border
        if self.body[0].x > WIDTH // CELL - 1:
            self.alive = False
        # checks the left border
        if self.body[0].x < 0:
            self.alive = False
        # checks the bottom border
        if self.body[0].y > HEIGHT // CELL - 1:
            self.alive = False
        # checks the top border
        if self.body[0].y < 0:
            self.alive = False

        #check collision with itself 
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                self.alive = False


    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL)) #draw head
        for segment in self.body[1:]: #draw body
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.score += food.weight
            # add new segment to snake body
            self.body.append(Point(head.x, head.y))
            #update level
            self.level = 1 + self.score // 3

            # increase snake speed by decreasing delay
            self.move_delay = max(70, 200 - self.level * 15)
            food.generate_random_food(self.body)
            

class Food:
    def __init__(self):
        self.pos = Point(9, 9)
        self.weight = 1
        #time when food was generated
        self.spawn_time = pygame.time.get_ticks()

        #food disappears after this time
        self.life_time = 6000

    def draw(self):

        if self.weight == 1:
            color = colorGREEN
            size = CELL
        elif self.weight == 2:
            color = colorBLUE
            size = CELL - 4
        else:
            color = colorPURPLE
            size = CELL - 8

        offset = (CELL - size) // 2


        pygame.draw.rect(screen, color, (self.pos.x * CELL + offset, self.pos.y * CELL + offset, size, size))

    def generate_random_food(self, snake_body):
        #random food weight
        self.weight = random.choice([1, 2, 3])

        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, HEIGHT // CELL - 1)
            if not any(self.pos.x == s.x and self.pos.y == s.y for s in snake_body) and self.pos.y > 0:
                break

        #reset food timer
        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        #check if food dissapeared by timer
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time > self.life_time

#setup
FPS = 5
clock = pygame.time.Clock()

food = Food()
snake = Snake()
food.generate_random_food(snake.body)  
running = True

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #control snake 
        if snake.alive and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP:
                snake.dx, snake.dy = 0, -1

    
    if snake.alive:
        # move snake only when enough time has passed
        if current_time - snake.last_move_time > snake.move_delay:
            snake.move()
            snake.check_collision(food)
            snake.last_move_time = current_time

        #if food timer is over, generate new food
        if food.is_expired():
            food.generate_random_food(snake.body)


        draw_grid_chess()

        snake.draw()
        food.draw()
        pygame.draw.rect(screen, colorBLACK, (0, 0, WIDTH, 35))
        
        score_text = font.render(f"Score: {snake.score}", True, colorWHITE)
        level_text = font.render(f"Level: {snake.level}", True, colorWHITE)
        weight_text = font.render(f"Food: +{food.weight}", True, colorWHITE)

        screen.blit(score_text, (2, 0))
        screen.blit(level_text, (140, 0))
        screen.blit(weight_text, (270, 0))    

    else:
        
        result_text = f"Score: {snake.score}  Level: {snake.level}"
        sc_r = font.render(result_text, True, colorRED)
        
        screen.fill(colorBLACK)
        screen.blit(image_game_over, image_game_over_rect)
        screen.blit(sc_r, sc_rect)
       

    pygame.display.flip() 
    clock.tick(FPS)

pygame.quit()