all: clean build upload-test

clean:
	rm -rf build dist rallf.egg-info

build:
	python3 setup.py sdist bdist_wheel

upload:
	twine upload --repository prod dist/*

upload-test:
	twine upload --repository test dist/*

