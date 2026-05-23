"""Reusable MicroLens media card component."""
from __future__ import annotations

import base64

import streamlit as st

try:
    import streamlit_shadcn_ui as ui
    _HAS_SCU = True
except ImportError:
    _HAS_SCU = False

from src.state.session import add_seed, remove_seed, is_seed

_PLACEHOLDER_H = 150


# ── Helpers ───────────────────────────────────────────────────────────────────

def _fmt(v: int | float | None) -> str:
    if v is None:
        return "N/A"
    n = int(v)
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def _safe_id(item_id: object) -> str:
    return str(item_id)


def _render_cover(cover: str | None, height: int = 160) -> None:
    if cover:
        try:
            with open(cover, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            ext = "png" if str(cover).endswith(".png") else "jpeg"
            st.markdown(
                f'<div style="position:relative;margin-bottom:8px;border-radius:8px;overflow:hidden;">'
                f'<img src="data:image/{ext};base64,{b64}" '
                f'style="width:100%;height:{height}px;object-fit:cover;display:block;" />'
                f'<div style="position:absolute;bottom:0;left:0;right:0;height:55px;'
                f'background:linear-gradient(transparent,rgba(0,0,0,0.72));"></div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        except Exception:
            st.image(cover, use_container_width=True)
    else:
        st.markdown(
            f'<div style="height:{_PLACEHOLDER_H}px;'
            f'background:linear-gradient(135deg,#0f172a,#1e293b);'
            f'border-radius:8px;display:flex;align-items:center;'
            f'justify-content:center;margin-bottom:8px;">'
            f'<span style="color:#334155;font-size:28px;">🎬</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _render_stats(likes, views) -> None:
    parts = []
    if likes is not None:
        parts.append(f'<span class="chip chip-likes">❤ {_fmt(likes)}</span>')
    if views is not None:
        parts.append(f'<span class="chip chip-views">👁 {_fmt(views)}</span>')
    if parts:
        st.markdown(
            f'<div style="display:flex;gap:5px;flex-wrap:wrap;margin:4px 0 5px;">'
            + "".join(parts)
            + '</div>',
            unsafe_allow_html=True,
        )


def _render_score_bar(score: float) -> None:
    pct = min(100, int(score * 100))
    st.markdown(
        f'<div class="score-bar">'
        f'<div class="score-bar-header"><span>Match score</span><span>{score:.4f}</span></div>'
        f'<div class="score-bar-bg"><div class="score-bar-fill" style="width:{pct}%;"></div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ── Watch History panel ───────────────────────────────────────────────────────

def render_watch_history(
    history: list[dict],
    user_id: str,
    max_items: int = 20,
    height: int = 600,
) -> None:
    seed_count_in_hist = sum(1 for h in history if is_seed(str(h.get("id"))))
    caption = f"User `{user_id}` · **{len(history)}** interactions"
    if seed_count_in_hist:
        caption += f" · 🌱 **{seed_count_in_hist}** seeded"
    st.caption(caption)

    if not history:
        st.caption("No history found.")
        return

    with st.container(height=height, border=False):
        for h in history[:max_items]:
            item_id = str(h.get("id", ""))
            seeded = is_seed(item_id)
            ring = "2px solid #6366f1" if seeded else "1px solid rgba(99,102,241,0.15)"
            bg   = "rgba(99,102,241,0.06)" if seeded else "rgba(15,23,42,0.5)"

            cover = h.get("cover")
            t = str(h.get("title", ""))[:52]
            video_icon = "🎥 " if h.get("video") else ""
            seed_badge = (
                '<span style="font-size:9px;background:#6366f1;color:#fff;'
                'border-radius:3px;padding:1px 5px;margin-right:4px;font-weight:700;">SEED</span>'
                if seeded else ""
            )

            # Thumbnail
            thumb_html = ""
            if cover:
                try:
                    with open(cover, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode("utf-8")
                    ext = "png" if str(cover).endswith(".png") else "jpeg"
                    thumb_html = (
                        f'<img src="data:image/{ext};base64,{b64}" '
                        f'style="width:52px;height:42px;object-fit:cover;border-radius:6px;'
                        f'flex-shrink:0;border:{ring};" />'
                    )
                except Exception:
                    pass
            if not thumb_html:
                thumb_html = (
                    f'<div style="width:52px;height:42px;background:#1e293b;'
                    f'border-radius:6px;flex-shrink:0;display:flex;align-items:center;'
                    f'justify-content:center;border:{ring};">'
                    f'<span style="font-size:16px;">🎬</span></div>'
                )

            st.markdown(
                f'<div style="display:flex;gap:9px;align-items:center;'
                f'padding:6px 8px;border-radius:8px;background:{bg};margin-bottom:5px;">'
                + thumb_html
                + f'<p style="font-size:11px;margin:0;line-height:1.4;color:#cbd5e1;">'
                f'{seed_badge}{video_icon}{t}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        if len(history) > max_items:
            st.caption(f"…and {len(history) - max_items} more")


# ── Explore card ──────────────────────────────────────────────────────────────

def render_media_card(item: dict, key_prefix: str = "") -> None:
    try:
        _card_inner(item, key_prefix)
    except Exception as exc:
        st.warning(f"⚠️ Card error (id={item.get('id','?')}): {exc}")


def _card_inner(item: dict, key_prefix: str) -> None:
    item_id = _safe_id(item.get("id", "unknown"))
    title   = str(item.get("title", "Untitled")).strip() or "Untitled"
    cover   = item.get("cover")
    video   = item.get("video")
    likes   = item.get("likes")
    views   = item.get("views")

    play_key      = f"{key_prefix}_play_{item_id}"
    seed_key      = f"{key_prefix}_seed_{item_id}"
    already_seed  = is_seed(item_id)

    with st.container(border=True):
        _render_cover(cover)

        # Video player
        if video:
            if st.session_state.get(play_key):
                st.video(video)
                if st.button("✕ Close", key=f"{play_key}_close", use_container_width=True):
                    st.session_state[play_key] = False
                    st.rerun()
            else:
                if st.button("▶ Play", key=f"{play_key}_open", use_container_width=True):
                    st.session_state[play_key] = True
                    st.rerun()

        # Title
        video_dot = '<span class="chip chip-video" style="font-size:9px;padding:1px 6px;margin-bottom:3px;display:inline-block;">VIDEO</span><br>' if video else ""
        st.markdown(
            f'{video_dot}'
            f'<p style="font-weight:600;font-size:13px;line-height:1.4;'
            f'display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;'
            f'overflow:hidden;margin:2px 0 4px;color:#e2e8f0;">{title}</p>',
            unsafe_allow_html=True,
        )

        _render_stats(likes, views)

        # Seed action
        if already_seed:
            btn_label, btn_type = "✕ Remove seed", "destructive"
        else:
            btn_label, btn_type = "＋ Use as seed", "default"

        if _HAS_SCU:
            if ui.button(btn_label, key=seed_key, variant=btn_type, class_name="w-full mt-1"):
                if already_seed:
                    remove_seed(item_id)
                else:
                    add_seed(item)
                st.rerun()
        else:
            if st.button(btn_label, key=seed_key, use_container_width=True):
                if already_seed:
                    remove_seed(item_id)
                else:
                    add_seed(item)
                st.rerun()


# ── Result card (Recommend page) ──────────────────────────────────────────────

def render_result_card(item: dict, result: dict, key_prefix: str = "rec") -> None:
    try:
        _result_inner(item, result, key_prefix)
    except Exception as exc:
        st.warning(f"⚠️ Result card error (id={item.get('id','?')}): {exc}")


def _result_inner(item: dict, result: dict, key_prefix: str) -> None:
    item_id = _safe_id(item.get("id", "unknown"))
    title   = str(item.get("title", "Untitled")).strip() or "Untitled"
    cover   = item.get("cover")
    video   = item.get("video")
    likes   = item.get("likes")
    views   = item.get("views")

    rank        = result.get("rank", 0)
    score       = result.get("score", 0.0)
    reason_tags = result.get("reason_tags") or ["—"]

    hide_key = f"{key_prefix}_hide_{item_id}"
    play_key = f"{key_prefix}_play_{item_id}"

    if st.session_state.get(hide_key):
        return

    with st.container(border=True):
        # Rank + score header row
        r1, r2 = st.columns([1, 1])
        r1.markdown(
            f'<span style="background:linear-gradient(135deg,#7c3aed,#6366f1);'
            f'color:#fff;border-radius:6px;padding:2px 9px;font-size:11px;font-weight:800;">'
            f'#{rank}</span>',
            unsafe_allow_html=True,
        )
        r2.markdown(
            f'<span style="background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.25);'
            f'border-radius:6px;padding:2px 7px;font-size:11px;color:#a5b4fc;font-weight:600;">'
            f'{score:.4f}</span>',
            unsafe_allow_html=True,
        )

        _render_cover(cover, height=150)

        # Video player
        if video:
            if st.session_state.get(play_key):
                st.video(video)
                if st.button("✕ Close", key=f"{play_key}_close", use_container_width=True):
                    st.session_state[play_key] = False
                    st.rerun()
            else:
                if st.button("▶ Play", key=f"{play_key}_open", use_container_width=True):
                    st.session_state[play_key] = True
                    st.rerun()

        # Title
        st.markdown(
            f'<p style="font-weight:600;font-size:13px;line-height:1.4;'
            f'display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;'
            f'overflow:hidden;margin:4px 0 2px;color:#e2e8f0;">{title}</p>',
            unsafe_allow_html=True,
        )

        _render_stats(likes, views)
        _render_score_bar(score)

        # Reason tags
        tags_html = " · ".join(
            f'<span style="color:#a78bfa;">{tag}</span>' for tag in reason_tags
        )
        st.markdown(
            f'<div style="font-size:11px;margin:2px 0 6px;line-height:1.4;">✦ {tags_html}</div>',
            unsafe_allow_html=True,
        )

        # Actions
        a1, a2, a3 = st.columns(3)
        with a1:
            if st.button("👍", key=f"{key_prefix}_more_{item_id}",
                         use_container_width=True, help="More like this"):
                st.toast("Noted: more like this!", icon="👍")
        with a2:
            if st.button("👎", key=f"{key_prefix}_less_{item_id}",
                         use_container_width=True, help="Less like this"):
                st.toast("Noted: less like this!", icon="👎")
        with a3:
            if st.button("✕", key=hide_key,
                         use_container_width=True, help="Hide this result"):
                st.session_state[hide_key] = True
                st.rerun()
