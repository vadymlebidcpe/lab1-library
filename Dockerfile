# Используем базовый образ Python
FROM python:3.13.1

# Указываем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Указываем команду для запуска приложения
CMD ["python", "app.py"]
