import pytest
import random
import pyxel
from typing import Callable
from kektris.kektris import Game
from blocks import Grid


class FixedSeed:
    """Context manager to set random seed
    """
    def __init__(self, seed):
        self.seed = seed
        self.state = None

    def __enter__(self):
        self.state = random.getstate()
        random.seed(self.seed)

    def __exit__(self, exc_type, exc_value, traceback):
        random.setstate(self.state)


@pytest.fixture(scope="function")
def mock_app(monkeypatch) -> Callable:
    """Mock user data
    """
    def mock_run(*args, **kwargs) -> Callable:
        return None

    def mock_load(*args, **kwargs) -> Callable:
        return None

    def mock_init(*args, **kwargs) -> Callable:
        return None

    def mock_image(*args, **kwargs) -> Callable:
        class M:
            def __init__(self, *args, **kwargs) -> None:
                pass

            def load(self, *args, **kwargs):
                return None
        return M

    def mock_sounds(*args, **kwargs) -> Callable:
        class M:
            def __init__(self, *args, **kwargs) -> None:
                pass

            def set(self, *args, **kwargs):
                return None
        return M

    def mock_play(*args, **kwargs) -> Callable:
        return None

    monkeypatch.setattr(pyxel, "run", mock_run)
    monkeypatch.setattr(pyxel, "load", mock_load)
    monkeypatch.setattr(pyxel, "init", mock_init)
    monkeypatch.setattr(pyxel, "image", mock_image)
    monkeypatch.setattr(pyxel, "sound", mock_sounds)
    monkeypatch.setattr(pyxel, "play", mock_play)

@pytest.fixture(scope="function")
def make_app(monkeypatch, mock_app: Callable) -> Game:
    """Make app
    """
    def mock_draw_cells(*args, **kwargs) -> Callable:
        return None

    monkeypatch.setattr(Game, "draw_cells", mock_draw_cells)
    return Game()

@pytest.fixture(scope='function')
def grid() -> Grid:
    return Grid()
