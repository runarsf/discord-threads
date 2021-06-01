FROM python:3

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN python -m pip install -U -r requirements.txt

CMD [ "python", "-u", "threads.py" ]