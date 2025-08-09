import csv
import sys

def filter_csv(input_file, output_file, column_name, search_string):
    try:
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            if column_name not in reader.fieldnames:
                print(f"Error: Column '{column_name}' not found in the CSV.")
                return
            
            filtered_rows = [row for row in reader if search_string in row[column_name]]

        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(filtered_rows)

        print(f"Filtered CSV written to {output_file}. {len(filtered_rows)} rows matched.")
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python filter_csv_columnString.py <input_file> <output_file> <column_name> <search_string>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    column_name = sys.argv[3]
    search_string = sys.argv[4]

    filter_csv(input_file, output_file, column_name, search_string)
