import sys
import os
import Orange
import Orange.data
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output

from PyQt5.QtWidgets import (
    QTableWidgetItem, QTableWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QLineEdit, QPushButton, QWidget, QApplication, QPlainTextEdit
)
from PyQt5.QtGui import QDoubleValidator
from PyQt5 import uic, QtWidgets
from AnyQt.QtCore import Qt

class TableEditor(widget.OWWidget):
    name = "Table Editor"
    description = "Editing table elements and returning the edited datatable"
    icon = "icons/table_editor.png"

    dossier_du_script = os.path.dirname(os.path.abspath(__file__))
    input_data = None

    class Inputs:
        input_data = Input("Data", Orange.data.Table)

    class Outputs:
        data_out = Output("Data", Orange.data.Table)

    @Inputs.input_data
    def set_data(self, input_data):
        self.input_data = input_data

        # Print information about the data
        if input_data:
            # Fill the table with the data
            self.fill_table()

    def __init__(self):
        super().__init__()
        self.init_Ui()

    def init_Ui(self):
        # QT Management
        uic.loadUi(os.path.join(self.dossier_du_script, 'widget_designer/table_editor.ui'), self)

        self.table_widget = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.reset_button = self.findChild(QtWidgets.QPushButton, 'reset')
        self.validate_button = self.findChild(QtWidgets.QPushButton, 'validate')

        # Set size policies
        self.table_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Adjust the size of the table to fit contents
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.table_widget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Connect buttons to their actions
        self.reset_button.clicked.connect(self.reset_table)
        self.validate_button.clicked.connect(self.save_and_send)

        # Resize the table when the window is resized
        self.resizeEvent = self.on_resize

        # Connect cell double click to edit start
        self.table_widget.cellDoubleClicked.connect(self.start_editing)

    def on_resize(self, event):
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

    def reset_table(self):
        # Reset the table with the initial data
        self.fill_table()

    def fill_table(self):
        # Check if data is available
        if self.input_data:
            # Clear any previous data in the table
            self.table_widget.clear()

            # Get domain (column names)
            domain = self.input_data.domain
            column_names = [attr.name for attr in domain.attributes]
            meta_names = [meta.name for meta in domain.metas]

            # Get data (instance values) and metas
            data = self.input_data.X
            metas = self.input_data.metas

            # Set number of rows and columns
            num_rows = len(data)
            num_cols = len(column_names) + len(meta_names)

            # Set number of columns in the table
            self.table_widget.setColumnCount(num_cols)
            self.table_widget.setRowCount(num_rows)

            # Set column names in the table
            self.table_widget.setHorizontalHeaderLabels(column_names + meta_names)

            # Add data to the table
            for row_index, row_data in enumerate(data):
                for col_index, value in enumerate(row_data):
                    if isinstance(domain.attributes[col_index], Orange.data.DiscreteVariable):
                        combobox = QComboBox()
                        values = domain.attributes[col_index].values
                        combobox.addItems(values)
                        # Set current text based on the value
                        current_value = domain.attributes[col_index].str_val(value)
                        combobox.setCurrentText(current_value)
                        self.table_widget.setCellWidget(row_index, col_index, combobox)
                    elif isinstance(domain.attributes[col_index], Orange.data.ContinuousVariable):
                        line_edit = QLineEdit(str(value))
                        validator = QDoubleValidator()
                        line_edit.setValidator(validator)
                        self.table_widget.setCellWidget(row_index, col_index, line_edit)
                    else:
                        item = QTableWidgetItem(str(value))
                        self.table_widget.setItem(row_index, col_index, item)

            # Add meta data to the table
            if metas.shape[1] > 0:  # Ensure there are meta columns
                for row_index, row_data in enumerate(metas):
                    for meta_index, value in enumerate(row_data):
                        col_index = len(column_names) + meta_index
                        if meta_index < len(domain.metas):  # Ensure the index is within bounds
                            if isinstance(domain.metas[meta_index], Orange.data.DiscreteVariable):
                                combobox = QComboBox()
                                values = sorted(set(str(m) for m in metas[:, meta_index]))
                                combobox.addItems(values)
                                combobox.setCurrentText(str(value))
                                self.table_widget.setCellWidget(row_index, col_index, combobox)
                            else:
                                # Check if value is a long string to decide between QPlainTextEdit or QLineEdit
                                if len(str(value)) > 20:
                                    plain_text_edit = QPlainTextEdit(str(value))
                                    self.table_widget.setCellWidget(row_index, col_index, plain_text_edit)
                                else:
                                    line_edit = QLineEdit(str(value))
                                    self.table_widget.setCellWidget(row_index, col_index, line_edit)

            # Adjust the size of the table to fit contents
            self.table_widget.resizeColumnsToContents()
            self.table_widget.resizeRowsToContents()

    def start_editing(self, row, column):
        item = self.table_widget.item(row, column)
        if item is not None:
            self.table_widget.openPersistentEditor(item)

    # Override closeEvent to save changes
    def closeEvent(self, event):
        for row in range(self.table_widget.rowCount()):
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item is not None:
                    self.table_widget.closePersistentEditor(item)
        event.accept()

    def get_edited_data(self):
        edited_data = []

        for i in range(self.table_widget.rowCount()):
            row = []
            for j in range(self.table_widget.columnCount()):
                cell_widget = self.table_widget.cellWidget(i, j)
                if cell_widget and isinstance(cell_widget, QComboBox):
                    row.append(cell_widget.currentText())
                elif cell_widget and isinstance(cell_widget, QLineEdit):
                    row.append(cell_widget.text())
                elif cell_widget and isinstance(cell_widget, QPlainTextEdit):
                    row.append(cell_widget.toPlainText())
                else:
                    item = self.table_widget.item(i, j)
                    if item is not None:
                        row.append(item.text())
                    else:
                        row.append('')
            edited_data.append(row)
        return edited_data

    def save_and_send(self):
        edited_data = self.get_edited_data()

        # Retrieve domain names from the original table
        original_domain = self.input_data.domain
        attribute_names = [attr.name for attr in original_domain.attributes]
        meta_names = [meta.name for meta in original_domain.metas]

        attributes = []
        for column_idx, attribute_name in enumerate(attribute_names):
            values = set(row[column_idx] for row in edited_data)
            try:
                values = {float(value) for value in values}
                variable = Orange.data.ContinuousVariable(attribute_name)
            except ValueError:
                variable = Orange.data.DiscreteVariable(attribute_name, values=list(values))
            attributes.append(variable)

        metas = [Orange.data.StringVariable(meta) for meta in meta_names]

        # Create a new domain with the same meta attributes
        domain = Orange.data.Domain(attributes, metas=metas)

        # Create a new table with the edited data
        new_data = Orange.data.Table.from_list(domain, edited_data)

        # Send the edited data to the output
        self.Outputs.data_out.send(new_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    table_editor = TableEditor()
    table_editor.show()
    sys.exit(app.exec_())
