FROM python:3.12-slim

# Создаём непривилегированного пользователя
RUN groupadd -r appuser && useradd -r -g appuser -d /home/appuser -s /sbin/nologin appuser

WORKDIR /app

COPY app.py .

# Меняем владельца файлов на appuser
RUN chown -R appuser:appuser /app

# Переходим на непривилегированного пользователя
USER appuser

EXPOSE 8080

CMD ["python", "app.py"]