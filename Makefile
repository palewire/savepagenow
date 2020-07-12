.PHONY: freeze ship test


freeze:
	pipenv lock --dev -r > .github/workflows/requirements.txt


ship:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/* --skip-existing


test:
	flake8 savepagenow
	coverage run test.py
	coverage report -m
