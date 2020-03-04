FROM python:3.6

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/var/
WORKDIR /usr/var/

CMD ["python", "./init.py"]
