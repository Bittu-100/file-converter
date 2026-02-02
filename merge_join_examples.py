"""
Comprehensive merge examples demonstrating all join types and output formats
"""

from converter.merge_cli import FileMerger
import csv
import os


def create_sample_data():
    """Create sample CSV files for demonstration"""
    
    # Customers file
    customers = [
        ['CustomerID', 'Name', 'City', 'Status'],
        ['C001', 'Alice Johnson', 'New York', 'Active'],
        ['C002', 'Bob Smith', 'Los Angeles', 'Active'],
        ['C003', 'Charlie Brown', 'Chicago', 'Inactive'],
        ['C004', 'Diana Prince', 'Houston', 'Active'],
    ]
    
    # Orders file
    orders = [
        ['CustomerID', 'OrderID', 'Amount', 'Date'],
        ['C001', 'ORD001', '1500', '2024-01-15'],
        ['C002', 'ORD002', '2300', '2024-01-20'],
        ['C004', 'ORD003', '950', '2024-01-25'],
        ['C005', 'ORD004', '3200', '2024-02-01'],  # C005 not in customers
    ]
    
    with open('customers.csv', 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(customers)
    
    with open('orders.csv', 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(orders)
    
    print("[OK] Sample data created: customers.csv, orders.csv")


def demonstrate_join_types():
    """Demonstrate all join types"""
    
    print("\n" + "="*70)
    print("DEMONSTRATING ALL JOIN TYPES")
    print("="*70 + "\n")
    
    merger = FileMerger()
    
    # LEFT JOIN
    print("\n[1] LEFT JOIN - All customers + their orders (if any)")
    print("-" * 70)
    outputs = merger.merge_two_files(
        'customers.csv', 'orders.csv',
        'CustomerID', 'CustomerID',
        output_base='demo_left_join',
        output_format='both',  # Create both XLSX and CSV
        join_type='left'
    )
    print(f"Result: {len(outputs)} files created")
    display_file_content(outputs[0], limit=4)
    
    # INNER JOIN
    print("\n[2] INNER JOIN - Only customers who have placed orders")
    print("-" * 70)
    outputs = merger.merge_two_files(
        'customers.csv', 'orders.csv',
        'CustomerID', 'CustomerID',
        output_base='demo_inner_join',
        output_format='csv',
        join_type='inner'
    )
    print(f"Result: {len(outputs)} file created")
    display_file_content(outputs[0], limit=4)
    
    # RIGHT JOIN
    print("\n[3] RIGHT JOIN - All orders + customer info (if available)")
    print("-" * 70)
    outputs = merger.merge_two_files(
        'customers.csv', 'orders.csv',
        'CustomerID', 'CustomerID',
        output_base='demo_right_join',
        output_format='csv',
        join_type='right'
    )
    print(f"Result: {len(outputs)} file created")
    display_file_content(outputs[0], limit=4)
    
    # OUTER JOIN
    print("\n[4] OUTER JOIN - All customers AND all orders")
    print("-" * 70)
    outputs = merger.merge_two_files(
        'customers.csv', 'orders.csv',
        'CustomerID', 'CustomerID',
        output_base='demo_outer_join',
        output_format='xlsx',
        join_type='outer'
    )
    print(f"Result: {len(outputs)} file created (Excel format)")


def demonstrate_multi_column_join():
    """Demonstrate multi-column join"""
    
    print("\n" + "="*70)
    print("MULTI-COLUMN JOIN EXAMPLE")
    print("="*70)
    
    # Create departments and salary data
    departments_data = [
        ['DeptID', 'EmployeeID', 'Name', 'Position'],
        ['D001', 'E001', 'Alice', 'Manager'],
        ['D001', 'E002', 'Bob', 'Developer'],
        ['D002', 'E003', 'Charlie', 'Analyst'],
    ]
    
    salaries_data = [
        ['DeptID', 'EmployeeID', 'Salary', 'BonusPercentage'],
        ['D001', 'E001', '80000', '15'],
        ['D001', 'E002', '65000', '10'],
        ['D002', 'E003', '60000', '8'],
        ['D003', 'E004', '55000', '5'],  # D003 doesn't exist
    ]
    
    with open('departments.csv', 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(departments_data)
    
    with open('salaries.csv', 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(salaries_data)
    
    print("\nJoining on TWO columns: DeptID and EmployeeID")
    print("-" * 70)
    
    merger = FileMerger()
    outputs = merger.merge_two_files(
        'departments.csv', 'salaries.csv',
        'DeptID,EmployeeID',  # MULTI-COLUMN
        'DeptID,EmployeeID',  # MULTI-COLUMN
        output_base='demo_multi_column',
        output_format='csv',
        join_type='inner'
    )
    
    print(f"Result: {len(outputs)} file created")
    display_file_content(outputs[0], limit=4)
    
    # Cleanup
    os.remove('departments.csv')
    os.remove('salaries.csv')


def display_file_content(filepath, limit=None):
    """Display file content in a formatted way"""
    try:
        if filepath.endswith('.csv'):
            delimiter = ','
        else:
            delimiter = '\t'
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=delimiter)
            rows = list(reader)
        
        # Print header
        if rows:
            print(f"\nHeader: {', '.join(rows[0])}")
            print(f"Total rows: {len(rows)-1}\n")
            
            # Print sample data
            display_rows = rows[1:limit+1] if limit else rows[1:]
            for i, row in enumerate(display_rows, 1):
                print(f"  {i}. {row}")
            
            if limit and len(rows) > limit + 1:
                print(f"  ... and {len(rows)-limit-1} more rows")
    
    except Exception as e:
        print(f"Error reading file: {e}")


def main():
    """Main demonstration"""
    
    print("\n" + "="*70)
    print("FILE MERGE UTILITY - COMPREHENSIVE EXAMPLES")
    print("="*70)
    
    try:
        create_sample_data()
        demonstrate_join_types()
        demonstrate_multi_column_join()
        
        print("\n" + "="*70)
        print("[OK] ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*70 + "\n")
        
        print("KEY TAKEAWAYS:")
        print("  • LEFT JOIN: Keep all rows from first file")
        print("  • RIGHT JOIN: Keep all rows from second file")
        print("  • INNER JOIN: Keep only matching rows")
        print("  • OUTER JOIN: Keep all rows from both files")
        print("  • Multi-column joins: Use comma-separated column names")
        print("  • Output formats: xlsx, csv, txt, or both\n")
        
        return 0
    
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return 1
    
    finally:
        # Cleanup
        for f in ['customers.csv', 'orders.csv']:
            if os.path.exists(f):
                os.remove(f)
        
        for prefix in ['demo_left_join', 'demo_inner_join', 'demo_right_join', 
                       'demo_outer_join', 'demo_multi_column']:
            for ext in ['.csv', '.xlsx', '.txt']:
                if os.path.exists(f"{prefix}{ext}"):
                    os.remove(f"{prefix}{ext}")


if __name__ == "__main__":
    import sys
    sys.exit(main())
