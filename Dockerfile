FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/

# La cartella services viene montata come volume
# così puoi aggiungere servizi senza rebuild

EXPOSE 8080

CMD ["python", "app.py"]
