# AutoGrader — Week 1 Prototype

A small Python coordinator that compiles a student's C file with GCC, runs JSON-defined tests, applies a time limit per test, and writes JSON and text reports.

## Requirements

- Python 3.9+
- GCC available on PATH

Check:
```bash
python --version
gcc --version
```

## Run

From the project root:

```bash
python main.py submissions/add.c
```

Optional arguments:
```bash
python main.py submissions/add.c --rules config/rules.json --tests tests/tests.json
```

Reports are written to `reports/`. The executable is written to `build/student_program`.

## Change tests

Edit `tests/tests.json`. Each test has `name`, `input`, and `expected`.

## Important limitations

This is a Week 1 prototype, not a secure sandbox. `memory_limit_mb` is included in the rules for the next stage but is not enforced yet. A timeout is applied to each program run, but robust isolation and OS-level CPU/memory/process restrictions must be added before running untrusted submissions. The grade currently equals the percentage of tests passed; metric weights and advanced analyzers will be added later.
