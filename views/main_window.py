from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QMessageBox, QFileDialog,
    QDialog, QLabel, QTabWidget
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
        main_layout = QVBoxLayout()

        # Создаем TabWidget
        tab_widget = QTabWidget()

        # Вкладка "Клиенты"
        clients_tab = QWidget()
        clients_layout = QVBoxLayout()

        # Table
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Имя", "Email", "Телефон"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        # setToolTip -- подсказки при наведении
        self.table.setToolTip("Таблица клиентов. Двойной клик для выбора клиента")
        clients_layout.addWidget(self.table)

        # Search section
        search_layout = QHBoxLayout()
        self.search_input.setPlaceholderText("Поиск по имени, email и телефону")
        self.search_input.setToolTip("Введите текст для поиска по всем полям")

        search_button = QPushButton("Поиск")
        search_button.setToolTip("Нажмите для поиска клиентов")
        search_button.clicked.connect(self.search_clients)

        clear_button = QPushButton("Очистить выбор")
        clear_button.setToolTip("Очистить результаты поиска")
        clear_button.clicked.connect(self.clear_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(clear_button)
        clients_layout.addLayout(search_layout)

        # Form section
        form_layout = QHBoxLayout()
        self.name_input.setPlaceholderText("Имя")
        self.name_input.setToolTip("Введите имя клиента")

        self.email_input.setPlaceholderText("Email")
        self.email_input.setToolTip("Введите email клиента")

        self.phone_input.setPlaceholderText("Телефон")
        self.phone_input.setToolTip("Введите телефон клиента")

        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.phone_input)

        add_button = QPushButton("Добавить клиента")
        add_button.setToolTip("Добавить нового клиента с указанными данными")
        add_button.clicked.connect(self.add_client)
        form_layout.addWidget(add_button)

        clients_layout.addLayout(form_layout)

        # Control buttons
        buttons_layout = QHBoxLayout()

        delete_button = QPushButton("Удалить клиента")
        delete_button.setToolTip("Удалить выбранного клиента")
        delete_button.clicked.connect(self.delete_client)
        buttons_layout.addWidget(delete_button)

        update_button = QPushButton("Обновить клиента")
        update_button.setToolTip("Обновить данные выбранного клиента")
        update_button.clicked.connect(self.update_client)
        buttons_layout.addWidget(update_button)

        clients_layout.addLayout(buttons_layout)
        clients_tab.setLayout(clients_layout)

        # Вкладка "Импорт/Экспорт"
        import_export_tab = QWidget()
        import_export_layout = QVBoxLayout()

        export_button = QPushButton("Экспортировать таблицу CSV")
        export_button.setToolTip("Сохранить данные клиентов в CSV файл")
        export_button.clicked.connect(self.export_to_csv)

        import_button = QPushButton("Импортировать таблицу CSV")
        import_button.setToolTip("Загрузить данные клиентов из CSV файла")
        import_button.clicked.connect(self.import_from_csv)

        import_export_layout.addWidget(export_button)
        import_export_layout.addWidget(import_button)
        import_export_layout.addStretch()
        import_export_tab.setLayout(import_export_layout)

        # Вкладка "Об авторе"
        about_tab = QWidget()
        about_layout = QVBoxLayout()

        # Добавляем текст
        text = QLabel("Соня Кузина\nИСТ-211\n☆*:.｡.o(≧▽≦)o.｡.:*☆")
        text.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(text)

        # Добавляем фото
        photo_label = QLabel()
        pixmap = QPixmap("resources/img.jpg")
        # Масштабируем фото до размера 200x200 пикселей с сохранением пропорций
        scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        photo_label.setPixmap(scaled_pixmap)
        photo_label.setAlignment(Qt.AlignCenter)

        about_layout.addWidget(photo_label)
        about_layout.addStretch()
        about_tab.setLayout(about_layout)

        # Добавляем вкладки в TabWidget
        tab_widget.addTab(clients_tab, "Клиенты")
        tab_widget.addTab(import_export_tab, "Импорт/Экспорт")
        tab_widget.addTab(about_tab, "Об авторе")

        # Добавляем TabWidget в главный layout
        main_layout.addWidget(tab_widget)

        central_widget.setLayout(main_layout)
        self.load_data()

    # Остальные методы остаются без изменений
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
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("Об авторе")
        about_dialog.setFixedSize(300, 100)

        layout = QVBoxLayout()
        text = QLabel("Соня Кузина\nИСТ-211\n☆*:.｡.o(≧▽≦)o.｡.:*☆", self)
        layout.addWidget(text)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(about_dialog.accept)
        layout.addWidget(close_button)

        about_dialog.setLayout(layout)
        about_dialog.exec_()
