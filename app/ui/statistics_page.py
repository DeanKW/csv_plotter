from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTableWidget, \
    QTableWidgetItem, QGroupBox, QFormLayout, QScrollArea, QListWidget
import pandas as pd

class StatisticsPage(QWidget):
    def __init__(self, data_model, parent=None):
        super().__init__(parent)
        self.data_model = data_model
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.column_selector = QComboBox()
        self.column_selector.addItems(self.data_model.get_columns())
        self.column_selector.currentTextChanged.connect(self.update_stats)
        layout.addWidget(QLabel("Select column for statistics:"))
        layout.addWidget(self.column_selector)

        layout.addWidget(QLabel("Summary Statistics:"))
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.stats_container = QWidget()
        self.stats_layout = QFormLayout(self.stats_container)
        self.scroll_area.setWidget(self.stats_container)
        layout.addWidget(self.scroll_area)

        self.update_stats()

    def clear_stats(self, layout=None):
        """Recursively clear all widgets and layouts in the given layout."""
        if layout is None:
            layout = self.stats_layout
        while layout.count():
            item = layout.takeAt(0)

            # Remove widgets if present
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

            # Remove nested layouts
            sub_layout = item.layout()
            if sub_layout is not None:
                self.clear_stats(sub_layout)

    def update_stats(self):
        self.clear_stats()
        col = self.column_selector.currentText()
        df = self.data_model.get_filtered_data()

        if col and col in df.columns:
            series = df[col]
            if pd.api.types.is_numeric_dtype(series):
                self.stats_layout.addRow("Mean:", QLabel(str(series.mean())))
                self.stats_layout.addRow("Median:", QLabel(str(series.median())))
                self.stats_layout.addRow("Std Dev:", QLabel(str(series.std())))
                self.stats_layout.addRow("Min:", QLabel(str(series.min())))
                self.stats_layout.addRow("Max:", QLabel(str(series.max())))
                self.stats_layout.addRow("Count:", QLabel(str(series.count())))
            elif pd.api.types.is_categorical_dtype(series) or series.dtype == object:
                value_counts = series.value_counts()
                for val, count in value_counts.items():
                    self.stats_layout.addRow(str(val), QLabel(str(count)))

    
    def refresh_columns(self):
        self.column_selector.clear()
        self.column_selector.addItems(self.data_model.get_columns())
        #self.update_stats()
