from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QFileDialog, QComboBox, QListWidget, QCheckBox, QHBoxLayout, QListWidgetItem
from PyQt5.QtCore import Qt
import pandas as pd

class FilterWidget(QWidget):
    def __init__(self, data_model, parent=None):
        super().__init__(parent)
        self.data_model = data_model
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Column selection
        layout.addWidget(QLabel("Select Column:"))
        self.column_selector = QComboBox()
        self.column_selector.addItems(self.data_model.get_columns())
        self.column_selector.currentTextChanged.connect(self.update_filter_options)
        layout.addWidget(self.column_selector)

        # Filter options container
        self.filter_options_layout = QVBoxLayout()
        layout.addLayout(self.filter_options_layout)

        # Logical operator selection
        layout.addWidget(QLabel("Logical Operator:"))
        self.logical_operator_selector = QComboBox()
        self.logical_operator_selector.addItems(["AND", "OR", "XOR"])
        layout.addWidget(self.logical_operator_selector)

        # Apply filter button
        self.apply_filter_button = QPushButton("Apply Filters")
        self.apply_filter_button.clicked.connect(self.apply_filters)
        layout.addWidget(self.apply_filter_button)

        layout.addStretch()

        # Initialize filter options
        self.update_filter_options()

    def update_filter_options(self):
        """Update filter options based on the selected column's data type."""
        pass

   

    def apply_filters(self):
        """Apply filters to the data."""
        pass

if __name__ == "__main__":
    import sys
    import os
    from PyQt5.QtWidgets import QApplication

    
    plotter_path='/home/dean/Documents/gitRepos/csv_plotter'
    sample_csv = os.path.join(plotter_path, "samples", "example_data.csv")

    # Add the project root (one level up from /tests) to sys.path
    sys.path.append(plotter_path)
    from app.model.data_model import DataModel

    app = QApplication(sys.argv)
    data_model = DataModel()
    data_model.load_csv(sample_csv)  # Replace with actual CSV file path
    filter_widget = FilterWidget(data_model)
    filter_widget.show()
    sys.exit(app.exec_())