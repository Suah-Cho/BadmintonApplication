FROM python:3.11.7

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache -r requirements.txt

COPY . .

EXPOSE 8000

#CMD ["gunicorn", "main:app"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]