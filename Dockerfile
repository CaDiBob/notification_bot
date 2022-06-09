FROM python:3.8-slim-buster
WORKDIR /app
COPY bot.py /app/
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV PATH=/root/.local:$PATH
ENTRYPOINT ["python", "/app/bot.py"]
