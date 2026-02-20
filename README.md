# bkp6

## Система отбора комплектов документации по триггерам

Репозиторий теперь содержит не только описание, но и минимально рабочий MVP:
- шаблон входного Excel;
- CLI/GUI для отбора комплектов;
- сборку в один `.exe` через PyInstaller.

---

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 1) Шаблон входного Excel

Сгенерировать шаблон:

```bash
python scripts/create_excel_template.py
```

По умолчанию файл создаётся в `templates/input_template.xlsx` с листами:
1. `Комплекты`
2. `Матрица_триггеров`
3. `Правила`
4. `Результат`

---

## 2) Минимальный MVP (CLI / GUI)

### CLI

```bash
python -m src.bkp6_mvp.cli \
  --input templates/input_template.xlsx \
  --trigger SEIS_7_9 \
  --discipline KZ \
  --output output/result.xlsx \
  --db output/rules.db
```

Что делает CLI:
1. читает Excel;
2. проверяет активацию `триггер + спец` по матрице;
3. применяет правила (`INCLUDE`, затем `EXCLUDE`) с wildcard-паттернами;
4. сохраняет результат в Excel;
5. пишет запись в SQLite-историю запусков.

### GUI

```bash
python main.py --gui
```

Экран позволяет выбрать входной файл, триггер, спец, путь результата и БД, затем запустить расчёт кнопкой.

---

## 3) Сборка в один `.exe` (PyInstaller)

### Linux/macOS

```bash
./build/build_exe.sh
```

### Windows

```bat
build\build_exe.bat
```

Файлы сборки:
- `bkp6.spec` — конфигурация PyInstaller;
- выходной артефакт: `dist/bkp6-mvp` (или `dist\bkp6-mvp.exe` на Windows).

---

## 4) Структура MVP

- `scripts/create_excel_template.py` — генератор шаблона Excel;
- `src/bkp6_mvp/excel_handler.py` — чтение/выгрузка Excel;
- `src/bkp6_mvp/rule_engine.py` — движок правил;
- `src/bkp6_mvp/database.py` — SQLite и история запусков;
- `src/bkp6_mvp/cli.py` — запуск через CLI;
- `src/bkp6_mvp/gui.py` — минимальный tkinter GUI;
- `main.py` — переключение CLI/GUI;
- `build/*` и `bkp6.spec` — сборка в `.exe`.
