import streamlit as st
import base64
from pathlib import Path

def _load_base64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()

def inject_theme():
    parchment = _load_base64("assets/parchment.jpg")
    font = _load_base64("assets/gothic.ttf")

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
            color: #e6dccf; /* parchment-light ink */
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

        </style>
        """,
        unsafe_allow_html=True
    )

