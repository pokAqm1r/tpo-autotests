# Автотесты по дисциплине «Тестирование программного обеспечения»

![Run autotests](https://github.com/pokAqm1r/tpo-autotests/actions/workflows/run-tests.yml/badge.svg)

Репозиторий содержит автотесты из лабораторных работ и workflow GitHub Actions,
который запускает их при каждом push.

| Папка | Что тестируется | Инструменты |
|---|---|---|
| `lab4_ui_tests` | контактная форма (`contact.html`), Page Object | Selenium WebDriver, pytest |
| `lab5_api_tests` | REST API JSONPlaceholder `/users` | requests, pytest, Postman/Newman |
| `lab6_unit_tests` | класс `Calculator` | pytest, параметризация |

## Локальный запуск

```bash
cd lab6_unit_tests            # или lab4_ui_tests / lab5_api_tests
python -m pip install -r requirements.txt
python -m pytest -v
```

UI-тесты без окна браузера: `HEADLESS=1 python -m pytest -v`.

## CI

Файл `.github/workflows/run-tests.yml`: Ubuntu → Python 3.13 → установка
зависимостей → `pytest` для каждой папки (matrix) + запуск Postman-коллекции
через Newman.
