# praktikum_new_diplom

for API docs:

```Bash
cd infra
sudo docker-compose up
```
http://localhost/api/docs/redoc.html
```Bash
sudo docker-compose down
```

in foodgram-project-react/frontend:
```Bash
npm run start
```

in foodgram-project-react/frontend:
```Bash
cd backend/foodgram/foodgram
python3 manage.py runserver
```



# foodgram_project_react

## Описание

Соцсеть для обмена рецептами с возможностью подписываться на авторов, добавлять рецепты в корзину и скачивать список покупок по добавленный рецептам. API написан на вьюсетах, используются пагинация. Проект разворачивается в трёх контейнерах Docker.
***
## Установка проекта локально

```bash
docker-compose up
```
Далее в контейнере backend:

```bash
python3 manage.py migrate
python3 manage.py createsuperuser --email admin@admin.com --username admin -v 3
```
Задайте пароль для суперпользователя. Логин суперпользователя - admin. При заполнении БД тестовыми данными, суперпользователь уже создан. `Login: admin, pass: admin`  
Для проверки работоспособности, перейдите на http://127.0.0.1/
***

## Данные для входа на сайт и в админку
http://51.250.103.207/  
email:  admin@admin.com  
pass:   admin

## Пример .env файла

```
SECRET_KEY=xxx
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=root
DB_HOST=db
DB_PORT=5432
```

## Пользовательские роли

- **Аноним** — доступна главная страница, страница отдельного рецепта, форма авторизации, система восстановления пароля, форма регистрации.

- **Аутентифицированный пользователь** - доступна главная страница, страница другого пользователя, страница отдельного рецепта, страница «Мои подписки».

- **Администратор** — полные права на управление всем контентом проекта. Может создавать и удалять рецепты, ингредиенты и теги.
***

## Стек

Python, Django REST framework, Django, Docker, Nginx

## Авторы

**Семён Егоров**

[LinkedIn](https://www.linkedin.com/in/simonegorov/)  
[Email](simon.egorov.job@gmail.com)  
[Telegram](https://t.me/SamePersoon)
