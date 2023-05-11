import pytest
from constraints import FigureOrientation


@pytest.fixture(scope='function', params=FigureOrientation.get_includes())
def orientation(request) -> FigureOrientation:
    return request.param


def test_figure_orientations():
    """Test figure orientations enum
    """
    assert len(FigureOrientation.get_names()) == 7*4-3, 'wrong names'
    assert len(FigureOrientation.get_includes()) == 7*4, 'wrong includes'
    assert len(FigureOrientation.get_values()) == 7*4-3, 'wrong values'


def test_figure_orientation_color(orientation: FigureOrientation) -> None:
    """Test figure color
    """
    assert isinstance(orientation.get_figure_color(), int), 'not a color'
