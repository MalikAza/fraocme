from functools import cache
from typing import List, Literal, Tuple, TypedDict

class CornersPositions(TypedDict):
    down_right: Tuple[int, int]
    down_left: Tuple[int, int]
    up_right: Tuple[int, int]
    up_left: Tuple[int, int]

class NSEWPositions(TypedDict):
    down: Tuple[int, int]
    right: Tuple[int, int]
    up: Tuple[int, int]
    left: Tuple[int, int]

class AroundPositions(CornersPositions, NSEWPositions):
    pass

DIRECTION_TYPE = Literal['^', '>', 'v', '<']

class MapUtils:
    possible_directions: List[DIRECTION_TYPE] = ['^', '>', 'v', '<']
    start: Tuple[int, int] | None = None
    end: Tuple[int, int] | None = None

    def __init__(self,
                 data: str,
                 start_value: str = None,
                 end_value: str = None
                ):
        self.map = data.split('\n')
        self.__start_value = start_value
        self.__end_value = end_value

        self.__search_start_and_end()

    @cache
    def is_position_out_of_bounds(self, position: Tuple[int, int]):
        x, y = position
        return y < 0 or y >= len(self.map) or x < 0 or x >= len(self.map[y])
    
    @cache
    def get_positions_to_down(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return (position[0], position[1] + 1)

    @cache
    def get_positions_to_right(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return (position[0] + 1, position[1])

    @cache
    def get_positions_to_up(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return (position[0], position[1] - 1)

    @cache
    def get_positions_to_left(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return (position[0] - 1, position[1])
    
    @cache
    def get_positions_to_down_right(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return self.get_positions_to_down(self.get_positions_to_right(position))
    
    @cache
    def get_positions_to_down_left(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return self.get_positions_to_down(self.get_positions_to_left(position))
    
    @cache
    def get_positions_to_up_right(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return self.get_positions_to_up(self.get_positions_to_right(position))
    
    @cache
    def get_positions_to_up_left(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return self.get_positions_to_up(self.get_positions_to_left(position))
    
    @cache
    def get_positions_in_corners(self, position: Tuple[int, int]) -> CornersPositions:
        return {
            'down_right': self.get_positions_to_down_right(position),
            'down_left': self.get_positions_to_down_left(position),
            'up_right': self.get_positions_to_up_right(position),
            'up_left': self.get_positions_to_up_left(position),
        }

    @cache
    def get_positions_in_NSEW(self, position: Tuple[int, int]) -> NSEWPositions:
        return {
            'down': self.get_positions_to_down(position),
            'right': self.get_positions_to_right(position),
            'up': self.get_positions_to_up(position),
            'left': self.get_positions_to_left(position),
        }
    
    @cache
    def get_positions_around(self, position: Tuple[int, int]) -> AroundPositions:
        return {
            **self.get_positions_in_NSEW(position),
            **self.get_positions_in_corners(position)
        }
    
    @cache
    def get_position_to_direction(self, position: Tuple[int, int], direction: DIRECTION_TYPE) -> Tuple[int, int]:
        match direction:
            case '^':
                return self.get_positions_to_up(position)
            case '>':
                return self.get_positions_to_right(position)
            case 'v':
                return self.get_positions_to_down(position)
            case '<':
                return self.get_positions_to_left(position)

    def __search_start_and_end(self):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if self.__start_value and cell == self.__start_value:
                    self.start = (x, y)

                if self.__end_value and cell == self.__end_value:
                    self.end = (x, y)

    def search_value(self, value: str) -> Tuple[Tuple[int, int]]:
        positions = []
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == value:
                    positions.append((x, y))

        return tuple(positions)

    def get_cell_value_from_position(self, position: Tuple[int, int]) -> None | str:
        if self.is_position_out_of_bounds(position):
            return None
        
        return self.map[position[1]][position[0]]