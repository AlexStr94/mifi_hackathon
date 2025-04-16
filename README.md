# mifi_hackathon

## Локальная разработка:

Создание виртуального окружения:
```
python -m venv venv
```

Активация виртуального окружения (Linux):
```
. venv/bin/activate
```

Установить зависимости:
```
pip install -r requirements.txt
```

Поднятие контейнера:
```
docker compose up -d
```

Накатить миграции:
```
python manage.py migrate
```

Заполнить фейковыми данными бд:
```
python manage.py fake_data
```