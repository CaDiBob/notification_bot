FROM python:3.8-slim
WORKDIR /app
COPY bot.py /app/
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python", "/app/bot.py"]
CMD ["/app/bot.py"]
