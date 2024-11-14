# CW_DRF
Курсовая работа по DRF DJANGO (good habbits)

### работают следующие команды для Windows с celery и celery-beat
`celery -A config worker --loglevel=info -E -P eventlet`
`celery -A config beat -l info -S django`

# CW_DRF_DOCKER
1 Запускаем докер
2 Создаем сеть `docker network create habits`
3 Заполяем .env на примере .env_example

```
    SECRET_KEY=your secret key
    
    DB_ENGINE=django.db.backends.postgresql
    POSTGRES_DB=drf_cw
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=your_password
    DB_HOST=db
    DB_PORT=5432
    
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    
    TG_BOT_TOKEN=78******39:key    
```
4 для корректной работы необходимо добавить `TG_BOT_TOKEN`
5 Пулим Python `docker pull python`
5 Запускаем контейнер  `docker-compose up -d --build`
6 Проверяем запуск `docker ps`
7 Запускаем для теста сайт документации: http://localhost:8000/redoc/
