
# from .instance_parser import InstanceDataParser
from instance_summary_parser import InstanceSummaryParser
from equipment_forms_parser import EquipmentFormsParser
from labor_forms_parser import LaborFormParser

import os


# folder containing .xlsx files
def read_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing {file_path}")

            # load workbook
            if 'labour' in filename or "labor" in filename:
                parser = LaborFormParser(file_path)
                data = parser.parse()
                print("\n", data)

                print(f"... parsed labor data {file_path}")
                # return data
            
            elif "truck" in filename or "dozer" in filename or "excavator" in filename:
                parser = EquipmentFormsParser(file_path)
                data = parser.parse()
                print("\n", data)
                print(f"... parsed equipment data {file_path}")

                # return data
            else:
                continue
                raise ValueError("Form is not compatible")
    
    return None


if __name__ == "__main__":
    read_files("./")