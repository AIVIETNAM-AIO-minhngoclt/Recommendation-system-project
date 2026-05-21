---
title: Streamlit UI Skill
description: Build and modify the media-first Streamlit UI for the MicroLens recommender app.
---

# Streamlit UI Skill

## When to use
Use this skill for tasks involving:
- Streamlit page layout
- Media card rendering
- Filters, search, seed basket, inspector panels
- Recommendation result presentation
- Empty/loading/error states
- `streamlit_shadcn_ui` controls and feedback

Do not use this skill for:
- recommendation algorithm changes
- feature engineering
- data normalization logic
- model evaluation code

## Canonical files
- `src/app.py`
- `src/pages/explore.py`
- `src/pages/recommend.py`
- `src/pages/compare.py`
- `src/pages/inspect.py`
- `src/components/media_card.py`
- `src/components/filter_bar.py`
- `src/components/seed_panel.py`

## Design system
- Core UI unit: `MicroLens Item Card`
- Canonical card component: `src/components/media_card.py`
- Layout primitives: `st.columns`, `st.container`, `st.sidebar`, `st.expander`
- UI polish: `streamlit_shadcn_ui`
- Default desktop layout: 3 zones
  - left: filters / controls
  - center: content feed or results
  - right: seed basket / inspector summary

## Product shape
This app is a media-first recommender workbench.
It is not a CRUD dashboard and not a raw table browser.

Prefer:
- card grids
- media previews
- clear actions
- visible recommendation reasons

Avoid:
- dense admin layouts
- giant forms
- table-first browsing
- excessive controls above the fold

## UI principles
- Modern, app-like, card-first
- Strong visual hierarchy
- Minimal clutter
- One obvious next action per section
- Important actions must produce visible feedback
- Every page must support loading, empty, and error states

## Card contract
Each item card should try to render:
- cover
- preview area
- title
- likes
- views
- stable item ID

If data is missing:
- missing cover -> show placeholder block
- missing preview -> show preview fallback area
- missing likes/views -> show `N/A`
- long title -> clamp to 2 lines
- malformed item -> do not crash page

## Interaction rules
Explore cards may expose:
- `Use as seed`
- `Inspect`
- `Find similar`

Recommendation cards may expose:
- `More like this`
- `Less like this`
- `Hide`
- `Inspect`

Do not place more than 3 primary actions on one card.

## streamlit_shadcn_ui usage
Use `streamlit_shadcn_ui` for:
- buttons
- badges
- metric cards
- segmented/radio selection
- dialogs and feedback

Do not use it to force the entire layout.
Use native Streamlit layout primitives for page structure.

## Execution rules
When changing UI:
1. Read `.specify/memory/ui-spec.md`
2. Read `.specify/memory/acceptance-criteria.md`
3. Reuse existing components before creating new ones
4. Keep business logic out of page files
5. Keep recommendation logic out of UI components
6. Make minimal, localized changes

## Verification
After UI changes, verify:
- page renders without exception
- cards still render with partial/missing media
- seed actions still work
- layout remains usable on laptop-width screens
- empty/loading/error states still exist
- no default flow was replaced by a table unless explicitly requested

## Done criteria
A UI task is complete only if:
- requested UI behavior works
- no page crashes on incomplete item data
- the media-card-first UX is preserved
- modified files stay limited and explainable