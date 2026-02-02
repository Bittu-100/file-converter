# File Converter

Lightweight Python CLI + library to convert and merge CSV/TSV/Excel/JSON files, with multi-column SQL-style joins.

## Quick start

Install (editable):

```bash
pip install -e ./converter
```

Convert a TXT (tab-delimited) file to Excel:

```bash
python -m converter.cli convert "data.txt" "data.xlsx" --input-delimiter "\t"
```

Merge many files with a reference file:

```bash
python -m converter.cli merge-ref reference.csv -d branch_data/ -rc ID -ic ID -fmt both
```

## Features

- Convert between CSV / TSV / TXT / JSON / XLSX
- Multi-column SQL-style joins: left, right, inner, outer
- Batch merge-to-reference (one reference → many inputs)
- Custom delimiters and Excel formatting via openpyxl

## License

MIT
