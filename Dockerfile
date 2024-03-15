FROM python:3.9
WORKDIR /Kiribot
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
