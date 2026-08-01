# axiomata

![version](https://img.shields.io/badge/version-0.1.0-blue)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)

Importable modules for mathematical and CS proof, analysis, and reasoning.

## Modules

| Module | What it does |
|---|---|
| [`induction/`](induction/README.md) | Checks mathematical induction proofs of arithmetic-series identities |
| [`checks/`](checks/README.md) | Symbolic equality checks for algebraic expressions |
| [`calculate/`](calculate/README.md) | Master Theorem recurrence classification |

Each module has its own README with usage examples.

## Dev setup

```bash
cd axiomata

python -m venv .venv
powershell -ExecutionPolicy Bypass -File .venv\Scripts\Activate.ps1

python -m pip install -U pip
python -m pip install -e ".[dev]"

pytest
```

## License

MIT
