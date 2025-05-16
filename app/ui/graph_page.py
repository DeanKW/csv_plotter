from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QMessageBox
from app.ui.widgets.graph_selector_widget import GraphSelectorWidget
from app.ui.widgets.plot_widget import PlotWidget

class GraphPage(QWidget):
    def __init__(self, data_model, parent=None):
        super().__init__(parent)
        self.data_model = data_model
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.graph_selector_widget = GraphSelectorWidget(self.data_model)
        layout.addWidget(self.graph_selector_widget)
        # Tab widget for multiple graphs
        self.graph_tabs = QTabWidget()
        layout.addWidget(self.graph_tabs)

        # Connect the graph button
        self.graph_selector_widget.graph_button.clicked.connect(self.plot_new_graph)

    def add_graph_tab(self, title=None):
        plot_widget = PlotWidget()
        self.graph_tabs.addTab(plot_widget, title)
        return plot_widget

    def plot_new_graph(self):
        graph_type = self.graph_selector_widget.graph_type
        x_col = self.graph_selector_widget.x_axis
        y_col = self.graph_selector_widget.y_axis
        filtered_data = self.data_model.get_filtered_data()
        
        current_tab = self.add_graph_tab(f"{graph_type} Plot")
        if graph_type in ["Scatter", "Line"]:
            current_tab.plot_data(filtered_data, plot_type=graph_type.lower(), x_col=x_col, y_col=y_col)
        elif graph_type == "Bar":
            current_tab.plot_data(filtered_data, plot_type="bar", x_col=x_col, y_col=y_col)
        elif graph_type == "Histogram":
            current_tab.plot_data(filtered_data, plot_type="histogram", x_col=x_col)
        else:
            QMessageBox.warning(self, f"{graph_type} is not yet implemented")
