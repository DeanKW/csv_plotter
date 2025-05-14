from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt

class LabeledInput(QWidget):
    def __init__(self, label_text, input_widget, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.label = QLabel(label_text)
        self.input = input_widget
        self.label.setMinimumWidth(100)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    @property
    def value(self):
        if isinstance(self.input, QLineEdit):
            return self.input.text()
        elif isinstance(self.input, QComboBox):
            return self.input.currentText()
        # elif isinstance(self.input, QCheckBox):
        #    return self.input.isChecked()
      #  elif isinstance(self.input, QSlider):
       #     return self.input.value()
        return None