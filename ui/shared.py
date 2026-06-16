"""Shared layout, state and visual helpers."""

from __future__ import annotations

import html

import streamlit as st

from core.rsa_service import generate_keys


def init_session_state() -> None:
    defaults = {
        "rsa_keys": generate_keys(3, 11, 3),
        "simulation_mode": "Nhập số",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');

        :root {
            --ink: #10233d;
            --muted: #64748b;
            --navy: #071a33;
            --blue: #176bda;
            --cyan: #20b9ca;
            --lime: #c4ee78;
            --paper: #f6f8fc;
            --line: #dce5f1;
            --soft-blue: #eaf4ff;
            --soft-cyan: #e9fbfc;
            --soft-green: #eef9df;
        }

        html, body, [class*="css"] {
            font-family: "Be Vietnam Pro", sans-serif;
        }

        .stApp {
            color: var(--ink);
            background:
                radial-gradient(circle at 92% 3%, rgba(32,185,202,.12), transparent 28rem),
                radial-gradient(circle at 8% 88%, rgba(23,107,218,.08), transparent 30rem),
                var(--paper);
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2.2rem;
            padding-bottom: 5rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(165deg, #06162b 0%, #0b2949 68%, #0d4058 100%);
            border-right: 1px solid rgba(255,255,255,.08);
        }

        [data-testid="stSidebar"] * { color: #eef7ff; }

        [data-testid="stSidebar"] .stRadio label {
            width: 100%;
            background: rgba(255,255,255,.04);
            border: 1px solid rgba(255,255,255,.08);
            border-radius: 14px;
            padding: .72rem .82rem;
            margin-bottom: .42rem;
            transition: 150ms ease;
        }

        [data-testid="stSidebar"] .stRadio label:hover {
            background: rgba(32,185,202,.15);
            border-color: rgba(32,185,202,.4);
            transform: translateX(2px);
        }

        .brand { margin: .25rem 0 1.6rem; }
        .brand-mark {
            width: 48px;
            height: 48px;
            display: grid;
            place-items: center;
            border-radius: 15px;
            color: white;
            background: linear-gradient(135deg, var(--cyan), var(--blue));
            font-family: "JetBrains Mono", monospace;
            font-weight: 800;
            box-shadow: 0 12px 28px rgba(32,185,202,.24);
            margin-bottom: .8rem;
        }
        .brand-title { color: white; font-size: 1.15rem; font-weight: 800; }
        .brand-subtitle {
            color: #a9bfd2;
            font-size: .76rem;
            line-height: 1.55;
            margin-top: .3rem;
        }
        .sidebar-group {
            color: #8faac1;
            font-size: .68rem;
            font-weight: 800;
            letter-spacing: .12em;
            text-transform: uppercase;
            margin: 1.2rem 0 .5rem;
        }

        .hero {
            position: relative;
            overflow: hidden;
            border-radius: 28px;
            padding: 2.35rem 2.45rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(125deg, #071a33 0%, #0d3459 65%, #0f6373 100%);
            box-shadow: 0 24px 60px rgba(8,26,51,.16);
        }
        .hero::after {
            content: "";
            position: absolute;
            width: 320px;
            height: 320px;
            right: -100px;
            top: -160px;
            border: 1px solid rgba(196,238,120,.34);
            border-radius: 50%;
            box-shadow: 0 0 0 38px rgba(32,185,202,.055), 0 0 0 76px rgba(32,185,202,.03);
        }
        .eyebrow {
            position: relative;
            z-index: 1;
            color: var(--lime);
            font-size: .75rem;
            font-weight: 800;
            letter-spacing: .14em;
            text-transform: uppercase;
            margin-bottom: .72rem;
        }
        .hero h1 {
            position: relative;
            z-index: 1;
            max-width: 900px;
            color: white;
            font-size: clamp(2rem, 4vw, 3.45rem);
            line-height: 1.08;
            letter-spacing: -.045em;
            margin: 0;
        }
        .hero p {
            position: relative;
            z-index: 1;
            max-width: 800px;
            color: #c7d8e7;
            font-size: 1rem;
            line-height: 1.75;
            margin: 1rem 0 0;
        }

        .page-title { margin-bottom: 1.35rem; }
        .page-title .eyebrow { color: var(--blue); margin-bottom: .45rem; }
        .page-title h1 {
            color: var(--ink);
            font-size: clamp(1.75rem, 3vw, 2.65rem);
            line-height: 1.15;
            letter-spacing: -.04em;
            margin: 0;
        }
        .page-title p {
            max-width: 820px;
            color: var(--muted);
            line-height: 1.72;
            margin: .65rem 0 0;
        }

        .learning-map {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: .62rem;
            margin: 1rem 0 1.6rem;
        }
        .map-item {
            background: rgba(255,255,255,.9);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: .85rem;
            min-height: 105px;
            box-shadow: 0 10px 28px rgba(16,35,61,.04);
        }
        .map-item span {
            display: grid;
            place-items: center;
            width: 27px;
            height: 27px;
            border-radius: 9px;
            color: var(--blue);
            background: var(--soft-blue);
            font-size: .72rem;
            font-weight: 800;
        }
        .map-item strong { display: block; font-size: .82rem; margin-top: .6rem; }
        .map-item small { color: var(--muted); font-size: .7rem; line-height: 1.4; }

        .definition-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .8rem;
            margin: .9rem 0 1.4rem;
        }
        .definition-card, .formula-card, .note-card {
            background: rgba(255,255,255,.9);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1rem 1.08rem;
            box-shadow: 0 12px 32px rgba(16,35,61,.045);
        }
        .definition-card .symbol {
            color: var(--blue);
            font-family: "JetBrains Mono", monospace;
            font-size: 1.15rem;
            font-weight: 800;
        }
        .definition-card strong { display: block; margin: .48rem 0 .25rem; }
        .definition-card p, .note-card p {
            color: var(--muted);
            font-size: .82rem;
            line-height: 1.58;
            margin: 0;
        }

        .formula-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: .8rem;
            margin: 1rem 0 1.4rem;
        }
        .formula-label {
            color: var(--muted);
            font-size: .7rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: .09em;
        }
        .formula-value {
            color: var(--navy);
            font-family: "JetBrains Mono", monospace;
            font-weight: 700;
            font-size: 1rem;
            line-height: 1.55;
            margin-top: .42rem;
        }

        .analogy {
            border-radius: 20px;
            padding: 1.15rem 1.3rem;
            background: linear-gradient(135deg, #eaf8fb, #edf4ff);
            border: 1px solid #cfe6ed;
            color: #23445f;
            line-height: 1.65;
            margin: 1rem 0;
        }
        .analogy strong { color: #0c5970; }

        .section-label {
            color: var(--ink);
            font-size: 1.18rem;
            font-weight: 800;
            letter-spacing: -.025em;
            margin: 1.55rem 0 .6rem;
        }

        .step-card {
            background: rgba(255,255,255,.92);
            border: 1px solid var(--line);
            border-left: 5px solid var(--blue);
            border-radius: 19px;
            padding: 1.15rem 1.25rem;
            margin: 1rem 0 .8rem;
            box-shadow: 0 13px 35px rgba(16,35,61,.05);
        }
        .step-card.success { border-left-color: #1aa675; }
        .step-card.warning { border-left-color: #f0a328; }
        .step-head { display: flex; gap: .85rem; align-items: flex-start; }
        .step-number {
            flex: 0 0 auto;
            width: 38px;
            height: 38px;
            display: grid;
            place-items: center;
            border-radius: 12px;
            background: var(--soft-blue);
            color: var(--blue);
            font-family: "JetBrains Mono", monospace;
            font-weight: 800;
        }
        .step-title { font-weight: 800; font-size: 1.05rem; }
        .step-description {
            color: var(--muted);
            font-size: .82rem;
            line-height: 1.55;
            margin-top: .25rem;
        }
        .substeps {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .65rem;
            margin: .85rem 0 1.1rem;
        }
        .substep {
            background: #f8fafc;
            border: 1px solid #e1e8f1;
            border-radius: 14px;
            padding: .78rem .85rem;
            color: #40536b;
            font-size: .77rem;
            line-height: 1.5;
        }
        .substep b { color: var(--blue); }

        .key-card {
            color: white;
            background: #071a33;
            border-radius: 18px;
            padding: 1.08rem 1.18rem;
            min-height: 112px;
            box-shadow: 0 16px 35px rgba(8,26,51,.14);
        }
        .key-card.private { background: linear-gradient(135deg, #123c52, #08727e); }
        .key-card .label {
            color: #a5bfd2;
            font-size: .7rem;
            font-weight: 800;
            letter-spacing: .09em;
            text-transform: uppercase;
        }
        .key-card code {
            display: block;
            color: #dffb9e;
            background: transparent !important;
            border: 0 !important;
            padding: 0 !important;
            font-family: "JetBrains Mono", monospace;
            font-size: 1rem;
            margin-top: .72rem;
        }

        .result-banner {
            border-radius: 20px;
            padding: 1.2rem 1.35rem;
            background: linear-gradient(135deg, #e9f8ef, #f4fbe7);
            border: 1px solid #cfe8d3;
            color: #215b3d;
            line-height: 1.6;
            margin: 1rem 0;
        }
        .result-banner strong { display: block; font-size: 1.08rem; margin-bottom: .2rem; }

        div[data-testid="stMetric"] {
            background: rgba(255,255,255,.9);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: .85rem 1rem;
            box-shadow: 0 10px 28px rgba(16,35,61,.045);
        }
        div[data-testid="stMetricValue"] {
            color: var(--ink);
            font-family: "JetBrains Mono", monospace;
        }

        .stButton > button {
            border-radius: 12px;
            border: 1px solid var(--blue);
            min-height: 2.72rem;
            font-weight: 700;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--blue), #1354b5);
            box-shadow: 0 9px 22px rgba(23,107,218,.18);
        }
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div {
            border-radius: 12px;
            border-color: #cfdbea;
            background: rgba(255,255,255,.92);
        }
        [data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 15px;
            overflow: hidden;
        }
        .footer-note {
            color: #8291a6;
            text-align: center;
            font-size: .72rem;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid var(--line);
        }

        @media (max-width: 900px) {
            .learning-map, .definition-grid, .formula-grid, .substeps {
                grid-template-columns: 1fr;
            }
            .hero { padding: 1.65rem; border-radius: 22px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_brand() -> None:
    st.sidebar.markdown(
        """
        <div class="brand">
            <div class="brand-mark">R</div>
            <div class="brand-title">RSA Learning Lab</div>
            <div class="brand-subtitle">
                Học lý thuyết và quan sát toàn bộ thuật toán RSA từng bước.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_title(kicker: str, title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="page-title">
            <div class="eyebrow">{html.escape(kicker)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(description)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_step(number: int, title: str, description: str, state: str = "") -> None:
    css_state = f" {state}" if state else ""
    st.markdown(
        f"""
        <div class="step-card{css_state}">
            <div class="step-head">
                <div class="step-number">{number:02d}</div>
                <div>
                    <div class="step-title">{html.escape(title)}</div>
                    <div class="step-description">{html.escape(description)}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_substeps(items: list[tuple[str, str]]) -> None:
    content = "".join(
        f'<div class="substep"><b>{html.escape(label)}</b><br>{html.escape(text)}</div>'
        for label, text in items
    )
    st.markdown(f'<div class="substeps">{content}</div>', unsafe_allow_html=True)


def render_key_cards(keys: dict) -> None:
    public_key = keys["public_key"]
    private_key = keys["private_key"]
    col_public, col_private = st.columns(2)
    with col_public:
        st.markdown(
            f"""
            <div class="key-card">
                <div class="label">Khóa công khai · có thể chia sẻ</div>
                <code>(e, n) = ({public_key["e"]}, {public_key["n"]})</code>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_private:
        st.markdown(
            f"""
            <div class="key-card private">
                <div class="label">Khóa bí mật · chỉ người nhận giữ</div>
                <code>(d, n) = ({private_key["d"]}, {private_key["n"]})</code>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_footer() -> None:
    st.markdown(
        """
        <div class="footer-note">
            Mô phỏng dùng số nhỏ để học. RSA thực tế cần khóa lớn, padding an toàn
            như OAEP và thư viện mật mã đã được kiểm chứng.
        </div>
        """,
        unsafe_allow_html=True,
    )
