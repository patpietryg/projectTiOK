# syntax=docker/dockerfile:1
   
FROM python:3.7
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]
EXPOSE 8000