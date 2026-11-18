.PHONY: test demo check setup-sim check-sim

test:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v

demo:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m laser_turret.demo

setup-sim:
	./scripts/bootstrap_simulation.sh

check-sim:
	.venv/bin/python scripts/check_simulation_environment.py
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v

check: test
	git diff --check
