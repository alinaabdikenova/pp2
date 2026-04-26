import pygame
from collections import deque


# Return selected color
def get_color(mode):
    if mode == "blue":
        return (0, 0, 255)
    elif mode == "red":
        return (255, 0, 0)
    elif mode == "green":
        return (0, 255, 0)
    elif mode == "black":
        return (0, 0, 0)
    return (0, 0, 255)


# Draw freehand line
def draw_pencil(surface, start, end, color, width):
    pygame.draw.line(surface, color, start, end, width)


# Draw straight line
def draw_line(surface, start, end, color, width):
    pygame.draw.line(surface, color, start, end, width)


# Draw rectangle
def draw_rectangle(surface, start, end, color, width):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])

    pygame.draw.rect(surface, color, (x, y, w, h), width)


# Draw circle
def draw_circle(surface, start, end, color, width):
    center_x = (start[0] + end[0]) // 2
    center_y = (start[1] + end[1]) // 2

    radius = int(
        (((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5) / 2
    )

    if radius > 0:
        pygame.draw.circle(surface, color, (center_x, center_y), radius, width)


# Draw square
def draw_square(surface, start, end, color, width):
    side = min(abs(start[0] - end[0]), abs(start[1] - end[1]))

    x = start[0]
    y = start[1]

    if end[0] < start[0]:
        x -= side
    if end[1] < start[1]:
        y -= side

    pygame.draw.rect(surface, color, (x, y, side, side), width)


# Draw right triangle
def draw_right_triangle(surface, start, end, color, width):
    p1 = start
    p2 = (start[0], end[1])
    p3 = end

    pygame.draw.polygon(surface, color, [p1, p2, p3], width)


# Draw equilateral triangle
def draw_equilateral_triangle(surface, start, end, color, width):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    size = abs(end[0] - start[0]) // 2

    p1 = (cx, cy - size)
    p2 = (cx - size, cy + size)
    p3 = (cx + size, cy + size)

    pygame.draw.polygon(surface, color, [p1, p2, p3], width)


# Draw rhombus
def draw_rhombus(surface, start, end, color, width):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2

    w = abs(end[0] - start[0]) // 2
    h = abs(end[1] - start[1]) // 2

    p1 = (cx, cy - h)
    p2 = (cx + w, cy)
    p3 = (cx, cy + h)
    p4 = (cx - w, cy)

    pygame.draw.polygon(surface, color, [p1, p2, p3, p4], width)


# Flood fill tool
def flood_fill(surface, start_pos, fill_color):
    width, height = surface.get_size()

    x, y = start_pos

    # Do not fill outside the canvas
    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))

    if target_color == fill_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        x, y = queue.popleft()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), fill_color)

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))