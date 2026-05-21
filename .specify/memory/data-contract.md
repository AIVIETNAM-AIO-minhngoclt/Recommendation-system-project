# Data Contract

## Purpose
Define the expected schema for a MicroLens item as used by the Streamlit UI and recommendation pipeline.

## Canonical item shape
Each item should be normalized into the following structure:

```python
{
    "id": str | int,
    "title": str,
    "cover": str | None,
    "preview_frames": list[str],
    "video": str | None,
    "likes": int | float | None,
    "views": int | float | None,
    "tags": list[str] | None,
    "meta": dict | None,
}
```

## Required for rendering
- `id`
- `title`

## Strongly recommended for full UX
- `cover`
- `preview_frames`
- `likes`
- `views`

## Rendering fallback rules
- If `cover` is missing, show a placeholder image block.
- If `preview_frames` is empty, show a fallback preview area.
- If `likes` or `views` is missing, show `N/A`.
- If `title` is too long, clamp to 2 lines in UI.
- All IDs must be rendered in a stable string form.

## Normalization rules
- Convert likes and views to numeric if possible.
- Normalize missing media fields to `None` or empty list.
- Strip whitespace from title.
- Reject rows with missing `id` or missing `title`.

## Recommender output contract
Each recommendation result should have:

```python
{
    "item_id": str | int,
    "score": float,
    "rank": int,
    "reason_tags": list[str],
    "source_seed_ids": list[str | int] | None,
}
```

## Notes
Raw dataset fields may differ from the normalized UI shape.
Always normalize before rendering or ranking.
