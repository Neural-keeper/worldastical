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

        @font-face {{
            font-family: 'Gothic';
            src: url(data:font/ttf;base64,{font}) format('truetype');
        }}

        html, body, [class*="css"] {{
            font-family: 'Gothic', serif;
            color: #2b1b0f;
        }}

        .stApp {{
            background-image: url("data:image/jpg;base64,{parchment}");
            background-size: cover;
            background-attachment: fixed;
        }}

        h1, h2, h3 {{
            letter-spacing: 0.08em;
            border-bottom: 2px solid #5a3b1c;
            padding-bottom: 0.3em;
        }}

        textarea, input, select {{
            background-color: rgba(250, 240, 215, 0.85) !important;
            border: 1px solid #5a3b1c !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )
