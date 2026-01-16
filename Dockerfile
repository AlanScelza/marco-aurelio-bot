FROM python:3

COPY requirements.txt /requirements.txt
COPY bot.py /bot.py

RUN chmod +x /bot.py

RUN pip3 install -r /requirements.txt

ENTRYPOINT [ "python", "/bot.py" ]