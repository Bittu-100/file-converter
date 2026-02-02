"""
Test script for merge functionality
Creates sample data files and demonstrates the merge operation
"""

import csv
import os
from pathlib import Path
from converter.merge_cli import FileMerger


def create_sample_files():
    """Create sample CSV files for testing merge functionality"""
    
    # Sample data 1: Customer data
    customers_data = [
        ['CustomerID', 'CustomerName', 'City', 'Country'],
        ['C001', 'John Smith', 'New York', 'USA'],
        ['C002', 'Jane Doe', 'London', 'UK'],
        ['C003', 'Bob Johnson', 'Toronto', 'Canada'],
        ['C004', 'Alice Williams', 'Sydney', 'Australia'],
        ['C005', 'Charlie Brown', 'Paris', 'France'],
    ]
    
    # Sample data 2: Order data (some customers have multiple orders)
    orders_data = [
        ['CustomerID', 'OrderID', 'OrderDate', 'Amount'],
        ['C001', 'O001', '2024-01-15', '150.00'],
        ['C001', 'O002', '2024-02-20', '200.00'],
        ['C002', 'O003', '2024-01-10', '75.50'],
        ['C003', 'O004', '2024-02-05', '300.00'],
        ['C004', 'O005', '2024-02-15', '125.75'],
    ]
    
    # Create customers file
    with open('test_customers.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(customers_data)
    
    # Create orders file
    with open('test_orders.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(orders_data)
    
    print("[OK] Created test_customers.csv")
    print("[OK] Created test_orders.csv")


def test_merge():
    """Test the merge functionality"""
    
    print("\n" + "="*60)
    print("TESTING MERGE FUNCTIONALITY")
    print("="*60 + "\n")
    
    # Create sample files
    print("Step 1: Creating sample data files...")
    create_sample_files()
    
    # Perform merge
    print("\nStep 2: Merging files...")
    print("-" * 60)
    
    merger = FileMerger()
    
    try:
        outputs = merger.merge_two_files(
            'test_customers.csv',
            'test_orders.csv',
            'CustomerID',
            'CustomerID',
            'merged_customer_orders'
        )
        
        # Normalize outputs for backward compatibility in test
        txt_output = None
        excel_output = None
        for p in outputs:
            if p.endswith('.txt'):
                txt_output = p
            elif p.endswith('.csv'):
                txt_output = p
            elif p.endswith('.xlsx') or p.endswith('.xls'):
                excel_output = p
        
        print("\n" + "-" * 60)
        print("[OK] MERGE COMPLETED SUCCESSFULLY")
        print("-" * 60)
        print(f"\nOutput files:")
        if txt_output:
            print(f"  * TSV/CSV file:   {txt_output}")
        if excel_output:
            print(f"  * Excel file: {excel_output}")
        
        # Display merged data
        print("\nStep 3: Reading merged data...")
        print("-" * 60)
        
        if txt_output:
            with open(txt_output, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter='\t')
                rows = list(reader)

                print(f"\nMerged data preview ({len(rows)-1} data rows + 1 header row):")
                print("\nHeader row:")
                print(f"  {rows[0]}")
                print("\nFirst few data rows:")
                for i, row in enumerate(rows[1:4], 1):
                    print(f"  {row}")
                if len(rows) > 4:
                    print(f"  ... and {len(rows) - 4} more rows")
        elif excel_output:
            try:
                import openpyxl
                wb = openpyxl.load_workbook(excel_output)
                ws = wb.active
                rows = list(ws.iter_rows(values_only=True))
                print(f"\nMerged data preview ({len(rows)-1} data rows + 1 header row):")
                print("\nHeader row:")
                print(f"  {list(rows[0])}")
                print("\nFirst few data rows:")
                for i, row in enumerate(rows[1:4], 1):
                    print(f"  {list(row)}")
                if len(rows) > 4:
                    print(f"  ... and {len(rows) - 4} more rows")
            except Exception:
                print("Could not read Excel preview (missing openpyxl).")
        else:
            print("No output file to preview.")
        
        print("\n" + "="*60)
        print("[OK] TEST COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        
        # Cleanup
        print("Cleaning up test files...")
        os.remove('test_customers.csv')
        os.remove('test_orders.csv')
        print("[OK] Cleanup complete")
        
        return 0
    
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        print("\nCleaning up test files...")
        for f in ['test_customers.csv', 'test_orders.csv']:
            if os.path.exists(f):
                os.remove(f)
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(test_merge())
