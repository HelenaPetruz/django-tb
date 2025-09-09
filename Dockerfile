FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PRODUCTION 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./ /app/

WORKDIR /app/tb_project
ENV PRODUCTION=true

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "tb_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]

