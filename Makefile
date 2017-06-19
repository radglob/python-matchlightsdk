PYENVS=2.7.11 3.3.6 3.4.3 3.5.0
REQUIREMENTS_DIR=requirements
REQUIREMENTS_ARTIFACTS=$(REQUIREMENTS_DIR)/%.txt
REQUIREMENTS_TARGETS=build main qa test

.PHONY: clean clean_wheels

bdist_wheel:
	@python setup.py bdist_wheel

clean: clean_build clean_docs clean_requirements clean_wheels

clean_docs:
	cd docs && make clean

clean_build:
	python setup.py clean --all
	rm -rf dist/

clean_requirements:
	rm -rf requirements/*.txt

clean_wheels:
	rm -rf wheelhouse/

.PHONY: docs
docs:
	tox -e docs

serve_docs:
	tox -e docs,serve-docs

# Wheel generation targets borrowed from sdispater/pendulum:
# <https://github.com/sdispater/pendulum/blob/master/Makefile>

# build_wheels_x64:
# 	docker pull quay.io/pypa/manylinux1_x86_64
# 	docker run --rm -v `pwd`:/io \
# 		quay.io/pypa/manylinux1_x86_64 /io/build-wheels.sh
#
# build_wheels_i686:
# 	docker pull quay.io/pypa/manylinux1_i686
# 	docker run --rm -v `pwd`:/io \
# 		quay.io/pypa/manylinux1_i686 /io/build-wheels.sh

# wheels_x64: clean_wheels build_wheels_x64
#
# wheels_i686: clean_wheels build_wheels_i686

$(REQUIREMENTS_ARTIFACTS): $(REQUIREMENTS_DIR)/src/%.in
	pip-compile $< -o $@

requirements: $(patsubst %,$(REQUIREMENTS_ARTIFACTS),$(REQUIREMENTS_TARGETS))

tox:
	@pyenv local ${PYENVS}
	@tox
