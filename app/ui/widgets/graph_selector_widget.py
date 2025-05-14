from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton


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

        layout.addLayout(graph_type_layout)

    

if __name__ == "__main__":

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