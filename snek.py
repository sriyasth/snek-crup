import curses
from typing import Optional


class SnakeGame:
    def __init__(self, width: int, height: int):
        """
        Game should be initialized according to width
        and height. The game is played using wasd keys.

        The initial state should be:
        - Snake of length 3
        - Snake moving right
        - Snake in the center
        """
        self.length = 3
        self.gameGrid = [["0" for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height
        self.direction = "d"
        self.center_x = width//2
        self.center_y = height//2
        self.snake = [
        (self.center_y, self.center_x),
        (self.center_y, self.center_x - 1),
        (self.center_y, self.center_x - 2),
        ]
        for y, x in self.snake:
            self.gameGrid[y][x] = "s"


    def grid(self) -> list[list[str]]:
        """
        Handles the display of the grid
        Should return a 2D list of characters
        """
        return self.gameGrid

    def set_direction(self, key_input: Optional[str]):
        """
        Set the direction.
        Assume input will either be w, a, s, d, or None
        """
        if key_input in ["w", "a", "s", "d"]:
            self.direction = key_input

    def do_step(self) -> bool:
        """
        Performs a single step during 1 tick
        Return False if the game should end
        """
        head_y, head_x = self.snake[0]

        if self.direction == "w":
            new_head = (head_y - 1, head_x)
        elif self.direction == "s":
            new_head = (head_y + 1, head_x)
        elif self.direction == "a":
            new_head = (head_y, head_x - 1)
        elif self.direction == "d":
            new_head = (head_y, head_x + 1)
        else:
            return True  

        new_y, new_x = new_head

        if new_y < 0 or new_y >= self.height or new_x < 0 or new_x >= self.width or new_head in self.snake:
            return False

        self.snake.insert(0, new_head)  
        self.snake.pop() 
        self.gameGrid = [["0" for _ in range(self.width)] for _ in range(self.height)]
        for y, x in self.snake:
            self.gameGrid[y][x] = "s"
        return True


def game_loop(stdscr):
    """
    Main game loop that manages game setup and execution.
    """
    game = SnakeGame(25, 15)

    # Game setup
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(400)

    # Game loop
    while True:
        key = stdscr.getch()
        key = chr(key) if 0 <= key < 256 else None

        game.set_direction(key)
        if not game.do_step():
            print("Game over!")
            return

        stdscr.clear()

        # Draw grid
        for y, row in enumerate(game.grid()):
            for x, char in enumerate(row):
                stdscr.addch(y, x, ord(str(char)))

        # Refresh screen
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(game_loop)
