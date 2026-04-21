import pandas as pd
from pathlib import Path


class DataParser:
    def __init__(self, path: str | None = None, sheet: str | int | None = 0):
        self._path = Path(path) if path else None
        self._sheet = sheet
        self._dataframe = None

    def load(self, path: str | None = None):
        """
        Load Excel file into pandas DataFrame
        """
        if path:
            self._path = Path(path)

        if not self._path:
            raise ValueError("File path must be provided")

        self._dataframe = pd.read_excel(
            self._path,
            sheet_name=self._sheet,
            engine="openpyxl"
        )

        return self

    def get_dataframe(self) -> pd.DataFrame:
        if self._dataframe is None:
            raise ValueError("No data loaded. Call load() first.")
        return self._dataframe

    def to_dict(self):
        """
        Convert DataFrame to list of dicts
        """
        return self.get_dataframe().to_dict(orient="records")

    def preview(self, rows: int = 5):
        return self.get_dataframe().head(rows)



if __name__ == "__main__":
	parser = DataParser(path="dozer_records.xlsx")
	parser.load()
	print(parser.preview())
	data = parser.to_dict()
	print("\n######## Data ######")
	# print(data)