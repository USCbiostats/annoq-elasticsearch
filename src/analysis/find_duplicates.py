import argparse
import json
import csv
from collections import defaultdict

import pandas as pd

def group_columns(file_path):
    df = pd.read_csv(file_path, delimiter='\t', dtype=str)
    
    col_hashes = {col: hash(tuple(df[col])) for col in df.columns}
    
    groups = defaultdict(list)
    for col, col_hash in col_hashes.items():
        groups[col_hash].append(col)
    
    duplicate_groups = {f"group{i+1}": cols for i, cols in enumerate(groups.values()) if len(cols) > 1}

    return duplicate_groups


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str, help="Path to the TSV file.")
    
    args = parser.parse_args()
    result = group_columns(args.file_path)
    
    print(json.dumps(result, indent=4))
    

if __name__ == "__main__":
    main()