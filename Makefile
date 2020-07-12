.PHONY: freeze ship test

freeze:
	pipenv lock -r > .github/workflows/requirements.txt


ship:
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing


test:
	flake8 savepagenow
	coverage run test.py
	coverage report -m
