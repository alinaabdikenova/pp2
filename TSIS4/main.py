import pygame
import json
from game import game_loop, WIDTH, HEIGHT, FPS
from db import create_tables, save_result, get_top_scores

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)
YELLOW = (230, 230, 0)

font_big = pygame.font.SysFont(None, 60)
font = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 26)


def load_settings():
    with open("settings.json", "r", encoding="utf-8") as file:
        return json.load(file)


def save_settings(settings):
    with open("settings.json", "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, GRAY, (x, y, w, h))
    label = font.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=(x + w // 2, y + h // 2)))
    return pygame.Rect(x, y, w, h)


def username_screen():
    username = ""

    while True:
        screen.fill(BLACK)

        title = font_big.render("Enter Username", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 160)))

        text = font.render(username + "|", True, WHITE)
        screen.blit(text, text.get_rect(center=(WIDTH // 2, 260)))

        hint = font_small.render("Press Enter to continue", True, WHITE)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 330)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username.strip() == "":
                        username = "Player"
                    return username

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    username += event.unicode

        pygame.display.flip()
        clock.tick(FPS)


def leaderboard_screen():
    while True:
        screen.fill(BLACK)

        title = font_big.render("Leaderboard", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 50)))

        rows = get_top_scores()

        y = 110

        if not rows:
            empty = font.render("No scores yet", True, WHITE)
            screen.blit(empty, empty.get_rect(center=(WIDTH // 2, 260)))
        else:
            for i, row in enumerate(rows, start=1):
                username, score, level, played_at = row

                line = font_small.render(
                    f"{i}. {username} | Score: {score} | Level: {level} | {played_at.strftime('%Y-%m-%d')}",
                    True,
                    WHITE
                )
                screen.blit(line, (30, y))
                y += 35

        back_btn = draw_button("Back", 200, 520, 200, 45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(FPS)


def settings_screen():
    settings = load_settings()

    while True:
        screen.fill(BLACK)

        title = font_big.render("Settings", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

        grid_text = "Grid: ON" if settings["grid"] else "Grid: OFF"
        

        grid_btn = draw_button(grid_text, 180, 130, 240, 45)
        

        yellow_btn = draw_button("Snake: Yellow", 180, 260, 240, 45)
        green_btn = draw_button("Snake: Green", 180, 320, 240, 45)
        blue_btn = draw_button("Snake: Blue", 180, 380, 240, 45)

        save_btn = draw_button("Save & Back", 180, 470, 240, 45)

        current = font_small.render(
            f"Current color: {settings['snake_color']}",
            True,
            WHITE
        )
        screen.blit(current, current.get_rect(center=(WIDTH // 2, 435)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if grid_btn.collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]


                elif yellow_btn.collidepoint(event.pos):
                    settings["snake_color"] = [230, 230, 0]

                elif green_btn.collidepoint(event.pos):
                    settings["snake_color"] = [0, 180, 0]

                elif blue_btn.collidepoint(event.pos):
                    settings["snake_color"] = [0, 0, 220]

                elif save_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return

        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen(score, level, best):
    while True:
        screen.fill(BLACK)

        title = font_big.render("Game Over", True, RED)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 140)))

        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        best_text = font.render(f"Personal Best: {best}", True, WHITE)

        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, 230)))
        screen.blit(level_text, level_text.get_rect(center=(WIDTH // 2, 270)))
        screen.blit(best_text, best_text.get_rect(center=(WIDTH // 2, 310)))

        retry_btn = draw_button("Retry", 200, 390, 200, 45)
        menu_btn = draw_button("Main Menu", 200, 450, 200, 45)

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


def main_menu():
    username = username_screen()

    while True:
        screen.fill(BLACK)

        title = font_big.render("Snake Game", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        user_text = font_small.render(f"Player: {username}", True, WHITE)
        screen.blit(user_text, user_text.get_rect(center=(WIDTH // 2, 155)))

        play_btn = draw_button("Play", 200, 220, 200, 45)
        leaderboard_btn = draw_button("Leaderboard", 200, 280, 200, 45)
        settings_btn = draw_button("Settings", 200, 340, 200, 45)
        quit_btn = draw_button("Quit", 200, 400, 200, 45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):

                    while True:
                        score, level, best = game_loop(screen, clock, username)

                        save_result(username, score, level)

                        if score > best:
                            best = score

                        action = game_over_screen(score, level, best)

                        if action == "retry":
                            continue

                        if action == "menu":
                            break

                elif leaderboard_btn.collidepoint(event.pos):
                    leaderboard_screen()

                elif settings_btn.collidepoint(event.pos):
                    settings_screen()

                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        pygame.display.flip()
        clock.tick(FPS)


create_tables()
main_menu()

pygame.quit()