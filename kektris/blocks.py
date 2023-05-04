from typing import TypeAlias, Optional
from kektris.constraints import (
    Direction,
    Orientation,
    CellState,
    FigureOrientation,
        )
from kektris.constraints import GameConst as const


class Cell:
    """This class represent a cell of grid
    """
    pixel_size = 5

    def __init__(
        self, x: int,
        y: int,
        state: CellState = CellState.CLEAR
            ) -> None:
        self.x = x
        self.y = y
        self.state = state
        self._pos = (x, y)

    def __repr__(self) -> str:
        return f'Cell with position ({self.x}, {self.y}), state: {self.state.name}'

    @property
    def pos(self) -> tuple[int]:
        """Return current position
        """
        return self._pos

    @property
    def is_frozen(self) -> bool:
        return self.state == CellState.FR0ZEN

    @property
    def is_clear(self) -> bool:
        return self.state == CellState.CLEAR

    @property
    def is_blocked(self) -> bool:
        return self.state == CellState.BLOCK

    def __hash__(self) -> int:
        return hash(self.pos)

    def __eq__(self, other) -> bool:
        if isinstance(other, Cell):
            return self.pos == other.pos
        return NotImplemented

    def freeze(self) -> None:
        """Freeze cell
        """
        self.state = CellState.FR0ZEN

    def clear(self) -> None:
        """Clear the cell
        """
        self.state = CellState.CLEAR

    def block(self) -> None:
        """Block the cell
        """
        self.state = CellState.BLOCK


Cells: TypeAlias = list[list[Cell]]


class Grid:
    """This class represent a grid of cells
    """
    cells = 34

    def __init__(self) -> None:
        self.grid: Cells = self._make_grid()

    def _make_grid(self) -> list[list[Cells]]:
        """Make grid matrix
        """
        return [
            [Cell(x, y) for y in range(self.cells)]
            for x in range(self.cells)
                ]

    @property
    def get_clear(self) -> list[Cell]:
        """Get all clear cell
        """
        return [cell for row in self.grid for cell in row if cell.is_clear]

    @property
    def get_frozen(self) -> list[Cell]:
        """Get all froxen cell
        """
        return [cell for row in self.grid for cell in row if cell.is_frozen]

    @property
    def get_blocked(self) -> list[Cell]:
        """Get all blocked
        """
        return [cell for row in self.grid for cell in row if cell.is_blocked]

    def is_clear(self, pos: tuple[int, int]) -> bool:
        """Is cell with given position clear
        """
        return self.grid[pos[0]][pos[1]].is_clear

    def is_frozen(self, pos: tuple[int, int]) -> bool:
        """Is cell with given position frozen
        """
        return self.grid[pos[0]][pos[1]].is_frozen

    def is_blocked(self, pos: tuple[int, int]) -> bool:
        """Is cell with given position blocked
        """
        return self.grid[pos[0]][pos[1]].is_blocked

    def freeze_blocked(self) -> None:
        """Freeze all blocked cells
        """
        [cell.freeze() for cell in self.get_blocked]

    def clear_blocked(self) -> None:
        """Clear all blocked cells
        """
        [cell.clear() for cell in self.get_blocked]


class Window:
    """Represents 4x4 figure window
    """

    def __init__(
        self,
        top_left: tuple[int, int],
        orientation: FigureOrientation,
        grid: Grid,
        move_direction: Optional[Direction] = None,
            ) -> None:
        self.top_left = top_left
        self.orientation = orientation
        self.grid = grid
        if not move_direction:
            self.move_direction: Direction = self._set_move_direction(top_left)
        else:
            self.move_direction = move_direction
        self._get_window: Optional[list[list[Cell | None]]] = None
        self._map_window: Optional[list[Cell]] = None
        self._quarter: list[tuple[int, int]] = None

    def __repr__(self) -> str:
        return f'Window top_left: {self.top_left}, orientation: {self.orientation.name} ' \
               f'move direction: {self.move_direction.name})'

    def _set_move_direction(self, top_left: tuple[int, int]) -> Direction:
        """Set move direction
        """
        match top_left:
            case _ if top_left in const.ARRIVE_LEFT:
                return Direction.RIGHT
            case _ if top_left in const.ARRIVE_RIGHT:
                return Direction.LEFT
            case _ if top_left in const.ARRIVE_TOP:
                return Direction.DOWN
            case _ if top_left in const.ARRIVE_BOTTOM:
                return Direction.UP
        raise ValueError

    @property
    def get_window(self) -> list[list[Cell | None]]:
        """Get window of cells
        """
        if self._get_window is None:
            self._get_window = [[None, None, None, None] for _ in range(4)]
            for row in range(4):
                y = row + self.top_left[1]
                for col in range(4):
                    x = col + self.top_left[0]
                    if (34 > x >= 0) and (34 > y >= 0):
                        self._get_window[row][col] = self.grid.grid[x][y]
        return self._get_window

    @property
    def quarter(self) -> list[tuple[int, int]]:
        """Get quarter on grid for current window
        """
        if self._quarter is None:
            match self.move_direction:
                case Direction.RIGHT:
                    self._quarter = const.LEFT_QUARTER
                case Direction.LEFT:
                    self._quarter = const.RIGHT_QUARTER
                case Direction.UP:
                    self._quarter = const.BOTTOM_QUARTER
                case Direction.DOWN:
                    self._quarter = const.TOP_QUARTER
        return self._quarter

    @property
    def map_window(self) -> list[Cell]:
        """Get mapped cell
        """
        if self._map_window is None:
            self._map_window = []
            for maps, cells in zip(self.orientation.value, self.get_window):
                self._map_window.extend(
                    [cell for m, cell in zip(maps, cells) if cell and m]
                        )
        return self._map_window

    def has_frozen(self) -> bool:
        """Has figure frozen cells in mapped window
        """
        for cell in self.map_window:
            if cell.is_frozen:
                return True
        return False

    def is_in_quarter(self) -> bool:
        """Is all figure cells in quarter
        """
        for cell in self.map_window:
            if cell.pos not in self.quarter:
                return False
        return True

    def is_on_grid(self) -> bool:
        """Is figure on grid
        """
        return len(self.map_window) > 0

    def is_full_on_grid(self) -> bool:
        """Is figure on grid completly
        """
        return len(self.map_window) == 4


class Figure:
    """Kektris figure with its current
    orientation and position on the game grid
    """

    def __init__(
        self,
        window: Window,
            ) -> None:
        self.window = window
        self.shape = window.orientation.name[0]

    def move_figure(self, direction: Direction) -> Optional[Window]:
        """Move a figure one step in a given direction
        """
        x, y = self.window.top_left
        match direction, self.window.move_direction:
            case Direction.LEFT, d if d != Direction.RIGHT:
                new_window = Window(
                    (x-1, y),
                    self.window.orientation,
                    self.window.grid,
                    self.window.move_direction
                        )
            case Direction.RIGHT, d if d != Direction.LEFT:
                new_window = Window(
                    (x+1, y),
                    self.window.orientation,
                    self.window.grid,
                    self.window.move_direction
                        )
            case Direction.UP, d if d != Direction.DOWN:
                new_window = Window(
                    (x, y-1),
                    self.window.orientation,
                    self.window.grid,
                    self.window.move_direction
                        )
            case Direction.DOWN, d if d != Direction.UP:
                new_window = Window(
                    (x, y+1),
                    self.window.orientation,
                    self.window.grid,
                    self.window.move_direction
                        )
            case _, _:
                return
        return new_window

    def rotate_figure(self, direction: Direction) -> Optional[Window]:
        """Rotates a figure in a given rotation side
        """
        new_window = Window(
            self.window.top_left,
            FigureOrientation[
                self.shape + '_' + self._choose_orientation(direction).name
                    ],
            self.window.grid,
            self.window.move_direction
                )
        return new_window

    def _choose_orientation(self, direction: Direction) -> Orientation:
        """Choose orientation of figure after rotation
        """
        ind = Orientation[self.window.orientation.name[2]].value
        match direction, ind:
            case Direction.RIGHT, 4:
                return Orientation(1)
            case Direction.RIGHT, o if o < 4:
                return Orientation(ind+1)
            case Direction.LEFT, 1:
                return Orientation(4)
            case Direction.LEFT, o if o > 1:
                return Orientation(ind-1)
            case _:
                raise ValueError('Wrong direction!')

    def block_figure(self, window: Window) -> None:
        """Block cells for figure
        """
        cells = window.map_window
        self.window.grid.clear_blocked()
        [self.window.grid.grid[cell.x][cell.y].block() for cell in cells]
        self.window = window

    def is_valid_figure(
        self,
        window: Optional[Window],
            ) -> bool:
        """"Returns true if all the cells of the block are valid
        i.e. on the grid and doesn't occupy already frozen cells
        or new figure cant move across its freeze quarter
        """
        if window \
                and not window.has_frozen() \
                and window.is_in_quarter():
            return True
        return False
