"""
Example script demonstrating the merge functionality
"""

from converter.merge_cli import FileMerger
import sys


def main():
    """
    Example of how to use the merge functionality programmatically
    """
    merger = FileMerger()
    
    # Example 1: Basic merge
    print("=" * 60)
    print("MERGE EXAMPLE")
    print("=" * 60)
    print("\nThis example demonstrates the merge functionality.")
    print("\nUsage:")
    print("  From CLI: python -m converter.cli merge <file1> <file2> <col1> <col2> [-o output_base]")
    print("  From code: merger.merge_two_files(file1, file2, col1, col2)")
    print("\nExample commands:")
    print("  python -m converter.cli merge data1.csv data2.csv ID id -o merged_data")
    print("  python -m converter.cli merge file1.xlsx file2.xlsx name Name")
    print("\n" + "=" * 60)
    
    # Check if arguments are provided
    if len(sys.argv) > 4:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        column1 = sys.argv[3]
        column2 = sys.argv[4]
        output_base = sys.argv[5] if len(sys.argv) > 5 else None
        
        try:
            txt_output, excel_output = merger.merge_two_files(file1, file2, column1, column2, output_base)
            print(f"\n✓ Merge completed successfully!")
            print(f"  TSV output: {txt_output}")
            print(f"  Excel output: {excel_output}")
        except Exception as e:
            print(f"\n✗ Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("\nNo files specified. Use the CLI command or provide arguments:")
        print("  python merge_example.py <file1> <file2> <column1> <column2> [output_base]")


if __name__ == "__main__":
    main()
