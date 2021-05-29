# api_yamdb

## Описание
API для проекта yamdb.

### Требования
Необходим установленный и запущенный Docker.

Инструкции по установке см. [Docker](https://www.docker.com/get-started#h_installation)

### Первый запуск проекта
     
1. Клонирование репозитория 
```bash
git clone https://github.com/Zaluznyak/infra_sp2.git
```
2. Сборка и запуск образа (находимся в корне проекта)
```bash
docker-compose up -d --build
```
3. Создание миграций
```bash
docker-compose exec web python manage.py makemigrations users
docker-compose exec web python manage.py makemigrations titles
```
4. Применение миграций
```bash
docker-compose exec web python manage.py migrate
```
5. Сбор статики
```bash
docker-compose exec web python manage.py collectstatic
```
6. Создание учетной записи администратора
```bash
docker-compose exec web python manage.py createsuperuser
```
7. Загрузка в базу тестовых данных
```bash
docker-compose exec web python manage.py loaddata fixtures.json
```
8. Переходим на сайт http://127.0.0.1

### Технологии
- Python 3.8.5
- Django 3.0.5
- DRF 3.11.0
- PostgreSQL 12.4
- nginx 1.19.3  
- Docker

