import pygame
from racer import init_game_assets
from ui import main_menu

pygame.init()

WIDTH = 400
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer")

clock = pygame.time.Clock()

# Load images and sounds
init_game_assets()

# Start game from main menu
main_menu(screen, clock)

pygame.quit()