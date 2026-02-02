"""
Command-line interface for the file converter
"""

import argparse
import sys
from pathlib import Path
from .core import FileConverter
from .merge_cli import FileMerger


def create_parser():
    """Create command-line argument parser"""
    parser = argparse.ArgumentParser(
        description='Convert files between different formats (CSV, Excel, JSON, TSV, TXT) and merge files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py convert input.csv output.xlsx
  python cli.py convert data.json output.csv
  python cli.py convert stats.xlsx output.json
  python cli.py convert file.tsv output.xlsx
  python cli.py merge file1.csv file2.csv col1 col2
  python cli.py merge file1.xlsx file2.xlsx ID id -o merged_output
  python cli.py formats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert file format')
    convert_parser.add_argument('input', help='Input file path')
    convert_parser.add_argument('output', help='Output file path')
    convert_parser.add_argument(
        '-d', '--delimiter',
        help='Delimiter for output file (for CSV/TSV/TXT). Default: comma for CSV, tab for TSV, comma for TXT',
        default=None
    )
    convert_parser.add_argument(
        '-id', '--input-delimiter',
        help='Delimiter for input TXT file (if input is .txt format)',
        default=None
    )
    
    # Merge command
    merge_parser = subparsers.add_parser('merge', help='Merge two files on common column(s)')
    merge_parser.add_argument('file1', help='First input file path')
    merge_parser.add_argument('file2', help='Second input file path')
    merge_parser.add_argument('column1', help='Column name(s) in file1 to merge on (comma-separated for multi-column)')
    merge_parser.add_argument('column2', help='Column name(s) in file2 to merge on (comma-separated for multi-column)')
    merge_parser.add_argument(
        '-o', '--output',
        help='Base name for output files (without extension). Default: merged_<file1>_<file2>',
        default=None
    )
    merge_parser.add_argument(
        '-f', '--format',
        help='Output format: xlsx (default), csv, txt, or both',
        choices=['xlsx','csv','txt','both'],
        default='xlsx'
    )
    merge_parser.add_argument(
        '-j', '--join-type',
        help='Type of join: left (default), right, inner, outer',
        choices=['left','right','inner','outer'],
        default='left'
    )
    
    # Merge-with-reference command
    merge_ref_parser = subparsers.add_parser('merge-ref', help='Merge multiple files with a reference file')
    merge_ref_parser.add_argument('reference', help='Reference file to merge with')
    merge_ref_parser.add_argument(
        '-f', '--files',
        help='Input file(s) to merge (space-separated list)',
        nargs='+',
        default=None
    )
    merge_ref_parser.add_argument(
        '-p', '--pattern',
        help='File pattern to search for (e.g., *.csv, *.xlsx)',
        default=None
    )
    merge_ref_parser.add_argument(
        '-d', '--dirs',
        help='Directory/directories to search for files (space-separated)',
        nargs='+',
        default=None
    )
    merge_ref_parser.add_argument(
        '-rc', '--ref-column',
        help='Column name in reference file to merge on (comma-separated for multi-column)',
        required=True
    )
    merge_ref_parser.add_argument(
        '-ic', '--input-column',
        help='Column name in input files to merge on (comma-separated for multi-column)',
        required=True
    )
    merge_ref_parser.add_argument(
        '-o', '--output-dir',
        help='Output directory for results (default: merged_results)',
        default='merged_results'
    )
    merge_ref_parser.add_argument(
        '-fmt', '--format',
        help='Output format: xlsx (default), csv, txt, or both',
        choices=['xlsx','csv','txt','both'],
        default='xlsx'
    )
    merge_ref_parser.add_argument(
        '-j', '--join-type',
        help='Type of join: left (default), right, inner, outer',
        choices=['left','right','inner','outer'],
        default='left'
    )
    merge_ref_parser.add_argument(
        '-r', '--recursive',
        help='Search directories recursively',
        action='store_true',
        default=False
    )
    
    # Formats command
    subparsers.add_parser('formats', help='List supported formats')
    
    return parser


def show_formats():
    """Display supported file formats"""
    converter = FileConverter()
    formats = converter.get_supported_formats()
    
    print("\n" + "="*50)
    print("SUPPORTED FILE FORMATS")
    print("="*50)
    
    for ext, description in sorted(formats.items()):
        print(f"  .{ext:<6} - {description}")
    
    print("="*50 + "\n")


def convert_file(input_file: str, output_file: str, delimiter=None, input_delimiter=None):
    """Convert file from one format to another"""
    converter = FileConverter()
    
    try:
        result = converter.convert(input_file, output_file, delimiter, input_delimiter)
        print("\n" + "="*50)
        print(result)
        print("="*50 + "\n")
        return 0
    
    except FileNotFoundError as e:
        print(f"\n[ERROR] Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"\n[ERROR] Error: {e}", file=sys.stderr)
        return 1
    except ImportError as e:
        print(f"\n[ERROR] Error: {e}", file=sys.stderr)
        print("Install missing dependencies with: pip install -r requirements.txt", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}", file=sys.stderr)
        return 1


def merge_files_cmd(file1: str, file2: str, column1: str, column2: str, output_base: str = None, output_format: str = 'xlsx', join_type: str = 'left'):
    """Merge two files on specified columns"""
    merger = FileMerger()
    
    try:
        print("\n" + "="*60)
        print("MERGING FILES")
        print("="*60 + "\n")
        
        outputs = merger.merge_two_files(file1, file2, column1, column2, output_base, output_format, join_type)
        
        print("\n" + "="*60)
        print("[OK] MERGE COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"\nOutput files created:")
        for p in outputs:
            print(f"  • {p}")
        print("="*60 + "\n")
        return 0
    
    except FileNotFoundError as e:
        print(f"\n[ERROR] Error: {e}", file=sys.stderr)
        return 1
    except KeyError as e:
        print(f"\n[ERROR] Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"\n[ERROR] Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}", file=sys.stderr)
        return 1


def merge_ref_files_cmd(reference: str, files: list, pattern: str, dirs: list, ref_column: str,
                       input_column: str, output_dir: str, output_format: str, 
                       join_type: str, recursive: bool):
    """Merge multiple files with a reference file"""
    merger = FileMerger()
    
    try:
        print("\n" + "="*60)
        print("MERGE-TO-REFERENCE")
        print("="*60 + "\n")
        
        outputs = merger.merge_with_reference(
            reference_file=reference,
            input_files=files,
            ref_column=ref_column,
            input_column=input_column,
            output_dir=output_dir,
            output_format=output_format,
            join_type=join_type,
            file_pattern=pattern,
            search_dirs=dirs
        )
        
        print("\n" + "="*60)
        print("[OK] MERGE-TO-REFERENCE COMPLETED")
        print("="*60)
        print(f"\n{len(outputs)} result file(s) created in: {output_dir}/")
        print("="*60 + "\n")
        return 0
    
    except FileNotFoundError as e:
        print(f"\n[ERROR] Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"\n[ERROR] Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    if args.command == 'formats':
        show_formats()
        return 0
    
    elif args.command == 'convert':
        return convert_file(args.input, args.output, args.delimiter, args.input_delimiter)
    
    elif args.command == 'merge':
        return merge_files_cmd(args.file1, args.file2, args.column1, args.column2, args.output, args.format, args.join_type)
    
    elif args.command == 'merge-ref':
        return merge_ref_files_cmd(args.reference, args.files, args.pattern, args.dirs,
                                  args.ref_column, args.input_column, args.output_dir,
                                  args.format, args.join_type, args.recursive)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())