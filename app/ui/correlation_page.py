from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem
import pandas as pd

class CorrelationPage(QWidget):
    def __init__(self, data_model, parent=None):
        super().__init__(parent)
        self.data_model = data_model
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Correlation Matrix (numeric columns only):"))
        self.corr_table = QTableWidget()
        layout.addWidget(self.corr_table)
        self.update_correlation()

    def update_correlation(self):
        df = self.data_model.get_filtered_data().select_dtypes(include='number')
        corr = df.corr()
        self.corr_table.setRowCount(len(corr))
        self.corr_table.setColumnCount(len(corr))
        self.corr_table.setHorizontalHeaderLabels(corr.columns)
        self.corr_table.setVerticalHeaderLabels(corr.index)
        for i, row in enumerate(corr.index):
            for j, col in enumerate(corr.columns):
                item = QTableWidgetItem(f"{corr.loc[row, col]:.2f}")
                self.corr_table.setItem(i, j, item)

    def refresh_correlation(self):
        self.update_correlation()
