FROM python:3.12-alpine3.21

# рабочая директория
WORKDIR /app

# код в контейнер
COPY . /app

# pip upgrade и install 
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# открываем порт
EXPOSE 8000

# подгрузка тестовых данных :)
RUN python3 -m app.test_data
# запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
