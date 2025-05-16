from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
import pandas as pd

# TODO: Review that this is done properly, I am not super familiar with the Model/View pattern, as
# GUIs are not my forte.  
class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self._df = df

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return str(self._df.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._df.columns[section])
            else:
                return str(self._df.index[section])
        return None

    def set_dataframe(self, df):
        self.beginResetModel()
        self._df = df
        self.endResetModel()

class TablePage(QWidget):
    def __init__(self, data_model, parent=None):
        super().__init__(parent)
        self.data_model = data_model
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.table_view = QTableView()
        self.model = PandasModel(self.data_model.get_filtered_data())
        self.table_view.setModel(self.model)
        layout.addWidget(self.table_view)

    # TBD if we need this?
    def update_table(self):
        self.model.set_dataframe(self.data_model.get_filtered_data())
