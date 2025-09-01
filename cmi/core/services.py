from openpyxl import Workbook, load_workbook
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO, StringIO
import os
import csv
from .models import Project, Engineer, Collector


class ProjectDataTemplateGenerator:
    """
    Generates Excel and CSV templates for different data types.
    """
    def __init__(self, data_type=None):
        self.data_type = data_type
        self.headers = self._get_headers()
    
    def _get_headers(self):
        """
        Maps data types to their corresponding headers.
        """
        headers_map = {
            'project': [field.name for field in Project._meta.fields if field.name != 'id'],
            'engineer': [field.name for field in Engineer._meta.fields if field.name != 'id'],
            'collector': [field.name for field in Collector._meta.fields if field.name != 'id']
        }
        return headers_map.get(self.data_type, [])
    
    def create_template(self, file_format='xlsx'):
        """
        Creates an Excel or CSV template with predefined headers.
        Returns a file-like object (BytesIO).
        """
        if not self.headers:
            raise ValueError("Invalid data type provided.")

        if file_format == 'xlsx':
            return self._create_xlsx_template()
        elif file_format == 'csv':
            return self._create_csv_template()
        else:
            raise ValueError("Unsupported file format. Use 'xlsx' or 'csv'.")
    
    def _create_xlsx_template(self):
        """
        Internal method to create an XLSX template.
        """
        wb = Workbook()
        ws = wb.active
        ws.title = self.data_type.capitalize() + " Template"
        ws.append(self.headers)
        
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output
    
    def _create_csv_template(self):
        """
        Internal method to create a CSV template.
        """
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(self.headers)
        
        output.seek(0)
        return output
    

class ProjectDataParser:
    """
    Parses data from uploaded Excel or CSV files.
    """
    def __init__(self, data_file: InMemoryUploadedFile, data_type=None):
        self.data_file = data_file
        self.data_type = data_type

    def parse(self):
        """
        Determines the file type and calls the appropriate parser.
        """
        file_ext = self.data_file.name.split('.')[-1].lower()

        if file_ext == 'xlsx':
            return self._parse_xlsx()
        elif file_ext == 'csv':
            return self._parse_csv()
        else:
            raise ValueError("Unsupported file type. Please upload a .xlsx or .csv file.")

    def _parse_xlsx(self):
        """
        Internal method to parse an XLSX file.
        Returns a list of dictionaries, with each dictionary representing a row.
        """
        try:
            workbook = load_workbook(self.data_file)
            sheet = workbook.active
            rows = sheet.iter_rows(min_row=2, values_only=True)
            headers = [cell.value for cell in sheet[1]]
            
            data = []
            for row in rows:
                if any(row):  # Check if the row is not completely empty
                    row_data = dict(zip(headers, row))
                    data.append(row_data)
            return data
        except Exception as e:
            raise ValueError(f"Error parsing XLSX file: {e}")

    def _parse_csv(self):
        """
        Internal method to parse a CSV file.
        Returns a list of dictionaries.
        """
        try:
            # Decode the file in-memory
            decoded_file = self.data_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            data = [row for row in reader]
            return data
        except Exception as e:
            raise ValueError(f"Error parsing CSV file: {e}")