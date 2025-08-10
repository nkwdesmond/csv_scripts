import os
import sys
import pandas as pd
from pathlib import Path

def main():
    if len(sys.argv) != 3:
        print("Usage: python csv_extract_countryIPs.py <csv_folder_path> <country_code>")
        sys.exit(1)

    csv_directory = sys.argv[1]
    country_code = sys.argv[2].upper()  # normalize case

    # Create output folder named after country code
    output_dir = Path(csv_directory) / f"{country_code}_ips"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Sets for unique IPs
    src_addrs = set()
    dst_addrs = set()

    for filename in os.listdir(csv_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(csv_directory, filename)
            try:
                df = pd.read_csv(file_path, usecols=['SrcAddr', 'DstAddr', 'SrcCountry', 'DstCountry'])

                # Collect SrcAddr where SrcCountry matches
                src_addrs.update(
                    df.loc[df['SrcCountry'].str.upper() == country_code, 'SrcAddr']
                    .dropna()
                    .unique()
                )

                # Collect DstAddr where DstCountry matches
                dst_addrs.update(
                    df.loc[df['DstCountry'].str.upper() == country_code, 'DstAddr']
                    .dropna()
                    .unique()
                )

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Output file paths
    src_file = output_dir / "src_ips.txt"
    dst_file = output_dir / "dst_ips.txt"
    all_file = output_dir / "all_ips.txt"

    # Write src_ips.txt
    with open(src_file, "w") as f:
        for ip in sorted(src_addrs):
            f.write(ip + "\n")

    # Write dst_ips.txt
    with open(dst_file, "w") as f:
        for ip in sorted(dst_addrs):
            f.write(ip + "\n")

    # Write all_ips.txt
    all_addrs = src_addrs.union(dst_addrs)
    with open(all_file, "w") as f:
        for ip in sorted(all_addrs):
            f.write(ip + "\n")

    # Summary
    print(f"✅ Unique {country_code} SrcAddr: {len(src_addrs)} (saved to {src_file})")
    print(f"✅ Unique {country_code} DstAddr: {len(dst_addrs)} (saved to {dst_file})")
    print(f"✅ Total unique {country_code} IPs: {len(all_addrs)} (saved to {all_file})")

if __name__ == "__main__":
    main()