FROM python:3.10-slim

WORKDIR /app

RUN pip install numpy flask flask-cors tensorflow pandas music21 gunicorn

COPY ./ ./

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]