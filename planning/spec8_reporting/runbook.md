# spec8_reporting — Runbook

## Setup Requirements
None beyond the existing setup. 

## Validation Commands
Run the test suite to verify the reporter module functions correctly and handles filenames properly:
```bash
pytest tests/test_reporting.py
```

Check the `outputs/reports/` directory after running an agent script to find your generated `.md` files.
