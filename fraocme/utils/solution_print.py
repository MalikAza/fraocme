import time
from typing import Callable

GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def solution_print(part: int, solution_func: Callable[[], int | str]) -> None:
    part_string = ''

    match part:
        case 1:
            part_string = 'one'
        case 2:
            part_string = 'two'
    
    start_time = time.time()
    result = solution_func()
    end_time = time.time()
    elapsed_ms = (end_time - start_time) * 1000
    
    print(f"{CYAN}Part {part_string}{RESET} solution is: {GREEN}{result}{RESET} {YELLOW}({elapsed_ms:.2f}ms){RESET}")
