# Car_critic
API-сервер, который даст возможность поделиться мнением об автомобилях.
## Как запустить проект
Клонировать репозиторий
```
git clone git@github.com:Gustcat/Car_critic.git
```
В корневой директории проекта запустите сборку сети контейнеров(в режиме демона):
```
sudo docker compose up -d
```
Сделайте миграции в контейнере backend:
```
sudo docker compose exec backend python manage.py migrate
```
Для проверки эндпоинтов, можно воспользоваться дампом Car_critic.postman_collection.json, загрузив его в Postman.

## Список используемых библиотек
Необходимые зависимости для приложения backend находятся в файле /backend/requirements.txt.

## Автор
https://github.com/Gustcat
