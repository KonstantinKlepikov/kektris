import pyxel
import random
from typing import Optional
from blocks import Grid, Figure, Window
from constraints import Direction, FigureOrientation
from constraints import GameConst as const


class Game:
    def __init__(self) -> None:
        pyxel.init(256, 256, title="Kektris")
        pyxel.image(0).load(0, 0, "Q-tris-s.png")
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self) -> None:
        """Reset game state
        """
        # menu parameters
        self.paused: bool = True
        self.score: int = 0
        self.speed: int = 0
        self.line_lenght: int = const.START_CLEAR_LENGTH
        self.score_color_timeout = const.COLOR_TIMOUT
        self.speed_color_timeout = const.COLOR_TIMOUT
        self.line_color_timeout = const.COLOR_TIMOUT

        # grid
        self.grid: Grid = Grid()
        self.grid_higlight: bool = False
        self.figure = self.arrive_figure()
        self.figure_next = self.arrive_figure()

        # game
        self.frame_count_from_last_move: int = const.START_FRAME_COUNT
        self.is_game_over: bool = False

    def draw(self) -> None:
        """Draw current screen
        """
        pyxel.cls(0)
        self.draw_controls()
        self.draw_aside()
        self.mark_grid()
        self.draw_cells()

    def update(self) -> None:
        """Update current game state
        """
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()
            return

        if pyxel.btnp(pyxel.KEY_P):
            if self.paused:
                self.paused = False
            else:
                self.paused = True

        if pyxel.btnp(pyxel.KEY_G):
            if self.grid_higlight:
                self.grid_higlight = False
            else:
                self.grid_higlight = True

        if self.is_game_over:
            return

        if self.paused:
            return

        move_direction = None
        rotate_direction = None
        if pyxel.btnp(pyxel.KEY_LEFT, 8, 1):
            move_direction = Direction.LEFT
        elif pyxel.btnp(pyxel.KEY_RIGHT, 8, 1):
            move_direction = Direction.RIGHT
        elif pyxel.btnp(pyxel.KEY_DOWN, 8, 1):
            move_direction = Direction.DOWN
        elif pyxel.btnp(pyxel.KEY_UP, 8, 1):
            move_direction = Direction.UP
        elif pyxel.btnp(pyxel.KEY_Z, 12, 20):
            rotate_direction = Direction.LEFT
        elif pyxel.btnp(pyxel.KEY_X, 12, 20):
            rotate_direction = Direction.RIGHT

        self.move_figure(move_direction, self.figure.move_figure)
        self.move_figure(rotate_direction, self.figure.rotate_figure)

        if self.frame_count_from_last_move == const.MAX_GAME_SPEED - self.speed:
            window = self.figure.move_figure(self.figure.window.move_direction)
            self.final_moves_and_game_checks(window)
            return

        self.frame_count_from_last_move += 1

    @classmethod
    def get_chunked(
        cls,
        line: list[int],
        chunked: list[list[int]]
            ) -> tuple[list, list[list[int]]]:
        """Separate line to chunked lines
        """
        chunk = []
        while line:
            a = line.pop()
            if chunk:
                if chunk[-1] - a == 1:
                    chunk.append(a)
                else:
                    line.append(a)
                    line, chunked = cls.get_chunked(line, chunked)
            else:
                chunk.append(a)
        chunked.append(chunk)
        return line, chunked

    @staticmethod
    def sign(n: int) -> int:
        """Return sign of int
        """
        if n > 0:
            return 1
        elif n == 0:
            return 0
        else:
            return -1

    @staticmethod
    def generate_figure_start_position() -> tuple[tuple[int, int], FigureOrientation]:
        """Genrate random start position
        """
        return (
            random.choice(const.ARRIVE),
            random.choice(FigureOrientation.get_includes())
                )

    @staticmethod
    def display_next_figure(window: Window) -> None:
        """Draw next figure
        """
        blocked_color = window.orientation.get_figure_color()
        for maps, cells in zip(window.orientation.value, const.NEXT_FIGURE_GRID_POS):
            [
                pyxel.rect(pos[0], pos[1], 5, 5, blocked_color)
                for cell, pos
                in zip(maps, cells)
                if cell
                    ]

    @staticmethod
    def draw_up_marker(x: int, y: int, color: int = 12) -> None:
        """Draw up marker
        """
        pyxel.pset(x, y, color)
        pyxel.pset(x-1, y+1, color)
        pyxel.pset(x+1, y+1, color)
        pyxel.pset(x-2, y+2, color)
        pyxel.pset(x+2, y+2, color)

    @staticmethod
    def draw_down_marker(x: int, y: int, color: int = 12) -> None:
        """Draw down marker
        """
        pyxel.pset(x-2, y-2, color)
        pyxel.pset(x+2, y-2, color)
        pyxel.pset(x-1, y-1, color)
        pyxel.pset(x+1, y-1, color)
        pyxel.pset(x, y, color)

    def draw_controls(self) -> None:
        """Draw controls helper
        """
        pyxel.rectb(14, 220, 13, 13, 1)
        pyxel.rectb(28, 220, 13, 13, 12)
        pyxel.rectb(42, 220, 13, 13, 1)
        pyxel.rectb(14, 235, 13, 13, 12)
        pyxel.rectb(28, 235, 13, 13, 12)
        pyxel.rectb(42, 235, 13, 13, 12)

        pyxel.text(19, 224, "Z", 1)
        self.draw_up_marker(34, 225)
        pyxel.text(47, 224, "X", 1)
        pyxel.text(19, 239, "<", 12)
        self.draw_down_marker(34, 242)
        pyxel.text(47, 239, ">", 12)

        pyxel.rectb(62, 220, 13, 13, 10)
        pyxel.text(67, 224, "R", 10)
        pyxel.text(77, 224, "restart", 10)

        pyxel.rectb(110, 220, 13, 13, 12)
        pyxel.text(115, 224, "P", self.hide_reveal(self.paused))
        pyxel.text(125, 224, "play/pause", 12)

        pyxel.rectb(170, 220, 13, 13, 12)
        pyxel.text(175, 224, "G", self.hide_reveal(self.grid_higlight))
        pyxel.text(185, 224, "grid", 12)

        pyxel.blt(187, 235, 0, 0, 0, 65, 18)

    def draw_aside(self) -> None:
        """Draw aside parameters
        """
        pyxel.text(219, 20, "SCORE", 10)
        pyxel.text(219, 30, str(self.score), self.set_color("score_color_timeout"))

        pyxel.text(219, 50, "SPEED", 10)
        pyxel.text(219, 60, str(self.speed), self.set_color("speed_color_timeout"))

        pyxel.text(219, 80, "LINE", 10)
        pyxel.text(219, 90, str(self.line_lenght), self.set_color("line_color_timeout"))

        # display next figure
        for p in const.NEXT_FIGURE_GRID[0]:
            pyxel.line(p, 135, p, 159, 13)
        for p in const.NEXT_FIGURE_GRID[1]:
            pyxel.line(219, p, 243, p, 13)

        if not self.is_game_over:
            pyxel.text(219, 115, "NEXT", 10)
            if not self.figure.window.is_full_on_grid():
                window = self.figure.window
            else:
                window = self.figure_next.window

            match window.move_direction:
                case Direction.RIGHT:
                    pyxel.text(219, 125, ">>>", pyxel.frame_count % 8)
                case Direction.LEFT:
                    pyxel.text(219, 125, "<<<", pyxel.frame_count % 8)
                case Direction.UP:
                    self.draw_up_marker(221, 125, pyxel.frame_count % 8)
                    self.draw_up_marker(227, 125, pyxel.frame_count % 8)
                    self.draw_up_marker(233, 125, pyxel.frame_count % 8)
                case Direction.DOWN:
                    self.draw_down_marker(221, 127, pyxel.frame_count % 8)
                    self.draw_down_marker(227, 127, pyxel.frame_count % 8)
                    self.draw_down_marker(233, 127, pyxel.frame_count % 8)

            self.display_next_figure(window)

        # pause or game over
        if self.is_game_over:
            pyxel.text(219, 175, "GAME END", pyxel.frame_count % 8)
        elif self.paused:
            pyxel.text(219, 175, "Press P", pyxel.frame_count % 8)
            pyxel.text(219, 182, "to play", pyxel.frame_count % 8)

    def mark_grid(self) -> None:
        """Draw grid mark
        """
        # grid border
        pyxel.rectb(10, 10, 205, 205, 1)

        # grid
        if self.grid_higlight:
            for p in range(10, 217, 6):
                pyxel.line(p, 10, p, 214, 13)
                pyxel.line(10, p, 214, p, 13)

        # axis
        if not self.is_game_over and not self.paused:
            match self.figure.window.move_direction:
                case Direction.RIGHT | Direction.LEFT:
                    pyxel.line(112, 10, 112, 214, pyxel.frame_count % 8)
                case Direction.DOWN | Direction.UP:
                    pyxel.line(10, 112, 214, 112, pyxel.frame_count % 8)

        # central point
        pyxel.pset(112, 112, 8)

    def arrive_figure(self) -> Figure:
        """Arrive figure at random
        """
        top_left, orientation = self.generate_figure_start_position()
        window = Window(top_left, orientation, self.grid)
        return Figure(window)

    def push_next_figure(self) -> None:
        """Push figure_next to replace current an arrive next
        """
        self.figure = self.figure_next
        self.figure_next = self.arrive_figure()

    def draw_cells(self) -> None:
        """Draw blocked and frozen cells from Grid object
        """
        blocked_color = self.figure.window.orientation.get_figure_color()
        for n, row in enumerate(self.grid.grid):
            for m, cell in enumerate(row):
                x = cell.pos[0] * 5 + 11 + n
                y = cell.pos[1] * 5 + 11 + m
                if cell.is_blocked:
                    pyxel.rect(x, y, 5, 5, blocked_color)
                if cell.is_frozen:
                    pyxel.rect(x, y, 5, 5, 7)

    def check_line(
        self,
        dimension: int,
        frozen_pos: list[tuple[int, int]]
        ) -> Optional[list[tuple[int, int]]]:
        """Check is line ready to clear and return positions to clear
        """
        s_d = 0 if dimension else 1
        comparison = [c[dimension] for c in frozen_pos]
        min_ = min(comparison)
        max_ = max(comparison) + 1
        for n in range(min_, max_):
            line = [pos for pos in frozen_pos if pos[dimension] == n]
            if len(line) >= self.line_lenght:
                l_comparison = sorted([pos[s_d] for pos in line])
                _, chunked = self.get_chunked(l_comparison, [])
                to_clear = [
                    n for chunk in chunked
                    for n in chunk
                    if len(chunk) >= self.line_lenght
                        ]
                if to_clear:
                    return [pos for pos in line if pos[s_d] in to_clear]

    def get_shift(self, shift_x: int, shift_y: int) -> tuple[int, int]:
        """Get shift for frozen to move it when clear line
        """
        match self.figure.window.move_direction:
            case Direction.RIGHT:
                shift_x -= 1
            case Direction.LEFT:
                shift_x += 1
            case Direction.UP:
                shift_y += 1
            case Direction.DOWN:
                shift_y -= 1
        return shift_x, shift_y

    def get_shifted_frozen(
        self,
        line: list[tuple[int, int]]
            ) -> list[tuple[int, int]]:
        """Get shifted frozen positions to move cells when clear line
        """
        shift_x, shift_y = 0, 0
        shifted = []
        while True:
            shift_x, shift_y = self.get_shift(shift_x, shift_y)
            s_x, s_y = self.sign(shift_x), self.sign(shift_y)
            sh = []
            for pos in line:
                p = (pos[0]+shift_x, pos[1]+shift_y)

                if p in self.figure.window.quarter \
                        and p not in line \
                        and self.grid.grid[p[0]][p[1]].is_frozen \
                        and (
                            self.grid.grid[p[0]-s_x][p[1]-s_y].is_frozen
                            or self.grid.grid[p[0]-s_x][p[1]-s_y].pos in line
                                ):
                    sh.append(p)
            if sh:
                shifted.extend(sh)
            else:
                break
        return shifted

    def move_shifted_frozen(self, shifted: list[tuple[int, int]]) -> None:
        """Move frozen rows after clear
        """
        shift_x, shift_y = self.get_shift(0, 0)
        [self.grid.grid[pos[0]][pos[1]].clear() for pos in shifted]
        [
            self.grid.grid[pos[0]-shift_x][pos[1]-shift_y].freeze()
            for pos in shifted
            if pos in self.figure.window.quarter
                ]

    # TODO: test me
    def move_figure(self, direction: Optional[Direction], operation) -> None:
        """Move or rotate figure
        """
        if direction and self.figure.window.is_on_grid():
            window: Window = operation(direction)
            if self.figure.is_valid_figure(window) and window.is_on_grid():
                self.figure.block_figure(window)

    # TODO: test me
    def clear_lines(self) -> None:
        """Clear line
        """
        frozen_pos = [cell.pos for cell in self.grid.get_frozen]
        if len(frozen_pos) >= self.line_lenght:
            for dim in [0, 1]:
                line = self.check_line(dim, frozen_pos)
                if line:
                    for pos in line:
                        self.grid.grid[pos[0]][pos[1]].clear()
                        self.change_score()
                        self.change_speed()
                        self.change_line_lenght()
                    shifted = self.get_shifted_frozen(line)
                    if shifted:
                        self.move_shifted_frozen(shifted)
                    self.clear_lines()

    # TODO: test me
    def final_moves_and_game_checks(self, window: Window) -> None:
        """Move figures and check game conditions when count of frames
        from lst move is overflow
        """
        if self.figure.is_valid_figure(window):
            self.figure.block_figure(window)
        elif not self.figure.window.is_full_on_grid():
            self.is_game_over = True
        else:
            self.grid.freeze_blocked()
            self.clear_lines()
            self.push_next_figure()
        self.frame_count_from_last_move = const.START_FRAME_COUNT

    def change_score(self) -> None:
        """Change score and set flash timeout
        """
        self.score += const.PRIZE_BY_CLEAR
        self.score_color_timeout = const.COLOR_TIMOUT

    def change_speed(self) -> None:
        """Change speed and set flash timeout
        """
        if self.score // const.SPEED_MODIFICATOR > self.speed \
                 and self.speed < const.MAX_GAME_SPEED:
            self.speed += 1
            self.speed_color_timeout = const.COLOR_TIMOUT

    def change_line_lenght(self) -> None:
        """Change line lenght every X points to maximum y
        """
        if self.score // const.LENGHT_MODIFICATOR > \
            self.line_lenght - const.START_CLEAR_LENGTH \
            and self.line_lenght < const.MAX_CLEAR_LENGHT:
                self.line_lenght += 1
                self.line_color_timeout = const.COLOR_TIMOUT

    def set_color(self, color_attr: str) -> int:
        """Set flash color
        """
        val = getattr(self, color_attr)
        if val:
            setattr(self, color_attr, val - 1)
            return pyxel.frame_count % 8
        return 12

    def hide_reveal(self, marker: bool) -> int:
        """Hide or reveal flashed marker
        """
        if marker:
            return pyxel.frame_count % 8
        return 12


if __name__ == '__main__':
    Game()
