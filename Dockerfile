FROM python:3.13.1-slim

WORKDIR /flash_card_app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY .  /flash_card_app/

COPY static/input_files /flash_card_app/static/input_files

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "--workers", "3", "wsgi:application"]