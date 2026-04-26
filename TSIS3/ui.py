import pygame
from persistence import load_settings, save_settings, load_leaderboard
from racer import game_loop

WIDTH = 400
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GRAY = (100, 100, 100)


def draw_button(screen, font, text, x, y, w, h):
    # Draw simple button
    pygame.draw.rect(screen, GRAY, (x, y, w, h))

    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))

    screen.blit(label, label_rect)

    return pygame.Rect(x, y, w, h)


def get_username(screen, clock):
    # Screen for entering player name
    font_big = pygame.font.SysFont("Verdana", 42)
    font = pygame.font.SysFont("Verdana", 20)
    font_small = pygame.font.SysFont("Verdana", 16)

    name = ""

    while True:
        screen.fill(BLACK)

        title = font_big.render("Enter Name", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 150)))

        text = font.render(name + "|", True, WHITE)
        screen.blit(text, text.get_rect(center=(WIDTH // 2, 250)))

        hint = font_small.render("Press Enter to start", True, WHITE)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 320)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() == "":
                        name = "Player"
                    return name

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    name += event.unicode

        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen(screen, clock, score, coins, distance):
    # Game over screen with retry and menu buttons
    font_big = pygame.font.SysFont("Verdana", 42)
    font = pygame.font.SysFont("Verdana", 20)

    while True:
        screen.fill(BLACK)

        title = font_big.render("Game Over", True, RED)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 150)))

        score_text = font.render(f"Score: {score}", True, WHITE)
        coins_text = font.render(f"Coins: {coins}", True, WHITE)
        distance_text = font.render(f"Distance: {distance}", True, WHITE)

        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, 230)))
        screen.blit(coins_text, coins_text.get_rect(center=(WIDTH // 2, 260)))
        screen.blit(distance_text, distance_text.get_rect(center=(WIDTH // 2, 290)))

        retry_btn = draw_button(screen, font, "Retry", 100, 360, 200, 45)
        menu_btn = draw_button(screen, font, "Main Menu", 100, 420, 200, 45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    return "retry"

                if menu_btn.collidepoint(event.pos):
                    return "menu"

        pygame.display.flip()
        clock.tick(FPS)


def leaderboard_screen(screen, clock):
    # Show top 10 scores from leaderboard.json
    font_big = pygame.font.SysFont("Verdana", 38)
    font = pygame.font.SysFont("Verdana", 20)
    font_small = pygame.font.SysFont("Verdana", 16)

    while True:
        screen.fill(BLACK)

        title = font_big.render("Leaderboard", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

        leaderboard = load_leaderboard()

        y = 120

        if not leaderboard:
            empty_text = font.render("No scores yet", True, WHITE)
            screen.blit(empty_text, empty_text.get_rect(center=(WIDTH // 2, 250)))
        else:
            for i, item in enumerate(leaderboard[:10], start=1):
                text = font_small.render(
                    f"{i}. {item['name']} | Score: {item['score']} | Distance: {item['distance']}",
                    True,
                    WHITE
                )
                screen.blit(text, (25, y))
                y += 30

        back_btn = draw_button(screen, font, "Back", 100, 520, 200, 45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(FPS)


def settings_screen(screen, clock):
    # Settings screen: sound, car color and difficulty
    font_big = pygame.font.SysFont("Verdana", 42)
    font = pygame.font.SysFont("Verdana", 18)
    font_small = pygame.font.SysFont("Verdana", 15)

    settings = load_settings()

    while True:
        screen.fill(BLACK)

        title = font_big.render("Settings", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 45)))

        sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"

        sound_btn = draw_button(screen, font, sound_text, 80, 90, 240, 35)

        red_btn = draw_button(screen, font, "Car Color: Red", 80, 140, 240, 35)
        blue_btn = draw_button(screen, font, "Car Color: Blue", 80, 185, 240, 35)
        green_btn = draw_button(screen, font, "Car Color: Green", 80, 230, 240, 35)

        easy_btn = draw_button(screen, font, "Difficulty: Easy", 80, 290, 240, 35)
        normal_btn = draw_button(screen, font, "Difficulty: Normal", 80, 335, 240, 35)
        hard_btn = draw_button(screen, font, "Difficulty: Hard", 80, 380, 240, 35)

        current = font_small.render(
            f"Current: color={settings['car_color']} | difficulty={settings['difficulty']}",
            True,
            WHITE
        )
        screen.blit(current, current.get_rect(center=(WIDTH // 2, 445)))

        back_btn = draw_button(screen, font, "Back", 80, 500, 240, 35)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)

                elif red_btn.collidepoint(event.pos):
                    settings["car_color"] = "red"
                    save_settings(settings)

                elif blue_btn.collidepoint(event.pos):
                    settings["car_color"] = "blue"
                    save_settings(settings)

                elif green_btn.collidepoint(event.pos):
                    settings["car_color"] = "green"
                    save_settings(settings)

                elif easy_btn.collidepoint(event.pos):
                    settings["difficulty"] = "easy"
                    save_settings(settings)

                elif normal_btn.collidepoint(event.pos):
                    settings["difficulty"] = "normal"
                    save_settings(settings)

                elif hard_btn.collidepoint(event.pos):
                    settings["difficulty"] = "hard"
                    save_settings(settings)

                elif back_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return

        pygame.display.flip()
        clock.tick(FPS)


def main_menu(screen, clock):
    # Main menu screen
    font_big = pygame.font.SysFont("Verdana", 42)
    font = pygame.font.SysFont("Verdana", 20)

    while True:
        screen.fill(BLACK)

        title = font_big.render("Racer Game", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        play_btn = draw_button(screen, font, "Play", 100, 200, 200, 45)
        leaderboard_btn = draw_button(screen, font, "Leaderboard", 100, 260, 200, 45)
        settings_btn = draw_button(screen, font, "Settings", 100, 320, 200, 45)
        quit_btn = draw_button(screen, font, "Quit", 100, 380, 200, 45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    username = get_username(screen, clock)

                    while True:
                        settings = load_settings()

                        score, coins, distance = game_loop(
                            screen,
                            clock,
                            username,
                            settings
                        )

                        action = game_over_screen(
                            screen,
                            clock,
                            score,
                            coins,
                            distance
                        )

                        if action == "retry":
                            continue

                        if action == "menu":
                            break

                elif leaderboard_btn.collidepoint(event.pos):
                    leaderboard_screen(screen, clock)

                elif settings_btn.collidepoint(event.pos):
                    settings_screen(screen, clock)

                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        pygame.display.flip()
        clock.tick(FPS)