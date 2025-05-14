from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

    def plot_data(self, data, plot_type="scatter", x_col=None, y_col=None):
        """Plot the given data."""
        ax = self.figure.add_subplot(111)
        ax.clear()

        if plot_type == "scatter":
            ax.scatter(data[x_col], data[y_col])
        elif plot_type == "line":
            ax.plot(data[x_col], data[y_col])
        elif plot_type == "bar":
            ax.bar(data[x_col], data[y_col])
        elif plot_type == "histogram":
            ax.hist(data[x_col])

        ax.set_title(f"{plot_type.capitalize()} Plot")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        self.canvas.draw()

if __name__ == "__main__":
    import sys
    import pandas as pd
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    plot_widget = PlotWidget()
    plot_widget.show()

    sample_data = {
        'x': [1, 2, 3, 4, 5],
        'y': [5, 4, 3, 2, 1]
    }
    df = pd.DataFrame(sample_data)
    plot_widget.plot_data(df, plot_type="scatter", x_col='x', y_col='y')
   # plot_widget.plot_data(df, plot_type="line", x_col='x', y_col='y')
   # plot_widget.plot_data(df, plot_type="bar", x_col='x', y_col='y')
   # plot_widget.plot_data(df, plot_type="histogram", x_col='x')
    sys.exit(app.exec_())
