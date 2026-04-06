# Portfolio Evidence

This document packages the project proof points that are most useful in a portfolio review.

## Clean Run Evidence

Commands executed:

```bash
python -m src.pipeline.run_pipeline
pytest -v
```

Recorded outputs:

- [pipeline_clean.txt](./sample-output/pipeline_clean.txt)
- [pytest_clean.txt](./sample-output/pytest_clean.txt)

Key result:

```text
============================== 89 passed in 1.28s ==============================
```

Pipeline summary excerpt:

```text
Loading 3000 rows into customers
Loading 3309 rows into products
Loading 3000 rows into orders
Loading 10171 rows into order_items
SQLite database created at .../database/pipeline.db
Pipeline completed successfully
```

## Bad Data Failure Evidence

Command executed:

```bash
PIPELINE_RAW_DIR=data/bad pytest tests/test_pipeline_smoke.py tests/test_schema.py tests/test_nulls.py tests/test_duplicates.py tests/test_referential_integrity.py tests/test_business_rules.py -v
```

Recorded output:

- [pytest_bad_data.txt](./sample-output/pytest_bad_data.txt)

Why this matters:

- The bad dataset intentionally violates primary-key, foreign-key, schema, and business-rule expectations.
- The pipeline fails immediately instead of silently loading corrupted records.
- That behavior demonstrates that the framework blocks invalid data rather than only reporting issues after the fact.

Representative failure excerpt:

```text
sqlite3.IntegrityError: UNIQUE constraint failed: customers.customer_id
```

## What Reviewers Should Notice

- The project validates a relational pipeline, not a single flat file.
- The clean path is deterministic because the curated subset is committed in the repo.
- The bad path proves the checks are meaningful and enforceable.
- CI can rerun the same commands on every push and pull request.
