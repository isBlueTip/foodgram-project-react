FROM python:3.9-bullseye

WORKDIR /app
RUN pip install --upgrade pip

COPY /requirements_prod.txt ./
RUN pip install -r ./requirements_prod.txt --no-cache-dir

COPY ./ ./

RUN export DJANGO_SETTINGS_MODULE=foodgram.settings.settings_prod

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000"]