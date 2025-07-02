# backend/Dockerfile

# Используем официальный базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install torch==2.3.0+cu121 --index-url
https://download.pytorch.org/whl/cu121

# Копируем весь код бэкенда (внутри /backend, т.е. из текущей директории)
COPY . .

# Открываем порт
EXPOSE 8000

# Команда запуска Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
