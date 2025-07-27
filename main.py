"""
Snake Game implemented with tkinter.

A classic Snake game where the player controls a snake to eat food and grow longer
while avoiding collisions with walls and the snake's own body.
"""

from __future__ import annotations

import random
import tkinter as tk
from enum import Enum
from typing import List, Optional


class Direction(Enum):
    """Enum representing the four possible movement directions."""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class GameConfig:
    """Configuration constants for the Snake game."""
    ROWS: int = 25
    COLS: int = 25
    TILE_SIZE: int = 25
    WINDOW_WIDTH: int = COLS * TILE_SIZE
    WINDOW_HEIGHT: int = ROWS * TILE_SIZE
    GAME_SPEED: int = 200  # milliseconds between updates

    # Colors
    BACKGROUND_COLOR: str = "black"
    SNAKE_COLOR: str = "lime green"
    FOOD_COLOR: str = "red"
    TEXT_COLOR: str = "white"

    # Fonts
    GAME_OVER_FONT: tuple[str, int] = ("Arial", 24)
    SCORE_FONT: tuple[str, int] = ("Arial", 14)


class Tile:
    """Represents a single tile in the game grid."""

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize a tile with given coordinates.

        Args:
            x: X coordinate in pixels
            y: Y coordinate in pixels
        """
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        """Check if two tiles have the same position."""
        if not isinstance(other, Tile):
            return NotImplemented
        return self.x == other.x and self.y == other.y


class SnakeGame:
    """Main Snake game class handling all game logic and rendering."""

    def __init__(self) -> None:
        """Initialize the Snake game."""
        self.config = GameConfig()
        self._setup_window()
        self._reset_game()

    def _setup_window(self) -> None:
        """Set up the game window and canvas."""
        self.window = tk.Tk()
        self.window.title("Snake Game")
        self.window.resizable(False, False)

        self.canvas = tk.Canvas(
            self.window,
            background=self.config.BACKGROUND_COLOR,
            width=self.config.WINDOW_WIDTH,
            height=self.config.WINDOW_HEIGHT,
            borderwidth=0,
            highlightthickness=0
        )
        self.canvas.pack()
        self.window.update()

        # Center the window on the screen
        self._center_window()

        # Bind keyboard events
        self.window.bind("<KeyPress>", self._handle_keypress)
        self.window.focus_set()  # Ensure window receives key events

    def _center_window(self) -> None:
        """Center the game window on the screen."""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_x = (screen_width - self.config.WINDOW_WIDTH) // 2
        window_y = (screen_height - self.config.WINDOW_HEIGHT) // 2

        self.window.geometry(
            f"{self.config.WINDOW_WIDTH}x{self.config.WINDOW_HEIGHT}"
            f"+{window_x}+{window_y}"
        )

    def _reset_game(self) -> None:
        """Reset the game to initial state."""
        self.snake_head = Tile(5 * self.config.TILE_SIZE,
                               5 * self.config.TILE_SIZE)
        self.snake_body: List[Tile] = []
        self.food = self._generate_food()
        self.direction: Optional[Direction] = None
        self.game_over = False
        self.score = 0

    def _generate_food(self) -> Tile:
        """Generate food at a random position that doesn't overlap with the snake."""
        while True:
            food_x = random.randint(
                0, self.config.COLS - 1) * self.config.TILE_SIZE
            food_y = random.randint(
                0, self.config.ROWS - 1) * self.config.TILE_SIZE
            food = Tile(food_x, food_y)

            # Ensure food doesn't spawn on snake
            if food != self.snake_head and food not in self.snake_body:
                return food

    def _handle_keypress(self, event: tk.Event) -> None:
        """Handle keyboard input for changing snake direction."""
        if self.game_over:
            if event.keysym == "space":
                self._reset_game()
            return

        key_to_direction = {
            "Up": Direction.UP,
            "Down": Direction.DOWN,
            "Left": Direction.LEFT,
            "Right": Direction.RIGHT,
            "w": Direction.UP,
            "s": Direction.DOWN,
            "a": Direction.LEFT,
            "d": Direction.RIGHT,
        }

        new_direction = key_to_direction.get(event.keysym)
        if new_direction and self._is_valid_direction_change(new_direction):
            self.direction = new_direction

    def _is_valid_direction_change(self, new_direction: Direction) -> bool:
        """Check if the direction change is valid (not opposite to current direction)."""
        if self.direction is None:
            return True

        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }

        return new_direction != opposite_directions[self.direction]

    def _check_wall_collision(self) -> bool:
        """Check if the snake head collides with the walls."""
        return (
            self.snake_head.x < 0 or
            self.snake_head.x >= self.config.WINDOW_WIDTH or
            self.snake_head.y < 0 or
            self.snake_head.y >= self.config.WINDOW_HEIGHT
        )

    def _check_self_collision(self) -> bool:
        """Check if the snake head collides with its own body."""
        return self.snake_head in self.snake_body

    def _update_snake_position(self) -> None:
        """Update the snake's position based on current direction."""
        if self.direction is None:
            return

        # Move body segments
        for i in range(len(self.snake_body) - 1, -1, -1):
            if i == 0:
                self.snake_body[i].x = self.snake_head.x
                self.snake_body[i].y = self.snake_head.y
            else:
                prev_segment = self.snake_body[i - 1]
                self.snake_body[i].x = prev_segment.x
                self.snake_body[i].y = prev_segment.y

        # Move head
        dx, dy = self.direction.value
        self.snake_head.x += dx * self.config.TILE_SIZE
        self.snake_head.y += dy * self.config.TILE_SIZE

    def _check_food_collision(self) -> bool:
        """Check if the snake head collides with food."""
        return self.snake_head == self.food

    def _handle_food_consumption(self) -> None:
        """Handle what happens when snake eats food."""
        # Add new body segment at food position
        self.snake_body.append(Tile(self.food.x, self.food.y))

        # Generate new food
        self.food = self._generate_food()

        # Increase score
        self.score += 1

    def _update_game_state(self) -> None:
        """Update the game state for one frame."""
        if self.game_over:
            return

        # Update snake position
        self._update_snake_position()

        # Check collisions
        if self._check_wall_collision() or self._check_self_collision():
            self.game_over = True
            return

        # Check food consumption
        if self._check_food_collision():
            self._handle_food_consumption()

    def _draw_tile(self, tile: Tile, color: str) -> None:
        """Draw a single tile on the canvas."""
        self.canvas.create_rectangle(
            tile.x,
            tile.y,
            tile.x + self.config.TILE_SIZE,
            tile.y + self.config.TILE_SIZE,
            fill=color
        )

    def _draw_game_elements(self) -> None:
        """Draw all game elements on the canvas."""
        # Clear canvas
        self.canvas.delete("all")

        # Draw food
        self._draw_tile(self.food, self.config.FOOD_COLOR)

        # Draw snake head
        self._draw_tile(self.snake_head, self.config.SNAKE_COLOR)

        # Draw snake body
        for segment in self.snake_body:
            self._draw_tile(segment, self.config.SNAKE_COLOR)

    def _draw_ui(self) -> None:
        """Draw the user interface elements."""
        if self.game_over:
            self.canvas.create_text(
                self.config.WINDOW_WIDTH // 2,
                self.config.WINDOW_HEIGHT // 2,
                text=f"Game Over!\nScore: {self.score}\n\nPress SPACE to restart.",
                fill=self.config.TEXT_COLOR,
                font=self.config.GAME_OVER_FONT,
                justify=tk.CENTER
            )
        else:
            self.canvas.create_text(
                10,
                10,
                text=f"Score: {self.score}",
                fill=self.config.TEXT_COLOR,
                font=self.config.SCORE_FONT,
                anchor="nw"
            )

    def _game_loop(self) -> None:
        """Main game loop that updates and renders the game."""
        self._update_game_state()
        self._draw_game_elements()
        self._draw_ui()

        # Schedule next frame
        self.window.after(self.config.GAME_SPEED, self._game_loop)

    def run(self) -> None:
        """Start the game."""
        self._game_loop()
        self.window.mainloop()


def main() -> None:
    """Main function to start the Snake game."""
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    main()
