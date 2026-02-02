"""
Test multi-column joins
"""
import csv
import os
from converter.merge_cli import FileMerger


def create_multi_column_test_files():
    """Create sample files for multi-column join testing"""
    
    # Employees: ID and Department
    employees = [
        ['EmpID', 'Dept', 'Name', 'Salary'],
        ['E001', 'Sales', 'Alice', '50000'],
        ['E002', 'Sales', 'Bob', '55000'],
        ['E003', 'IT', 'Charlie', '65000'],
        ['E004', 'IT', 'Diana', '68000'],
    ]
    
    # Projects: ID and Department
    projects = [
        ['EmpID', 'Dept', 'Project', 'Budget'],
        ['E001', 'Sales', 'Website', '10000'],
        ['E002', 'Sales', 'Marketing', '15000'],
        ['E003', 'IT', 'Database', '20000'],
        ['E005', 'HR', 'Training', '5000'],  # E005 doesn't exist in employees
    ]
    
    with open('employees.csv', 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(employees)
    
    with open('projects.csv', 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(projects)
    
    print("[OK] Created employees.csv and projects.csv")


def display_results(join_type, output_file):
    """Display merged results"""
    print(f"\n{join_type.upper()} JOIN (Multi-column on EmpID, Dept):")
    print("-" * 60)
    
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            rows = list(reader)
            
            print(f"Header: {rows[0]}")
            print(f"Rows: {len(rows)-1}")
            for i, row in enumerate(rows[1:], 1):
                print(f"  {i}. {row}")
    except Exception as e:
        print(f"Error reading {output_file}: {e}")


def test_multi_column_joins():
    """Test multi-column joins"""
    
    print("\n" + "="*60)
    print("TESTING MULTI-COLUMN JOINS")
    print("="*60 + "\n")
    
    print("Step 1: Creating sample data files...")
    create_multi_column_test_files()
    
    merger = FileMerger()
    join_types = ['left', 'inner', 'right', 'outer']
    
    try:
        for join_type in join_types:
            print(f"\nStep 2: Running {join_type.upper()} JOIN (multi-column)...")
            
            # Multi-column join: EmpID,Dept
            outputs = merger.merge_two_files(
                'employees.csv',
                'projects.csv',
                'EmpID,Dept',  # Multiple columns
                'EmpID,Dept',  # Multiple columns
                output_base=f'result_multi_{join_type}',
                output_format='txt',
                join_type=join_type
            )
            
            display_results(join_type, outputs[0])
        
        print("\n" + "="*60)
        print("[OK] MULTI-COLUMN JOIN TESTS COMPLETED!")
        print("="*60 + "\n")
        
        print("MULTI-COLUMN JOIN EXPLANATION:")
        print("  Joining on TWO columns: (EmpID, Dept)")
        print("  This matches rows where BOTH EmpID AND Dept match\n")
        
        print("LEFT JOIN: 4 rows (all employees, matching projects)")
        print("  - E001,Sales -> matched with project")
        print("  - E002,Sales -> matched with project")
        print("  - E003,IT -> matched with project")
        print("  - E004,IT -> no matching project (empty cols)\n")
        
        print("INNER JOIN: 3 rows (only matching combos)")
        print("  - E001,Sales, E002,Sales, E003,IT\n")
        
        print("RIGHT JOIN: 4 rows (all projects, matching employees)")
        print("  - E001,Sales, E002,Sales, E003,IT, E005,HR (empty emp cols)\n")
        
        print("OUTER JOIN: 5 rows (all combos from both files)")
        print("  - All employees + all projects\n")
        
        return 0
    
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        return 1
    
    finally:
        # Cleanup
        print("Cleaning up...")
        for f in ['employees.csv', 'projects.csv']:
            if os.path.exists(f):
                os.remove(f)
        for join_type in join_types:
            f = f'result_multi_{join_type}.txt'
            if os.path.exists(f):
                os.remove(f)
        print("[OK] Cleanup complete")


if __name__ == "__main__":
    import sys
    sys.exit(test_multi_column_joins())
