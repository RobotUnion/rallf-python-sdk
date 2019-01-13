BUILD_REV := $(shell grep "version=" < setup-dev.py | grep -v "^ *\#" | sed -r 's/.*[0-9]+\.[0-9]+\.[0-9]+-[a-z]*([0-9]+).*/\1/g')
INCREMENT := 1

all: clean build deploy-test
release: all deploy-prod

clean:
	rm -rf build dist rallf.egg-info

build:
	sed -r "s/([0-9]+)\.([0-9]+)\.([0-9]+)-([a-z]*)([0-9]+)/\1.\2.\3-\4$$(( $(BUILD_REV) + $(INCREMENT) ))/g" -i setup-dev.py
	python3 setup-dev.py sdist bdist_wheel


build-prod:
	sed -r "s/([0-9]+)\.([0-9]+)\.([0-9]+)-([a-z]*)([0-9]+)/\1.\2.\3/g" < setup-dev.py > setup.py
	python3 setup.py sdist bdist_wheel

deploy-prod: build-prod
	twine upload dist/*

deploy-test:
	twine upload --repository test dist/*

