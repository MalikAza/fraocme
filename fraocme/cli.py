import argparse
import sys
from pathlib import Path

from .core.runner import Runner
from .profiling.stats import Stats


def main():
    parser = argparse.ArgumentParser(
        prog="fraocme",
        description="Advent of Code framework"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # ─────────────────────────────────────────────────────────
    # run command
    # ─────────────────────────────────────────────────────────
    
    run_parser = subparsers.add_parser("run", help="Run solution(s)")
    run_parser.add_argument(
        "day",
        type=int,
        nargs="?",
        default=None,
        help="Day number to run"
    )
    run_parser.add_argument(
        "-p", "--part",
        type=int,
        choices=[1, 2],
        default=None,
        help="Run only specific part"
    )
    run_parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Run all days"
    )
    run_parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Enable debug output"
    )
    run_parser.add_argument(
        "--no-stats",
        action="store_true",
        help="Don't save stats"
    )
    
    # ─────────────────────────────────────────────────────────
    # stats command
    # ─────────────────────────────────────────────────────────
    
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    stats_parser.add_argument(
        "day",
        type=int,
        nargs="?",
        default=None,
        help="Day number (omit for all days)"
    )
    stats_parser.add_argument(
        "--best",
        action="store_true",
        help="Show only best times"
    )
    
    
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



# ─────────────────────────────────────────────────────────
# Command handlers
# ─────────────────────────────────────────────────────────

def cmd_run(args):
    """Handle run command."""
    runner = Runner()
    stats = Stats()
    
    # Determine which parts to run
    parts = [args.part] if args.part else [1, 2]
    
    # Run all days
    if args.all:
        results = runner.run_all(parts=parts, debug=args.debug)
        if not args.no_stats:
            for day, day_results in results.items():
                stats.update(day, day_results)
            stats.save()
        return
    
    # Run specific day
    if args.day is None:
        print("\033[91mError: Specify a day number or use --all\033[0m")
        sys.exit(1)
    
    if not runner.day_exists(args.day):
        print(f"\033[91mError: Day {args.day} not found\033[0m")
        sys.exit(1)
    
    results = runner.run_day(args.day, parts=parts, debug=args.debug)
    
    if not args.no_stats:
        stats.update(args.day, results)
        stats.save()


def cmd_stats(args):
    """Handle stats command."""
    return NotImplemented

    


if __name__ == "__main__":
    main()