from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from ui.widgets.generic_widgets import LabeledInput

class GraphSelectorWidget(QWidget):
    def __init__(self, data_model, parent=None):
        super().__init__(parent)
        self.data_model = data_model
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Graph type selection
        graph_type_layout = QHBoxLayout()
        self.graph_type_combo = QComboBox()
        self.graph_type_combo.addItems(["Scatter", "Line", "Bar", "Histogram"])
        self.graph_button = QPushButton("Graph")
        graph_type_layout.addWidget(QLabel("Graph Type:"))
        graph_type_layout.addWidget(self.graph_type_combo)
        graph_type_layout.addWidget(self.graph_button)

        # Dynamic options widget
        self.graph_options_widget = QWidget()
        self.graph_options_layout = QVBoxLayout(self.graph_options_widget)

        self._add_plot_options()
        self.fill_graph_options_from_data()
        self.update_graph_options()  # Initialize with the default graph type

        # Connect graph type selection to update options
        self.graph_type_combo.currentTextChanged.connect(self.update_graph_options)

        layout.addLayout(graph_type_layout)
        layout.addWidget(self.graph_options_widget)

    def _add_plot_options(self):
        """Add plot options."""
        # Scatter and line plot options

        self.x_axis_combo = LabeledInput("X-Axis:", QComboBox())
        self.y_axis_combo = LabeledInput("Y-Axis:", QComboBox())

        self.graph_options_layout.addWidget(self.x_axis_combo)
        self.graph_options_layout.addWidget(self.y_axis_combo)

        # Bar plot options
        self.category_combo = LabeledInput("Category:", QComboBox())
        self.value_combo = LabeledInput("Value:", QComboBox())

        self.graph_options_layout.addWidget(self.category_combo)
        self.graph_options_layout.addWidget(self.value_combo)

        # Histogram plot options
        self.column_combo = LabeledInput("Column:", QComboBox())
        self.graph_options_layout.addWidget(self.column_combo)

    def fill_graph_options_from_data(self):
        """Fill the graph options based on the loaded data."""
        if self.data_model.raw_df is not None:
            columns = self.data_model.raw_df.columns
            self.x_axis_combo.input.clear()
            self.y_axis_combo.input.clear()
            self.category_combo.input.clear()
            self.value_combo.input.clear()
            self.column_combo.input.clear()

            self.x_axis_combo.input.addItems(columns)
            self.y_axis_combo.input.addItems(columns)
            self.category_combo.input.addItems(columns)
            self.value_combo.input.addItems(columns)
            self.column_combo.input.addItems(columns)

    def update_graph_options(self):
        """Update the graph options widget based on the selected graph type."""
        choice = self.graph_type_combo.currentText()
        self.x_axis_combo.setVisible(choice in ["Scatter", "Line"])
        self.y_axis_combo.setVisible(choice in ["Scatter", "Line"])

        self.category_combo.setVisible(choice == "Bar")
        self.value_combo.setVisible(choice == "Bar")

        self.column_combo.setVisible(choice == "Histogram")
        self.graph_options_widget.setVisible(choice in ["Scatter", "Line", "Bar", "Histogram"])

if __name__ == "__main__":
    # This is a test script to run the GraphSelectorWidget independently
    # and visualize its functionality without the full application context.

    # To run this script, use the command:
    # python -m app.ui.widgets.graph_selector_widget

    import sys
    import os
    app_path='/home/dean/Documents/gitRepos/csv_plotter/app'
    plotter_path='/home/dean/Documents/gitRepos/csv_plotter'

    sample_csv = os.path.join(plotter_path, "samples", "example_data.csv")
    # Add the project root (one level up from /tests) to sys.path
    sys.path.append(plotter_path)

    from PyQt5.QtWidgets import QApplication
    from app.model.data_model import DataModel

    app = QApplication([])
    data_model = DataModel()
    data_model.load_csv(sample_csv)
    graph_selector_widget = GraphSelectorWidget(data_model)
    graph_selector_widget.show()
    app.exec_()