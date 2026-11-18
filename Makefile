.PHONY: test demo check

test:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v

demo:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m laser_turret.demo

check: test
	git diff --check
