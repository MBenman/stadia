.PHONY: run clean
VENV = venv
PYTHON = python3
PIP = $(VENV)/bin/pip

run: $(VENV)/bin/activate
	$(PYTHON) manage.py runserver

venv/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf $(VENV)