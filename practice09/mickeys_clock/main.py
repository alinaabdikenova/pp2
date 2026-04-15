import pygame
from clock import MickeyClock 

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Mickey Clock OOP")
clock = pygame.time.Clock()


mickey_clock = MickeyClock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill((255, 255, 255))
    
    
    mickey_clock.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()