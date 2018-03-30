from drawing.visible import Visible


def test_rect_is_centered():
    vis = Visible((10, 10), (10, 10))
    assert vis.rect.center == (10, 10)


def test_update_rect_center():
    vis = Visible((10, 10), (10, 10))
    vis.change_rect_center((20, 20))
    assert vis.rect.center == (20, 20)


def test_update_rect_center_rounds_floats():
    vis = Visible((10, 10), (10, 10))
    vis.change_rect_center((1.6, 1.4))
    assert vis.rect.center == (2, 1)
