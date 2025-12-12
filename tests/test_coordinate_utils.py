from fraocme.common import coordinate_utils as cu


# line_points
def test_line_points_horizontal():
    assert cu.line_points((1, 2), (4, 2)) == {(1, 2), (2, 2), (3, 2), (4, 2)}


def test_line_points_vertical():
    assert cu.line_points((3, 1), (3, 4)) == {(3, 1), (3, 2), (3, 3), (3, 4)}


# build_outline_from_vertices
def test_build_outline_from_vertices_square():
    square = [(0, 0), (2, 0), (2, 2), (0, 2)]
    outline = cu.build_outline_from_vertices(square, closed=True)
    assert (0, 0) in outline and (2, 2) in outline
    assert len(outline) > 0

    # fill_outline_floodfill
    outline = {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)}
    filled = cu.fill_outline_floodfill(outline)
    assert (1, 1) in filled
    assert (0, 0) in filled  # outline points are included


# polygon_interior_points
def test_polygon_interior_points_rectangle():
    rect = [(0, 0), (2, 0), (2, 2), (0, 2)]
    interior = cu.polygon_interior_points(rect)
    assert isinstance(interior, set)


# rectangle_area
def test_rectangle_area():
    assert cu.rectangle_area((0, 0), (2, 2)) == 9
    assert cu.rectangle_area((1, 1), (3, 4)) == 12


# rectangle_points
def test_rectangle_points():
    pts = cu.rectangle_points((0, 0), (1, 1))
    assert (0, 0) in pts and (1, 1) in pts
    assert len(pts) == 4


# rectangle_contains
def test_rectangle_contains():
    assert cu.rectangle_contains((0, 0), (2, 2), (1, 1))
    assert not cu.rectangle_contains((0, 0), (2, 2), (3, 3))


# largest_valid_rectangle
def test_largest_valid_rectangle():
    reds = [(0, 0), (2, 2)]
    allowed = {(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)}
    area, rect = cu.largest_valid_rectangle(reds, allowed)
    assert area > 0
    assert isinstance(rect, tuple)


# largest_valid_polygon
def test_largest_valid_polygon():
    rect = [(0, 0), (2, 0), (2, 2), (0, 2)]
    allowed = {(x, y) for x in range(3) for y in range(3)}
    area, poly = cu.largest_valid_polygon([rect], allowed)
    assert area > 0
    assert isinstance(poly, list)
