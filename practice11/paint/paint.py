import pygame

def main():
    pygame.init()  # initializes all the pygame sub-modules
    screen = pygame.display.set_mode((900, 600)) # create window
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    radius = 8 # brush size 
    mode = 'blue' # current color
    tool = 'brush' # current tool

    points = [] # for smooth drawing
    drawing_shape = False
    start_pos = (0, 0)
    end_pos = (0, 0)

    canvas = pygame.Surface((900, 600))
    canvas.fill((255, 255, 255)) # for white background

    while True:
        pressed = pygame.key.get_pressed()

        #check ctrl/alt
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return # close program

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                # colors
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_k:
                    mode = 'black'

                # tools
                elif event.key == pygame.K_p:
                    tool = 'brush'
                elif event.key == pygame.K_t:
                    tool = 'rect'
                elif event.key == pygame.K_c:
                    tool = 'circle'
                elif event.key == pygame.K_e:
                    tool = 'eraser'
                elif event.key == pygame.K_s:
                    tool = 'square'
                elif event.key == pygame.K_q:
                    tool = 'right_triangle'
                elif event.key == pygame.K_u:
                    tool = 'equilateral_triangle'
                elif event.key == pygame.K_h:
                    tool = 'rhombus'
                # mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if tool == 'brush' or tool == 'eraser':
                        points = [event.pos]
                    else:
                        drawing_shape = True
                        start_pos = event.pos
                        end_pos = event.pos

                # change size of brush
                elif event.button == 4:
                    radius = min(50, radius + 1)
                elif event.button == 5:
                    radius = max(1, radius - 1)
            # mouse move
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if tool == 'brush' or tool == 'eraser':
                        points.append(event.pos)

                        #draw smooth line
                        if len(points) >= 2:
                            drawLineBetween(canvas, points[-2], points[-1], radius, tool, mode)
                    else:
                        end_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if tool == 'rect':
                        drawRectangle(canvas, start_pos, end_pos, radius, mode)
                    elif tool == 'circle':
                        drawCircle(canvas, start_pos, end_pos, radius, mode)
                    elif tool == 'square':
                        drawSquare(canvas, start_pos, end_pos, radius, mode)
                    elif tool == 'right_triangle':
                        drawRightTriangle(canvas, start_pos, end_pos, radius, mode)
                    elif tool == 'equilateral_triangle':
                        drawEquilateralTriangle(canvas, start_pos, end_pos, radius, mode)
                    elif tool == 'rhombus':
                        drawRhombus(canvas, start_pos, end_pos, radius, mode)
                    drawing_shape = False
                    points = []

        screen.blit(canvas, (0, 0))

        if drawing_shape:
            temp = canvas.copy()
            if tool == 'rect':
                drawRectangle(temp, start_pos, end_pos, radius, mode)
            elif tool == 'circle':
                drawCircle(temp, start_pos, end_pos, radius, mode)
            elif tool == 'square':
                drawSquare(temp, start_pos, end_pos, radius, mode)
            elif tool == 'right_triangle':
                drawRightTriangle(temp, start_pos, end_pos, radius, mode)
            elif tool == 'equilateral_triangle':
                drawEquilateralTriangle(temp, start_pos, end_pos, radius, mode)
            elif tool == 'rhombus':
                drawRhombus(temp, start_pos, end_pos, radius, mode)
            
            screen.blit(temp, (0, 0))
            
        info1 = font.render("Colors: R-red  G-green  B-blue  K-black", True, (0, 0, 0))
        info2 = font.render("Tools: P-brush  T-rectangle  C-circle  E-eraser  Q-Right Triangle  U-Equilateral Triangle  H-Rhombus  S-Square", True, (0, 0, 0))
        info3 = font.render(f"Current tool: {tool}   Current color: {mode}   Size: {radius}", True, (0, 0, 0))

        screen.blit(info1, (10, 10))
        screen.blit(info2, (10, 35))
        screen.blit(info3, (10, 60))

        pygame.display.flip() # update screen
        clock.tick(60)

# return color based on mode
def getColor(mode):
    if mode == 'blue':
        return (0, 0, 255)
    elif mode == 'red':
        return (255, 0, 0)
    elif mode == 'green':
        return (0, 255, 0)
    elif mode == 'black':
        return (0, 0, 0)


def drawLineBetween(screen, start, end, width, tool, mode):
    if tool == 'eraser': #erase with white
        color = (255, 255, 255)
    else:
        color = getColor(mode)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    if iterations == 0:
        pygame.draw.circle(screen, color, start, width)
        return

    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


def drawRectangle(screen, start, end, width, mode):
    color = getColor(mode)
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    pygame.draw.rect(screen, color, (x, y, w, h), width)


def drawCircle(screen, start, end, width, mode):
    color = getColor(mode)
    center_x = (start[0] + end[0]) // 2
    center_y = (start[1] + end[1]) // 2
    radius = int((((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5) / 2)

    if radius > 0:
        pygame.draw.circle(screen, color, (center_x, center_y), radius, width)

def drawSquare(screen, start, end, width, mode):
    # get color
    color = getColor(mode)

    # calculate size (equal sides)
    side = min(abs(start[0] - end[0]), abs(start[1] - end[1]))

    x = start[0]
    y = start[1]

    # adjust direction
    if end[0] < start[0]:
        x -= side
    if end[1] < start[1]:
        y -= side

    pygame.draw.rect(screen, color, (x, y, side, side), width)

def drawRightTriangle(screen, start, end, width, mode):
    color = getColor(mode)

    # 3 points of triangle
    p1 = start
    p2 = (start[0], end[1])
    p3 = (end[0], end[1])

    pygame.draw.polygon(screen, color, [p1, p2, p3], width)

def drawEquilateralTriangle(screen, start, end, width, mode):
    color = getColor(mode)

    # center and size
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    size = abs(end[0] - start[0]) // 2

    # triangle points
    p1 = (cx, cy - size)
    p2 = (cx - size, cy + size)
    p3 = (cx + size, cy + size)

    pygame.draw.polygon(screen, color, [p1, p2, p3], width)

def drawRhombus(screen, start, end, width, mode):
    color = getColor(mode)

    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2

    w = abs(end[0] - start[0]) // 2
    h = abs(end[1] - start[1]) // 2

    # 4 points of rhombus
    p1 = (cx, cy - h)
    p2 = (cx + w, cy)
    p3 = (cx, cy + h)
    p4 = (cx - w, cy)

    pygame.draw.polygon(screen, color, [p1, p2, p3, p4], width)


main()