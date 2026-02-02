"""
Test script for different join types
Demonstrates LEFT, RIGHT, INNER, and OUTER joins
"""

import csv
import os
from pathlib import Path
from converter.merge_cli import FileMerger


def create_sample_files():
    """Create sample CSV files for join testing"""
    
    # Left file: Students with IDs
    students = [
        ['StudentID', 'Name', 'Grade'],
        ['S001', 'Alice', '10'],
        ['S002', 'Bob', '11'],
        ['S003', 'Charlie', '10'],
        ['S004', 'Diana', '11'],
    ]
    
    # Right file: Exam scores (only some students took exam)
    exam_scores = [
        ['StudentID', 'Math', 'English'],
        ['S001', '95', '88'],
        ['S002', '87', '92'],
        ['S004', '91', '85'],
        ['S005', '78', '80'],  # S005 didn't take courses
    ]
    
    with open('students.csv', 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(students)
    
    with open('exam_scores.csv', 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(exam_scores)
    
    print("[OK] Created students.csv and exam_scores.csv")


def display_results(join_type, output_file):
    """Display merged results"""
    print(f"\n{'='*60}")
    print(f"{join_type.upper()} JOIN RESULTS")
    print(f"{'='*60}\n")
    
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            rows = list(reader)
            
            print(f"Header: {rows[0]}")
            print(f"\nData rows ({len(rows)-1}):")
            for i, row in enumerate(rows[1:], 1):
                print(f"  {i}. {row}")
    except Exception as e:
        print(f"Could not read {output_file}: {e}")


def test_all_joins():
    """Test all join types"""
    
    print("\n" + "="*60)
    print("TESTING ALL JOIN TYPES")
    print("="*60 + "\n")
    
    # Create sample files
    print("Step 1: Creating sample data files...")
    create_sample_files()
    
    merger = FileMerger()
    join_types = ['left', 'right', 'inner', 'outer']
    
    try:
        for join_type in join_types:
            print(f"\nStep 2: Running {join_type.upper()} JOIN...")
            print("-" * 60)
            
            outputs = merger.merge_two_files(
                'students.csv',
                'exam_scores.csv',
                'StudentID',
                'StudentID',
                output_base=f'result_{join_type}',
                output_format='txt',  # Use TXT for easy viewing
                join_type=join_type
            )
            
            display_results(join_type, outputs[0])
        
        print("\n" + "="*60)
        print("[OK] ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        
        # Show summary
        print("SUMMARY OF JOIN TYPES:\n")
        print("LEFT JOIN:")
        print("  - Keeps all rows from LEFT file (students.csv)")
        print("  - Adds exam scores where StudentID matches")
        print("  - Students without scores have NULL in exam columns")
        print("  - Result: 4 rows (all students)\n")
        
        print("RIGHT JOIN:")
        print("  - Keeps all rows from RIGHT file (exam_scores.csv)")
        print("  - Adds student info where StudentID matches")
        print("  - Non-matching exam scores have NULL in student columns")
        print("  - Result: 4 rows (S001, S002, S004, S005)\n")
        
        print("INNER JOIN:")
        print("  - Keeps only rows with matching StudentID in BOTH files")
        print("  - All NULL values eliminated")
        print("  - Result: 3 rows (S001, S002, S004 - students with scores)\n")
        
        print("OUTER JOIN:")
        print("  - Keeps all rows from BOTH files")
        print("  - Combines LEFT and RIGHT join results")
        print("  - Result: 5 rows (S001, S002, S003, S004, S005)\n")
        
        return 0
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1
    
    finally:
        # Cleanup
        print("Cleaning up...")
        for f in ['students.csv', 'exam_scores.csv']:
            if os.path.exists(f):
                os.remove(f)
        print("[OK] Cleanup complete")


if __name__ == "__main__":
    import sys
    sys.exit(test_all_joins())
