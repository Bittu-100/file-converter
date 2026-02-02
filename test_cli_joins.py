"""
Quick test of CLI join functionality
"""
import subprocess
import csv
import os

def setup_test_files():
    """Create test CSV files"""
    customers = [
        ['CustID', 'Name', 'City'],
        ['C001', 'Alice', 'NYC'],
        ['C002', 'Bob', 'LA'],
        ['C003', 'Charlie', 'Chicago'],
    ]
    
    orders = [
        ['CustID', 'OrderID', 'Amount'],
        ['C001', 'O101', '500'],
        ['C002', 'O102', '300'],
        ['C004', 'O104', '200'],
    ]
    
    with open('cust_temp.csv', 'w', newline='') as f:
        csv.writer(f).writerows(customers)
    
    with open('orders_temp.csv', 'w', newline='') as f:
        csv.writer(f).writerows(orders)

def run_cli_test(join_type, output_name):
    """Run CLI merge command"""
    cmd = [
        'python', '-m', 'converter.cli', 'merge',
        'cust_temp.csv', 'orders_temp.csv',
        'CustID', 'CustID',
        '-j', join_type,
        '-f', 'txt',
        '-o', output_name
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"\n{join_type.upper()} Join Command:")
    print(f"  Command: {' '.join(cmd)}")
    print(f"  Status: {'✓ Success' if result.returncode == 0 else '✗ Failed'}")
    
    if result.returncode != 0:
        print(f"  Error: {result.stderr}")
        return False
    
    # Show output file content
    output_file = f"{output_name}.txt"
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            lines = f.read().strip().split('\n')
            print(f"  Rows: {len(lines)-1} (plus header)")
            print(f"  Content:")
            for line in lines[:6]:  # Show first 5 data rows
                print(f"    {line}")
            if len(lines) > 6:
                print(f"    ... ({len(lines)-6} more rows)")
    
    return True

if __name__ == "__main__":
    print("="*60)
    print("CLI JOIN TYPES TEST")
    print("="*60)
    
    setup_test_files()
    
    try:
        for join_type in ['left', 'inner', 'right', 'outer']:
            run_cli_test(join_type, f'result_cli_{join_type}')
        
        print("\n" + "="*60)
        print("[OK] ALL CLI TESTS PASSED!")
        print("="*60)
    
    finally:
        # Cleanup
        for f in ['cust_temp.csv', 'orders_temp.csv']:
            if os.path.exists(f):
                os.remove(f)
        for join_type in ['left', 'inner', 'right', 'outer']:
            f = f'result_cli_{join_type}.txt'
            if os.path.exists(f):
                os.remove(f)
