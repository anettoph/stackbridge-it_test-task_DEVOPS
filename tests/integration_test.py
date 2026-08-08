import threading
import unittest
from backend.app import SimpleHandler, HTTPServer
from http.client import HTTPConnection

class TestRunningServer(unittest.TestCase):
    # Метод вызывается перед каждым тестом в классе
    def setUp(self):
        # Инициализируем сервер с указанным обработчиком SimpleHandler
        self.server = HTTPServer(('localhost', 18080), SimpleHandler)
        # Создаем отдельный поток для работы сервера (чтобы он работал параллельно с тестами)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        # Устанавливаем daemon=True, чтобы поток автоматически завершался при выходе из тестов
        self.server_thread.daemon = True
        # Запускаем сервер в фоне (запуск цикла обработки запросов)
        self.server_thread.start()

    # Метод вызывается после каждого теста в классе для очистки ресурсов
    def tearDown(self):
        # Останавливаем цикл обработки запросов сервера
        self.server.shutdown()
        # Закрываем сокет (освобождает порт)
        self.server.server_close()
        # Ждём завершения фонового потока (чтобы избежать утечек памяти)
        self.server_thread.join()
    
    # Тест: проверка корневого эндпоинта (/)
    def test_root_endpoint(self):
        conn = HTTPConnection('localhost', 18080, timeout = 60)  # Создаём клиент HTTP с таймаутом 60 секунд
        try:
            conn.request('GET', '/')  # Отправляем GET-запрос к корневому пути
            response = conn.getresponse()  # Получаем ответ от сервера
            
            self.assertEqual(response.status, 200)  # Проверяем статус код ответа — должен быть 200 OK
            content = response.read().decode()  # Читаем тело ответа и декодируем его из байтов в строку
            self.assertEqual(content, 'Hello from Effective Mobile!')  # Проверяем содержимое ответа на соответствие ожидаемой строке
        finally:
            conn.close()  # Обязательно закрываем соединение после использования
    
    # Тест: проверка поведения при обращении к несуществующему эндпоинту
    def test_not_found_endpoint(self):
        conn = HTTPConnection('localhost', 18080, timeout = 60)  # Создаём клиент HTTP с таймаутом 60 секунд
        try:
            conn.request('GET', '/nonexistent')  # Отправляем GET-запрос к несуществующему пути
            response = conn.getresponse()  # Получаем ответ от сервера
            
            self.assertEqual(response.status, 404)  # Проверяем статус код ответа — должен быть 404 Not Found
        finally:
            conn.close()  # Обязательно закрываем соединение после использования


# Точка входа в тесты при прямом выполнении файла
if __name__ == '__main__':
    unittest.main()