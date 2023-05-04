import pytest
import random
import pyxel
from typing import Callable
from kektris.kektris import Game
from kektris.blocks import Grid


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

    monkeypatch.setattr(pyxel, "run", mock_run)
    monkeypatch.setattr(pyxel, "load", mock_load)
    monkeypatch.setattr(pyxel, "init", mock_init)

@pytest.fixture(scope="function")
def make_app(monkeypatch, mock_app: Callable) -> Game:
    """Make app
    """
    def mock_draw_figures(*args, **kwargs) -> Callable:
        return None

    monkeypatch.setattr(Game, "_draw_figures", mock_draw_figures)
    return Game()

@pytest.fixture(scope='function')
def grid() -> Grid:
    return Grid()
