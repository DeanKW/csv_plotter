from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QFileDialog, QComboBox, QListWidget, QCheckBox, QHBoxLayout, QListWidgetItem, QScrollArea, QGridLayout
from PyQt5.QtCore import Qt
import pandas as pd
from ui.widgets.generic_widgets import LabeledInput

class FilterWidget(QWidget):
    def __init__(self, data_model, parent=None):
        super().__init__(parent)
        self.data_model = data_model
        self.filters = []  # Store filter widgets
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Scrollable area for filters
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.filter_container = QWidget()
        self.filter_layout = QGridLayout(self.filter_container)
        self.scroll_area.setWidget(self.filter_container)
        layout.addWidget(self.scroll_area)

        # Add filter button
        self.add_filter_button = QPushButton("Add Filter")
        self.add_filter_button.clicked.connect(self.add_filter)
        layout.addWidget(self.add_filter_button)

        # Apply filter button
        self.apply_filter_button = QPushButton("Apply Filters")
        self.apply_filter_button.clicked.connect(self.apply_filters)
        layout.addWidget(self.apply_filter_button)

        layout.addStretch()

    def add_filter(self):
        """Add a new filter section."""
        row = len(self.filters)

        # Column selector
        column_selector = QComboBox()
        column_selector.addItems(self.data_model.get_columns())
        column_selector.currentTextChanged.connect(lambda: self.update_filter_options(row))
        self.filter_layout.addWidget(column_selector, row, 0)

        # Filter options container
        filter_options = QWidget()
        filter_options_layout = QVBoxLayout(filter_options)
        self.filter_layout.addWidget(filter_options, row, 1)

        # Logical operator selector
        logical_operator = QComboBox()
        logical_operator.addItems(["AND", "OR"])
        self.filter_layout.addWidget(logical_operator, row, 2)

        # Remove filter button
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.remove_filter(row))
        self.filter_layout.addWidget(remove_button, row, 3)

        # Store filter components
        self.filters.append({
            "column_selector": column_selector,
            "filter_options": filter_options,
            "filter_options_layout": filter_options_layout,
            "logical_operator": logical_operator,
            "remove_button": remove_button
        })

    def remove_filter(self, row):
        """Remove a filter section."""
        print('STUB: Removing filter at row:', row)

    def update_filter_options(self, row):
        print('STUB: Updating filter options for row:', row)

    def apply_filters(self):
        """Apply all filters to the data model."""
        print('STUB: Applying filters to data model')

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