# Day 04 - Range Utility Functions

## Overview
Demonstrates range manipulation functions from `fraocme.common.range_utils`.

## Functions Demonstrated

### Overlap Detection
- `ranges_overlap()` - Check if two ranges overlap
- `range_intersection()` - Get the overlapping part

### Range Merging
- `merge_ranges()` - Merge overlapping/adjacent ranges
- `within_range()` - Check if value is in any range

### Coverage Analysis
- `range_coverage()` - Calculate total coverage

## Run
```bash
fraocme run 4 --debug
```

## Key Takeaways
- Use `merge_ranges()` to eliminate overlap
- `range_coverage()` calculates total span
- Inclusive vs exclusive modes matter
- Great for interval scheduling problems
- Perfect for analyzing sensor ranges
- Adjacent ranges can be merged when inclusive=True
