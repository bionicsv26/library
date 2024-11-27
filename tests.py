import unittest
from io import StringIO
from pathlib import Path
from unittest import mock

from main import Book, Library


class TestBook(unittest.TestCase):

    def test_book_creation(self):
        """Проверяет создание экземпляра класса Book."""
        book = Book("Война и мир", "Лев Толстой", 1869)
        self.assertEqual(book.title, "Война и мир")
        self.assertEqual(book.author, "Лев Толстой")
        self.assertEqual(book.year, 1869)
        self.assertEqual(book.status, "в наличии")
        self.assertIsNotNone(book.id)  # Проверяем, что ID сгенерировался
        self.assertTrue(isinstance(book.id, str)) # Проверяем тип ID


    def test_book_creation_with_id(self):
        """Проверяет создание экземпляра класса Book с заданным ID."""
        book_id = "1274d8e0-3b49-41eb-b3f6-1ee5fd38aae1"
        book = Book("Анна Каренина", "Лев Толстой", 1877, id=book_id)
        self.assertEqual(book.title, "Анна Каренина")
        self.assertEqual(book.id, book_id)


    def test_book_creation_with_status(self):
        """Проверяет создание экземпляра класса Book с заданным статусом."""
        book = Book("Преступление и наказание", "Фёдор Достоевский", 1866, status="выдана")
        self.assertEqual(book.status, "выдана")


    def test_book_str_representation(self):
        """Проверяет строковое представление книги."""
        book = Book("Мёртвые души", "Николай Гоголь", 1842)
        expected_str = f"{book.id} Мёртвые души - Николай Гоголь, 1842 (в наличии)"
        self.assertEqual(str(book), expected_str)


class TestLibrary(unittest.TestCase):
    """Тестовый класс для проверки функциональности класса Library."""

    def setUp(self):
        """Создает временный файл для хранения данных библиотеки перед каждым тестом."""
        self.temp_file = Path("test_library.json")
        self.library = Library(str(self.temp_file))

    def tearDown(self):
        """Удаляет временный файл после каждого теста."""
        if self.temp_file.exists():
            self.temp_file.unlink()

    def test_library_creation(self):
        """Проверяет создание объекта библиотеки."""
        self.assertEqual(len(self.library.books), 0)  # Библиотека пуста при создании
        self.assertTrue(isinstance(self.library, Library))

    def test_add_book(self):
        """Проверяет добавление книги в библиотеку."""
        self.library.add_book("Война и мир", "Лев Толстой", 1869)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Война и мир")

    def test_remove_book(self):
        """Проверяет удаление книги из библиотеки."""
        book1 = Book("Война и мир", "Лев Толстой", 1869)
        self.library.books = [book1]
        self.library.remove_book(str(book1.id))
        self.assertEqual(len(self.library.books), 0)

        # Попытка удалить несуществующую книгу
        self.library.remove_book("nonexistent_id")
        self.assertEqual(len(self.library.books), 0)


    def test_find_book(self):
        """Проверяет поиск книг по различным критериям."""
        self.assertEqual(len(self.library.books), 0)
        self.library.add_book("Война и мир", "Лев Толстой", 1869)
        self.library.add_book("Анна Каренина", "Лев Толстой", 1877)
        self.assertEqual(len(self.library.books), 2)
        with mock.patch('sys.stdout', new_callable=lambda: StringIO()) as stdout: #используется лямбда-функция для создания экземпляра класса StringIO
            self.library.find_book("Толстой") # поиск по автору
        expected_str = f"Найденные книги:\n{self.library.books[0].id} Война и мир - Лев Толстой, 1869 (в наличии)\n{self.library.books[1].id} Анна Каренина - Лев Толстой, 1877 (в наличии)\n"
        self.assertEqual(stdout.getvalue(), expected_str)

        with mock.patch('sys.stdout', new_callable=lambda: StringIO()) as stdout: #используется лямбда-функция для создания экземпляра класса StringIO
            self.library.find_book("1877") # поиск по году
        expected_str = f"Найденные книги:\n{self.library.books[1].id} Анна Каренина - Лев Толстой, 1877 (в наличии)\n"
        self.assertEqual(stdout.getvalue(), expected_str)

        with mock.patch('sys.stdout', new_callable=lambda: StringIO()) as stdout: #используется лямбда-функция для создания экземпляра класса StringIO
            self.library.find_book("Преступление") # поиск по названию отсутствующей книги
        expected_str = "Книги по вашему запросу не найдены.\n"
        self.assertEqual(stdout.getvalue(), expected_str)


    def test_display_books(self):
        """Проверяет отображение списка книг."""
        self.library.add_book("Война и мир", "Лев Толстой", 1869)
        with mock.patch('sys.stdout', new_callable=lambda: StringIO()) as stdout: #используется лямбда-функция для создания экземпляра класса StringIO
            self.library.display_books()
        expected_str = f"Список книг в библиотеке:\n{self.library.books[0].id} Война и мир - Лев Толстой, 1869 (в наличии)\n"
        self.assertEqual(stdout.getvalue(), expected_str)


    def test_save_and_load_books(self):
        """Проверяет сохранение и загрузку данных библиотеки в файл."""
        book1 = Book("Преступление и наказание", "Фёдор Достоевский", 1866)
        book2 = Book("Идиот", "Фёдор Достоевский", 1869)
        self.library.books = [book1, book2]
        self.library.save_books()

        loaded_library = Library(str(self.temp_file))
        self.assertEqual(len(loaded_library.books), 2)
        self.assertEqual(loaded_library.books[0].title, "Преступление и наказание")
        self.assertEqual(loaded_library.books[1].title, "Идиот")

    def test_load_empty_file(self):
        """Проверяет загрузку данных из пустого файла."""
        self.temp_file.touch()  # Создаем пустой файл
        loaded_library = Library(str(self.temp_file))
        self.assertEqual(len(loaded_library.books), 0) # Проверяем, что библиотека пуста 


if __name__ == '__main__':
    unittest.main()
