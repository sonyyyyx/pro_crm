import csv

from models.database import Database


class ClientController:
    def __init__(self):
        self.db = Database()

    def get_clients(self):
        query = "SELECT * FROM clients"
        return self.db.fetch_all(query)

    def add_client(self, name, email, phone):
        query = "INSERT INTO clients (name, email, phone) VALUES (?, ?, ?)"
        self.db.execute_query(query, (name, email, phone))

    def delete_client(self, client_id):
        query = "DELETE FROM clients WHERE id = ?"
        self.db.execute_query(query, (client_id,))

    def update_client(self, client_id, name, email, phone):
        query = "UPDATE clients SET name = ?, email = ?, phone = ? WHERE id = ?"
        self.db.execute_query(query, (name, email, phone, client_id))

    def search_clients(self, keyword):
        query = """
        SELECT * FROM clients
        WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?
        """
        return self.db.fetch_all(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    def export_to_csv(self, file_path):
        clients = self.get_clients()
        try:
            with open(file_path, mode="w", newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Email", "Phone"])
                for client in clients:
                    writer.writerow(client[1:])
            return True, "Успешный экспорт."
        except Exception as e:
            return False, f"Ошибка: {e}"

    def import_from_csv(self, file_path):
        try:
            with open(file_path, mode="r", newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) != 3:
                        continue  # Пропустить некорректные строки
                    name, email, phone = row
                    self.add_client(name, email, phone)
            return True, "Успешно"
        except Exception as e:
            return False, f"Ошибка: {e}"
