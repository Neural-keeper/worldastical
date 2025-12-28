import streamlit as st
import base64
from pathlib import Path

def _load_base64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()

def inject_theme():
    parchment = _load_base64("assets/parchment.jpg")
    font = _load_base64("assets/gothic.ttf")
    sidebar_parchment = _load_base64("assets/parchment_sidebar.jpg")

    st.markdown(
        f"""
        <style>

        /* --- Gothic Font --- */
        @font-face {{
            font-family: 'Gothic';
            src: url(data:font/ttf;base64,{font}) format('truetype');
        }}

        /* --- Global Text --- */
        html, body, [class*="css"] {{
            font-family: 'Gothic', serif;
        }}

        /* --- App Background (Darkened Parchment) --- */
        .stApp {{
            background:
                linear-gradient(
                    rgba(20, 15, 10, 0.88),
                    rgba(20, 15, 10, 0.88)
                ),
                url("data:image/jpg;base64,{parchment}");
            background-size: cover;
            background-attachment: fixed;
        }}

        /* --- Headers --- */
        h1, h2, h3 {{
            letter-spacing: 0.1em;
            color: #f1e6d3;
            border-bottom: 1px solid #8a6a3f;
            padding-bottom: 0.35em;
        }}

        /* --- Inputs --- */
        textarea, input, select {{
            background-color: rgba(35, 28, 20, 0.9) !important;
            color: #f1e6d3 !important;
            border: 1px solid #8a6a3f !important;
        }}

        textarea::placeholder,
        input::placeholder {{
            color: #b9a98f;
        }}

        /* --- Markdown / Manuscript Panels --- */
        .stMarkdown {{
            background-color: rgba(30, 24, 18, 0.85);
            padding: 1.3em;
            border: 1px solid #8a6a3f;
            box-shadow: inset 0 0 12px rgba(0,0,0,0.6);
        }}

        /* --- Sidebar --- */
        section[data-testid="stSidebar"] {{
            background-color: rgba(18, 14, 10, 0.95);
            border-right: 1px solid #5a4428;
        }}

        /* --- Buttons --- */
        button {{
            background-color: #3a2b1c !important;
            color: #f1e6d3 !important;
            border: 1px solid #8a6a3f !important;
            letter-spacing: 0.05em;
        }}

        button:hover {{
            background-color: #4a3724 !important;
            border-color: #c0a46a !important;
        }}

        /* --- Dividers --- */
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(
                to right,
                transparent,
                #8a6a3f,
                transparent
            );
            margin: 1.5em 0;
        }}

        /* --- Page Width & Manuscript Rhythm --- */
        .main .block-container {{
            max-width: 900px;
            padding-top: 3rem;
            padding-bottom: 4rem;
            line-height: 1.75;
        }}

        /* Paragraph spacing like a printed book */
        .stMarkdown p {{
            margin-bottom: 1.1em;
        }}

        /* --- Illuminated Drop Cap --- */
        .stMarkdown p:first-of-type::first-letter {{
            float: left;
            font-size: 3.2em;
            line-height: 1;
            padding-right: 0.12em;
            padding-top: 0.08em;
            color: #c9a35f;
            text-shadow:
                0 0 6px rgba(201,163,95,0.4),
                0 0 14px rgba(0,0,0,0.8);
        }}

        /* --- Header Sigils --- */
        h2 {{
            position: relative;
            padding-left: 3.2rem;
        }}

        /* Default sigil (fallback) */
        h2::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 50%;
            width: 2.2rem;
            height: 2.2rem;
            transform: translateY(-50%);
            opacity: 0.22;
            background-size: contain;
            background-repeat: no-repeat;
        }}

        /* --- SIDEBAR PARCHMENT --- */
        section[data-testid="stSidebar"] {{
            background-image: url("data:image/jpg;base64,{sidebar_parchment}");
            background-size: cover;
            background-position: center;
            border-right: 1px solid rgba(139,111,71,0.4);
        }}

        /* Sidebar content spacing */
        section[data-testid="stSidebar"] > div {{
            padding-top: 2rem;
        }}

        /* Sidebar text */
        section[data-testid="stSidebar"] * {{
            color: #e6dcc6;
            font-family: 'Gothic', serif;
        }}

        /* Sidebar navigation items */
        section[data-testid="stSidebar"] a {{
            text-decoration: none;
            padding: 0.4rem 0.6rem;
            border-radius: 4px;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }}

        section[data-testid="stSidebar"] a:hover {{
            background-color: rgba(139,111,71,0.15);
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

