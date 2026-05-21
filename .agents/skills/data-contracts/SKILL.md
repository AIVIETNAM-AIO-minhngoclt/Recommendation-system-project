---
title: Data Contracts Skill
description: Canonical item shapes and normalization rules.
---
# Data Contract Implementation

## Canonical Item Structure
Always normalize data to this shape before rendering or ranking:
- `id`: Unique identifier (stable string).
- `title`: Cleaned string.
- `cover`: URL/Path or `None`.
- `preview_frames`: List of strings.
- `video`: URL/Path or `None`.
- `likes/views`: Numeric or `None`.
