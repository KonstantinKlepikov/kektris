from enum import Enum, auto


class BaseEnum(Enum):
    """Base class for enumeration
    """
    @classmethod
    def has_value(cls, value: int) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def get_values(cls) -> list[int]:
        return [e.value for e in cls]

    @classmethod
    def get_includes(cls) -> list['BaseEnum']:
        """This used for randobm figure generation
        """
        return [i for i in cls]

    @classmethod
    def get_names(cls) -> list[str]:
        return cls._member_names_


class Direction(BaseEnum):
    """Move or rotation directions
    """
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()


class Orientation(BaseEnum):
    """Block orientation
    """
    U = auto()
    L = auto()
    D = auto()
    R = auto()


class CellState(BaseEnum):
    """Possible state of item
    """
    CLEAR = auto()
    BLOCK = auto()
    FR0ZEN = auto()


class FigureOrientation(BaseEnum):
    """All figures orientation (by longest flat side faces)
    """

    # all orientations of figure I
    I_U = (
        (False, False, False, False),
        (True, True, True, True),
        (False, False, False, False),
        (False, False, False, False),
            )
    I_L = (
        (False, True, False, False),
        (False, True, False, False),
        (False, True, False, False),
        (False, True, False, False),
            )
    I_D = (
        (False, False, False, False),
        (False, False, False, False),
        (True, True, True, True),
        (False, False, False, False),
            )
    I_R = (
        (False, False, True, False),
        (False, False, True, False),
        (False, False, True, False),
        (False, False, True, False),
            )

    # all orientations of figure O
    O = (
        (False, False, False, False),
        (False, True, True, False),
        (False, True, True, False),
        (False, False, False, False),
            )

    # all orientations of figure J
    J_U = (
        (True, False, False, False),
        (True, True, True, False),
        (False, False, False, False),
        (False, False, False, False),
            )
    J_L = (
        (False, True, True, False),
        (False, True, False, False),
        (False, True, False, False),
        (False, False, False, False),
            )
    J_D = (
        (False, False, False, False),
        (True, True, True, False),
        (False, False, True, False),
        (False, False, False, False),
            )
    J_R = (
        (False, True, False, False),
        (False, True, False, False),
        (True, True, False, False),
        (False, False, False, False),
            )

    # all orientations of figure L
    L_U = (
        (False, False, True, False),
        (True, True, True, False),
        (False, False, False, False),
        (False, False, False, False),
            )
    L_L = (
        (False, True, False, False),
        (False, True, False, False),
        (False, True, True, False),
        (False, False, False, False),
            )
    L_D = (
        (False, False, False, False),
        (True, True, True, False),
        (True, False, False, False),
        (False, False, False, False),
            )
    L_R = (
        (True, True, False, False),
        (False, True, False, False),
        (False, True, False, False),
        (False, False, False, False),
            )

    # all orientations of figure S
    S_U = (
        (False, True, True, False),
        (True, True, False, False),
        (False, False, False, False),
        (False, False, False, False),
            )
    S_L = (
        (False, True, False, False),
        (False, True, True, False),
        (False, False, True, False),
        (False, False, False, False),
            )
    S_D = (
        (False, False, False, False),
        (False, True, True, False),
        (True, True, False, False),
        (False, False, False, False),
            )
    S_R = (
        (True, False, False, False),
        (True, True, False, False),
        (False, True, False, False),
        (False, False, False, False),
            )

    # all orientations of figure Z
    Z_U = (
        (True, True, False, False),
        (False, True, True, False),
        (False, False, False, False),
        (False, False, False, False),
            )
    Z_L = (
        (False, False, True, False),
        (False, True, True, False),
        (False, True, False, False),
        (False, False, False, False),
            )
    Z_D = (
        (False, False, False, False),
        (True, True, False, False),
        (False, True, True, False),
        (False, False, False, False),
            )
    Z_R = (
        (False, True, False, False),
        (True, True, False, False),
        (True, False, False, False),
        (False, False, False, False),
            )

    # all orientations of figure T
    T_U = (
        (False, False, False, False),
        (True, True, True, False),
        (False, True, False, False),
        (False, False, False, False),
            )
    T_L = (
        (False, True, False, False),
        (False, True, True, False),
        (False, True, False, False),
        (False, False, False, False),
            )
    T_D = (
        (False, True, False, False),
        (True, True, True, False),
        (False, False, False, False),
        (False, False, False, False),
            )
    T_R = (
        (False, True, False, False),
        (True, True, False, False),
        (False, True, False, False),
        (False, False, False, False),
            )

    @classmethod
    def get_includes(cls) -> list['FigureOrientation']:
        """This used for randobm figure generation
        """
        includes = [i for i in cls]
        for _ in range(3):
            includes.append(cls.O)
        return includes

    def get_figure_color(self) -> int:
        """Color of figure
        """
        match self.name[0]:
            case 'I':
                return 8
            case 'O':
                return 9
            case 'J':
                return 14
            case 'L':
                return 11
            case 'S':
                return 12
            case 'Z':
                return 15
            case 'T':
                return 2


def get_next_figure_grid_pos() -> list[list[tuple[int, int]]]:
    return [[(x+1, y+1) for x in range(219, 243, 6)] for y in range(135, 155, 6)]

class GameConst:
    """Game constants"""

    ARRIVE_TOP: list[tuple[int, int]] = [(x, -4) for x in range(30)]
    ARRIVE_BOTTOM: list[tuple[int, int]] = [(x, 34) for x in range(30)]
    ARRIVE_LEFT: list[tuple[int, int]] = [(-4, y) for y in range(30)]
    ARRIVE_RIGHT: list[tuple[int, int]] = [(34, y) for y in range(30)]
    ARRIVE = ARRIVE_TOP + ARRIVE_BOTTOM + ARRIVE_LEFT + ARRIVE_RIGHT

    LEFT_QUARTER: list[tuple[int, int]] = [(x, y) for x in range(-4, 17) for y in range(0, 34)]
    RIGHT_QUARTER: list[tuple[int, int]] = [(x, y) for x in range(17, 37) for y in range(0, 34)]
    BOTTOM_QUARTER: list[tuple[int, int]] = [(x, y) for x in range(0, 34) for y in range(17, 37)]
    TOP_QUARTER: list[tuple[int, int]] = [(x, y) for x in range(0, 34) for y in range(-4, 17)]

    NEXT_FIGURE_GRID: tuple[list[int], list[int]] = [n for n in range(219, 249, 6)], \
        [n for n in range(135, 165, 6)]
    NEXT_FIGURE_GRID_POS: list[list[tuple[int, int]]] = get_next_figure_grid_pos()

    START_FRAME_COUNT: int = 5
    COLOR_TIMOUT: int = 60

    PRIZE_BY_CLEAR: int = 60
    START_CLEAR_LENGTH: int = 6
    MAX_CLEAR_LENGHT: int = 10
    LENGHT_MODIFICATOR: int = 7000
    MAX_GAME_SPEED: int = 22
    GAME_SPEED_LIMIT: int = 30
    SPEED_MODIFICATOR: int = 1000
