"""
app.py
------
WebTrust AI — Financial Website Risk Intelligence Platform.

Entry point for the Streamlit application.

Pages
-----
  Home               — Product overview, features, workflow, and about section.
  Login              — Module 2: authentication form.
  Analyst Detection  — Module 4: analyst-facing URL analysis interface.
  URL Analysis       — Module 1: standalone URL validation view (legacy).

Navigation is managed via Streamlit's st.navigation (Streamlit ≥ 1.29).
The sidebar nav is hidden; each page renders its own top bar.
Access control is enforced at the top of each protected page
(analyst_detection.py, url_analysis.py) — not only in the UI.

Run
---
    .venv\\Scripts\\Activate.ps1
    py -m streamlit run app.py

Security notes
--------------
- The URL validation and analysis pages perform NO network requests.
- DNS checking is a separate, explicitly triggered operation.
- Credentials are loaded from environment variables at startup.
- Session state is used for authentication; it is per-session, not persistent.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration  (must be the very first Streamlit call in the app)
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="WebTrust AI",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Page definitions
# ---------------------------------------------------------------------------

home_page = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠",
    default=True,
)

login_page = st.Page(
    "pages/login.py",
    title="Sign In",
    icon="🔑",
)

analyst_detection_page = st.Page(
    "pages/analyst_detection.py",
    title="Analyze URL",
    icon="🔍",
)

url_analysis_page = st.Page(
    "pages/url_analysis.py",
    title="URL Validation",
    icon="🔗",
)

# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
# position="hidden" — each page renders its own branded top bar.
# The Streamlit built-in nav sidebar is suppressed to keep the UI clean.

pg = st.navigation(
    [home_page, login_page, analyst_detection_page, url_analysis_page],
    position="hidden",
)

pg.run()
