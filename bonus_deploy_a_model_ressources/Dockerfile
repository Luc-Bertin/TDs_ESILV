FROM python:slim

COPY requirements.txt /deploy/
RUN pip3 install -r /deploy/requirements.txt

WORKDIR /deploy/
COPY web_app.py .
COPY model.sav .

EXPOSE 80

CMD ["python", "web_app.py"]