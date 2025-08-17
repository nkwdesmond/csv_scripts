import argparse
import os
import sqlite3
import json
import csv
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse JSON from table in .db files.")
    parser.add_argument("-d", "--directory", required=True, help="Directory containing .db files")
    parser.add_argument("table", help="Name of the table to extract JSON from (e.g., tbllog)")
    return parser.parse_args()

def extract_json_from_table(db_path, table_name):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]

        json_rows = []

        for row in rows:
            for value in row:
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, dict):
                        json_rows.append(parsed)
                    else:
                        json_rows.append({"value": parsed})
                except (json.JSONDecodeError, TypeError):
                    continue

        return json_rows

    except sqlite3.Error as e:
        print(f"Failed to parse {db_path}: {e}")
        return []
    finally:
        if conn:
            conn.close()

def write_to_csv(data, output_file):
    if not data:
        print(f"No JSON data found to write to {output_file}")
        return

    keys = set()
    for entry in data:
        keys.update(entry.keys())

    keys = sorted(keys)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved CSV: {output_file}")

def main():
    args = parse_arguments()

    db_files = Path(args.directory).glob("*.db")
    for db_file in db_files:
        print(f"Parsing: {db_file.name}")
        json_data = extract_json_from_table(db_file, args.table)

        if json_data:
            output_csv = db_file.with_suffix('.csv')
            write_to_csv(json_data, output_csv)
        else:
            print(f"No JSON data found in {db_file}")

if __name__ == "__main__":
    main()