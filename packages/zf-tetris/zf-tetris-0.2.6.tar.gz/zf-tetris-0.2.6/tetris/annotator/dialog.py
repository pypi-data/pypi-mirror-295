from PyQt5.QtWidgets import (QColorDialog, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QHBoxLayout,
                             QLabel, QLineEdit, QListWidget, QPushButton,
                             QTextEdit, QVBoxLayout)


class AnnotationInputDialog(QDialog):
    def __init__(self, parent=None, text_zone=None):
        super().__init__(parent)
        self.setWindowTitle("Annotation Input")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.title_input = QLineEdit(self)
        self.title_input.setMinimumWidth(350)
        form_layout.addRow("Title:", self.title_input)

        self.description_input = QTextEdit(self)
        self.description_input.setMinimumWidth(350)
        self.description_input.setMinimumHeight(100)
        form_layout.addRow("Description:", self.description_input)

        self.font_family_input = QComboBox(self)
        self.font_family_input.addItems(["Arial", "Helvetica", "Impact", "Times New Roman", "Courier", "Verdana"])
        self.font_family_input.setCurrentText("Arial")
        form_layout.addRow("Font Family:", self.font_family_input)

        self.font_size_input = QComboBox(self)
        self.font_size_input.addItems([str(i) for i in range(8, 73, 2)])
        self.font_size_input.setCurrentText("32")
        form_layout.addRow("Font Size:", self.font_size_input)

        self.font_color_button = QPushButton("Select Color")
        self.font_color_button.clicked.connect(self.select_color)
        self.font_color = "#000000"
        self.font_color_button.setStyleSheet(f"background-color: {self.font_color};")
        form_layout.addRow("Font Color:", self.font_color_button)

        layout.addLayout(form_layout)

        examples_layout = QVBoxLayout()
        examples_label = QLabel("Examples:")
        examples_layout.addWidget(examples_label)

        self.examples_list = QListWidget(self)
        self.examples_list.setMinimumWidth(350)
        self.examples_list.setMinimumHeight(100)
        examples_layout.addWidget(self.examples_list)

        example_input_layout = QHBoxLayout()
        self.example_input = QLineEdit(self)
        example_input_layout.addWidget(self.example_input)
        add_example_button = QPushButton("Add")
        add_example_button.clicked.connect(self.add_example)
        example_input_layout.addWidget(add_example_button)
        examples_layout.addLayout(example_input_layout)

        layout.addLayout(examples_layout)

        if text_zone:
            self.title_input.setText(text_zone.title)
            self.description_input.setText(text_zone.description)
            self.font_family_input.setCurrentText(text_zone.font_family)
            self.font_size_input.setCurrentText(str(text_zone.font_size))
            self.font_color = text_zone.font_color
            self.font_color_button.setStyleSheet(f"background-color: {self.font_color};")
            for example in text_zone.examples:
                self.examples_list.addItem(example)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def add_example(self):
        example = self.example_input.text().strip()
        if example:
            self.examples_list.addItem(example)
            self.example_input.clear()

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.font_color = color.name()
            self.font_color_button.setStyleSheet(f"background-color: {self.font_color};")

    def get_inputs(self):
        examples = [
            self.examples_list.item(i).text() for i in range(self.examples_list.count())
        ]
        return (
            self.title_input.text(),
            self.description_input.toPlainText(),
            examples,
            self.font_family_input.currentText(),
            int(self.font_size_input.currentText()),
            self.font_color
        )

