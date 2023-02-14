import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLineEdit
from dataFrameModel import DataFrameModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table_view = QTableView(self)
        self.open_file_button = QPushButton("Open File")
        self.generate_csv_button = QPushButton("Generate File")
        self.generate_csv_button.setEnabled(False)
       
        

        layout = QVBoxLayout()
        layout.addWidget(self.open_file_button)
        layout.addWidget(self.table_view)
       
        layout.addWidget(self.generate_csv_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.open_file_button.clicked.connect(self.open_file_dialog)
        self.generate_csv_button.clicked.connect(self.generate_csv)
       
        

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            self.load_data(file_name)

        

    def load_data(self, file_name):
        self.df = pd.read_csv(file_name)
        self.df['Selected'] = False
        self.table_view.setModel(DataFrameModel(self.df))
        self.table_view.clicked.connect(self.select_cell)
        self.generate_csv_button.setEnabled(True)
        

    
        
    def select_cell(self, index):
        row = index.row()
        self.df.at[row, 'Selected'] = not self.df.at[row, 'Selected']
        self.table_view.model().dataChanged.emit(index, index)

    def generate_csv(self):
        selected_df = self.df[self.df['Selected'] == True]
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "CSV Files (*.csv);;All Files (*)")
        if file_name:
            selected_df.iloc[:,0].to_csv(file_name, index=False)
    
    
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
