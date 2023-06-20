from utils import *

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Paint by HubercikTM1")
icon = pg.image.load("icon.png")
pg.display.set_icon(icon)

def init_grid(rows,cols,color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[i].append(color)

    return grid

def draw_single_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pg.draw.rect(win, pixel, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pg.draw.line(win, BLACK, (0, i * PIXEL_SIZE), (WIDTH, i * PIXEL_SIZE))
        for j in range(COLS + 1):
            pg.draw.line(win, BLACK,(j * PIXEL_SIZE, 0), (j * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))


def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_single_grid(win, grid)

    for button in buttons:
        button.draw(win)

    pg.display.update()


def get_row_col_from_position(position):
    x, y = position
    row = y  // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        #ERROR
        raise IndexError

    return row, col


# GAME
isRunning = True
clock = pg.time.Clock()
grid = init_grid(ROWS,COLS,BG_COLOR)
drawing_color = BLACK

button_y = HEIGHT - TOOLBAR_HEIGHT/2 - 25
buttons = [
    Button(10, button_y, 50, 50, BLACK),
    Button(70, button_y, 50, 50, RED),
    Button(130, button_y, 50, 50, GREEN),
    Button(190, button_y, 50, 50, BLUE),
    Button(250, button_y, 50, 50, WHITE, "Erase", BLACK),
    Button(310, button_y, 50, 50, WHITE, "Clear", BLACK)
]

while isRunning:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            isRunning = False

        if pg.mouse.get_pressed()[0]:
            position = pg.mouse.get_pos()
            try:
                row, col = get_row_col_from_position(position)
                grid[row][col] = drawing_color
            except IndexError:
                for button in buttons:
                    if not button.clicked(position):
                        continue

                    drawing_color = button.color
                    if button.text == "Clear":
                        grid = init_grid(ROWS,COLS,BG_COLOR)
                        drawing_color = BLACK

    draw(WIN, grid, buttons)

pg.quit()
