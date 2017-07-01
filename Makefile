# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @Date:   2016-03-12
# @Last Modified by:   Tasdik Rahman
# @Last Modified time: 2016-04-05 16:32:19
# @GPLv3 License
# @http://tasdikrahman.me
# @https://github.com/tasdikrahman/plino

# virtualenv executables
PIP := $(BIN)/pip
PYTHON := $(BIN)/python
FLAKE8 := $(BIN)/flake8
PEP257 := $(BIN)/pep257
COVERAGE := $(BIN)/coverage
TESTRUN := $(BIN)/py.test

EGG_INFO := $(subst -,_,$(PROJECT)).egg-info


.clean-build:
#	@find -name $(PACKAGE).c -delete
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -delete
	@rm -rf $(EGG_INFO)
	@rm -rf __pycache__


.git-no-changes:
	@if git diff --name-only --exit-code;         \
	then                                          \
		echo Git working copy is clean...;        \
	else                                          \
		echo ERROR: Git working copy is dirty!;   \
		echo Commit your changes and try again.;  \
		exit -1;                                  \
	fi;

register: 
	python setup.py register -r pypi

dist: test
	python setup.py sdist
	python setup.py bdist_wheel

upload: .git-no-changes 
	python setup.py sdist upload -r pypi
	#$(PYTHON) setup.py bdist_wheel upload -r pypi


.PHONY: help
help:
	@echo "\nPlease call with one of these targets:\n"
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F:\
        '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}'\
        | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs | tr ' ' '\n' | awk\
        '{print "    - "$$0}'
	@echo "\n"
