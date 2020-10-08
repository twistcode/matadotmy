FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --nocache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--reload"]