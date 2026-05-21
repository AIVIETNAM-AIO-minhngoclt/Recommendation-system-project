# UI Specification

## Global layout
The app uses a 3-zone layout on desktop:
- left: filters / controls
- center: content feed or results grid
- right: seed basket / session summary / inspector shortcuts

On smaller screens:
- left and right panels collapse into expanders or tabs
- center area remains the primary content area

## Design style
- Clean, modern, app-like
- Card-first
- Minimal clutter
- Strong visual hierarchy
- Use `streamlit_shadcn_ui` for controls and lightweight polish

## Shared UI elements
- top header with app title and current mode
- metric cards for quick stats
- badges for tags, reason labels, model labels, popularity buckets
- toast or inline success/error feedback where appropriate
- empty state message on every screen
- loading placeholder/skeleton where possible

## Screen: Explore
### Purpose
Help users discover items and choose seeds.

### Layout
- left panel: search, sort, popularity filters, optional tag filters
- center: item card grid
- right panel: selected seeds and quick actions

### Card content
Each card should display:
- cover
- preview area
- title
- likes
- views
- item ID
- actions:
  - Use as seed
  - Inspect
  - Find similar

### Key interactions
- search by title or ID
- sort by likes, views, recency, random
- add/remove seed item
- multi-select seed building

## Screen: Recommend
### Purpose
Show top recommendations from selected seeds.

### Layout
- left panel: recommendation mode and parameters
- center: recommendation result cards
- right panel: selected seeds + current run summary

### Controls
- model selector: content-based / collaborative / hybrid
- top-k selector
- rerank options
- explainability toggle

### Result card
- same base media card
- score badge
- rank label
- reason tags
- actions:
  - More like this
  - Less like this
  - Hide
  - Inspect

## Screen: Compare Models
### Purpose
Compare recommendation outputs from multiple strategies.

### Layout
- side-by-side columns for 2 or 3 models
- each column shows top-k results
- overlap summary at top

### Required comparisons
- model label
- top-k overlap
- diversity summary
- qualitative difference in recommendations

## Screen: Inspect Item
### Purpose
Explain one item in depth.

### Sections
- hero card with full item summary
- metadata details
- nearest neighbors
- why this item was recommended
- source seed links
- raw feature preview if available

## Empty states
Every screen must define:
- no data loaded
- no seed selected
- no recommendation results
- item missing media

## Error states
Every screen must define:
- invalid input
- failed recommendation run
- malformed item data

## Interaction principles
- visible next action at all times
- no dead-end screens
- feedback after every important action
- no more than 3 primary actions per item card
