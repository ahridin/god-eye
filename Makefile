# Some simple testing tasks (sorry, UNIX only).

FLAGS=


flake:
	flake8 agent tests

test:
	python3.5 -m "nose" -s $(FLAGS) ./tests/

vtest: flake develop
	nosetests --exe python3 -s -v $(FLAGS) ./tests/

cov cover coverage: flake
	@coverage erase
	@coverage run -m nose -s $(FLAGS) tests
	@coverage report
	@coverage html
	@echo "open file://`pwd`/coverage/index.html"