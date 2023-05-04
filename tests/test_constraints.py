from kektris.constraints import FigureOrientation


def test_figure_orientations():
    """Test figure orientations enum
    """
    names = [f.name for f in FigureOrientation]
    includes_names = [i.name for i in FigureOrientation.get_includes()]
    assert names == includes_names, 'wrong includes'
