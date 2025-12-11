import argparse
import sys

from fraocme.ui.printer import print_header

from .core.runner import Runner
from .profiling.stats import Stats
from .ui.colors import c


def main():
    parser = argparse.ArgumentParser(
        prog="fraocme", description="Advent of Code framework"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # ─────────────────────────────────────────────────────────
    # run command
    # ─────────────────────────────────────────────────────────

    run_parser = subparsers.add_parser("run", help="Run solution(s)")
    run_parser.add_argument(
        "day", type=int, nargs="?", default=None, help="Day number to run"
    )
    run_parser.add_argument(
        "-p",
        "--part",
        type=int,
        choices=[1, 2],
        default=None,
        help="Run only specific part",
    )
    run_parser.add_argument("-a", "--all", action="store_true", help="Run all days")
    run_parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug output"
    )
    run_parser.add_argument(
        "--example",
        action="store_true",
        help="Run with example input instead of main input",
    )
    run_parser.add_argument(
        "--no-traceback", action="store_true", help="Don't show traceback on errors"
    )
    run_parser.add_argument("--no-stats", action="store_true", help="Don't save stats")

    # ─────────────────────────────────────────────────────────
    # stats command
    # ─────────────────────────────────────────────────────────

    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    stats_parser.add_argument(
        "day", type=int, nargs="?", default=None, help="Day number (omit for all days)"
    )
    stats_parser.add_argument(
        "--best", action="store_true", help="Show only best times"
    )
    stats_parser.add_argument(
        "--reset", action="store_true", help="Reset stats for a day or all days"
    )
    stats_parser.add_argument(
        "--all", action="store_true", help="Apply reset to all days"
    )

    # ─────────────────────────────────────────────────────────
    # create command
    # ─────────────────────────────────────────────────────────

    create_parser = subparsers.add_parser(
        "create", help="Create a new day solution folder and files"
    )
    create_parser.add_argument("day", type=int, help="Day number to create")

    # ─────────────────────────────────────────────────────────
    # Parse and dispatch
    # ─────────────────────────────────────────────────────────

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "run":
        cmd_run(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "create":
        cmd_create(args)


# ─────────────────────────────────────────────────────────
# Command handlers
# ─────────────────────────────────────────────────────────


def cmd_run(args):
    """Handle run command."""
    runner = Runner()
    stats = Stats()

    parts = [args.part] if args.part else [1, 2]

    # Run all days
    if args.all:
        results = runner.run_all(
            parts=parts,
            debug=args.debug,
            show_traceback=not args.no_traceback,
            use_example=args.example,
        )

        if not args.no_stats and not args.example:
            for day, day_results in results.items():
                stats.update(day, day_results)
            stats.save()
        return

    # Run specific day
    if args.day is None:
        print(c.error("Error: Specify a day number or use --all"))
        sys.exit(1)

    if not runner.day_exists(args.day):
        print(
            c.error("Error: Day ")
            + c.bold(c.green(str(args.day)))
            + c.error(" not found")
        )
        sys.exit(1)

    results = runner.run_day(
        args.day,
        parts=parts,
        debug=args.debug,
        show_traceback=not args.no_traceback,
        use_example=args.example,
    )

    # Prevent stats update if --example is used
    if not args.no_stats and not args.example:
        stats.update(args.day, results)
        stats.save()


def cmd_stats(args):
    """Handle stats command."""
    print_header("Profiling Statistics")
    stats = Stats()
    from fraocme.profiling.printer import print_stats_day, print_stats_summary_table

    if args.reset:
        if args.all:
            stats.reset_all()
            print(c.success("✓ All stats reset."))
        elif args.day is not None:
            stats.reset_day(args.day)
            print(c.success(f"✓ Stats for day {args.day} reset."))
        else:
            print(c.error("Specify a day to reset or use --all."))
        return
    if args.day is not None:
        data = stats.get_day(args.day)
        print_stats_day(args.day, data, best_only=args.best)
    else:
        data = stats.get_all()
        if args.best:
            print_stats_summary_table(data)
        else:
            days = sorted(data.keys(), key=lambda x: int(x.split("_")[1]))
            for day_key in days:
                day_num = int(day_key.split("_")[1])
                print_stats_day(day_num, data[day_key], best_only=False)


def cmd_create(args):
    """Handle create command."""
    from pathlib import Path

    day_num = args.day

    # Validate day number
    if day_num < 1 or day_num > 25:
        print(
            c.error("Error: Day number must be between 1 and 25, got ")
            + c.bold(str(day_num))
        )
        sys.exit(1)

    day_dir = Path.cwd() / "days" / f"day_{day_num:02d}"

    # Check if day already exists
    if day_dir.exists():
        print(c.warning("Warning: ") + f"Day {day_num} already exists at {day_dir}")
        return

    # Create directory
    day_dir.mkdir(parents=True, exist_ok=True)

    # Create input.txt
    input_file = day_dir / "input.txt"
    input_file.write_text("")

    # Create example_input.txt
    example_input_file = day_dir / "example_input.txt"
    example_input_file.write_text("")

    # Create solution.py template
    day_class_name = f"Day{day_num}"
    solution_template = f'''from fraocme import Solver


class {day_class_name}(Solver):
    def __init__(self, day: int = {day_num}, **kwargs):
        super().__init__(day=day, **kwargs)

    def parse(self, raw: str):
        """Parse the input data."""
        return raw.strip().split("\\n")

    def part1(self, data):
        """Solve part 1."""
        return None

    def part2(self, data):
        """Solve part 2."""
        return None
'''

    solution_file = day_dir / "solution.py"
    solution_file.write_text(solution_template)

    print(
        c.success("✓ Created day ")
        + c.bold(c.cyan(str(day_num)))
        + c.success(" at ")
        + c.bold(str(day_dir))
    )
    print(
        c.muted("Created:")
        + f" {input_file.name}"
        + f", {example_input_file.name}"
        + f", {solution_file.name}"
    )


if __name__ == "__main__":
    main()
