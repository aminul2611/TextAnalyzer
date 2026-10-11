import streamlit as st
import unicodedata
from st_keyup import st_keyup


# ---------- Page ----------
st.set_page_config(
    page_title="Text Analyzer • Aminul Islam",
    page_icon="🔍",
    layout="centered",
)


# ---------- Colors ----------
BG = "#F3F5FB"
TEXT = "#18233B"
MUTED = "#778198"
PRIMARY = "#635BFF"

STAT_STYLES = [
    ("total_word", "✎  Total word", "#DC2626", "#FFF1F2"),
    ("characters", "▤  Characters", "#0284C7", "#EAF6FF"),
    ("uppercase", "↑  Uppercase", "#059669", "#E7F8F0"),
    ("lowercase", "↓  Lowercase", "#DB2777", "#FDECF5"),
    ("digits", "# No  Digits", "#E11D48", "#FFECEF"),
    ("symbols", "✦  Symbols", "#4F46E5", "#ECEEFF"),
    ("spaces", "↔  Spaces / gaps", "#475569", "#EDF2F7"),
    ("lines", "☰  Lines", "#EA580C", "#FFF1E7"),
]

FUN_MESSAGES = {
    "total_word": "Every character has an ID. No hiding!",
    "characters": "Word squad reporting. Coffee requested!",
    "uppercase": "LOUD agents! Stealth training failed!",
    "lowercase": "Undercover agents. Please whisper!",
    "digits": "Code breakers—or just counting snacks!",
    "symbols": "Special agents with suspicious disguises!",
    "spaces": "Social distancing for secret agents!",
    "lines": "New checkpoint. Same sleepy guard!",
}

MESSAGE_COLORS = {
    "total_word": "#2563EB",
    "characters": "#C026D3",
    "uppercase": "#0284C7",
    "lowercase": "#9333EA",
    "digits": "#1D4ED8",
    "symbols": "#047857",
    "spaces": "#C2410C",
    "lines": "#BE185D",
}


# ---------- Functions ----------
def analyze_text(text):
    return {
        # Your naming:
        # Hello World -> Total word: 10, Characters: 2
        "total_word": sum(
            not char.isspace() for char in text
        ),
        "characters": len(text.split()),
        "uppercase": sum(char.isupper() for char in text),
        "lowercase": sum(char.islower() for char in text),
        "digits": sum(char.isdecimal() for char in text),
        "symbols": sum(
            unicodedata.category(char)[0] in {"P", "S"}
            for char in text
        ),
        "spaces": sum(char.isspace() for char in text),
        "lines": text.count("\n") + 1 if text else 0,
    }


    def clear_text():
        st.session_state["input_version"] = (
                st.session_state.get("input_version", 0) + 1
        )


# ---------- Design ----------
st.markdown(
    f"""
    <style>
        .stApp {{
            background: {BG};
        }}

        .block-container {{
            max-width: 1000px;
            padding-top: 80px;
            padding-bottom: 20px;
        }}

        .brand {{
            border-left: 4px solid {PRIMARY};
            padding: 12px 0 12px 14px;
            margin-bottom: 14px;
        }}

        .brand-tag {{
            color: {PRIMARY};
            font-family: "Segoe UI", sans-serif;
            font-size: 11px;
            font-weight: bold;
        }}

        .brand-title {{
            color: {TEXT};
            font-family: "Segoe UI", sans-serif;
            font-size: 30px;
            font-weight: bold;
            line-height: 1.2;
            margin: 16px 0;
        }}

        .brand-subtitle {{
            color: {MUTED};
            font-family: "Segoe UI", sans-serif;
            font-size: 14px;
            line-height: 1.6;
        }}

        div[data-testid="stTextArea"] textarea {{
            background: #F7F9FD;
            color: {TEXT};
            font-family: "Segoe UI", sans-serif;
            font-size: 14px;
            border-radius: 10px;
        }}

        div[data-testid="stTextArea"] textarea:focus {{
            background: white;
            outline-color: #A59EFF;
        }}

        div[data-testid="stButton"] button {{
            font-family: "Segoe UI", sans-serif;
            border-radius: 9px;
            font-weight: 600;
        }}

        div[data-testid="stButton"] button[kind="primary"] {{
            background: {PRIMARY};
            border-color: {PRIMARY};
            color: white;
        }}

        .input-heading {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            margin-bottom: 5px;
        }}

        .input-title {{
            color: {TEXT};
            font-size: 18px;
            font-weight: bold;
        }}

        .live-badge {{
            color: #047857;
            background: #E7F8F0;
            font-size: 11px;
            font-weight: bold;
            border-radius: 20px;
            padding: 4px 9px;
        }}

        .helper {{
            color: {MUTED};
            font-size: 13px;
            margin-bottom: 8px;
        }}

        .overview {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 16px 0 12px;
        }}

        .overview-title {{
            color: {TEXT};
            font-size: 21px;
            font-weight: bold;
        }}

        .overview-count {{
            color: {MUTED};
            font-size: 12px;
        }}

        .stat-card {{
            padding: 12px 14px;
            border-radius: 12px;
            margin-bottom: 12px;
            box-shadow: 0 2px 6px rgba(24, 35, 59, 0.04);
        }}

        .stat-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
        }}

        .stat-title {{
            font-family: "Segoe UI", sans-serif;
            font-size: 20px;
            font-weight: bold;
        }}

        .stat-value {{
            color: {TEXT};
            font-family: "Segoe UI", sans-serif;
            font-size: 25px;
            font-weight: bold;
            overflow-wrap: anywhere;
        }}

        .stat-message {{
            font-family: Georgia, serif;
            font-size: 16px;
            font-style: italic;
            line-height: 1.5;
            margin-top: 5px;
        }}

        .footer {{
            text-align: center;
            padding: 12px 0;
        }}

        .footer-label {{
            color: {MUTED};
            font-size: 10px;
            font-weight: bold;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }}

        .footer-name {{
            display: inline-block;
            font-family: Georgia, serif;
            font-size: 18px;
            font-weight: bold;
            color: {PRIMARY};
            background: #EFEEFF;
            padding: 8px 14px;
            border-radius: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

def clear_text():
    st.session_state["input_version"] = (
        st.session_state.get("input_version", 0) + 1
    )


# ---------- Heading Left + Input Right ----------
heading_column, input_column = st.columns([2, 3])

with heading_column:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-tag">
                YOUR TEXT. EVERY DETAIL.
            </div>
            <div class="brand-title">
                Text Analyzer
            </div>
            <div class="brand-subtitle">
                Explore your text—with a little undercover humor.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with input_column:
    with st.container(border=True):
        st.markdown(
            """
            <div class="input-heading">
                <span class="input-title">Your text</span>
                <span class="live-badge">● LIVE</span>
            </div>
            <div class="helper">
                A few words. A little insight.
            </div>
            """,
            unsafe_allow_html=True,
        )


        text = st_keyup(
            "Your text",
            value="",
            key=f"live_text_{st.session_state.get('input_version', 0)}",
            debounce=0,
            label_visibility="collapsed",
            placeholder="Type or paste your text...",
        ) or ""

        analyze_column, clear_column = st.columns(2)

        with analyze_column:
            st.button(
                "Analyze →",
                type="primary",
                use_container_width=True,
            )

        with clear_column:
            st.button(
                "Clear",
                on_click=clear_text,
                use_container_width=True,
            )

        if text:
            st.markdown(
                '<div style="color:#059669;font-size:12px;">'
                '● Results updated</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div style="color:{MUTED};font-size:12px;">'
                '● Awaiting input</div>',
                unsafe_allow_html=True,
            )


# ---------- Results ----------
counts = analyze_text(text)

st.markdown(
    """
    <div class="overview">
        <span class="overview-title">Text overview</span>
        <span class="overview-count">8 checkpoints</span>
    </div>
    """,
    unsafe_allow_html=True,
)

for index in range(0, len(STAT_STYLES), 2):
    columns = st.columns(2)

    for column, card in zip(
        columns, STAT_STYLES[index:index + 2]
    ):
        key, title, accent, background = card
        value = counts[key]

        if not text:
            caption = "Agents are on a tea break!"
        elif value == 0:
            caption = "No agents here. Check the cafeteria!"
        else:
            caption = FUN_MESSAGES[key]

        with column:
            st.markdown(
                f"""
                <div class="stat-card"
                     style="background:{background};">
                    <div class="stat-top">
                        <span class="stat-title"
                              style="color:{accent};">
                            {title}
                        </span>
                        <span class="stat-value">
                            {value}
                        </span>
                    </div>
                    <div class="stat-message"
                         style="color:{MESSAGE_COLORS[key]};">
                        {caption}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------- Footer ----------
st.markdown(
    """
    <div class="footer">
        <div class="footer-label">CRAFTED BY</div>
        <div class="footer-name">✦ Aminul Islam ✦</div>
    </div>
    """,
    unsafe_allow_html=True,
)