test:
	python -m pytest -x -s -v

run:
	python src/kektris/kektris.py

test-pypi:
	python setup.py check
	rm -rf dist
	python setup.py sdist bdist_wheel
	twine upload -r testpypi dist/*

pypi:
	python setup.py check
	rm -rf dist
	python setup.py sdist bdist_wheel
	twine upload -r pypi dist/*

build-example:
	rm -f kektris.pyxapp
	rm -f kektris.html
	pyxel package src/kektris src/kektris/kektris
	pyxel app2html kektris
	mv kektris.pyxapp example/
	mv kektris.html example/
