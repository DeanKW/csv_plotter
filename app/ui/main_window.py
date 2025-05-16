import sys
app_path='/home/dean/Documents/gitRepos/csv_plotter/app'
plotter_path='/home/dean/Documents/gitRepos/csv_plotter'
# Add the project root (one level up from /tests) to sys.path
sys.path.append(plotter_path)
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QTabWidget, QMenuBar, QAction, QMessageBox, QFileDialog, QStackedWidget
from PyQt5.QtCore import Qt
from app.model.data_model import DataModel
from app.ui.widgets.filter_widget import FilterWidget
from app.ui.graph_page import GraphPage
from app.ui.table_page import TablePage
from app.ui.correlation_page import CorrelationPage


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

        # Splitter for filter and graph area
        splitter = QSplitter(Qt.Horizontal)

        # Left: Filter widget
        self.filter_widget = FilterWidget(self.data_model)
        splitter.addWidget(self.filter_widget)

        # QStackedWidget for pages
        self.stacked_widget = QStackedWidget()
        self.graph_page = GraphPage(self.data_model)
        self.table_page = TablePage(self.data_model)
        self.correlation_page = CorrelationPage(self.data_model)
        self.stacked_widget.addWidget(self.graph_page)
        self.stacked_widget.addWidget(self.table_page)
        self.stacked_widget.addWidget(self.correlation_page)
        splitter.addWidget(self.stacked_widget)

        # Add splitter to main layout
        main_layout.addWidget(splitter)

        self.setCentralWidget(main_widget)

        # Default to graph page
        self.stacked_widget.setCurrentWidget(self.graph_page)

        # Connect filter apply to table update
        self.filter_widget.apply_filter_button.clicked.connect(self.table_page.update_table)
        self.filter_widget.apply_filter_button.clicked.connect(self.correlation_page.refresh_correlation)

        self.filter_widget.reset_filters_callbacks.append(self.table_page.update_table)
        self.filter_widget.reset_filters_callbacks.append(self.correlation_page.refresh_correlation)

        # Maybe we want to connect it to the graph page too


    def create_menu_bar(self):
        """Create the menu bar with File, View, and Help menus."""

        menu_bar = QMenuBar(self)

        # File menu
        file_menu = menu_bar.addMenu("File")
        load_file_action = QAction("Load File", self)
        load_file_action.triggered.connect(self.load_file)
        file_menu.addAction(load_file_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu for switching pages
        view_menu = menu_bar.addMenu("View")
        graph_action = QAction("Graph Page", self)
        graph_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.graph_page))
        view_menu.addAction(graph_action)
        table_action = QAction("Table Page", self)
        table_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.table_page))
        view_menu.addAction(table_action)
        corr_action = QAction("Correlation / Analysis / Insights Page", self)
        corr_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.correlation_page))
        view_menu.addAction(corr_action)

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

            self.graph_page.graph_selector_widget.fill_graph_options_from_data()  # Update graph options based on new data
            self.table_page.update_table()  # Update table with new data
            self.correlation_page.refresh_correlation()

    def apply_filters_and_graph(self):
        """Apply filters to the data and update the plots."""
        graph_type = self.graph_page.graph_selector_widget.graph_type
        x_col = self.graph_page.graph_selector_widget.x_axis
        y_col = self.graph_page.graph_selector_widget.y_axis
        filtered_data = self.data_model.get_filtered_data()

        # TBD: Do we want to update plot?
        # If so, we need an update function in the graph page
        #self.graph_page.plot_widget.plot_data(filtered_data, plot_type=graph_type.lower(), x_col=x_col, y_col=y_col)

        # No need to call a table update function, as it is auto-updated because we are using a Model/View approach

    def show_about_dialog(self):
        """Show an about dialog."""
        QMessageBox.about(
            self,
            "About CSV Plotter",
            "CSV Plotter\nVersion 0.1.x\n\nA tool for visualizing CSV data with live filtering and plotting."
        )


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())