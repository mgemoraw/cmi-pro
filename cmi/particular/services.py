import csv
from io import TextIOWrapper
# import pandas as pd
from openpyxl import load_workbook
from . models import Particular, Task, Division


class GridDataParser:
    def __init__(self, file, file_format):
        self.file = file
        self.format = file_format.lower()

    def parse(self):
        """Main method to parse the file based on its format."""
        if self.format == 'csv':
            return self.parse_csv()
        elif self.format in ('xlsx', 'xls'):
            return self.parse_xlsx()
        else:
            raise ValueError(f"Unsupported file format: {self.format}")

    def parse_csv(self):
        """Parse CSV file into a list of rows (lists)."""
        try:
            # Try UTF-8 first
            file_data = TextIOWrapper(self.file.file, encoding='utf-8', errors='replace')
            reader = csv.reader(file_data)
            rows = [row for row in reader]
        except Exception as e:
            raise ValueError(f"Error parsing CSV: {e}")
        return rows

    def parse_xlsx(self):
        """Parse XLSX file into a list of rows (lists)."""
        try:
            wb = load_workbook(self.file.file, data_only=True)
            sheet = wb.active  # You can customize which sheet to use
            rows = [[cell for cell in row] for row in sheet.iter_rows(values_only=True)]
        except Exception as e:
            raise ValueError(f"Error parsing XLSX: {e}")
        return rows
