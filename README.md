# bkp6

Минимальный Python-проект, который удобно запускать в GitHub Codespaces.

## Что уже настроено
- пакет `app` с объектом `app` (`title`, `version`) и базовой функциональностью (`health`, `add`)
- smoke-check через `python -m compileall app`
- тесты на `unittest` без внешних зависимостей

## Запуск в GitHub Codespaces
1. Откройте репозиторий в Codespaces.
2. В терминале проверьте версию Python:

   ```bash
   python --version
   ```

3. (Опционально) создайте виртуальное окружение:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

4. Установите зависимости (файл есть, даже если внешние зависимости не требуются):

   ```bash
   pip install -r requirements.txt
   ```

## Как запустить функционал
- Проверка импорта и метаданных:

  ```bash
  python -c "from app.main import app; print(app.title, app.version)"
  ```

- Запуск модуля (печатает health-статус):

  ```bash
  python -m app.main
  ```

## Как протестировать
- Компиляция Python-файлов:

  ```bash
  python -m compileall app
  ```

- Юнит-тесты:

  ```bash
  python -m unittest discover -s tests -v
  ```
