REQUIREMENT = requirements.txt

VER  = $(word 2, $(shell python --version 2>&1))
SRC  = app.py app_test.py
PY36 = $(shell expr $(VER) \>= 3.6)
CEXT_DIR = src/cext
CEXT_BUILD = $(CEXT_DIR)/build
CAPI_DIR = src/cext/capi
PY_ARCH = $(shell python -c "import platform; print(platform.machine())")

.PHONY: build deps test format cext
build: html

%:
	cd docs && make $@

clean:
	cd docs && make clean
	rm -rf $(CEXT_BUILD)
	rm -rf $(CAPI_DIR)/build $(CAPI_DIR)/*.so $(CAPI_DIR)/*.egg-info

cext:
	@echo "Building C/C++ extensions for $(PY_ARCH)..."
	mkdir -p $(CEXT_BUILD) && \
	cd $(CEXT_BUILD) && \
	cmake -DCMAKE_OSX_ARCHITECTURES=$(PY_ARCH) .. && \
	make
	cd $(CAPI_DIR) && python setup.py build_ext --inplace

test: clean build cext
	pycodestyle $(SRC)
	pydocstyle $(SRC)
	bandit app.py
	coverage run app_test.py && coverage report --fail-under=100 -m $(SRC)
	python -m pytest src/basic/*.py src/new_py3/*.py -v
	python -m pytest $(CEXT_DIR)/test_cext.py -v
	python -m pytest $(CAPI_DIR)/test_capi.py -v
ifeq ($(PY36), 1)
	black --quiet --diff --check --line-length 79 $(SRC)
endif

deps:
	pip install -r requirements.txt
	pip install pybind11
ifeq ($(PY36), 1)
	pip install black==22.3.0
endif

format:
	black --line-length 79 $(SRC) src/
	find src/cext -type f \( -name "*.cpp" -o -name "*.c" -o -name "*.h" \) | xargs -I{} clang-format -style=file -i {}
