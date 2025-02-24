FROM python:3.13.1-slim

WORKDIR /flash_card_app

COPY requirements.txt .

# Create and activate the virtual environment
RUN python3 -m venv venv
ENV PATH="/flash_card_app/venv/bin:$PATH" 

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY .  /flash_card_app/

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "--workers", "3", "wsgi:app"]