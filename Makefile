.PHONY: lint test mypy serve-docs check-release build-release

lint:
	pipenv run flake8 ./

test:
	pipenv run pytest tests

mypy:
	pipenv run mypy ./savepagenow

check-release:
	pipenv run twine check dist/*

build-release:
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel

serve-docs:
	cd docs && pipenv run make livehtml
