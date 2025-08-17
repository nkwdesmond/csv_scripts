import os
import argparse
import csv
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(description="Merge all CSV files in a directory.")
    parser.add_argument("-d", "--directory", required=True, help="Directory containing CSV files")
    return parser.parse_args()

def merge_csv_files(directory):
    csv_files = list(Path(directory).glob("*.csv"))
    if not csv_files:
        print("No CSV files found in the directory.")
        return

    output_file = Path(directory) / "merged_output.csv"
    header_written = False

    with open(output_file, "w", newline="", encoding="utf-8") as fout:
        writer = None

        for csv_file in csv_files:
            with open(csv_file, "r", newline="", encoding="utf-8") as fin:
                reader = csv.DictReader(fin)
                if not reader.fieldnames:
                    continue  # Skip empty files

                if not header_written:
                    writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    header_written = True

                for row in reader:
                    writer.writerow(row)

            print(f"Merged: {csv_file.name}")

    print(f"\n✅ All CSVs merged into: {output_file}")

def main():
    args = parse_arguments()
    merge_csv_files(args.directory)

if __name__ == "__main__":
    main()