# File Format Converter

A powerful Python utility to convert between different file formats with support for CSV, Excel, JSON, TSV, and TXT files.

## Features

- **Multiple Format Support**: Convert between CSV, Excel (XLSX/XLS), JSON, TSV, and TXT
- **Easy-to-use CLI**: Simple command-line interface
- **File Merging**: Combine multiple files (concatenate, join, union)
- **Data Validation**: Automatic data type detection and validation
- **Excel Formatting**: Auto-formatted Excel output with headers and column sizing
- **Error Handling**: Comprehensive error messages and validation

## Supported Formats

- **.csv** - Comma Separated Values
- **.xlsx** - Microsoft Excel
- **.xls** - Microsoft Excel (Legacy)
- **.json** - JSON format
- **.tsv** - Tab Separated Values
- **.txt** - Text File

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install the package:
```bash
pip install -e .
```

## Usage

### Command Line

#### List Supported Formats
```bash
python -m converter.cli formats
```

#### Convert File
```bash
python -m converter.cli convert input.csv output.xlsx
python -m converter.cli convert data.json output.csv
python -m converter.cli convert stats.xlsx output.json
```

#### Convert with Custom Delimiter
```bash
python -m converter.cli convert input.csv output.txt --delimiter ";"
```

#### Merge Two Files (Left Join)
```bash
python -m converter.cli merge file1.csv file2.csv column1 column2
python -m converter.cli merge data1.xlsx data2.xlsx ID id -o merged_output
```

This performs a LEFT JOIN, keeping all rows from file1 and appending matching data from file2 based on the specified columns.

### Python Code

```python
from converter import FileConverter
from converter.merge_cli import FileMerger

# Initialize converter
converter = FileConverter()

# Convert file
converter.convert('input.csv', 'output.xlsx')

# Read file
data = converter.read_file('data.csv')

# Get supported formats
formats = converter.get_supported_formats()

# Merge two files
merger = FileMerger()
txt_output, excel_output = merger.merge_two_files(
    'file1.csv', 
    'file2.csv', 
    'column1',  # Column in file1
    'column2'   # Column in file2
)
```

### File Merging

#### Merge Two Files (Left Join)
```python
from converter.merge_cli import FileMerger

merger = FileMerger()

# Merge file1 and file2 on specified columns
# Keeps all rows from file1, appends matching data from file2
txt_output, excel_output = merger.merge_two_files(
    'base_data.csv', 
    'additional_data.csv', 
    'ID',           # Column name in base_data.csv
    'id',           # Column name in additional_data.csv
    'output_merged' # Optional: output base name
)
# Creates: output_merged.txt and output_merged.xlsx
```

#### Other Merge Operations (Concatenate, Join, Union)
```python
# Concatenate files
merger.merge_files(['file1.csv', 'file2.csv'], 'merged.xlsx', operation='concat')

# Join files on a key
merger.merge_files(['file1.csv', 'file2.csv'], 'joined.csv', merge_key='ID', operation='join')

# Union unique records
merger.merge_files(['file1.csv', 'file2.csv'], 'union.json', operation='union')
```

## Examples

### Example 1: CSV to Excel
```bash
python -m converter.cli convert data.csv data.xlsx
```

### Example 2: JSON to CSV
```bash
python -m converter.cli convert data.json data.csv
```

### Example 3: Excel to JSON
```bash
python -m converter.cli convert stats.xlsx stats.json
```

### Example 4: TSV to Excel
```bash
python -m converter.cli convert data.tsv output.xlsx
```

### Example 5: Merge Two Files (Left Join)
```bash
python -m converter.cli merge customers.csv orders.csv CustomerID CustomerID
# Creates: merged_customers_orders.txt and merged_customers_orders.xlsx

# With custom output name
python -m converter.cli merge customers.xlsx orders.xlsx ID id -o customer_orders
# Creates: customer_orders.txt and customer_orders.xlsx
```

In this merge example:
- All rows from `customers.csv` are kept (left file)
- Data from `orders.csv` is appended where `CustomerID` matches (right file)
- If no match is found, the columns from the right file are filled with None/empty values
- Output is created in both TSV (.txt) and Excel (.xlsx) formats

## Project Structure

```
converter/
├── __init__.py          # Package initialization
├── core.py              # Core conversion logic
├── cli.py               # Command-line interface
├── merge_cli.py         # File merging functionality
├── setup.py             # Setup configuration
├── requirements.txt     # Dependencies
└── README.md            # This file
```

## API Reference

### FileConverter Class

#### Methods

- `get_supported_formats()` - Returns dict of supported formats
- `read_file(file_path)` - Read file and return list of dictionaries
- `convert(input_file, output_file, delimiter=None)` - Convert file format
- `merge_files(file1, file2, column1, column2, output_file_txt, output_file_excel)` - Merge two files on specified columns using left join

### FileMerger Class

#### Methods

- `merge_two_files(file1, file2, column1, column2, output_base=None)` - Merge two files on specified columns (left join)
  - **file1**: Left file (all rows will be kept)
  - **file2**: Right file (matching rows will be appended)
  - **column1**: Column name in file1 to merge on
  - **column2**: Column name in file2 to merge on
  - **output_base**: Optional base name for output files
  - **Returns**: Tuple of (txt_output_path, excel_output_path)

- `merge_files(input_files, output_file, merge_key=None, operation='concat')` - Merge multiple files

## Error Handling

The converter provides detailed error messages for:
- Missing files
- Unsupported formats
- Missing dependencies
- Invalid data
- File access issues

## Requirements

- Python 3.7+
- openpyxl (for Excel support)

## License

MIT License

## Contributing

Feel free to submit issues and enhancement requests!
