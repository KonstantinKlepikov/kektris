import pyxel
import random
from typing import Optional
from blocks import Grid, Figure, Window
from constraints import Direction, FigureOrientation
from constraints import GameConst as const


class Game:
    def __init__(self) -> None:
        pyxel.init(256, 256, title="Kektris")
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self) -> None:
        """Reset game state
        """
        # menu parameters
        self.paused: bool = True
        self.score: int = 0
        self.speed: int = 0
        self.score_color_timeout = const.COLOR_TIMOUT
        self.speed_color_timeout = const.COLOR_TIMOUT

        # grid
        self.grid: Grid = Grid()
        self.grid_higlight: bool = False
        self.figure = self._arrive_figure()

        # game
        self.frame_count_from_last_move: int = 0
        self.is_over: bool = False

    def draw(self) -> None:
        """Draw current screen
        """
        pyxel.cls(0)
        self._draw_controls()
        self._draw_aside()
        self._mark_grid()
        self._draw_figures()

    def update(self) -> None:
        """Update current game state
        """
        if pyxel.btnp(pyxel.KEY_T):
            pyxel.quit()

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

        if self._is_game_over():
            return

        if self.paused:
            return

        move_direction = None
        rotate_direction = None
        if pyxel.btnp(pyxel.KEY_LEFT, 12, 2):
            move_direction = Direction.LEFT
        elif pyxel.btnp(pyxel.KEY_RIGHT, 12, 2):
            move_direction = Direction.RIGHT
        elif pyxel.btnp(pyxel.KEY_DOWN, 12, 2):
            move_direction = Direction.DOWN
        elif pyxel.btnp(pyxel.KEY_UP, 12, 2):
            move_direction = Direction.UP
        elif pyxel.btnp(pyxel.KEY_Z, 12, 20):
            rotate_direction = Direction.LEFT
        elif pyxel.btnp(pyxel.KEY_X, 12, 20):
            rotate_direction = Direction.RIGHT

        self._move_figure(move_direction, self.figure.move_figure)
        self._move_figure(rotate_direction, self.figure.rotate_figure)

        if self.frame_count_from_last_move == const.GAME_SPEED - self.speed:
            window = self.figure.move_figure(self.figure.window.move_direction)
            if self.figure.is_valid_figure(window):
                self.figure.block_figure(window)
            else:
                self.grid.freeze_blocked()
                self._clear_rows()
                self.figure = self._arrive_figure()

            self.frame_count_from_last_move = 0
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

    def _draw_controls(self) -> None:
        """Draw controls
        """
        pyxel.rectb(14, 220, 13, 13, 1)
        pyxel.rectb(28, 220, 13, 13, 12)
        pyxel.rectb(42, 220, 13, 13, 1)
        pyxel.rectb(14, 235, 13, 13, 12)
        pyxel.rectb(28, 235, 13, 13, 12)
        pyxel.rectb(42, 235, 13, 13, 12)

        pyxel.text(19, 224, "Z", 1)
        pyxel.text(33, 223, "^", 12)
        pyxel.text(47, 224, "W", 1)
        pyxel.text(19, 239, "<", 12)
        pyxel.text(33, 239, "v", 12)
        pyxel.text(47, 239, ">", 12)

        pyxel.rectb(62, 220, 13, 13, 8)
        pyxel.text(67, 224, "T", 8)
        pyxel.text(77, 224, "exit", 8)

        pyxel.rectb(95, 220, 13, 13, 9)
        pyxel.text(100, 224, "R", 9)
        pyxel.text(110, 224, "restart", 9)

        pyxel.rectb(140, 220, 13, 13, 12)
        pyxel.text(145, 224, "P", self._hide_reveal(self.paused))
        pyxel.text(155, 224, "pause", 12)

        pyxel.rectb(177, 220, 13, 13, 12)
        pyxel.text(182, 224, "G", self._hide_reveal(self.grid_higlight))
        pyxel.text(192, 224, "grid", 12)

    def _draw_aside(self) -> None:
        """Draw aside parameters
        """
        pyxel.text(219, 20, "SCORE", 10)
        pyxel.text(219, 30, str(self.score), self._set_color("score_color_timeout"))

        pyxel.text(219, 50, "SPEED", 10)
        pyxel.text(219, 60, str(self.speed), self._set_color("speed_color_timeout"))

        pyxel.text(219, 80, "LINE", 10)
        pyxel.text(219, 90, str(const.CLEAR_LENGTH), 12)

        if self.is_over:
            pyxel.text(219, 110, "GAME END", pyxel.frame_count % 8)

    def _mark_grid(self) -> None:
        """Draw grid mark
        """
        pyxel.rectb(10, 10, 205, 205, 1)

        if not self.is_over:
            match self.figure.window.move_direction:
                case Direction.RIGHT | Direction.LEFT:
                    color = (15, pyxel.frame_count % 8)
                case Direction.DOWN | Direction.UP:
                    color = (pyxel.frame_count % 8, 15)
                case _:
                    color = (15, 15)
            pyxel.line(112, 10, 112, 214, color[1])
            pyxel.line(10, 112, 214, 112, color[0])

            if self.grid_higlight:
                for p in range(10, 217, 6):
                    if p != 112:
                        pyxel.line(p, 10, p, 214, 13)
                        pyxel.line(10, p, 214, p, 13)

    def _arrive_figure(self) -> Figure:
        """Arrive figure at random
        """
        top_left, orientation = self._generate_figure_start_position()
        window = Window(top_left, orientation, self.grid)
        return Figure(window)

    def _generate_figure_start_position(
        self) -> tuple[tuple[int, int], FigureOrientation]:
        """Genrate random start position
        """
        return (
            random.choice(const.ARRIVE),
            random.choice(FigureOrientation.get_includes())
                )

    def _draw_figures(self) -> None:
        """Draw blocked and frozen cells from Grid object
        """
        for n, row in enumerate(self.grid.grid):
            for m, cell in enumerate(row):
                x = cell.pos[0] * 5 + 11 + n
                y = cell.pos[1] * 5 + 11 + m
                if cell.is_blocked:
                    pyxel.rect(x, y, 5, 5, 10)
                if cell.is_frozen:
                    pyxel.rect(x, y, 5, 5, 7)

    def _check_line(
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
            if len(line) >= const.CLEAR_LENGTH:
                l_comparison = sorted([pos[s_d] for pos in line])
                _, chunked = self.get_chunked(l_comparison, [])
                to_clear = [
                    n for chunk in chunked
                    for n in chunk
                    if len(chunk) >= const.CLEAR_LENGTH
                        ]
                if to_clear:
                    return [pos for pos in line if pos[s_d] in to_clear]

    def _get_shift(self, shift_x: int, shift_y: int) -> tuple[int, int]:
        """Get shift for frozen to move it
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

    def _get_shifted_frozen(
        self,
        line: list[tuple[int, int]]
            ) -> list[tuple[int, int]]:
        """Get shifted frozen positions for move
        """
        shift_x, shift_y = 0, 0
        shifted = []
        while True:
            shift_x, shift_y = self._get_shift(shift_x, shift_y)
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

    def _move_shifted_frozen(self, shifted: list[tuple[int, int]]) -> None:
        """Move frozen rows after clear
        """
        shift_x, shift_y = self._get_shift(0, 0)
        [self.grid.grid[pos[0]][pos[1]].clear() for pos in shifted]
        [
            self.grid.grid[pos[0]-shift_x][pos[1]-shift_y].freeze()
            for pos in shifted
            if pos in self.figure.window.quarter
                ]

    # TODO: test me
    def _move_figure(self, direction: Optional[Direction], operation) -> None:
        """Move or rotate figure
        """
        if direction and self.figure.window.is_on_grid():
            window: Window = operation(direction)
            if self.figure.is_valid_figure(window) and window.is_full_on_grid():
                self.figure.block_figure(window)

    # TODO: test me
    def _clear_rows(self) -> None:
        """Clear filled row
        """
        frozen_pos = [cell.pos for cell in self.grid.get_frozen]
        if len(frozen_pos) >= const.CLEAR_LENGTH:
            for dim in [0, 1]:
                line = self._check_line(dim, frozen_pos)
                if line:
                    for pos in line:
                        self.grid.grid[pos[0]][pos[1]].clear()
                        self._change_score()
                        self._change_speed()
                    shifted = self._get_shifted_frozen(line)
                    if shifted:
                        self._move_shifted_frozen(shifted)
                    self._clear_rows()

    def _change_score(self) -> None:
        """Change score and set flash timeout
        """
        self.score += const.PRIZE_BY_CLEAR
        self.score_color_timeout = const.COLOR_TIMOUT

    def _change_speed(self) -> None:
        """Change speed and set flash timeout
        """
        if self.score // const.SPEED_MODIFICATOR > self.speed \
                 and self.speed < const.GAME_SPEED:
            self.speed += 1
            self.speed_color_timeout = const.COLOR_TIMOUT

    def _set_color(self, color_attr: str) -> int:
        """Set flash color
        """
        val = getattr(self, color_attr)
        if val:
            setattr(self, color_attr, val - 1)
            return pyxel.frame_count % 8
        return 12

    def _hide_reveal(self, marker: bool) -> int:
        """Hide or reveal flashed marker
        """
        if marker:
            return pyxel.frame_count % 8
        return 12

    def _is_game_over(self) -> bool:
        """Check is game over
        """
        if self.is_over == False:
            for pos in const.GAME_OVER_ZONE:
                if self.grid.grid[pos[0]][pos[1]].is_frozen:
                    self.is_over = True
                    break
        return self.is_over


if __name__ == '__main__':
    Game()
