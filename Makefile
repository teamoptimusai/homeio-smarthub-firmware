#* Variables
SHELL := /usr/bin/env bash
PYTHON := python3
PIP := pip3
PYTHONPATH := `pwd`
ENV_NAME := homeio

#* Setup
.PHONY : setup
setup :
	#* Creating virtual environment
	$(PIP) install virtualenv
	virtualenv -p $(PYTHON) $(ENV_NAME)
	source $(ENV_NAME)/bin/activate
	#* Installing dependencies
	$(PIP) install -r core/requirements.txt
	#* Downloading Weights
	sh core/models/get_weights.sh

#* Run the Core
.PHONY: run
run:
	sh core/run.sh