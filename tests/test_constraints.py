from constraints import FigureOrientation


def test_figure_orientations():
    """Test figure orientations enum
    """
    assert len(FigureOrientation.get_names()) == 7*4-3, 'wrong names'
    assert len(FigureOrientation.get_includes()) == 7*4, 'wrong includes'
    assert len(FigureOrientation.get_values()) == 7*4-3, 'wrong values'
