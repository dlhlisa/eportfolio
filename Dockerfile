FROM python:3

WORKDIR .

COPY requirements.txt ./
run pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "./app.py"]
