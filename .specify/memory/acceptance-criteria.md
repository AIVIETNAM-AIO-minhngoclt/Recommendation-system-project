# Acceptance Criteria

## Global
- App launches successfully with `streamlit run src/app.py`
- App works with mock data even when full dataset is unavailable
- No page crashes when optional media fields are missing
- Layout remains usable on laptop-width screens
- All major user actions provide visible feedback

## Explore
- Displays item cards, not just a table
- Each rendered card shows title and ID
- Search supports title or ID
- User can add and remove seeds
- Seed state persists during session
- Missing cover or preview does not crash the page

## Recommend
- Requires at least 1 seed item before running
- Returns and renders top-k recommendations
- Each result displays score and at least 1 reason tag
- User can hide a recommendation
- User can give positive or negative feedback

## Compare Models
- User can compare at least 2 recommendation strategies
- Results are shown side by side
- A simple overlap or similarity summary is displayed

## Inspect Item
- Opens a single item in more detail
- Shows metadata available for that item
- Shows recommendation explanation if available
- Handles missing fields gracefully

## Code quality
- Recommendation logic is not implemented inside page files
- Shared card rendering is extracted to reusable component(s)
- Session state usage is centralized or at least standardized
- New behavior includes or updates relevant tests
