# Changelog

All notable changes to the fraocme project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CLI framework for Advent of Code solutions
  - `fraocme run <day>` - Run solutions for specific day(s)
  - `fraocme stats` - Display performance statistics
  - `fraocme create <day>` - Create new day solution template (days 1-25)
- Solver base class for implementing solutions
- Runner class for discovering and executing solvers
- Grid utilities for grid-based puzzles
- Color and formatting utilities for output
- Performance profiling (Timer, decorators, Stats)
- Comprehensive test suite (211 tests)
- Input/output parsing utilities
- Debug utilities with conditional output

### Features
- Support for Python 3.13+
- Zero external dependencies for core functionality
- Built-in testing utilities
- Semantic color output
- Performance benchmarking tools
- Code quality tools (Ruff for linting/formatting)

---

For more information, see the [README](README.md).
