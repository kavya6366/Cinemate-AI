
import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

        :root {
            --background: #0b0d12;
            --surface: #131720;
            --surface-light: #1a202b;
            --accent: #a78bfa;
            --text: #f4f5f9;
            --muted: #9ba3b5;
        }

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        .stApp {
            background: var(--background);
            color: var(--text);
        }

        [data-testid="stHeader"] {
            background: rgba(11, 13, 18, 0.92);
        }

        [data-testid="stSidebar"] {
            background: #10131a;
            border-right: 1px solid #252b37;
        }

        .block-container {
            max-width: 1220px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif !important;
            letter-spacing: -0.6px;
        }

        p {
            line-height: 1.7;
        }

        .brand {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 25px;
            font-weight: 700;
            letter-spacing: -1px;
            color: #ffffff;
        }

        .brand span {
            color: #b7a0ff;
        }

        .eyebrow {
            color: #b7a0ff;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2.2px;
            text-transform: uppercase;
            margin-bottom: 16px;
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 64px 48px;
            margin: 20px 0 30px;
            border-radius: 24px;
            border: 1px solid #303044;
            background:
                radial-gradient(ellipse at 85% 20%, rgba(128, 91, 220, .25), transparent 36%),
                radial-gradient(ellipse at 70% 100%, rgba(65, 95, 165, .19), transparent 38%),
                linear-gradient(135deg, #1a1b2b 0%, #11141e 56%, #171321 100%);
        }

        .hero h1 {
            max-width: 720px;
            font-size: clamp(38px, 5vw, 66px);
            line-height: 1.08;
            font-weight: 700;
            margin: 12px 0 20px;
            color: #ffffff;
        }

        .hero h1 span {
            color: #b7a0ff;
        }

        .hero p {
            max-width: 610px;
            font-size: 17px;
            color: #c2c6d4;
            margin-bottom: 26px;
        }

        .hero-note {
            color: #d4c8ff;
            font-size: 12px;
            letter-spacing: 1px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .section-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 27px;
            font-weight: 700;
            color: #f6f5fb;
            margin: 24px 0 6px;
        }

        .section-subtitle {
            color: #9ba3b5;
            font-size: 14px;
            margin-bottom: 22px;
        }

        .feature-card {
            height: 175px;
            padding: 23px;
            border: 1px solid #292f3d;
            border-radius: 17px;
            background: linear-gradient(145deg, #171c26, #11151d);
        }

        .feature-icon {
            font-size: 26px;
            margin-bottom: 15px;
        }

        .feature-card h3 {
            font-size: 17px;
            color: #f5f5fa;
            margin-bottom: 8px;
        }

        .feature-card p {
            font-size: 13px;
            color: #a5adbd;
            margin: 0;
        }

        .stat-card {
            background: #131720;
            border: 1px solid #282e3a;
            border-radius: 14px;
            padding: 20px;
            margin: 8px 0;
        }

        .stat-label {
            color: #9ba3b5;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stat-value {
            color: #ffffff;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 25px;
            font-weight: 700;
            margin-top: 8px;
        }

        .info-panel {
            background: #151925;
            border: 1px solid #2b3040;
            border-radius: 18px;
            padding: 25px;
            margin-top: 18px;
        }

        .info-panel h3 {
            font-size: 20px;
            color: #f5f5fa;
        }

        .info-panel p {
            color: #aab1c0;
            font-size: 14px;
        }

        div.stButton > button {
            background: #b7a0ff;
            color: #171221;
            border: 1px solid #b7a0ff;
            border-radius: 10px;
            padding: 11px 22px;
            font-size: 15px;
            font-weight: 700;
            min-height: 45px;
            transition: all 0.2s ease;
        }

        div.stButton > button:hover {
            background: #d0c1ff;
            border-color: #d0c1ff;
            color: #171221;
            transform: translateY(-1px);
        }

        div[data-testid="stVerticalBlock"] div[data-testid="stForm"] {
            background: #131720;
            border: 1px solid #292f3d;
            padding: 22px;
            border-radius: 16px;
        }

        input, textarea {
            background: #11151d !important;
            color: #f5f5fa !important;
        }

        [data-testid="stMetric"] {
            background: #131720;
            padding: 17px;
            border: 1px solid #292f3d;
            border-radius: 13px;
        }

        [data-testid="stMetricValue"] {
            color: #f6f4ff;
        }

        hr {
            border-color: #292f3d;
        }

        .footer {
            text-align: center;
            padding: 28px 10px 5px;
            color: #777f90;
            font-size: 12px;
            border-top: 1px solid #242a35;
            margin-top: 45px;
        }

        @media (max-width: 700px) {
            .hero {
                padding: 36px 24px;
            }

            .hero h1 {
                font-size: 39px;
            }

            .hero p {
                font-size: 15px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
