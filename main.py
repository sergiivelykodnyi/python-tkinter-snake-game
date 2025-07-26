import tkinter
import random


# Configuration

ROWS = 25  # Number of rows in the game grid
COLS = 25  # Number of columns in the game grid
TILE_SIZE = 25  # Size of each tile in pixels

WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE


# Game window setup

window = tkinter.Tk()
window.title("Snake Game")
window.resizable(False, False)
canvas = tkinter.Canvas(
    window,
    background="black",
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    borderwidth=0,
    highlightthickness=0
)
canvas.pack()
window.update()

# Center the window on the screen

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = (screen_width - WINDOW_WIDTH) // 2
window_y = (screen_height - WINDOW_HEIGHT) // 2

window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{window_x}+{window_y}")


# Game elements

class Tile:
    """Represents a single tile in the game grid."""

    def __init__(self, x, y):
        self.x = x
        self.y = y


# Create single tile that is the snake's starting position
snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
food = Tile(
    random.randint(0, COLS - 1) * TILE_SIZE,
    random.randint(0, ROWS - 1) * TILE_SIZE
)
velocity_x = 0
velocity_y = 0
snake_body = []  # List to hold the snake's body segments
game_over = False
score = 0


def change_direction(event):
    """Changes the direction of the snake based on key presses."""
    global velocity_x, velocity_y, game_over

    if game_over:
        return

    if event.keysym == "Up" and velocity_y != 1:
        velocity_x = 0
        velocity_y = -1

    elif event.keysym == "Down" and velocity_y != -1:
        velocity_x = 0
        velocity_y = 1

    elif event.keysym == "Left" and velocity_x != 1:
        velocity_x = -1
        velocity_y = 0

    elif event.keysym == "Right" and velocity_x != -1:
        velocity_x = 1
        velocity_y = 0


def move():
    global snake, food, snake_body, game_over, score

    if game_over:
        return

    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return

    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    # Collision with food
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i - 1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocity_x * TILE_SIZE
    snake.y += velocity_y * TILE_SIZE


def draw():
    """Draws the game elements on the canvas."""
    global snake, food, snake_body, game_over, score

    move()

    # Clear the canvas
    canvas.delete("all")

    # Draw food
    canvas.create_rectangle(
        food.x,
        food.y,
        food.x + TILE_SIZE,
        food.y + TILE_SIZE,
        fill="red"
    )

    # Draw snake
    canvas.create_rectangle(
        snake.x,
        snake.y,
        snake.x + TILE_SIZE,
        snake.y + TILE_SIZE,
        fill="lime green"
    )

    for tile in snake_body:
        canvas.create_rectangle(
            tile.x,
            tile.y,
            tile.x + TILE_SIZE,
            tile.y + TILE_SIZE,
            fill="lime green"
        )

    if game_over:
        canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            text=f"Game Over!\nScore: {score}.",
            fill="white",
            font=("Arial", 24)
        )
    else:
        canvas.create_text(
            10,
            10,
            text=f"Score: {score}",
            fill="white",
            font=("Arial", 14),
            anchor="nw"
        )

    # Redraw screen every 150 milliseconds
    window.after(150, draw)


draw()
window.bind("<KeyPress>", change_direction)
window.mainloop()
