"""MicroLens Recommender Workbench – Streamlit entrypoint.

Launch with:
    streamlit run src/app.py

Architecture:
    src/app.py              ← this file (navigation shell only)
    src/pages/explore.py   ← Explore screen
    src/components/         ← reusable UI components
    src/state/session.py    ← session state API
    src/data/               ← data loading / mock data
    src/services/           ← recommender logic (future)
"""

from __future__ import annotations

# ── sys.path fix ──────────────────────────────────────────────────────────────
# Streamlit adds the script's directory (src/) to sys.path, not the project
# root.  Insert the root so that `from src.xxx` resolves correctly.
import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

import streamlit as st

# ── One-time data bootstrap (download + extract covers) ───────────────────────
@st.cache_resource(show_spinner="Preparing dataset…")
def _bootstrap_data():
    import zipfile
    from pathlib import Path

    root = Path(__file__).parent.parent
    data_dir = root / "microlens-5k"
    data_dir.mkdir(exist_ok=True)

    covers_dir = data_dir / "covers"
    zip_path   = data_dir / "covers.zip"

    # ── 1. Download covers.zip from Google Drive if not present ───────────
    if not covers_dir.exists() and not zip_path.exists():
        try:
            import gdown
            # Public Google Drive folder – downloads its contents into data_dir
            gdown.download_folder(
                "https://drive.google.com/drive/folders/1DXLfYCKWzbkE0mq7TMurNjhFa_ICRSrz",
                output=str(data_dir),
                quiet=True,
                use_cookies=False,
            )
        except Exception:
            pass  # graceful degradation: covers will show as placeholder

    # ── 2. Extract covers.zip if it was just downloaded (or already existed) ─
    if not covers_dir.exists() and zip_path.exists():
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(data_dir)

_bootstrap_data()

from src.state.session import init_session

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MicroLens Workbench",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global styles ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ── Hide Streamlit chrome ── */
    [data-testid="stSidebarNav"] { display: none; }
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    html, body, [class*="css"] { font-family: "Inter", sans-serif; }

    /* ── Custom scrollbar ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.35); border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.65); }

    /* ── Card containers (border=True) ── */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
        border: 1px solid rgba(99,102,241,0.18) !important;
        background: rgba(15,23,42,0.82) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        overflow: hidden;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 18px 44px rgba(0,0,0,0.48), 0 0 0 1px rgba(99,102,241,0.38) !important;
        border-color: rgba(99,102,241,0.45) !important;
    }

    /* ── Text inputs ── */
    [data-testid="stTextInput"] input {
        border-radius: 8px !important;
        border-color: rgba(99,102,241,0.3) !important;
        background: rgba(15,23,42,0.7) !important;
        transition: border-color 0.15s, box-shadow 0.15s;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: rgba(99,102,241,0.7) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
    }

    /* ── Select boxes ── */
    [data-testid="stSelectbox"] > div > div {
        border-radius: 8px !important;
        border-color: rgba(99,102,241,0.3) !important;
    }

    /* ── Dividers ── */
    hr[data-testid="stDivider"] {
        border-color: rgba(99,102,241,0.14) !important;
    }

    /* ── Sidebar shell ── */
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 0;
    }

    /* ── Nav buttons ── */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        padding: 9px 14px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        color: inherit;
        transition: background 0.15s ease, transform 0.15s ease;
        margin-bottom: 2px;
    }
    section[data-testid="stSidebar"] .stButton > button > div {
        justify-content: flex-start !important;
        width: 100%;
    }
    section[data-testid="stSidebar"] .stButton > button p {
        text-align: left !important;
        margin: 0 !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(99,102,241,0.12) !important;
        transform: translateX(3px);
    }
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(99,102,241,0.22), rgba(139,92,246,0.18)) !important;
        color: #a5b4fc !important;
        font-weight: 700;
        border-left: 3px solid #6366f1 !important;
    }

    /* ── Sidebar info card ── */
    .sidebar-info-card {
        background: rgba(99,102,241,0.07);
        border: 1px solid rgba(99,102,241,0.18);
        border-radius: 10px;
        padding: 10px 14px;
        margin-top: 4px;
        transition: border-color 0.2s;
    }
    .sidebar-info-card:hover { border-color: rgba(99,102,241,0.35); }
    .sidebar-info-card .label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: .08em;
        text-transform: uppercase;
        color: #6366f1;
        margin-bottom: 3px;
    }
    .sidebar-info-card .value {
        font-size: 14px;
        font-weight: 600;
    }

    /* ── Page hero ── */
    .page-hero {
        margin-bottom: 18px;
        padding-bottom: 14px;
        border-bottom: 1px solid rgba(99,102,241,0.12);
    }
    .page-hero h1 {
        margin: 0 0 4px;
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(130deg, #e2e8f0 30%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }
    .page-hero p {
        margin: 0;
        color: #64748b;
        font-size: 13px;
    }

    /* ── Stat chips ── */
    .chip { display:inline-flex; align-items:center; gap:4px; padding:2px 9px;
            border-radius:99px; font-size:11px; font-weight:600; }
    .chip-views { background:rgba(59,130,246,.12); color:#93c5fd; border:1px solid rgba(59,130,246,.2); }
    .chip-likes { background:rgba(239,68,68,.12);  color:#fca5a5; border:1px solid rgba(239,68,68,.2); }
    .chip-video { background:rgba(16,185,129,.12); color:#6ee7b7; border:1px solid rgba(16,185,129,.2); }

    /* ── Score progress bar ── */
    .score-bar { margin: 5px 0 7px; }
    .score-bar-header { display:flex; justify-content:space-between;
                        font-size:10px; color:#64748b; margin-bottom:3px; }
    .score-bar-bg { background:rgba(255,255,255,.05); border-radius:3px; height:4px; overflow:hidden; }
    .score-bar-fill { height:100%; border-radius:3px;
                      background:linear-gradient(90deg,#6366f1,#a78bfa); }

    /* ── Stats banner ── */
    .stats-banner {
        display: flex; gap: 12px; flex-wrap: wrap;
        padding: 10px 14px;
        background: rgba(99,102,241,0.06);
        border: 1px solid rgba(99,102,241,0.14);
        border-radius: 10px;
        margin-bottom: 14px;
    }
    .stats-banner-item { font-size: 12px; color: #94a3b8; }
    .stats-banner-item b { color: #e2e8f0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session init ──────────────────────────────────────────────────────────────
init_session()

# ── Navigation ────────────────────────────────────────────────────────────────
pages = {
    "🔍 Explore": "src/pages/explore.py",
    "⭐ Recommend": "src/pages/recommend.py",
    "📊 Compare Models": "src/pages/compare.py",
    "🔬 Inspect Item": "src/pages/inspect.py",
}

with st.sidebar:
    # ── Brand ────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;padding:0 4px 4px;">'
        '<span style="font-size:26px;">🎬</span>'
        '<div><p style="margin:0;font-size:18px;font-weight:700;line-height:1.1;">MicroLens</p>'
        '<p style="margin:0;font-size:11px;color:#94a3b8;letter-spacing:.05em;">REC WORKBENCH</p></div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    # ── Navigation ───────────────────────────────────────────────────────
    _PAGES = [
        ("🔍", "Explore"),
        ("⭐", "Recommend"),
    ]
    _PAGE_KEYS = [f"{icon} {label}" for icon, label in _PAGES]
    if "nav_selection" not in st.session_state:
        st.session_state["nav_selection"] = _PAGE_KEYS[0]

    for (icon, label), key in zip(_PAGES, _PAGE_KEYS):
        _active = st.session_state["nav_selection"] == key
        _btn_type = "primary" if _active else "secondary"
        if st.button(
            f"{icon}  {label}",
            key=f"nav_{key}",
            use_container_width=True,
            type=_btn_type,
        ):
            st.session_state["nav_selection"] = key
            st.rerun()

    st.divider()

    # ── Context info ─────────────────────────────────────────────────────
    from src.state.session import seed_count, get_selected_user
    n = seed_count()
    uid = get_selected_user()

    st.markdown(
        f'<div class="sidebar-info-card">'
        f'<div class="label">Active User</div>'
        f'<div class="value">👤 {uid if uid else "— None —"}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sidebar-info-card" style="margin-top:8px;">'
        f'<div class="label">Seeds Selected</div>'
        f'<div class="value">🌱 {n}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if n > 0 and st.session_state["nav_selection"] != "⭐ Recommend":
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        if st.button("🚀 Run Recommendations", key="sidebar_run", use_container_width=True):
            st.session_state["nav_selection"] = "⭐ Recommend"
            st.rerun()

selection = st.session_state.get("nav_selection", "🔍 Explore")

# ── Page dispatch ─────────────────────────────────────────────────────────────
if selection == "🔍 Explore":
    from src.pages.explore import render
    render()

elif selection == "⭐ Recommend":
    from src.pages.recommend import render as render_recommend
    render_recommend()
