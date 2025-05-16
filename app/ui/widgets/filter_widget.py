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
        # Might need to check if row is valid in the future
        #if row < len(self.filters):
        filter_widgets = self.filters[row]
        column_selector = filter_widgets["column_selector"]
        filter_options_layout = filter_widgets["filter_options_layout"]

        # Clear existing filter options

        # Count() returns the number of items in the layout
        # This is equivalent to len(filter_options_layout)
        # Using count because it's the PyQt way to get the number of items in a layout
        while filter_options_layout.count():
            # takeAt() returns the item at the given index and removes it from the layout
            child = filter_options_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        selected_column = column_selector.currentText()
        if selected_column:
            column_data = self.data_model.raw_df[selected_column]
            if pd.api.types.is_numeric_dtype(column_data):
                self.add_numeric_filter_options(filter_options_layout)
            elif pd.api.types.is_categorical_dtype(column_data) or column_data.dtype == object:
                self.add_categorical_filter_options(filter_options_layout, column_data)
            # Add more data type checks as needed

    def add_numeric_filter_options(self, layout):
        """Add filter options for numeric columns."""
        layout.addWidget(QLabel("Min Value:"))
        min_value_input = QLineEdit()
        layout.addWidget(min_value_input)

        layout.addWidget(QLabel("Max Value:"))
        max_value_input = QLineEdit()
        layout.addWidget(max_value_input)

    def add_categorical_filter_options(self, layout, column_data):
        """Add filter options for categorical columns."""
        layout.addWidget(QLabel("Select Categories:"))
        category_list = QListWidget()
        category_list.setSelectionMode(QListWidget.MultiSelection)
        unique_values = column_data.dropna().unique()
        for value in unique_values:
            item = QListWidgetItem(str(value))
            item.setCheckState(Qt.Unchecked)
            category_list.addItem(item)
        layout.addWidget(category_list)

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