PYTHON=python
VENV = .venv
PIP = $(VENV)/bin/pip
TABLES=41-60
TABLES_UNDERSCORE=$(subst -,_,$(TABLES))

RESULTS_DIR=results
NER_DIR=$(RESULTS_DIR)/ner
NEL_DIR=$(RESULTS_DIR)/nel
EVAL_DIR=$(RESULTS_DIR)/eval
TEST_DIR=data/test_set

NER_SPACY=$(NER_DIR)/ner_spacy_$(TABLES_UNDERSCORE).json
NER_GIGA_ZERO=$(NER_DIR)/ner_gigachat_zero_$(TABLES_UNDERSCORE).json
NER_GIGA_FEW=$(NER_DIR)/ner_gigachat_few_$(TABLES_UNDERSCORE).json

NEL_SPACY=$(NEL_DIR)/nel_spacy_$(TABLES_UNDERSCORE).json
NEL_GIGA_ZERO=$(NEL_DIR)/nel_gigachat_zero_$(TABLES_UNDERSCORE).json
NEL_GIGA_FEW=$(NEL_DIR)/nel_gigachat_few_$(TABLES_UNDERSCORE).json

EVAL_SPACY=$(EVAL_DIR)/eval_spacy_$(TABLES_UNDERSCORE).json
EVAL_GIGA_ZERO=$(EVAL_DIR)/eval_gigachat_zero_$(TABLES_UNDERSCORE).json
EVAL_GIGA_FEW=$(EVAL_DIR)/eval_gigachat_few_$(TABLES_UNDERSCORE).json

.PHONY: help dirs ner_spacy ner_gigachat_zero ner_gigachat_few \
        nel_spacy nel_gigachat_zero nel_gigachat_few \
        eval_spacy eval_gigachat_zero eval_gigachat_few all

help:
	@echo "Доступные команды:"
	@echo "  make venv          — Создать виртуальное окружение и установить зависимости"
	@echo "  make ner_spacy              — NER для spaCy"
	@echo "  make ner_gigachat_zero      — NER для GigaChat zero-shot"
	@echo "  make ner_gigachat_few       — NER для GigaChat few-shot"
	@echo "  make nel_spacy              — NEL для spaCy"
	@echo "  make nel_gigachat_zero      — NEL для GigaChat zero-shot"
	@echo "  make nel_gigachat_few       — NEL для GigaChat few-shot"
	@echo "  make eval_spacy             — Оценка NER spaCy"
	@echo "  make eval_gigachat_zero     — Оценка NER GigaChat zero-shot"
	@echo "  make eval_gigachat_few      — Оценка NER GigaChat few-shot"
	@echo "  make all                    — Запуск всего пайплайна"

venv:
	@if [ ! -d $(VENV) ]; then \
		python3 -m venv $(VENV); \
		echo "Создано виртуальное окружение $(VENV)"; \
	else \
		echo "Виртуальное окружение $(VENV) уже существует"; \
	fi
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt

ner_spacy: dirs
	$(PYTHON) run_ner.py --task ner --method spacy --tables $(TABLES)

ner_gigachat_zero: dirs
	$(PYTHON) run_ner.py --task ner --method gigachat_zero --tables $(TABLES)

ner_gigachat_few: dirs
	$(PYTHON) run_ner.py --task ner --method gigachat_few --tables $(TABLES)

nel_spacy:
	$(PYTHON) run_nel.py --input $(NER_SPACY) --output $(NEL_SPACY)

nel_gigachat_zero:
	$(PYTHON) run_nel.py --input $(NER_GIGA_ZERO) --output $(NEL_GIGA_ZERO)

nel_gigachat_few:
	$(PYTHON) run_nel.py --input $(NER_GIGA_FEW) --output $(NEL_GIGA_FEW)

eval_spacy:
	$(PYTHON) evaluate_ner.py \
	  --pred $(NER_SPACY) \
	  --gold_dir $(TEST_DIR) \
	  --output $(EVAL_SPACY)

eval_gigachat_zero:
	$(PYTHON) evaluate_ner.py \
	  --pred $(NER_GIGA_ZERO) \
	  --gold_dir $(TEST_DIR) \
	  --output $(EVAL_GIGA_ZERO)

eval_gigachat_few:
	$(PYTHON) evaluate_ner.py \
	  --pred $(NER_GIGA_FEW) \
	  --gold_dir $(TEST_DIR) \
	  --output $(EVAL_GIGA_FEW)

all: ner_spacy ner_gigachat_zero ner_gigachat_few \
     nel_spacy nel_gigachat_zero nel_gigachat_few \
     eval_spacy eval_gigachat_zero eval_gigachat_few