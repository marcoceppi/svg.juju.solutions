PROJECT=svgjujusolutions

PYHOME=.venv/bin
NOSE=$(PYHOME)/nosetests
FLAKE8=$(PYHOME)/flake8
PYTHON=$(PYHOME)/python3


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
	sudo apt-get install -qy python-virtualenv python3 python3-dev
	python3 -m venv --without-pip .venv
	curl https://bootstrap.pypa.io/ez_setup.py | $(PYTHON)
	$(PYHOME)/easy_install pip || venv/local/bin/easy_install pip
	rm setuptools*.zip

	$(PYHOME)/pip install bottle flake8 coverage nose pyaml networkx requests
	#$(PYTHON) setup.py develop
