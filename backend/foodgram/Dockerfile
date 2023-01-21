FROM python:3.9-bullseye

RUN mkdir /app
RUN pip install --upgrade pip

COPY /requirements_prod.txt /app
RUN pip install -r /app/requirements_prod.txt --no-cache-dir

COPY ./ /app
WORKDIR /app

RUN export DJANGO_SETTINGS_MODULE=foodgram.settings.settings_prod

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000"]