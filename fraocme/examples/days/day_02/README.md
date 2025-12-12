# Day 02 - Sequence Utility Functions

## Overview
Demonstrates sequence manipulation functions from `fraocme.common.sequence_utils`.

## Functions Demonstrated

### Counting & Checking
- `frequencies()` - Count occurrences
- `all_equal()` - Check if all same

### Grouping & Sliding
- `chunks()` - Fixed-size groups
- `windows()` - Sliding windows
- `pairwise()` - Consecutive pairs

### Transformation
- `rotate()` - Rotate left/right
- `unique()` - Remove duplicates
- `flatten()` - Flatten nested lists

## Run
```bash
fraocme run 2 --debug
```

## Key Takeaways
- Use `windows()` for sliding analysis (moving averages, etc.)
- `pairwise()` is perfect for detecting increases/decreases
- `chunks()` vs `windows()`: chunks don't overlap, windows do
- `unique()` preserves order unlike `set()`
