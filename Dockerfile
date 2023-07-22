FROM python:3.11
COPY . .

RUN pip3 install -r requirements.txt
CMD ["python", "identity_app/app.py"]
