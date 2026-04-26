import pygame
from datetime import datetime
from tools import *

pygame.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 18)
text_font = pygame.font.SysFont("Arial", 28)

# Canvas
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

# Current settings
mode = "blue"
tool = "pencil"
brush_size = 5

# Drawing variables
drawing = False
start_pos = None
end_pos = None
last_pos = None

# Text tool variables
text_mode = False
text_pos = None
text_value = ""


def save_canvas():
    # Save canvas with timestamp
    time_now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paint_{time_now}.png"
    pygame.image.save(canvas, filename)
    print(f"Saved as {filename}")


def draw_selected_shape(surface, tool, start, end, color, width):
    # Draw selected shape depending on current tool
    if tool == "line":
        draw_line(surface, start, end, color, width)
    elif tool == "rect":
        draw_rectangle(surface, start, end, color, width)
    elif tool == "circle":
        draw_circle(surface, start, end, color, width)
    elif tool == "square":
        draw_square(surface, start, end, color, width)
    elif tool == "right_triangle":
        draw_right_triangle(surface, start, end, color, width)
    elif tool == "equilateral_triangle":
        draw_equilateral_triangle(surface, start, end, color, width)
    elif tool == "rhombus":
        draw_rhombus(surface, start, end, color, width)


running = True

while running:
    pressed = pygame.key.get_pressed()

    ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

    current_color = get_color(mode)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Keyboard controls
        if event.type == pygame.KEYDOWN:

            # Ctrl + S saves canvas
            if event.key == pygame.K_s and ctrl_held:
                save_canvas()

            # If text tool is active, type text
            elif text_mode:
                if event.key == pygame.K_RETURN:
                    # Confirm text and draw it permanently
                    text_surface = text_font.render(text_value, True, current_color)
                    canvas.blit(text_surface, text_pos)

                    text_mode = False
                    text_value = ""

                elif event.key == pygame.K_ESCAPE:
                    # Cancel text typing
                    text_mode = False
                    text_value = ""

                elif event.key == pygame.K_BACKSPACE:
                    # Delete last character
                    text_value = text_value[:-1]

                else:
                    # Add typed character
                    text_value += event.unicode

            else:
                # Color selection
                if event.key == pygame.K_r:
                    mode = "red"
                elif event.key == pygame.K_g:
                    mode = "green"
                elif event.key == pygame.K_b:
                    mode = "blue"
                elif event.key == pygame.K_k:
                    mode = "black"

                # Brush sizes
                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

                # Tools
                elif event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_t:
                    tool = "rect"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_s:
                    tool = "square"
                elif event.key == pygame.K_q:
                    tool = "right_triangle"
                elif event.key == pygame.K_u:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    tool = "rhombus"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_x:
                    tool = "text"

        # Mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                start_pos = event.pos
                end_pos = event.pos
                last_pos = event.pos

                if tool == "fill":
                    # Fill selected area
                    flood_fill(canvas, event.pos, current_color)

                elif tool == "text":
                    # Start typing text at clicked position
                    text_mode = True
                    text_pos = event.pos
                    text_value = ""

                else:
                    drawing = True

        # Mouse moved
        if event.type == pygame.MOUSEMOTION:

            if drawing and pygame.mouse.get_pressed()[0]:

                end_pos = event.pos

                if tool == "pencil":
                    # Draw freehand line between previous and current position
                    draw_pencil(canvas, last_pos, event.pos, current_color, brush_size)
                    last_pos = event.pos

                elif tool == "eraser":
                    # Eraser draws white line
                    draw_pencil(canvas, last_pos, event.pos, (255, 255, 255), brush_size)
                    last_pos = event.pos

        # Mouse button released
        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1 and drawing:
                end_pos = event.pos

                # Draw final shape on canvas
                if tool not in ["pencil", "eraser", "fill", "text"]:
                    draw_selected_shape(canvas, tool, start_pos, end_pos, current_color, brush_size)

                drawing = False
                start_pos = None
                end_pos = None
                last_pos = None

    # Draw canvas
    screen.blit(canvas, (0, 0))

    # Live preview for shapes
    if drawing and tool not in ["pencil", "eraser", "fill", "text"]:
        temp = canvas.copy()
        draw_selected_shape(temp, tool, start_pos, end_pos, current_color, brush_size)
        screen.blit(temp, (0, 0))

    # Live preview for text
    if text_mode:
        text_surface = text_font.render(text_value, True, current_color)
        screen.blit(text_surface, text_pos)

        # Text cursor
        cursor_x = text_pos[0] + text_surface.get_width() + 2
        pygame.draw.line(
            screen,
            current_color,
            (cursor_x, text_pos[1]),
            (cursor_x, text_pos[1] + 28),
            2
        )

    # Toolbar text
    pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, 95))

    info1 = font.render(
        "Colors: R-red  G-green  B-blue  K-black",
        True,
        (0, 0, 0)
    )
    info2 = font.render(
        "Tools: P-pencil  L-line  T-rect  C-circle  E-eraser  S-square  Q-right triangle  U-equilateral  H-rhombus  F-fill  X-text",
        True,
        (0, 0, 0)
    )
    info3 = font.render(
        "Brush size: 1-small  2-medium  3-large   |   Ctrl+S-save",
        True,
        (0, 0, 0)
    )
    info4 = font.render(
        f"Current tool: {tool}   Color: {mode}   Brush size: {brush_size}",
        True,
        (0, 0, 0)
    )

    screen.blit(info1, (10, 8))
    screen.blit(info2, (10, 30))
    screen.blit(info3, (10, 52))
    screen.blit(info4, (10, 74))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()