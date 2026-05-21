---
title: Recommender Debug Skill
description: Commands and patterns for debugging recommendation logic.
---
# Recommender Debugging and Testing

## Commands
### Running the App
```bash
streamlit run src/app.py
```

### Running Tests
```bash
pytest -q                              # All tests
pytest tests/test_recommender.py -q    # Recommender logic
pytest tests/test_data_contract.py -q  # Schema validation
pytest tests/test_media_card.py -q     # UI component tests
```

### Quality Checks
```bash
ruff check .                           # Linting
ruff format .                          # Formatting
```
