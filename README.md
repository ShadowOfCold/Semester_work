# Семестровая работа
Цель работы: выработка и закрепление навыков по разработке систем искусственного интеллекта в контексте обработки естественного языка (Natural Language Processing – NLP).

Проект реализует распознавание именованных сущностей (NER) и их связывание с базой знаний (NEL) для русскоязычных табличных данных. Основной корпус данных — **RF-200 (ru-facts-200)**, таблицы в формате CSV.  

В проекте реализованы два подхода к NER:  
1. **Классические NLP-библиотеки** (Spacy)  
2. **Большие языковые модели (LLM)** с использованием GigaChat (zero-shot и few-shot)  

Для NEL используется связывание с **Wikidata** через API.

---

## Структура проекта

```
.
├── data/
|   ├── rf-200/csv/all-tables/     # Все таблицы из гитхаба
│   └── test_set/                  # Тестовые таблицы с эталонными сущностями (JSON)
├── results/
│   ├── ner/                       # Результаты NER
│   ├── nel/                       # Результаты NEL
│   └── eval/                      # Результаты оценки
├── src/
|   ├── loaders/                   # Загрузчики (загрузчик таблиц)             
│   ├── ner/                       # Классы и скрипты NER
│   └── nel/                       # Классы и скрипты NEL
├── run_ner.py                     # Запуск NER
├── run_nel.py                     # Запуск NEL
├── evaluate_ner.py                # Скрипт оценки NER
├── requirements.txt               # Зависимости
└── Makefile                       # Автоматизация задач
```

---

## Установка

Рекомендуется использовать виртуальное окружение Python.

1. Создаём виртуальное окружение и устанавливаем зависимости:

```bash
make venv
```

Это создаст `.venv` и установит все зависимости из `requirements.txt`.

2. Активируем виртуальное окружение:

```bash
source .venv/bin/activate
```

---

## Использование

### 1. NER

Запуск NER для выбранных таблиц:

```bash
# Spacy
make ner_spacy

# GigaChat zero-shot
make ner_gigachat_zero

# GigaChat few-shot
make ner_gigachat_few
```

Результаты сохраняются в `results/ner/` с именами файлов вида:  

```
ner_spacy_41_60.json
ner_gigachat_zero_41_60.json
ner_gigachat_few_41_60.json
```

---

### 2. NEL

Привязка сущностей к Wikidata:

```bash
# Spacy
make nel_spacy

# GigaChat zero-shot
make nel_gigachat_zero

# GigaChat few-shot
make nel_gigachat_few
```

Результаты сохраняются в `results/nel/` с аналогичной нумерацией.

---

### 3. Оценка NER

Оценка точности, полноты и F1-score (partial match):

```bash
make evaluate
```

Результаты сохраняются в `results/eval/evaluation.json` и выводятся в консоль в удобном виде:

```
=== Partial Match Evaluation ===

Метод: spacy
Таблица | TP  | FP  | FN  | Precision | Recall | F1
-----------------------------------------------
     41 |  ... | ... | ... |  ...     |  ...   | ...
...
Общие показатели:
Precision: 0.XXX, Recall: 0.XXX, F1: 0.XXX
```

---

### 4. Запуск всего пайплайна

```bash
make all
```

Выполняются все шаги: NER (spacy + GigaChat), NEL и оценка.

---

## Конфигурация

- Таблицы для обработки задаются в Makefile через переменную `TABLES`.  
- Путь к тестовым эталонным данным: `data/test_set/`.  
- Папки для сохранения результатов: `results/ner/`, `results/nel/`, `results/eval/`.

---

## Поддерживаемые категории NER

| Категория     | Описание |
|---------------|----------|
| PER           | Имя человека |
| ORG           | Организация, компания, учреждение |
| LOC           | Конкретное место (город, деревня, объект) |
| GPE           | Геополитическая территория (страна, регион) |
| DATE          | Дата, год, период времени |
| TIME          | Время |
| MONEY         | Денежные суммы |
| PERCENT       | Проценты |
| QUANTITY      | Количество или мера |
| EVENT         | Событие |
| WORK_OF_ART   | Произведение искусства |
| MISC          | Прочие значимые объекты |

---

## Требования

- Python >= 3.10  
- Библиотеки указаны в `requirements.txt`, включая:
  - `spacy`
  - `langchain_gigachat`
  - `requests`
  - и др.