# axiomata

![version](https://img.shields.io/badge/version-0.2.0-blue)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)

Importable modules for mathematical and CS proof, analysis, and reasoning.

## Modules

Everything lives under the single `axiomata` package — see [`axiomata/README.md`](axiomata/README.md) for full usage examples.

| Submodule | What it does |
|---|---|
| `axiomata.induction` | Checks mathematical induction proofs of arithmetic-series identities |
| `axiomata.checks` | Symbolic equality checks for algebraic expressions |
| `axiomata.master_theorem` | Master Theorem recurrence classification |

```python
from axiomata import induction, checks, master_theorem

induction.base_case("1 + 2 + 3 + ... + n = n(n+1)/2")
checks.equal("(k+1)³ − (k+1)", "(k³ − k) + 3k(k+1)")
master_theorem.calculate(2, 2, "n")
```

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
