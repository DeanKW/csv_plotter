import sys
app_path='/home/dean/Documents/gitRepos/csv_plotter/app'
plotter_path='/home/dean/Documents/gitRepos/csv_plotter'
# Add the project root (one level up from /tests) to sys.path
sys.path.append(plotter_path)
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QTabWidget, QMenuBar, QAction, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
from app.model.data_model import DataModel
from app.ui.widgets.filter_widget import FilterWidget
from app.ui.widgets.graph_selector_widget import GraphSelectorWidget
from app.ui.widgets.plot_widget import PlotWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Plotter")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize the DataModel
        self.data_model = DataModel()

        self.init_ui()

    def init_ui(self):
        # Create the menu bar
        self.create_menu_bar()

        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Toolbar for graph selection
        self.graph_selector_widget = GraphSelectorWidget(self.data_model)
        self.graph_selector_widget.graph_button.clicked.connect(self.apply_filters_and_graph)

        # Splitter for filter and graph area
        splitter = QSplitter(Qt.Horizontal)

        # Left: Filter widget
        self.filter_widget = FilterWidget(self.data_model)
        splitter.addWidget(self.filter_widget)

        # Center: Graph area with tabs
        self.graph_tabs = QTabWidget()
        splitter.addWidget(self.graph_tabs)

        # Add splitter and toolbar to main layout
        main_layout.addWidget(self.graph_selector_widget)
        main_layout.addWidget(splitter)

        self.setCentralWidget(main_widget)

    def create_menu_bar(self):
        """Create the menu bar with File and Help menus."""
        menu_bar = QMenuBar(self)

        # File menu
        file_menu = menu_bar.addMenu("File")
        load_file_action = QAction("Load File", self)
        load_file_action.triggered.connect(self.load_file)
        file_menu.addAction(load_file_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        self.setMenuBar(menu_bar)

    def load_file(self):
        """Open a file dialog to load a CSV file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options
        )
        if file_path:
            self.data_model.load_csv(file_path)
            print(f"Loaded file: {file_path}")

            self.graph_selector_widget.fill_graph_options_from_data()  # Update graph options based on new data

            # Update filter widget with new data

    def apply_filters_and_graph(self):
        """Apply filters to the data and update the plots."""
        graph_type = self.graph_selector_widget.graph_type
        x_col = self.graph_selector_widget.x_axis
        y_col = self.graph_selector_widget.y_axis
        filtered_data = self.data_model.get_filtered_data()

        if graph_type in ["Scatter", "Line"]:
            current_tab = self.add_graph_tab(f"{graph_type} Plot")
            current_tab.plot_data(filtered_data, plot_type=graph_type.lower(), x_col=x_col, y_col=y_col)
        elif graph_type == "Bar":
            current_tab = self.add_graph_tab(f"{graph_type} Plot")
            current_tab.plot_data(filtered_data, plot_type="bar", x_col=x_col, y_col=y_col)
        elif graph_type == "Histogram":
            current_tab = self.add_graph_tab(f"{graph_type} Plot")
            current_tab.plot_data(filtered_data, plot_type="histogram", x_col=x_col)
        else:
            QMessageBox.warning(self, f"{graph_type} is not yet implemented")

    def add_graph_tab(self, title="Graph"):
        """Add a new tab for displaying a graph."""
        plot_widget = PlotWidget()
        self.graph_tabs.addTab(plot_widget, title)
        return plot_widget

    def show_about_dialog(self):
        """Show an about dialog."""
        QMessageBox.about(
            self,
            "About CSV Plotter",
            "CSV Plotter\nVersion 1.0\n\nA tool for visualizing CSV data with live filtering and plotting."
        )


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())