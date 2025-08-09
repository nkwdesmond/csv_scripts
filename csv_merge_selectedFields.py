import os
import argparse
import csv
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(description="Merge CSV files and retain only specified fields.")
    parser.add_argument("-d", "--directory", required=True, help="Directory containing CSV files")
    parser.add_argument("-f", "--fields", required=True, help="Text file with fields to retain (one per line)")
    return parser.parse_args()

def read_fields(field_file):
    with open(field_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def merge_and_filter_csvs(directory, fields_to_keep):
    csv_files = list(Path(directory).glob("*.csv"))
    if not csv_files:
        print("❌ No CSV files found.")
        return

    output_file = Path(directory) / "filtered_merged_output.csv"
    total_rows = 0

    with open(output_file, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=fields_to_keep)
        writer.writeheader()

        for csv_file in csv_files:
            with open(csv_file, "r", encoding="utf-8") as fin:
                reader = csv.DictReader(fin)
                for row in reader:
                    filtered_row = {field: row.get(field, "") for field in fields_to_keep}
                    writer.writerow(filtered_row)
                    total_rows += 1
            print(f"✅ Processed: {csv_file.name}")

    print(f"\n✅ Merged {len(csv_files)} files with {total_rows} rows into: {output_file}")

def main():
    args = parse_arguments()
    fields_to_keep = read_fields(args.fields)
    if not fields_to_keep:
        print("❌ Field list is empty. Please provide a valid .txt file with field names.")
        return
    merge_and_filter_csvs(args.directory, fields_to_keep)

if __name__ == "__main__":
    main()