# Day 01 - Parser Functions

## Overview
Demonstrates all parser functions from `fraocme.common.parser`.

## Functions Demonstrated

### Basic Parsers
- `sections()` - Split by blank lines
- `lines()` - Split by newlines
- `ints()` - Parse integers per line
- `char_lines()` - Parse digit characters

### Advanced Parsers
- `key_ints()` - Parse key-value format
- `ranges()` - Parse range tuples
- `mapped()` - Custom line transformation

## Run
```bash
fraocme run 1 --debug
```

## Key Takeaways
- Use `sections()` when input has multiple blocks
- `char_lines()` is perfect for digit grids (when rows have different lengths)
- `key_ints()` handles equation-style formats
- `mapped()` allows any custom parsing logic
