import sys
import importlib
from pathlib import Path

from .types.main_args import MainArgs

__SOLUTIONS_DIR = Path(__file__).parent.parent / 'solutions'

def __parse_arg() -> MainArgs:
    if len(sys.argv) != 2:
        print('Usage: python runner.py <day_number>')
        sys.exit(1)

    day = int(sys.argv[1])

    args: MainArgs = {
        "day": day
    }

    return args

def __get_day_file_path(day: int) -> Path:
    day_dir = __SOLUTIONS_DIR / f'day_{day}'

    day_dir.mkdir(exist_ok=True)

    return day_dir / 'main.py'

def __check_solution_exists(day: int) -> None:
    day_file = __get_day_file_path(day)

    if not day_file.exists():
        print(f'No solution for day {day}.')
        sys.exit(1)

def __module_run(day: int) -> None:
    try:
        module = importlib.import_module(f'solutions.day_{day}.python.main')
        module.run()
    except Exception:
        import traceback
        print(f'\033[91mError running day {day}:\033[0m')
        print('\033[91m', end='')
        traceback.print_exc()
        print('\033[0m', end='')
        sys.exit(1)

def run():
    args = __parse_arg()
    __check_solution_exists(args['day'])
    __module_run(args['day'])

if __name__ == '__main__':
    run()
