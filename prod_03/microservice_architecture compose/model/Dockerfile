# Задаём базовый образ
FROM python:3.9
# Копируем содержимое папки ./app в рабочую директорию контейнера
COPY ./src ./
# Копируем файл requirements.txt в рабочую директорию контейнера
COPY ./requirements.txt ./
# Запускаем установку необходимых зависимостей
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./model.py" ]