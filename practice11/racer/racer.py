import pygame
import random
import time

pygame.init() # initializes all the pygame sub-modules
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # creating a game window
# set_mode() takes a tuple as an argument

#load images
image_background = pygame.image.load('resources/AnimatedStreet.png')
image_player = pygame.image.load('resources/Player.png')
image_enemy = pygame.image.load('resources/Enemy.png')
coin_image = pygame.image.load('resources/coin.png').convert_alpha()

collected = 0 #score

pygame.mixer.music.load('resources/background.wav') #load sounds
pygame.mixer.music.play(-1) #loop music 

sound_crash = pygame.mixer.Sound('resources/crash.wav')

# fonts
font = pygame.font.SysFont("Verdana", 60)  
fontt = pygame.font.SysFont("Verdana", 20)

image_game_over = font.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center = (WIDTH // 2, HEIGHT // 2))


speed_up_every = 5
max_enemy_speed = 15

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5
        

    def move(self):
        #get pressed keys
        keys = pygame.key.get_pressed()

        #move player left or right
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
            # keep inside screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 5
        

    def generate_random_rect(self):
        #generate enemy in random x position 
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0 # start from top

    def increase_speed(self):
        #increase enemy speed 
        if self.speed < max_enemy_speed:
            self.speed += 1


    def move(self):
        #move enemy down
        self.rect.move_ip(0, self.speed)
        # if enemy goes out of screen, generate it again
        if self.rect.top > HEIGHT:
            self.generate_random_rect()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = coin_image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  

        self.speed = 5
        self.weight = 1 #coin value

        self.generate_random_coin()       

    def generate_random_coin(self):
        # randomly choose coin weight
        self.weight = random.choice([1, 2, 3])
        #change coin size depending on weight 
        if self.weight == 1:
            size = 40
        elif self.weight == 2:
            size = 50
        else:
            size = 60

        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()

        # random x, but keep it within screen width
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.top = random.randint(-300, -50)
    
    def move(self):
        #move coin down
        self.rect.move_ip(0, self.speed)
        #if it gets out of screen generate a new one
        if self.rect.top > HEIGHT:
             self.generate_random_coin() 

running = True

# this object allows us to set the FPS
clock = pygame.time.Clock()
FPS = 60

player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy, coin)
enemy_sprites.add(enemy)
coin_sprites.add(coin)

last_speed_level = 0 #to increase speed only per n coins

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(image_background, (0, 0)) 

    score = fontt.render(f"Score: {collected}", True, "black")
    screen.blit(score, (270, 10))
    

    #move and draw objects
    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)
        
        
    # coin collision
    if pygame.sprite.spritecollideany(player, coin_sprites):
        collected += coin.weight
        coin.generate_random_coin()

    # increase enemy speed when player earns n coins 
    current_speed_level = collected // speed_up_every
    if current_speed_level > last_speed_level:
        enemy.increase_speed()
        last_speed_level = current_speed_level

    #enemy collision
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)

        running = False

        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()

        time.sleep(3)
        
    
    pygame.display.flip() # updates the screen
    clock.tick(FPS) # sets the FPS

pygame.quit()