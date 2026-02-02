# Join Types Summary

## Quick Reference Card

### LEFT JOIN (Default)
```
❶ Keeps all rows from FILE1
❷ Adds matching data from FILE2
❸ Unmatched rows get empty values

Usage: python -m converter.cli merge file1 file2 col col -j left
```

---

### INNER JOIN
```
❶ Keeps only rows that exist in BOTH files
❷ No empty values in result
❸ Only matching combinations

Usage: python -m converter.cli merge file1 file2 col col -j inner
```

---

### RIGHT JOIN
```
❶ Keeps all rows from FILE2
❷ Adds matching data from FILE1
❸ Unmatched rows get empty values

Usage: python -m converter.cli merge file1 file2 col col -j right
```

---

### OUTER JOIN (Full Outer Join)
```
❶ Keeps ALL rows from BOTH files
❂ Combines LEFT and RIGHT join results
❸ Includes all combinations

Usage: python -m converter.cli merge file1 file2 col col -j outer
```

---

## Comparison Table

| Feature | LEFT | RIGHT | INNER | OUTER |
|---------|------|-------|-------|-------|
| Keep all from File1 | ✅ | ✗ | ✗ | ✅ |
| Keep all from File2 | ✗ | ✅ | ✗ | ✅ |
| Only matches | ✗ | ✗ | ✅ | ✗ |
| All combinations | ✅ | ✅ | ✅ | ✅ |
| May have empty cells | ✅ | ✅ | ✗ | ✅ |

---

## Row Count Examples

**File1 has 4 rows, File2 has 4 rows, 3 rows match**

| Join Type | Result Rows |
|-----------|-------------|
| LEFT | 4 (all from File1) |
| RIGHT | 4 (all from File2) |
| INNER | 3 (only matches) |
| OUTER | 5 (all from both) |

---

## Multi-Column Join

Join on multiple columns using comma-separated names:

```bash
# Single column
python -m converter.cli merge file1 file2 ID ID -j left

# Multiple columns (must match in both)
python -m converter.cli merge file1 file2 "DeptID,EmpID" "DeptID,EmpID" -j left
```

---

## Output Format Options

```bash
# Excel (default)
python -m converter.cli merge file1 file2 col col -f xlsx

# CSV only
python -m converter.cli merge file1 file2 col col -f csv

# Tab-separated text
python -m converter.cli merge file1 file2 col col -f txt

# Both Excel and CSV
python -m converter.cli merge file1 file2 col col -f both
```

---

## Decision Tree

```
START: I need to merge two files

├─ Do I want to keep all rows from file1?
│  └─ YES → Use LEFT JOIN (default)
│  └─ NO → Continue...
│
├─ Do I want to keep all rows from file2?
│  └─ YES → Use RIGHT JOIN
│  └─ NO → Continue...
│
├─ Do I only want matching rows?
│  └─ YES → Use INNER JOIN
│  └─ NO → Continue...
│
├─ Do I want all rows from both files?
│  └─ YES → Use OUTER JOIN
│  └─ NO → Something else
```

---

## Example Scenarios

### Scenario A: Customer Analysis
- File1: All customers (don't lose any)
- File2: Orders (only some customers ordered)
- **Use: LEFT JOIN**
```bash
python -m converter.cli merge customers.csv orders.csv CustID CustID -j left
```

### Scenario B: Find Problems
- File1: Expected customers
- File2: Actual customers
- Want: Only those that match
- **Use: INNER JOIN**
```bash
python -m converter.cli merge expected.csv actual.csv ID ID -j inner
```

### Scenario C: Process All Orders
- File1: Customer info (not all have orders)
- File2: All orders (need to process each)
- **Use: RIGHT JOIN**
```bash
python -m converter.cli merge customers.csv orders.csv CustID CustID -j right
```

### Scenario D: Complete Picture
- File1: Employees
- File2: Contractors
- Want: Everyone
- **Use: OUTER JOIN**
```bash
python -m converter.cli merge employees.csv contractors.csv ID ID -j outer
```

---

## Testing

Run the test scripts to see all joins in action:

```bash
# Basic join types
python test_join_types.py

# CLI usage
python test_cli_joins.py

# Multi-column joins
python test_multi_column_joins.py

# Comprehensive examples
python merge_join_examples.py
```

---

## Cheat Sheet

```python
from converter.merge_cli import FileMerger

merger = FileMerger()

# LEFT JOIN (keep all from file1)
merger.merge_two_files('f1.csv', 'f2.csv', 'id', 'id', join_type='left')

# INNER JOIN (only matches)
merger.merge_two_files('f1.csv', 'f2.csv', 'id', 'id', join_type='inner')

# RIGHT JOIN (keep all from file2)
merger.merge_two_files('f1.csv', 'f2.csv', 'id', 'id', join_type='right')

# OUTER JOIN (all rows from both)
merger.merge_two_files('f1.csv', 'f2.csv', 'id', 'id', join_type='outer')

# Multi-column join
merger.merge_two_files('f1.csv', 'f2.csv', 'id,dept', 'id,dept', join_type='left')

# With custom output
merger.merge_two_files('f1.csv', 'f2.csv', 'id', 'id',
                       output_base='result',
                       output_format='both',
                       join_type='inner')
```

---

**Need help? Check `MERGE_GUIDE.md` for detailed documentation!**
