FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
RUN apk update && \
    apk add bash && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev
WORKDIR /usr/src/shortener
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "urlshortener.wsgi:application", "--bind", "0.0.0.0:8000"]