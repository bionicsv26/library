import json
import uuid
from typing import List


class Book:
    """Представляет книгу в библиотеке."""

    def __init__(self, title: str, author: str, year: int, id: str = None, status: str = "в наличии") -> None:
        """
        Инициализирует экземпляр книги.
        
        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
            id (str, optional): Уникальный идентификатор книги (по умолчанию None).
            status (str, optional): Статус книги ("в наличии" или "выдана").
        """
        self.id: str = id or str(uuid.uuid4()) # Генерируем ID только если id=None
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def __str__(self) -> str:
        """
        Возвращает строковое представление книги.
        
        Returns:
            str: Отформатированная строка с детальной информацией о книге.
        """
        return f"{self.id} {self.title} - {self.author}, {self.year} ({self.status})"

# Класс для управления библиотекой
class Library:
    """Представляет библиотеку книг."""
    def __init__(self, filename: str = "library.json") -> None:
        """
        Инициализирует объект библиотеки, загружая данные из файла JSON.

        Args:
            filename (str): Имя файла для сохранения данных. По умолчанию "library.json".
        """
        self.filename: str = filename
        self.books: List[Book] = self.load_books()  # Загружаем данные при создании объекта

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавляет новую книгу в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
        """
        book = Book(title, author, year)
        self.books.append(book)
        self.save_books()  # Сохраняем данные после добавления
        print(f"Книга '{title}' успешно добавлена.")

    def remove_book(self, book_id: str) -> None:
        """
        Удаляет книгу из библиотеки по её ID.

        Args:
            book_id (str): Уникальный идентификатор книги в формате UUID.
        """
        for book in self.books:
            if str(book.id) == book_id:
                self.books.remove(book)
                print(f"Книга с ID {book_id} успешно удалена.")
                self.save_books()  # Сохраняем данные после удаления
                return
        print(f"Книга с ID {book_id} не найдена.")

    def find_book(self, query: str) -> None:
        """
        Ищет книги по названию, автору или году издания.

        Args:
            query (str): Ключевое слово для поиска (название, автор или год издания).
        """
        found_books = [
            book for book in self.books
            if query.lower() in book.title.lower()
            or query.lower() in book.author.lower()
            or query == str(book.year)
        ]
        if found_books:
            print("Найденные книги:")
            for book in found_books:
                print(book)
        else:
            print("Книги по вашему запросу не найдены.")

    def display_books(self) -> None:
        """
        Отображает все книги в библиотеке.

        Если библиотека пуста, выводится соответствующее сообщение.
        """
        if not self.books:
            print("Библиотека пуста.")
        else:
            print("Список книг в библиотеке:")
            for book in self.books:
                print(book)

    def update_status(self, book_id: str, status: str) -> None:
        """
        Обновляет статус книги.

        Аргументы:
            book_id (str): Уникальный идентификатор книги в формате UUID.
            status (str): Новый статус книги. Допустимые значения: "в наличии", "выдана".
        """
        allowed_statuses = {"в наличии", "выдана"}

        # Проверка формата UUID
        try:
            book_id_uuid: uuid.UUID = uuid.UUID(book_id)
        except ValueError:
            print("Неверный формат ID книги.")
            return
        
        # Проверка на допустимые статусы
        if status not in allowed_statuses:
            print(f"Недопустимый статус. Возможные варианты: {', '.join(allowed_statuses)}.")
            return

        # Обновляем статус книги, если она найдена
        for book in self.books:
            if book.id == book_id_uuid:
                book.status = status
                self.save_books()
                print(f"Статус книги '{book.title}' обновлён на '{status}'.")
                return

        print("Книга с таким ID не найдена.")


    def save_books(self) -> None:
        """Сохраняет данные библиотеки в файл JSON."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([vars(book) for book in self.books], f, ensure_ascii=False, indent=4)


    def load_books(self) -> List[Book]:
        """
        Загружает данные библиотеки из файла JSON.
        
        Returns:
            list_books (List[Book]): список книг либо пустой список"""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data: List[dict] = json.load(f)
                list_books: List[Book] = [Book(**book_data) for book_data in data]
                return list_books
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Возвращаем пустой список, если файл не найден или поврежден

# Основное меню приложения
def main() -> None:
    """Запускает основное меню библиотеки."""
    library = Library()

    while True:
        print("\n=== Меню ===")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Обновить статус книги")
        print("6. Выход")

        choice = input("Выберите действие: ")
        print("\n============")

        match choice:
            case "1":
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = input("Введите год издания книги: ")
                library.add_book(title, author, year)

            case "2":
                book_id = input("Введите ID книги для удаления: ")
                library.remove_book(book_id)

            case "3":
                query = input("Введите название, автора или год издания для поиска: ")
                library.find_book(query)

            case "4":
                library.display_books()

            case "5":
                book_id = input("Введите ID книги для обновления статуса: ")
                status = input("Введите новый статус ('в наличии' или 'выдана'): ")
                library.update_status(book_id, status)

            case "6":
                print("Выход из программы. До свидания!")
                break

            case _:
                print("Неверный ввод. Повторите попытку.")

if __name__ == "__main__":
    main()
