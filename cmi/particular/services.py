from io import TextIOWrapper
import csv


def parse_csv_file(file_data):
    reader = csv.reader(file_data)

    for row in reader:
        # Example: process CSV data here
        print(row)  # Replace with saving to database logic

    return 0