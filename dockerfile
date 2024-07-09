FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN python manage.py collectstatic --noinput

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
