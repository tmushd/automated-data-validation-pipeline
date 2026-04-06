# Architecture Notes

## Flow

```mermaid
flowchart LR
    A["Olist subset CSVs"] --> B["extract.py"]
    B --> C["transform.py"]
    C --> D["processed Pandas DataFrames"]
    D --> E["load.py"]
    E --> F["SQLite warehouse"]
    F --> G["validators.py"]
    G --> H["Pytest suite"]
    H --> I["GitHub Actions CI"]
```

## Design Choices

- The repository commits a curated subset instead of downloading Kaggle data in CI.
- SQLite keeps the warehouse layer simple and reproducible for local development and GitHub Actions.
- Validators return structured dictionaries so the framework can support pytest assertions and standalone reporting.
- `data/bad/` demonstrates hard failures such as duplicate keys, orphan references, invalid statuses, and schema mismatches.
