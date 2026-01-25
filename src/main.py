import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from data.db_connection import DatabaseConnection

def main():
    app = QApplication(sys.argv)
    db = DatabaseConnection('Server', 'Database', 'UID', 'PWD')
    connection = db.connect()
    if connection:
        print("Connection successful")
    else:
        print("Connection failed")

    main_window = QMainWindow()
    main_window.setWindowTitle("English Center Manager")
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()