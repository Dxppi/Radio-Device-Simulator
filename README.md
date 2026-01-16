# Radio Device API

## Установка

1. Клонировать репозиторий / скопировать проект:

```bash
git clone https://github.com/Dxppi/Radio-Device-Simulator
cd Radio-Device-Simulator
```

2. Создать и активировать виртуальное окружение:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. Установить зависимости

```bash
pip install -r requirements.txt
```

4. Настройка окружения
Создать .env файла
```bash
DB_PATH=radioDevices.sqlite
```

5. Создать базу данных (инициализация таблицы)
```bash
python db_init.py
```

## Запуск

```bash
python app.py
```

## Тесты

```bash
pytest -q
```