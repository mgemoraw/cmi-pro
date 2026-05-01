
from config import CONFIG
from xlsx_processor import ExcelProcessor
from pathlib import Path
import os
import zipfile
from openpyxl import load_workbook
from xlsx_processor import ExcelProcessor, get_args, get_excel_files
from config import CONFIG

def main():
    args = get_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    template_path = Path(args.template)

    files = get_excel_files(input_dir)

    print(f"Found {len(files)} files")

    processor = ExcelProcessor(template_path, CONFIG)

    outputs = processor.process_files(files, output_dir)

    zip_file = processor.zip_outputs(outputs)

    print(f"Done. Output zip: {zip_file}")


# if __name__ == "__main__":
#     main()

processor = ExcelProcessor(
    template_path="target_template.xlsx",
    config=CONFIG
)

source_files = [
    "input1.xlsx",
    "input2.xlsx"
]

# Step 1: process
outputs = processor.process_files(source_files, "outputs")

# Step 2: zip
zip_file = processor.zip_outputs(outputs)

print("Generated:", zip_file)
