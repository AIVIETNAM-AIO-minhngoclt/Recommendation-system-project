# Product Overview

## Product name
MicroLens Recommender Workbench

## Goal
Build an interactive Streamlit app that helps users explore MicroLens short-video items, create preference signals, and inspect recommendation outputs.

## Target users
- ML engineers prototyping recommendation models
- researchers evaluating recommendation quality
- demo users who want to understand recommendation behavior visually

## Core jobs to be done
1. Browse MicroLens items visually.
2. Choose one or more seed items.
3. Generate recommendations from those seeds.
4. Compare recommendation strategies.
5. Inspect why a result was recommended.

## Product principles
- Media-first, not table-first.
- Fast feedback loops matter more than dense control panels.
- Explainability should be visible in the UI.
- The app should feel like a recommendation lab, not an admin console.

## Main screens
- Explore
- Recommend
- Compare Models
- Inspect Item

## Primary user flow
1. User opens Explore.
2. User searches or browses items.
3. User adds 1+ seed items.
4. User runs recommendation.
5. User reviews recommendation cards.
6. User provides feedback: more like this, less like this, hide.
7. User optionally compares models or inspects one item.

## Non-goals
- Full data labeling platform
- Dataset management console
- User authentication platform
- Heavy MLOps workflow UI
