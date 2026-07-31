# Effective Mobile - Nginx + Python backend

Простое веб-приложение, состоящее из двух контейнеров:

- **backend** - Python HTTP-сервер на `http.server`, отвечает текстом:
  `Hello from Effective Mobile!`
- **nginx** - reverse proxy, принимает запросы на порту `80` и проксирует их на backend


## Структура проекта
```text
├── backend/
│   ├── Dockerfile
│   └── app.py
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

## Как работает схема

Пользователь -> http://localhost:80 -> simple-nginx контейнер (снаружи порт 80 -> 8080 внутри) -> easy-python-http-server backend контейнер (порт 8080 внутри) -> Python http.server


## Как запустить проект

1. Убедитесь, что установлены:
   - Docker
   - Docker Compose

2. Соберите и запустите контейнеры:
docker compose up -d --build

3. Проверьте, что оба контейнера запустились и находятся в статусе UP
docker compose ps

3. Для проверки работоспособности:
curl -i http://localhost.

Ожидаемый ответ:

HTTP/1.1 200 OK
Server: nginx/1.31.3
Date: Fri, 31 Jul 2026 14:13:26 GMT
Content-Type: text/plain
Transfer-Encoding: chunked
Connection: keep-alive

4. В случае возникновения ошибок:

Читаем логи
docker compose logs

Смотрим запущенные в контейнерах процессы
docker compose top

5. Остановка проекта
docker compose down


## Использованные технологии

### Backend

Python 3.12 - язык программирования
http.server - стандартная библиотека Python для HTTP-сервера
BaseHTTPRequestHandler - обработчик HTTP-запросов
python:3.12-slim - официальный облегченный образ python 3.12

### Nginx

Nginx 1.31 - веб-сервер и reverse proxy
nginxinc/nginx-unprivileged - официальный образ nginx без root-привилегий
Alpine Linux 3.24 - базовый образ для nginx

### Контейнеризация

Docker - платформа для контейнеризации приложений
Docker Compose - оркестрация многоконтейнерных приложений
Docker Networks - изолированная сеть для взаимодействия контейнеров
Docker Volumes - монтирование конфигурационных файлов

### Конфигурация

YAML - формат файла docker-compose.yml
Nginx Configuration - конфигурация reverse proxy
Dockerfile - инструкции для сборки образа backend

### Инфраструктура

Linux - хостовая операционная система
Bridge Network Driver - тип Docker-сети для изоляции контейнеров

### Безопасность

Non-root users - запуск процессов от непривилегированных пользователей
Network Isolation - изоляция backend от внешней сети