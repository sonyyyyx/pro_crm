from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QMessageBox, QFileDialog, QDialog, QLabel
)

from controllers.client_controller import ClientController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.search_input = QLineEdit()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.table = QTableWidget()
        self.setWindowTitle("CRM система")
        self.setGeometry(100, 100, 1200, 600)

        self.controller = ClientController()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        # Table
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Имя", "Email", "Телефон"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
        # fld_for_search
        search_layout = QHBoxLayout()
        self.search_input.setPlaceholderText("Поиск по имени, email и телефону")
        search_button = QPushButton("Поиск")
        search_button.clicked.connect(self.search_clients)
        clear_button = QPushButton("Очистить выбор")
        clear_button.clicked.connect(self.clear_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(clear_button)
        layout.addLayout(search_layout)

        # add cleint
        form_layout = QHBoxLayout()
        self.name_input.setPlaceholderText("Имя")
        self.email_input.setPlaceholderText("Email")
        self.phone_input.setPlaceholderText("Телефон")
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.phone_input)

        add_button = QPushButton("Добавить клиента")
        add_button.clicked.connect(self.add_client)
        form_layout.addWidget(add_button)

        layout.addLayout(form_layout)

        # but_control
        buttons_layout = QHBoxLayout()
        delete_button = QPushButton("Удалить клиента")
        delete_button.clicked.connect(self.delete_client)
        buttons_layout.addWidget(delete_button)

        update_button = QPushButton("Обновить клиента")
        update_button.clicked.connect(self.update_client)
        buttons_layout.addWidget(update_button)
        export_button = QPushButton("Экспортировать таблицу CSV")
        export_button.clicked.connect(self.export_to_csv)
        import_button = QPushButton("Импортировать таблицу CSV")
        import_button.clicked.connect(self.import_from_csv)

        buttons_layout.addWidget(export_button)
        buttons_layout.addWidget(import_button)
        about_button = QPushButton("Об авторе")
        about_button.clicked.connect(self.show_about_dialog)  # Подключаем обработчик
        buttons_layout.addWidget(about_button)

        layout.addLayout(buttons_layout)

        central_widget.setLayout(layout)

        self.load_data()

    def load_data(self):
        clients = self.controller.get_clients()
        self.table.setRowCount(0)
        for row_number, client in enumerate(clients):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(client):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_client(self):
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()

        if not name or not email or not phone:
            QMessageBox.warning(self, "Ошибка", "Вы не правильно ввели данные")
            return

        self.controller.add_client(name, email, phone)
        self.name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.load_data()

    def delete_client(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Не выбран клиент")
            return

        client_id = self.table.item(selected_row, 0).text()
        self.controller.delete_client(client_id)
        self.load_data()

    def update_client(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Не выбран клиент")
            return

        client_id = self.table.item(selected_row, 0).text()
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()

        if not name or not email or not phone:
            QMessageBox.warning(self, "Ошибка", "Вы не правильно ввели данные")
            return

        self.controller.update_client(client_id, name, email, phone)
        self.name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.load_data()

    def search_clients(self):
        keyword = self.search_input.text()
        if keyword.strip():
            clients = self.controller.search_clients(keyword)
            self.update_table(clients)
        else:
            QMessageBox.warning(self, "Ошибка", "Введите ключевое слово")

    def clear_search(self):
        self.search_input.clear()
        self.load_data()

    def update_table(self, data):
        self.table.setRowCount(0)
        for row_number, client in enumerate(data):
            self.table.insertRow(row_number)
            for column_number, field in enumerate(client):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(field)))

    def export_to_csv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт клиентов в CSV", "", "CSV Files (*.csv);;All Files (*)", options=options
        )
        if file_path:
            success, message = self.controller.export_to_csv(file_path)
            if success:
                QMessageBox.information(self, "Экспорт успешный", message)
            else:
                QMessageBox.critical(self, "Ошибка при экспорте", message)

    def import_from_csv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Импорт клиентов из CSV", "", "CSV Files (*.csv);;All Files (*)", options=options
        )
        if file_path:
            success, message = self.controller.import_from_csv(file_path)
            if success:
                QMessageBox.information(self, "Импорт успешный", message)
                self.load_data()
            else:
                QMessageBox.critical(self, "Ошибка при импорте", message)

    def show_about_dialog(self):
        # Создаем окно "Об авторе"
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("Об авторе")
        about_dialog.setFixedSize(300, 100)

        # Добавляем текст о разработчике
        layout = QVBoxLayout()
        text = QLabel("Соня Кузина\nИСТ-211\n☆*:.｡.o(≧▽≦)o.｡.:*☆", self)
        layout.addWidget(text)

        # Кнопка "Закрыть"
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(about_dialog.accept)
        layout.addWidget(close_button)

        about_dialog.setLayout(layout)
        about_dialog.exec_()
