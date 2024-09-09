PHONY: install-requirements build-wheel format dist


install-requirements:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

build-wheel: make-dist
	python3 -m build
	ls -l dist/*.whl | awk '{print $$9}' | xargs pip install --force-reinstall

format:
	black src_py

make-dist:
	rm -rf dist
	mkdir dist

upload:
	python3 -m twine upload  dist/*
