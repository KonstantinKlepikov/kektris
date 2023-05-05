import pytest
from kektris.kektris import Game
from blocks import Grid, Figure
from constraints import FigureOrientation, Direction
from constraints import GameConst as const
from tests.conftest import FixedSeed


class TestGame:
    """Test game interfaces
    """

    def test_app_init(self, make_app: Game) -> None:
        """Test app init
        """
        assert make_app.paused, 'not paused'
        assert make_app.score == 0, 'wrong score'
        assert make_app.speed == 0, 'wrong speed'
        assert isinstance(make_app.grid, Grid), 'wrong grid'
        assert not make_app.grid_higlight, 'grid highlited'

    def test_generate_figure_start_position(self, make_app: Game) -> None:
        """Test random figure generation
        """
        with FixedSeed(42):
            top_left, orientation = make_app._generate_figure_start_position()
            assert isinstance(top_left, tuple), 'wrong result'
            assert top_left == (-4, 21), 'wrong top left position'
            assert orientation == FigureOrientation.I_R, 'wrong orientation'

    def test_generate_figure_start_position_probability(self, make_app: Game) -> None:
        """Test generate_figure_start_position probabilitie
        """
        figures = {name: 0 for name in FigureOrientation.get_names()}
        with FixedSeed(42):
            for _ in range(1000):
                figures[make_app._generate_figure_start_position()[1].name] += 1
            assert figures['O'] == 144, 'wrong sample'
            assert figures['I_U'] == 24, 'wrong sample'

    def test_arrive_figure(self, make_app: Game) -> None:
        """Test arrive figure
        """
        with FixedSeed(42):
            figure = make_app._arrive_figure()
            assert isinstance(figure, Figure), 'wrong figure move_direction'
            assert figure.window.top_left == (-4, 21), \
                'wrong top left position'
            assert figure.window.orientation == FigureOrientation.I_R, \
                'wrong orientation'

    def test_get_chunked(self, make_app: Game) -> None:
        """Test get chunked
        """
        i = [1, 2, 3]
        line, chunked = make_app.get_chunked(i, [])
        assert not line, 'line nt empty'
        assert isinstance(line, list), 'wrong line type'
        assert isinstance(chunked, list), 'wrong chunked type'
        assert len(chunked) == 1, 'wrong chunked len'
        assert chunked[0] == [3, 2, 1], 'wrong chunk'

    @pytest.mark.parametrize(
        'i,ch', [
            ([1, 2, 3, 4, 5, 6, 8, 9], [[6, 5, 4, 3, 2, 1], [9, 8]]),
            ([1, 3], [[1], [3]]),
            ([1, 2, 5, 6, 8, 9], [[2, 1], [6, 5], [9, 8]])
                    ]
                )
    def test_get_chunked_parts(self, make_app: Game, i: list[int], ch: list[list[int]]) -> None:
        """Test get chunked multiple parts
        """
        line, chunked = make_app.get_chunked(i, [])
        assert not line, 'line nt empty'
        assert isinstance(line, list), 'wrong line type'
        assert isinstance(chunked, list), 'wrong chunked type'
        assert len(chunked) == len(ch), 'wrong chunked len'
        assert isinstance(chunked[0], list), 'wrong chunk type'
        assert chunked[0] == ch[0], 'wrong chunked'
        assert chunked[1] == ch[1], 'wrong chunked'

    @pytest.mark.parametrize(
        'frozen,result,ost', [
            (
                [(p,0) for p in range(17)],
                [(p,0) for p in range(17)],
                []
                    ),
            (
                [(p,0) for p in range(7)]+[(0,4),],
                [(p,0) for p in range(7)],
                [(0,4),],
                    )
                ]
            )
    def test_check_line(
        self,
        make_app: Game,
        frozen: list[tuple[int, int]],
        result: list[tuple[int, int]],
        ost: list[tuple[int, int]],
        ) -> None:
        """Test is line is ready to clear
        """
        for p in frozen:
            make_app.grid.grid[p[0]][p[1]].freeze()
        frozen_pos = [p.pos for p in make_app.grid.get_frozen]
        assert len(make_app.grid.get_frozen) == len(frozen), 'wrong frozen'
        line = make_app._check_line(1, frozen_pos)
        assert isinstance(line, list), 'wrong line type'
        assert isinstance(line[0], tuple), 'wrong pos'
        assert line == result, 'wrong comparison'
        if ost:
            for p in ost:
                assert make_app.grid.grid[p[0]][p[1]].is_frozen, 'unfrozen'

    def test_check_line_parts(self, make_app: Game) -> None:
        """Test is line is ready to clear if parts
        """
        for p in range(12):
            make_app.grid.grid[p][0].freeze()
        for p in range(14, 17):
            make_app.grid.grid[p][0].freeze()
        frozen_pos = [p.pos for p in make_app.grid.get_frozen]
        assert len(make_app.grid.get_frozen) == 15, 'wrong frozen'
        line = make_app._check_line(1, frozen_pos)
        assert isinstance(line, list), 'wrong line type'
        assert isinstance(line[0], tuple), 'wrong pos'
        assert len(line) == 12, 'wrong line lenght'
        assert frozen_pos[0:12] == line, 'wrong comparison'

    def test_get_shift(self, make_app: Game) -> None:
        """Test get shift for frozen cells
        """
        make_app.figure.window.move_direction = Direction.LEFT
        assert make_app._get_shift(0, 0) == (1, 0), 'wrong left shift'
        assert make_app._get_shift(12, 0) == (13, 0), 'wrong colossal shift'
        make_app.figure.window.move_direction = Direction.RIGHT
        assert make_app._get_shift(0, 0) == (-1, 0), 'wrong right shift'
        assert make_app._get_shift(12, 0) == (11, 0), 'wrong colossal shift'
        make_app.figure.window.move_direction = Direction.UP
        assert make_app._get_shift(0, 0) == (0, 1), 'wrong up shift'
        make_app.figure.window.move_direction = Direction.DOWN
        assert make_app._get_shift(0, 0) == (0, -1), 'wrong down shift'

    @pytest.mark.parametrize(
        'frozen,line,result,direction', [
            (
                [(31,0), (31,1), (31,2), (32,0), (33,5)],
                [(30,n) for n in range(7)] ,
                [(31,0), (31,1), (31,2), (32,0)],
                Direction.LEFT,
                    ),
            (
                [(5,0), (5,1), (5,2), (4,0), (3,0), (33,5)],
                [(6,n) for n in range(7)] ,
                [(5,0), (5,1), (5,2), (4,0), (3,0)],
                Direction.RIGHT,
                    ),
                ]
            )
    def test_get_shifted_frozen(
        self,
        make_app: Game,
        frozen: list[tuple[int, int]],
        line: list[tuple[int, int]],
        result: list[tuple[int, int]],
        direction: Direction
            ) -> None:
        """Test frozen can be shifted
        """
        make_app.figure.window.move_direction = direction
        quarter = make_app.figure.window.quarter
        for pos in frozen:
            make_app.grid.grid[pos[0]][pos[1]].freeze()
        shifted = make_app._get_shifted_frozen(line)
        assert shifted == result, 'wrong shifted'
        for pos in shifted:
            assert pos in quarter, 'not in quarter'

    @pytest.mark.parametrize(
        'shifted,result,direction', [
            (
                [(31,0), (31,1), (31,2), (32,0)],
                {(30,0), (30,1), (30,2), (31,0)},
                Direction.LEFT,
                    ),
            (
                [(5,0), (5,1), (5,2), (4,0), (3,0)],
                {(6,0), (6,1), (6,2), (5,0), (4,0)},
                Direction.RIGHT,
                    ),
                    (
                [(0,16), (1,16), (1,17)],
                {(1,16),},
                Direction.UP,
                    ),
                ]
            )
    def test_move_shifted_frozen(
        self,
        make_app: Game,
        shifted: list[tuple[int, int]],
        result: list[tuple[int, int]],
        direction: Direction
            ) -> None:
        """Test move shifted frozen
        """
        make_app.figure.window.move_direction = direction
        quarter = make_app.figure.window.quarter
        for pos in shifted:
            make_app.grid.grid[pos[0]][pos[1]].freeze()
        make_app._move_shifted_frozen(shifted)
        assert {cell.pos for cell in make_app.grid.get_frozen} == result, 'wrong result'

    def test_change_speed(self, make_app: Game) -> None:
        """Test change speed
        """
        make_app._change_speed()
        assert make_app.speed == 0, 'mistaken grown'

        make_app.score = const.SPEED_MODIFICATOR
        make_app._change_speed()
        assert make_app.speed == 1, 'not grown'
        assert make_app.speed_color_timeout == const.COLOR_TIMOUT, 'wrong timout'

        make_app.score = const.SPEED_MODIFICATOR*const.GAME_SPEED
        make_app.speed = const.GAME_SPEED-1
        make_app._change_speed()
        assert make_app.speed == const.GAME_SPEED, 'not grown'

        make_app.score = const.SPEED_MODIFICATOR*100000
        make_app._change_speed()
        assert make_app.speed == const.GAME_SPEED, 'wrong grown'

    @pytest.mark.parametrize(
        'positions,result', [
        ([(0,0),], True),
        ([(1,1),], False),
        ([(1,1),(0,0)], True),
        ([(33,33),], True),
        ([(33,0),], True),
        ([(0,33),], True),
            ]
        )
    def test_is_game_over(
        self,
        make_app: Game,
        positions: list[tuple[int, int]],
        result: bool,
            ) -> None:
        """Test game is over
        """
        assert not make_app.is_over, 'game over'
        for pos in positions:
            make_app.grid.grid[pos[0]][pos[1]].freeze()
        assert make_app._is_game_over() == result, 'wrong result'
