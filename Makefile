.PHONY: run clean
VENV = venv
PYTHON = python3
PIP = $(VENV)/bin/pip
DOCKER = docker

run:
	$(DOCKER) compose up --build
	$(DOCKER) compose run django-web $(PYTHON) manage.py makemigrations 
	$(DOCKER) compose run django-web $(PYTHON) manage.py migrate 


clean:
	rm -rf __pycache__