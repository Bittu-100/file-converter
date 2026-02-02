"""
Advanced merge functionality for combining multiple files
"""

import csv
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from .core import FileConverter


class FileMerger:
    """Merge multiple files into one"""
    
    def __init__(self):
        self.converter = FileConverter()
    
    def merge_two_files(self, file1: str, file2: str, column1: str, column2: str,
                        output_base: str = None, output_format: str = 'xlsx',
                        join_type: str = 'left') -> list:
        """
        Merge two files on specified columns using specified join type
        (supports: left, right, inner, outer)
        
        Args:
            file1: Path to first file
            file2: Path to second file
            column1: Column name(s) in file1 to merge on (comma-separated for multi-column)
            column2: Column name(s) in file2 to merge on (comma-separated for multi-column)
            output_base: Optional base name for output files. If not provided, 
                        generates from file1 and file2 names
            output_format: One of 'xlsx', 'csv', 'txt', or 'both' (default 'xlsx')
            join_type: Type of join - 'left', 'right', 'inner', 'outer' (default 'left')
        
        Returns:
            List of output file paths generated
        """
        # Generate output base name if not provided
        if output_base is None:
            file1_base = Path(file1).stem
            file2_base = Path(file2).stem
            output_base = f"merged_{file1_base}_{file2_base}"
        
        # Use the converter's merge method with join type
        outputs = self.converter.merge_files(file1, file2, column1, column2,
                                             output_base=output_base,
                                             output_format=output_format,
                                             join_type=join_type)

        # Print summary message
        print(f"\n[OK] Successfully merged files. Outputs created: {outputs}")

        return outputs
    
    def merge_files(self, 
                   input_files: List[str], 
                   output_file: str,
                   merge_key: str = None,
                   operation: str = 'concat') -> str:
        """
        Merge multiple files
        
        Args:
            input_files: List of input file paths
            output_file: Output file path
            merge_key: Column to merge on (for join operations)
            operation: 'concat' (default), 'join' (merge on key), or 'union'
        
        Returns:
            Success message
        """
        if not input_files:
            raise ValueError("No input files provided")
        
        if operation == 'concat':
            return self._concat_files(input_files, output_file)
        elif operation == 'join' and merge_key:
            return self._join_files(input_files, output_file, merge_key)
        elif operation == 'union':
            return self._union_files(input_files, output_file)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    def _concat_files(self, input_files: List[str], output_file: str) -> str:
        """Concatenate files vertically"""
        all_data = []
        
        for file_path in input_files:
            print(f"Reading {file_path}...")
            data = self.converter.read_file(file_path)
            all_data.extend(data)
        
        if not all_data:
            raise ValueError("No data in any input files")
        
        output_ext = Path(output_file).suffix.lower().lstrip('.')
        
        if output_ext == 'csv':
            self.converter._write_csv(all_data, output_file, ',')
        elif output_ext == 'json':
            self.converter._write_json(all_data, output_file)
        elif output_ext in ['xlsx', 'xls']:
            self.converter._write_excel(all_data, output_file)
        
        return f"[OK] Merged {len(input_files)} files ({len(all_data)} total records) -> {output_file}"
    
    def _join_files(self, input_files: List[str], output_file: str, merge_key: str) -> str:
        """Merge files on a common key"""
        if len(input_files) < 2:
            raise ValueError("At least 2 files needed for join operation")
        
        # Read first file
        result = self.converter.read_file(input_files[0])
        
        # Join with remaining files
        for file_path in input_files[1:]:
            print(f"Joining with {file_path} on '{merge_key}'...")
            data = self.converter.read_file(file_path)
            
            # Create lookup dict
            lookup = {str(row.get(merge_key)): row for row in data}
            
            # Join records
            for row in result:
                key = str(row.get(merge_key))
                if key in lookup:
                    row.update(lookup[key])
        
        output_ext = Path(output_file).suffix.lower().lstrip('.')
        
        if output_ext == 'csv':
            self.converter._write_csv(result, output_file, ',')
        elif output_ext == 'json':
            self.converter._write_json(result, output_file)
        elif output_ext in ['xlsx', 'xls']:
            self.converter._write_excel(result, output_file)
        
        return f"[OK] Joined {len(input_files)} files -> {output_file}"
    
    def _union_files(self, input_files: List[str], output_file: str) -> str:
        """Union unique records from files"""
        all_data = []
        seen = set()
        
        for file_path in input_files:
            print(f"Reading {file_path}...")
            data = self.converter.read_file(file_path)
            
            for row in data:
                row_tuple = tuple(sorted(row.items()))
                if row_tuple not in seen:
                    seen.add(row_tuple)
                    all_data.append(row)
        
        if not all_data:
            raise ValueError("No unique data in any input files")
        
        output_ext = Path(output_file).suffix.lower().lstrip('.')
        
        if output_ext == 'csv':
            self.converter._write_csv(all_data, output_file, ',')
        elif output_ext == 'json':
            self.converter._write_json(all_data, output_file)
        elif output_ext in ['xlsx', 'xls']:
            self.converter._write_excel(all_data, output_file)
        
        return f"[OK] Union of {len(input_files)} files ({len(all_data)} unique records) -> {output_file}"

    def merge_with_reference(self, reference_file: str, input_files: list = None,
                            ref_column: str = None, input_column: str = None,
                            output_dir: str = 'merged_results',
                            output_format: str = 'xlsx',
                            join_type: str = 'left',
                            file_pattern: str = None,
                            search_dirs: list = None) -> list:
        """
        Merge multiple files with a single reference file (one-to-many merge)
        
        Each input file is merged separately with the reference file, producing one result per input file.
        
        Args:
            reference_file: Path to the reference file to merge with
            input_files: List of file paths to merge (use None if using file_pattern or search_dirs)
            ref_column: Column name in reference file to merge on (comma-separated for multi-column)
            input_column: Column name in input files to merge on (comma-separated for multi-column)
            output_dir: Directory to save results (default: 'merged_results')
            output_format: One of 'xlsx', 'csv', 'txt', or 'both'
            join_type: Type of join - 'left', 'right', 'inner', 'outer'
            file_pattern: Optional glob pattern to find files (e.g., '*.csv', '**/*.xlsx')
            search_dirs: Optional list of directories to search for files
        
        Returns:
            List of output file paths created
        
        Examples:
            # Merge specific files with reference
            outputs = merger.merge_with_reference(
                'reference.csv',
                ['file1.csv', 'file2.csv', 'file3.csv'],
                ref_column='ID',
                input_column='ID'
            )
            
            # Merge all CSVs in directory with reference
            outputs = merger.merge_with_reference(
                'reference.csv',
                file_pattern='*.csv',
                ref_column='ID',
                input_column='ID'
            )
            
            # Merge all CSVs from multiple directories with reference
            outputs = merger.merge_with_reference(
                'reference.csv',
                ref_column='ID',
                input_column='ID',
                search_dirs=['dir1/', 'dir2/', 'dir3/']
            )
        """
        outputs = self.converter.merge_files_with_reference(
            reference_file=reference_file,
            input_files=input_files or [],
            ref_column=ref_column,
            input_column=input_column,
            output_dir=output_dir,
            output_format=output_format,
            join_type=join_type,
            file_pattern=file_pattern,
            search_dirs=search_dirs
        )
        
        print(f"\n[OK] Merge-to-reference complete. {len(outputs)} result files created.")
        return outputs

    def get_files_from_dirs(self, directories: list, pattern: str = '*.csv',
                           recursive: bool = False) -> list:
        """
        Find files in specified directories
        
        Args:
            directories: List of directory paths to search
            pattern: File pattern (e.g., '*.csv', '*.xlsx')
            recursive: If True, search recursively in subdirectories
        
        Returns:
            List of file paths found
        """
        return self.converter.get_files_from_directories(directories, pattern, recursive)
