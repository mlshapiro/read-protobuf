# Automated tasks

help:
	echo "See Makefile for recipe list"

.PHONY: help


ruff:
	ruff read_protobuf.py tests

isort:
	isort read_protobuf.py tests/test_*

black:
	black read_protobuf.py tests/test_*

format: isort black ruff

pytest:
	pytest

pytest-cov:
	pytest --cov=read_protobuf

test: pytest-cov

build:
	python -m build

release-test:
	twine upload -r testpypi dist/*

release:
	twine upload dist/*
