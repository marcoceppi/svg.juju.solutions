PROJECT=svgjujusolutions

PYHOME=.venv/bin
NOSE=$(PYHOME)/nosetests
FLAKE8=$(PYHOME)/flake8
PYTHON=$(PYHOME)/python


all: lint test

.PHONY: clean
clean:
	rm -rf MANIFEST dist/* $(PROJECT).egg-info .coverage
	find . -name '*.pyc' -delete
	rm -rf .venv

test: .venv
	@echo Starting tests...
	@$(NOSE) --with-coverage --cover-package app.py

lint: .venv
	@$(FLAKE8) *.py --ignore E501 && echo OK

.venv:
	sudo apt-get install -qy python-virtualenv
	virtualenv .venv
	$(PYHOME)/pip install bottle flake8 coverage nose pyaml networkx
	#$(PYTHON) setup.py develop
