.PHONY: sample all test cov lint

all: cov

test: lint
	hatch run test

cov: lint
	hatch run cov

sample:
	hatch run pytest -s -v sample

lint:
	hatch run types:check
	hatch fmt
