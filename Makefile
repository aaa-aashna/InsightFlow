PYTHON ?= .venv/bin/python

install:
	$(PYTHON) -m pip install -r backend/requirements.txt

run:
	cd backend && $(PYTHON) -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

test:
	cd backend && $(PYTHON) -m pytest -q

fmt:
	cd backend && $(PYTHON) -m black app tests main.py
