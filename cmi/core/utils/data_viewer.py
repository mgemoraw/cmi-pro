import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtCore import QAbstractTableModel, Qt


class PandasModel(QAbstractTableModel):
    def __init__(self, dataframe: pd.DataFrame):
        super().__init__()
        self._df = dataframe

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._df.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._df.columns[section]
            else:
                return str(self._df.index[section])
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Example DataFrame
    df = pd.read_excel("dozer_records.xlsx", header=5)

    model = PandasModel(df)

    table = QTableView()
    table.setModel(model)
    table.resize(800, 500)
    table.show()

    sys.exit(app.exec())
