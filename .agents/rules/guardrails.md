# Guardrails and Constraints

## Prohibited Actions
- **DO NOT** rewrite the entire application or major modules without explicit permission.
- **DO NOT** place recommendation algorithms or complex logic inside Streamlit page files.
- **DO NOT** place Streamlit UI rendering logic inside service files.
- **DO NOT** add new dependencies for simple layout problems.
- **DO NOT** use ad-hoc utility functions if a standard one exists in `src/utils/`.

## Critical Rules
- **Media-first**: The MicroLens item card is the core unit. Never switch to raw tables as a default.
- **Small Diffs**: Prefer small, reversible changes over large refactors.
- **Privacy/Security**: Do not leak any sensitive data or include unnecessary print/console logs.
- **Data Integrity**: Fail gracefully if media fields are missing. Never assume records are clean.

## Ask Before
- Deleting files.
- Renaming major modules.
- Large architecture changes.
- Changing data contracts.
