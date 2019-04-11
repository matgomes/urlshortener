SHELL := /bin/bash

.PHONY: run
run:
	./venv/bin/python3 manage.py runserver

.PHONY: setup
setup:
	( \
	    virtualenv venv; \
		source venv/bin/activate; \
		pip3 install -r requirements.txt; \
	)

.PHONY: test
test:
	./venv/bin/python3 manage.py test