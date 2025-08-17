# csv_filter_columnString.py
Take a CSV as input and outputs a CSV with only entries that contain a specific string in a given column.<br><br>
Usage: `python csv_filter_columnString.py <input_file> <output_file> <column_name> <search_string>`

# csv_merge_selectedFields.py
Merge CSVs in a directory, retaining only fields (columns) specified in a txt file.<br><br>
Usage: `python csv_merge_selectedFields.py -d ./csv_folder -f fields.txt`

# csv_extract_countryIPs.py
Extract unique IPs belonging to a specified country from CSVs in a directory.<br>
Both IP and country information must be available in the CSV files.<br><br>
Usage: `python csv_extract_countryIPs.py <csv_folder_path> <country_code>`

# csv_merge.py
Merge CSVs in a directory.<br><br>
Usage: `python csv_merge.py -d ./csv_folder`

# parse_jsonInDbFile.py
Scan a directory for .db (SQLite) files, extract JSON data from a specified table, write the extracted JSON into CSVs.<br><br>
Usage: `python parse_jsonInDbFile.py -d ./db_folder <table>`
