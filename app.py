import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="CineMatch · AI Movie Discovery",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:        #020d0f;
    --bg2:       #051214;
    --card:      #071a1e;
    --card2:     #0a2028;
    --card3:     #0d2830;
    --c1:        #0d9488;
    --c2:        #14b8a6;
    --c3:        #2dd4bf;
    --c4:        #67e8f9;
    --gold:      #f59e0b;
    --gold2:     #fbbf24;
    --gold3:     #fde68a;
    --rose:      #fb7185;
    --lime:      #84cc16;
    --blue:      #38bdf8;
    --text:      #f0fafa;
    --muted:     #94a3b8;
    --dim:       #334155;
    --border:    #0f2d35;
    --border2:   #164048;
    --glow:      rgba(20,184,166,0.3);
    --glow2:     rgba(20,184,166,0.12);
    --goldglow:  rgba(245,158,11,0.25);
}

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}
.main .block-container { padding: 0 2rem 3rem 2rem !important; max-width: 1400px !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border2) !important;
    width: 295px !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }

.sb-logo {
    background: linear-gradient(160deg, #041a1e 0%, #020d10 100%);
    padding: 1.6rem 1.3rem 1.1rem;
    border-bottom: 1px solid var(--border2);
    margin-bottom: 1rem;
    position: relative; overflow: hidden;
}
.sb-logo::before {
    content: ''; position: absolute; top: -30%; right: -20%;
    width: 120px; height: 120px;
    background: radial-gradient(circle, rgba(20,184,166,0.2), transparent 70%);
    pointer-events: none;
}
.sb-logo-icon { font-size: 2rem; margin-bottom: 0.4rem; }
.sb-logo-title {
    font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 800;
    background: linear-gradient(135deg, #2dd4bf, #67e8f9);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}
.sb-logo-sub { font-size: 0.7rem; color: var(--dim); margin-top: 0.2rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }

.sb-section-label { font-size: 0.68rem; color: var(--dim); text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; padding: 0 1rem; margin-bottom: 0.5rem; }
.sb-stat-row { display: flex; flex-direction: column; gap: 0.45rem; padding: 0 1rem; }
.sb-stat {
    display: flex; align-items: center; justify-content: space-between;
    background: var(--card); border: 1px solid var(--border2);
    border-radius: 10px; padding: 0.55rem 0.85rem;
    transition: border-color 0.2s;
}
.sb-stat:hover { border-color: var(--c2); }
.sb-stat-label { font-size: 0.74rem; color: var(--muted); font-weight: 500; }
.sb-stat-val { font-family: 'Outfit', sans-serif; font-size: 0.86rem; font-weight: 700; color: var(--c3); }

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, #020f12 0%, #051e24 45%, #030f12 100%);
    border: 1px solid var(--border2);
    border-radius: 24px;
    padding: 3rem 3.5rem 2.5rem;
    margin: 1.5rem 0 2rem;
    position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; top: -50%; right: 5%;
    width: 55%; height: 200%;
    background: radial-gradient(ellipse, rgba(20,184,166,0.15) 0%, transparent 60%);
    pointer-events: none;
}
.hero::after {
    content: ''; position: absolute; bottom: -40%; left: -5%;
    width: 35%; height: 120%;
    background: radial-gradient(ellipse, rgba(245,158,11,0.1) 0%, transparent 60%);
    pointer-events: none;
}
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: rgba(20,184,166,0.12);
    border: 1px solid rgba(45,212,191,0.35);
    border-radius: 50px; padding: 0.28rem 1rem;
    font-size: 0.71rem; font-weight: 700; color: var(--c3);
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 900; line-height: 1.05; letter-spacing: -0.03em;
    background: linear-gradient(130deg, #ffffff 0%, #2dd4bf 35%, #67e8f9 65%, #fbbf24 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}
.hero-sub {
    color: var(--muted); font-size: 1rem; line-height: 1.75;
    max-width: 680px; margin-bottom: 1.8rem;
}
.hero-badges { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.hbadge {
    display: inline-flex; align-items: center; gap: 0.35rem;
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.05em;
    text-transform: uppercase; padding: 0.3rem 0.85rem;
    border-radius: 50px; white-space: nowrap;
}
.hb-teal   { background: rgba(20,184,166,0.15);  border: 1px solid rgba(45,212,191,0.4);  color: var(--c3); }
.hb-gold   { background: rgba(245,158,11,0.15);  border: 1px solid rgba(251,191,36,0.4);  color: var(--gold2); }
.hb-cyan   { background: rgba(56,189,248,0.12);  border: 1px solid rgba(103,232,249,0.35); color: var(--c4); }
.hb-lime   { background: rgba(132,204,22,0.12);  border: 1px solid rgba(163,230,53,0.35); color: #bef264; }
.hb-rose   { background: rgba(251,113,133,0.12); border: 1px solid rgba(251,113,133,0.35); color: var(--rose); }

/* ── KPI STRIP ── */
.kpi-strip { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
.kpi-card {
    background: var(--card); border: 1px solid var(--border2);
    border-radius: 18px; padding: 1.4rem 1.6rem;
    position: relative; overflow: hidden;
    transition: transform 0.25s, border-color 0.25s, box-shadow 0.25s;
}
.kpi-card:hover { transform: translateY(-4px); border-color: var(--c2); box-shadow: 0 14px 36px rgba(20,184,166,0.18); }
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--c1), var(--c3), var(--gold));
}
.kpi-glow {
    position: absolute; top: -20px; right: -20px;
    width: 80px; height: 80px;
    background: radial-gradient(circle, rgba(20,184,166,0.12), transparent 70%);
    pointer-events: none;
}
.kpi-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.kpi-val {
    font-family: 'Outfit', sans-serif; font-size: 1.9rem; font-weight: 800;
    background: linear-gradient(135deg, var(--c3), var(--c4));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1; margin-bottom: 0.35rem;
}
.kpi-val-gold {
    background: linear-gradient(135deg, var(--gold), var(--gold2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.kpi-label { font-size: 0.74rem; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.07em; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--card) !important; border: 1px solid var(--border2) !important;
    border-radius: 14px !important; padding: 5px !important; gap: 4px !important;
    margin-bottom: 1.5rem !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: var(--muted) !important;
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.88rem !important; padding: 0.55rem 1.4rem !important;
    border: none !important; transition: all 0.2s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text) !important; background: rgba(20,184,166,0.08) !important; }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--c1), var(--c2)) !important;
    color: #020d0f !important; font-weight: 800 !important;
    box-shadow: 0 4px 16px rgba(13,148,136,0.5) !important;
}

/* ── INPUTS ── */
.stTextInput input {
    background: var(--card2) !important; border: 1.5px solid var(--border2) !important;
    color: var(--text) !important; border-radius: 12px !important;
    font-size: 1rem !important; padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput input:focus { border-color: var(--c2) !important; box-shadow: 0 0 0 3px rgba(20,184,166,0.2) !important; }
.stNumberInput input { background: var(--card2) !important; border: 1.5px solid var(--border2) !important; color: var(--text) !important; border-radius: 12px !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, var(--c1), var(--c2)) !important;
    color: #020d0f !important; border: none !important;
    border-radius: 12px !important; font-weight: 800 !important;
    font-size: 0.9rem !important; padding: 0.6rem 1.2rem !important;
    transition: all 0.22s !important; box-shadow: 0 4px 16px rgba(13,148,136,0.4) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(20,184,166,0.55) !important; }

/* ── SLIDER ── */
.stSlider [data-baseweb="thumb"] { background: var(--c2) !important; border: 2px solid #020d0f !important; }
.stSlider [data-baseweb="track-fill"] { background: linear-gradient(90deg, var(--c1), var(--c3)) !important; }

/* ── MOVIE CARD ── */
.movie-card {
    background: var(--card); border: 1px solid var(--border2);
    border-radius: 16px; padding: 1.1rem 1.4rem;
    margin-bottom: 0.65rem; display: flex; align-items: center; gap: 1rem;
    transition: all 0.22s; position: relative; overflow: hidden;
}
.movie-card::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
    background: linear-gradient(180deg, var(--c1), var(--gold));
    opacity: 0; transition: opacity 0.22s;
}
.movie-card:hover { border-color: rgba(45,212,191,0.45); box-shadow: 0 8px 28px rgba(20,184,166,0.14); transform: translateX(5px); }
.movie-card:hover::before { opacity: 1; }

.rank-num {
    min-width: 40px; height: 40px;
    background: linear-gradient(135deg, var(--c1), var(--c3));
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 0.88rem; color: #020d0f;
    flex-shrink: 0; box-shadow: 0 4px 14px rgba(13,148,136,0.45);
}
.card-title { font-weight: 700; font-size: 0.95rem; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.card-genres { font-size: 0.75rem; color: var(--muted); margin-top: 0.25rem; }
.genre-tag {
    display: inline-block;
    background: rgba(20,184,166,0.12); border: 1px solid rgba(45,212,191,0.25);
    color: var(--c3); font-size: 0.63rem; font-weight: 700;
    padding: 0.12rem 0.5rem; border-radius: 6px; margin-right: 0.3rem;
    text-transform: uppercase; letter-spacing: 0.04em;
}
.score-teal {
    flex-shrink: 0;
    background: rgba(20,184,166,0.12); border: 1px solid rgba(45,212,191,0.3);
    color: var(--c3); font-size: 0.82rem; font-weight: 700;
    padding: 0.35rem 0.9rem; border-radius: 50px;
    font-family: 'JetBrains Mono', monospace; white-space: nowrap;
}
.score-gold {
    background: rgba(245,158,11,0.12); border: 1px solid rgba(251,191,36,0.35);
    color: var(--gold2);
}

/* ── SECTION HEAD ── */
.sec-head { display: flex; align-items: center; gap: 0.7rem; margin-bottom: 1.2rem; }
.sec-head-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--c1), var(--c3));
    border-radius: 10px; display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0; box-shadow: 0 4px 12px rgba(13,148,136,0.4);
}
.sec-head-text { font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 800; color: var(--text); }
.sec-head-count { margin-left: auto; background: var(--card2); border: 1px solid var(--border2); color: var(--muted); font-size: 0.74rem; font-weight: 600; padding: 0.22rem 0.75rem; border-radius: 50px; }

/* ── INFO / ERROR BOX ── */
.info-box {
    background: rgba(20,184,166,0.07); border: 1px solid rgba(45,212,191,0.25);
    border-left: 3px solid var(--c2); border-radius: 12px;
    padding: 1rem 1.25rem; color: var(--muted); font-size: 0.87rem;
    line-height: 1.65; margin-bottom: 1.4rem;
}
.info-box b { color: var(--text); }
.err-box {
    background: rgba(251,113,133,0.07); border: 1px solid rgba(251,113,133,0.3);
    border-left: 3px solid var(--rose); border-radius: 12px;
    padding: 1rem 1.25rem; color: #fda4af; font-size: 0.87rem;
}

/* ── MATCHED PILL ── */
.matched-pill {
    background: rgba(20,184,166,0.08); border: 1px solid rgba(45,212,191,0.28);
    border-radius: 12px; padding: 0.85rem 1.2rem; margin-bottom: 1.2rem;
    display: flex; align-items: center; gap: 0.75rem;
}
.matched-pill-title { font-weight: 700; color: var(--text); font-size: 0.95rem; }
.matched-pill-genre { font-size: 0.78rem; color: var(--muted); margin-top: 0.15rem; }

/* ── USER METRIC ── */
.u-metric {
    background: var(--card); border: 1px solid var(--border2);
    border-radius: 16px; padding: 1.3rem; text-align: center;
    position: relative; overflow: hidden;
}
.u-metric::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--c1), var(--gold));
}
.u-metric-val {
    font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800;
    background: linear-gradient(135deg, var(--c3), var(--c4));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.u-metric-label { font-size: 0.73rem; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.07em; margin-top: 0.3rem; }

/* ── QUICK PICKS LABEL ── */
.qp-label { font-size: 0.72rem; color: var(--dim); font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.6rem; }

/* ── DIVIDER ── */
.fancy-divider { height: 1px; background: linear-gradient(90deg, transparent, var(--border2) 30%, var(--border2) 70%, transparent); margin: 2rem 0; }

/* ── CHART TITLE ── */
.chart-title { font-size: 0.82rem; color: var(--muted); font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem; }

/* ── RATED CHIP ── */
.rated-chip { display: inline-block; background: var(--card2); border: 1px solid var(--border2); color: var(--muted); font-size: 0.78rem; font-weight: 500; padding: 0.3rem 0.75rem; border-radius: 8px; margin: 0.2rem; }

/* ── SVD CARD ── */
.svd-card { background: var(--card); border: 1px solid var(--border2); border-radius: 16px; padding: 1.2rem 1.4rem; }
.svd-card-val { font-family: 'Outfit', sans-serif; font-size: 1.6rem; font-weight: 800; background: linear-gradient(135deg, var(--c3), var(--c4)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.svd-card-label { font-size: 0.71rem; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.2rem; }

/* ── RMSE CALLOUT ── */
.rmse-callout {
    background: linear-gradient(135deg, rgba(20,184,166,0.1), rgba(245,158,11,0.06));
    border: 1px solid rgba(45,212,191,0.28); border-radius: 18px; padding: 1.5rem 1.8rem;
}
.rmse-val {
    font-family: 'Outfit', sans-serif; font-size: 2.6rem; font-weight: 900;
    background: linear-gradient(135deg, var(--c3), var(--gold2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* ── EMPTY STATE ── */
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-state-icon { font-size: 4rem; margin-bottom: 1rem; opacity: 0.4; }
.empty-state-text { font-size: 0.95rem; color: var(--muted); margin-top: 0.5rem; }

/* ── FOOTER ── */
.footer { text-align: center; padding: 2rem 0 0.5rem; color: var(--dim); font-size: 0.76rem; line-height: 1.8; }
.footer a { color: var(--c3); text-decoration: none; }
.footer-divider { height: 1px; background: linear-gradient(90deg, transparent, var(--border2) 30%, var(--border2) 70%, transparent); margin: 0 0 1.5rem; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--c1); border-radius: 4px; }

div[data-testid="stToolbar"] { visibility: hidden; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


from recommender import (
    load_data, build_user_item_matrix, build_content_model,
    build_collab_model, get_content_recommendations,
    get_collab_recommendations, compute_rmse,
)

@st.cache_data(show_spinner=False)
def cached_load_data():
    return load_data()

@st.cache_data(show_spinner=False)
def cached_uim(_r):
    return build_user_item_matrix(_r)

@st.cache_data(show_spinner=False)
def cached_content(_m):
    return build_content_model(_m)

@st.cache_data(show_spinner=False)
def cached_collab(_m):
    return build_collab_model(_m)

@st.cache_data(show_spinner=False)
def cached_rmse(_r, _m):
    return compute_rmse(_r, _m)


with st.spinner("⚡ Initialising CineMatch…"):
    movies, ratings = cached_load_data()
    uim              = cached_uim(ratings)
    tfidf_matrix, csim = cached_content(movies)
    svd_model, pred_df = cached_collab(uim)

avg_rating = round(ratings["rating"].mean(), 2)
n_users    = ratings["userId"].nunique()
n_movies   = len(movies)
n_ratings  = len(ratings)
density    = round(100 * n_ratings / (n_users * n_movies), 2)


with st.sidebar:
    st.markdown(f"""
    <div class="sb-logo">
        <div class="sb-logo-icon">🎬</div>
        <div class="sb-logo-title">CineMatch</div>
        <div class="sb-logo-sub">AI Movie Discovery Engine</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sb-section-label' style='margin-top:0.2rem'>⚙️ Controls</div>", unsafe_allow_html=True)
    n_recs = st.slider("Recommendations (N)", min_value=3, max_value=20, value=10, step=1)

    st.markdown("<div class='sb-section-label' style='margin-top:1rem'>📊 Dataset Stats</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="sb-stat-row">
        <div class="sb-stat"><span class="sb-stat-label">🎬 Movies</span><span class="sb-stat-val">{n_movies:,}</span></div>
        <div class="sb-stat"><span class="sb-stat-label">⭐ Ratings</span><span class="sb-stat-val">{n_ratings:,}</span></div>
        <div class="sb-stat"><span class="sb-stat-label">👤 Users</span><span class="sb-stat-val">{n_users:,}</span></div>
        <div class="sb-stat"><span class="sb-stat-label">📈 Avg Rating</span><span class="sb-stat-val">{avg_rating}/5</span></div>
        <div class="sb-stat"><span class="sb-stat-label">🧩 Density</span><span class="sb-stat-val">{density}%</span></div>
        <div class="sb-stat"><span class="sb-stat-label">📏 Scale</span><span class="sb-stat-val">0.5 – 5.0 ★</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='padding:1.2rem 1rem 0'>
        <div style='height:1px;background:linear-gradient(90deg,transparent,#164048,transparent);margin-bottom:1rem'></div>
        <div class='sb-section-label'>Developer</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin:0 1rem 1rem;background:linear-gradient(135deg,rgba(20,184,166,0.1),rgba(245,158,11,0.07));border:1px solid rgba(45,212,191,0.28);border-radius:14px;padding:1rem 1.1rem;position:relative;overflow:hidden'>
        <div style='position:absolute;top:-20px;right:-20px;width:70px;height:70px;background:radial-gradient(circle,rgba(20,184,166,0.18),transparent 70%);pointer-events:none'></div>
        <div style='font-family:Outfit,sans-serif;font-size:0.95rem;font-weight:800;color:#f0fafa;letter-spacing:-0.01em;margin-bottom:0.6rem'>Krishna Sarraf</div>
        <div style='display:flex;flex-direction:column;gap:0.3rem'>
            <div style='font-size:0.73rem;color:#94a3b8;font-weight:500'>VIT Vellore</div>
            <div style='font-size:0.73rem;color:#94a3b8;font-weight:500'>B.Tech CSE &middot; 3rd Year</div>
            <a href='https://github.com/KRISHNASARRAF13' target='_blank'
               style='font-size:0.73rem;color:#2dd4bf;font-weight:600;text-decoration:none;margin-top:0.3rem;display:flex;align-items:center;gap:0.35rem'>
                <svg width='13' height='13' viewBox='0 0 24 24' fill='currentColor'><path d='M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z'/></svg>
                github.com/KRISHNASARRAF13
            </a>
        </div>
    </div>
    <div style='padding:0 1rem 0.8rem;text-align:center'>
        <p style='font-size:0.63rem;color:#1e3a44;line-height:1.9'>
            <b style='color:#2d4a54'>Dataset:</b> MovieLens ml-latest-small<br>
            Harper &amp; Konstan (2015) &middot; ACM TIIS
        </p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🚀 CineMatch · AI Movie Discovery · MovieLens 2025</div>
    <div class="hero-title">CineMatch<br><span style="font-size:0.55em;font-weight:700;letter-spacing:0.02em;opacity:0.85">AI Movie Discovery Engine</span></div>
    <p class="hero-sub">
        A production-grade movie recommendation system fusing
        <strong style="color:#2dd4bf">Content-Based Filtering</strong> (TF-IDF + Cosine Similarity)
        with <strong style="color:#fbbf24">Collaborative Filtering</strong> (Truncated SVD Matrix Factorization)
        — validated against the MovieLens benchmark by Harper &amp; Konstan (2015).
    </p>
    <div class="hero-badges">
        <span class="hbadge hb-teal">TF-IDF Vectorizer</span>
        <span class="hbadge hb-gold">SVD · 20 Components</span>
        <span class="hbadge hb-cyan">Cosine Similarity</span>
        <span class="hbadge hb-lime">RMSE Validated</span>
        <span class="hbadge hb-rose">Scikit-Learn</span>
        <span class="hbadge hb-teal">Streamlit</span>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown(f"""
<div class="kpi-strip">
    <div class="kpi-card">
        <div class="kpi-glow"></div>
        <div class="kpi-icon">🎬</div>
        <div class="kpi-val">{n_movies:,}</div>
        <div class="kpi-label">Total Movies</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-glow"></div>
        <div class="kpi-icon">⭐</div>
        <div class="kpi-val">{n_ratings:,}</div>
        <div class="kpi-label">Total Ratings</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-glow"></div>
        <div class="kpi-icon">👥</div>
        <div class="kpi-val">{n_users:,}</div>
        <div class="kpi-label">Active Users</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-glow"></div>
        <div class="kpi-icon">✨</div>
        <div class="kpi-val kpi-val-gold">{avg_rating}</div>
        <div class="kpi-label">Avg Star Rating</div>
    </div>
</div>
""", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs([
    "🎯  Content-Based",
    "👤  Personalised SVD",
    "📊  Analytics & Insights",
])


with tab1:
    st.markdown("""
    <div class="info-box">
        <b>How it works:</b> Enter any movie title to find similar films using
        <b>TF-IDF genre vectorisation</b> and <b>cosine similarity</b> across all
        9,742 movies in the MovieLens catalogue. Supports partial title matching.
    </div>
    """, unsafe_allow_html=True)

    c_inp, c_btn = st.columns([5, 1])
    with c_inp:
        movie_input = st.text_input("ms", placeholder="🔍  Search a movie — e.g. Toy Story, Inception, Interstellar…", label_visibility="collapsed")
    with c_btn:
        search_btn = st.button("Search", use_container_width=True)

    st.markdown("<div class='qp-label'>⚡ Quick Picks</div>", unsafe_allow_html=True)
    qp_list = ["Toy Story", "Pulp Fiction", "The Matrix", "Forrest Gump", "Interstellar", "The Dark Knight"]
    qp_cols = st.columns(6)
    qs = None
    for i, qp in enumerate(qp_list):
        with qp_cols[i]:
            if st.button(qp, key=f"qp{i}", use_container_width=True):
                qs = qp

    query = qs if qs else (movie_input.strip() if (search_btn or movie_input.strip()) else None)

    if query:
        with st.spinner(f"Finding movies similar to **{query}**…"):
            res = get_content_recommendations(query, movies, csim, n=n_recs)

        if res.empty:
            st.markdown(f"""
            <div class="err-box">
                ❌ &nbsp;No match for <b>"{query}"</b> in the 9,742-movie catalogue.<br>
                Try a partial title: <i>"Dark"</i>, <i>"Star"</i>, <i>"Love"</i>…
            </div>""", unsafe_allow_html=True)
        else:
            match = movies[movies["title"].str.lower().str.contains(query.lower(), regex=False)]
            if not match.empty:
                mt = match.iloc[0]["title"]
                mg = match.iloc[0]["genres"]
                genre_pills = "".join([f"<span class='genre-tag'>{g}</span>" for g in mg.split("|")])
                st.markdown(f"""
                <div class="matched-pill">
                    <div style='font-size:1.4rem'>🎬</div>
                    <div>
                        <div class="matched-pill-title">{mt}</div>
                        <div class="matched-pill-genre">{genre_pills}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="sec-head">
                <div class="sec-head-icon">✨</div>
                <div class="sec-head-text">Similar Movies</div>
                <div class="sec-head-count">{len(res)} results</div>
            </div>""", unsafe_allow_html=True)

            for i, row in res.iterrows():
                gp = "".join([f"<span class='genre-tag'>{g}</span>" for g in row["genres"].split("|")[:3]])
                st.markdown(f"""
                <div class="movie-card">
                    <div class="rank-num">#{i+1}</div>
                    <div style='flex:1;min-width:0'>
                        <div class="card-title">{row['title']}</div>
                        <div class="card-genres">{gp}</div>
                    </div>
                    <div class="score-teal">{row['similarity_score']:.4f}</div>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🎬</div>
            <div style="font-size:1.05rem;color:#94a3b8;font-weight:600">Discover Similar Movies</div>
            <div class="empty-state-text">Search for any movie or tap a Quick Pick above</div>
        </div>""", unsafe_allow_html=True)


with tab2:
    st.markdown("""
    <div class="info-box">
        <b>How it works:</b> <b>Truncated SVD</b> decomposes the 610 × 9,742 user-item matrix
        into <b>20 latent factors</b>, capturing hidden taste preferences. Movies already rated
        are masked — only fresh, high-predicted films are recommended.
        Rating scale: <b>0.5 – 5.0 ★ (half-star)</b>.
    </div>
    """, unsafe_allow_html=True)

    valid_users = sorted(pred_df.index.tolist())
    min_u, max_u = int(min(valid_users)), int(max(valid_users))

    cu, cbtn = st.columns([4, 1])
    with cu:
        uid_input = st.number_input(f"User ID ({min_u} – {max_u})", min_value=min_u, max_value=max_u, value=min_u, step=1)
    with cbtn:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("🚀 Generate", use_container_width=True)

    uid = int(uid_input)
    with st.spinner(f"Personalising for User {uid}…"):
        cr = get_collab_recommendations(uid, pred_df, uim, movies, n=n_recs)

    if cr.empty:
        st.markdown(f"""<div class="err-box">❌ User <b>{uid}</b> not found. Valid range: {min_u}–{max_u}.</div>""", unsafe_allow_html=True)
    else:
        existing  = uim.loc[uid]
        rated_cnt = int((existing > 0).sum())

        m1, m2, m3 = st.columns(3)
        for col, val, lbl in [(m1, uid, "User ID"), (m2, rated_cnt, "Movies Rated"), (m3, n_recs, "New Picks")]:
            with col:
                st.markdown(f"""<div class="u-metric"><div class="u-metric-val">{val}</div><div class="u-metric-label">{lbl}</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="sec-head">
            <div class="sec-head-icon">🌟</div>
            <div class="sec-head-text">Personalised Picks</div>
            <div class="sec-head-count">{len(cr)} recommendations</div>
        </div>""", unsafe_allow_html=True)

        for i, row in cr.iterrows():
            pr = row["predicted_rating"]
            filled = round(pr * 2) / 2
            full_s = int(filled)
            half_s = 1 if (filled - full_s) >= 0.5 else 0
            stars  = "★" * full_s + ("½" if half_s else "") + "☆" * (5 - full_s - half_s)
            gp = "".join([f"<span class='genre-tag'>{g}</span>" for g in row["genres"].split("|")[:3]])
            st.markdown(f"""
            <div class="movie-card">
                <div class="rank-num">#{i+1}</div>
                <div style='flex:1;min-width:0'>
                    <div class="card-title">{row['title']}</div>
                    <div class="card-genres">{gp}</div>
                    <div style="font-size:0.78rem;color:#f59e0b;margin-top:0.3rem;letter-spacing:0.04em">{stars}</div>
                </div>
                <div class="score-teal score-gold">★ {pr:.3f}</div>
            </div>""", unsafe_allow_html=True)

        rated_ids    = existing[existing > 0].index.tolist()[:8]
        rated_titles = movies[movies["movieId"].isin(rated_ids)]["title"].tolist()
        if rated_titles:
            st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.72rem;color:#1e3a44;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem'>📼 Previously Rated by User {uid}</div>", unsafe_allow_html=True)
            chips = "".join([f"<span class='rated-chip'>{t}</span>" for t in rated_titles])
            st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)


with tab3:
    rmse_val     = cached_rmse(ratings, uim)
    avg_per_user = round(n_ratings / n_users, 1)
    explained    = svd_model.explained_variance_ratio_
    total_var    = round(float(np.sum(explained)) * 100, 2)

    ka, kb, kc, kd = st.columns(4)
    for col, icon, val, lbl in [
        (ka, "🎬", f"{n_movies:,}", "Total Movies"),
        (kb, "⭐", f"{n_ratings:,}", "Total Ratings"),
        (kc, "👥", f"{avg_per_user}", "Avg Ratings / User"),
        (kd, "🎯", f"{rmse_val}", "SVD RMSE"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="margin-bottom:0">
                <div class="kpi-glow"></div>
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-val">{val}</div>
                <div class="kpi-label">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cl, cr2 = st.columns([3, 2])
    with cl:
        st.markdown("<div class='chart-title'>⭐ Rating Distribution · 0.5 – 5.0 Half-Star Scale</div>", unsafe_allow_html=True)
        rdist = ratings["rating"].value_counts().sort_index()
        rdf   = pd.DataFrame({"Rating": rdist.index.astype(str), "Count": rdist.values}).set_index("Rating")
        st.bar_chart(rdf, color="#14b8a6", height=260)

    with cr2:
        st.markdown("<div class='chart-title'>🎭 Top 10 Genres in Catalogue</div>", unsafe_allow_html=True)
        gseries = (movies["genres"].str.split("|").explode()
                   .replace("(no genres listed)", pd.NA).dropna()
                   .value_counts().head(10))
        gdf = pd.DataFrame({"Count": gseries}).rename_axis("Genre")
        st.bar_chart(gdf, color="#f59e0b", height=260)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    ca, cb = st.columns(2)
    with ca:
        st.markdown("<div class='chart-title'>👤 Top 20 Most Active Users</div>", unsafe_allow_html=True)
        top_u = ratings.groupby("userId").size().nlargest(20)
        st.bar_chart(pd.DataFrame({"Ratings": top_u}).rename_axis("User ID"), color="#2dd4bf", height=220)
    with cb:
        st.markdown("<div class='chart-title'>🎬 Top 20 Most-Rated Movies</div>", unsafe_allow_html=True)
        top_m = (ratings.groupby("movieId").size().nlargest(20).reset_index()
                 .merge(movies[["movieId", "title"]], on="movieId"))
        top_m = top_m.set_index("title")[0].rename("Ratings")
        st.bar_chart(pd.DataFrame({"Ratings": top_m}), color="#67e8f9", height=220)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="sec-head">
        <div class="sec-head-icon">🔬</div>
        <div class="sec-head-text">SVD Model Details</div>
    </div>""", unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    for col, val, lbl in [
        (s1, "20", "Latent Components"),
        (s2, f"{total_var}%", "Variance Explained"),
        (s3, f"{uim.shape[0]:,}", "Users in Matrix"),
        (s4, f"{uim.shape[1]:,}", "Items in Matrix"),
    ]:
        with col:
            st.markdown(f"""<div class="svd-card"><div class="svd-card-val">{val}</div><div class="svd-card-label">{lbl}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>📉 Explained Variance % per SVD Component</div>", unsafe_allow_html=True)
    ev_df = pd.DataFrame({
        "Component": [f"C{i+1}" for i in range(len(explained))],
        "Variance %": [round(float(v)*100, 3) for v in explained]
    }).set_index("Component")
    st.bar_chart(ev_df, color="#0d9488", height=160)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    col_r, col_i = st.columns([1, 2])
    with col_r:
        st.markdown(f"""
        <div class="rmse-callout" style="text-align:center;height:100%">
            <div style="font-size:0.7rem;color:#1e4d50;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.5rem">SVD RMSE Score</div>
            <div class="rmse-val">{rmse_val}</div>
            <div style="font-size:0.75rem;color:#4a7a7e;margin-top:0.4rem">lower = better accuracy</div>
        </div>""", unsafe_allow_html=True)
    with col_i:
        st.markdown(f"""
        <div class="info-box" style="height:100%;margin-bottom:0">
            <b>📐 RMSE Evaluation</b><br>
            An <b>80/20 train-test split</b> on the {n_ratings:,} observed ratings was used to
            evaluate SVD prediction accuracy on the <b>0.5 – 5.0 half-star scale</b>.<br><br>
            <b>Reference:</b> Harper, F.M. &amp; Konstan, J.A. (2015).
            <i>The MovieLens Datasets: History and Context.</i>
            ACM Transactions on Interactive Intelligent Systems, 5(4), Article 19.
            DOI: 10.1145/2827872
        </div>""", unsafe_allow_html=True)


st.markdown("""
<div class="footer-divider"></div>
<div style='background:linear-gradient(135deg,rgba(20,184,166,0.06),rgba(245,158,11,0.04));border:1px solid rgba(45,212,191,0.2);border-radius:18px;padding:1.6rem 2rem;margin-bottom:1rem;text-align:center'>
    <div style='font-family:Outfit,sans-serif;font-size:1.15rem;font-weight:800;background:linear-gradient(135deg,#2dd4bf,#fbbf24);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-0.01em;margin-bottom:0.4rem'>Krishna Sarraf</div>
    <div style='display:flex;justify-content:center;align-items:center;gap:2rem;flex-wrap:wrap;margin-bottom:0.75rem'>
        <span style='font-size:0.82rem;color:#94a3b8;font-weight:600'>VIT Vellore</span>
        <span style='font-size:0.82rem;color:#94a3b8;font-weight:600'>B.Tech CSE &middot; 3rd Year</span>
        <a href='https://github.com/KRISHNASARRAF13' target='_blank'
           style='display:inline-flex;align-items:center;gap:0.4rem;font-size:0.82rem;font-weight:700;color:#2dd4bf;text-decoration:none;background:rgba(20,184,166,0.1);border:1px solid rgba(45,212,191,0.3);padding:0.3rem 0.85rem;border-radius:50px;transition:all 0.2s'>
            <svg width='14' height='14' viewBox='0 0 24 24' fill='currentColor'><path d='M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z'/></svg>
            KRISHNASARRAF13
        </a>
    </div>
    <div class="footer-divider" style='margin:0.8rem 0'></div>
    <div class="footer" style='padding:0'>
        Dataset: <a href="https://grouplens.org/datasets/movielens/" target="_blank">MovieLens ml-latest-small</a>
        &nbsp;&middot;&nbsp; Harper &amp; Konstan (2015) &middot; ACM TIIS
    </div>
</div>
""", unsafe_allow_html=True)
