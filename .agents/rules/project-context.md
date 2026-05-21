# Project Context

## Architecture Overview
- **Framework**: Streamlit
- **Domain**: MicroLens Short-Video Recommendation
- **Entrypoint**: `src/app.py`
- **Modules**:
    - `src/pages/`: UI screens
    - `src/services/`: Core logic (Recommender, Data Loader)
    - `src/components/`: Reusable UI elements
    - `src/state/`: Session state management

## Runtime Dependencies
- `streamlit`
- `streamlit_shadcn_ui`
- `pytest`
- `ruff`

## Domain Glossary
- **Seed Item**: An item selected by the user to base recommendations on.
- **Media Card**: The primary visual representation of a MicroLens item.
- **Recommendation Workbench**: The overall purpose of this application.
