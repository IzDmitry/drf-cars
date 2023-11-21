# Используем базовый образ Python
FROM python:3.9

# Устанавливаем зависимости
RUN pip install --upgrade pip
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Копируем файлы проекта в контейнер
COPY . /app
WORKDIR /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]