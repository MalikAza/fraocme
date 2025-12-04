# TODO: example function, need to make better later
def print_max_in_rows(grid: list[list[int]]) -> None:
    """Print the highest number in each row of a 2D grid."""
    for row in grid:
        if row:
            print(max(row))
        else:
            print("Empty row")
