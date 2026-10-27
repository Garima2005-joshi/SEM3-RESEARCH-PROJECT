"""
pages/analyst_detection.py
--------------------------
Module 4 — Analyst Detection Interface.

This is the primary analyst-facing page where a security analyst submits a
suspicious URL and views the assessment produced by currently integrated modules.

Access control
--------------
Requires authentication (analyst or admin role).
The admin researcher dashboard is NOT shown here.
Research-only model comparison metrics are never displayed on this page.

Current capabilities
---------------------
- URL validation (Module 1: fully implemented).
- Traditional URL feature extraction (Module 5: fully implemented).
- Website security analysis: not yet integrated.
- ML phishing classification: not yet integrated.

Integration contract for teammates
------------------------------------
When Module 3 (website security extraction) is ready, call it here by importing
and calling the agreed interface function. The Tab 3 skeleton is already defined.

When the ML models are ready, call them via the agreed interface. Display only
the analyst-facing result. Do not expose Model 1 vs. Model 2 comparison metrics
on this page.

Session state keys used
------------------------
  wt_analysis_url       — the URL that was most recently analysed
  wt_analysis_result    — ValidationResult for that URL
  wt_analysis_features  — FeatureResult for that URL (None if invalid)
"""

import streamlit as st

from modules.styles import inject_css
from modules.access_control import require_analyst_or_admin
from modules.authentication import (
    get_current_display_name,
    get_current_role,
    logout,
    ROLE_ADMIN,
)
from modules.url_validator import validate_url, ValidationResult
from modules.feature_extractor import extract_features, FeatureResult

# ---------------------------------------------------------------------------
# Access control — must be the first executed statement after imports
# ---------------------------------------------------------------------------

require_analyst_or_admin()

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

inject_css()

# ---------------------------------------------------------------------------
# Top navigation bar
# ---------------------------------------------------------------------------

_display_name = get_current_display_name()
_role = get_current_role()
_role_label = "Researcher / Admin" if _role == ROLE_ADMIN else "Security Analyst"

nav_brand, nav_right = st.columns([4, 2])

with nav_brand:
    st.markdown(
        """
        <div class="wt-topbar" style="padding-bottom:0.8rem;">
            <div class="wt-brand">
                <span style="font-size:1.4rem;">🛡️</span>
                <div>
                    <div class="wt-brand-name">WebTrust AI</div>
                    <div class="wt-brand-sub">Financial Website Risk Intelligence</div>
                </div>
            </div>
            <span class="badge" style="background:#DBEAFE;color:#1D4ED8;font-size:0.7rem;">
                URL Analysis
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_right:
    st.markdown("<div style='padding-top:1.15rem;'>", unsafe_allow_html=True)
    nb1, nb2 = st.columns(2)
    with nb1:
        if st.button("← Home", type="secondary", use_container_width=True):
            st.switch_page("pages/home.py")
    with nb2:
        if st.button("Sign out", type="secondary", use_container_width=True):
            logout()
            st.switch_page("pages/home.py")
    st.markdown("</div>", unsafe_allow_html=True)

# User context line
st.markdown(
    f"""
    <div style="text-align:right; font-size:0.8rem; color:#64748B;
                margin-top:-0.6rem; margin-bottom:0.6rem;">
        Signed in as <strong style="color:#475569;">{_display_name}</strong>
        &nbsp;&middot;&nbsp; {_role_label}
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Page title and description
# ---------------------------------------------------------------------------

st.markdown(
    """
    <div style="margin-bottom:1.2rem;">
        <h2 style="font-size:1.5rem;font-weight:800;color:#0F172A;
                   letter-spacing:-0.02em;margin:0 0 0.3rem 0;">
            Analyze a Suspicious URL
        </h2>
        <p style="font-size:0.88rem;color:#64748B;margin:0;line-height:1.5;">
            Submit a suspicious URL for structured analysis. The platform validates URL
            structure and extracts traditional features. No network requests are made.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# URL input area — compact
# ---------------------------------------------------------------------------

input_col, btn_col = st.columns([5, 1])
with input_col:
    url_input = st.text_input(
        label="URL to analyze",
        placeholder="https://suspicious-example.com/login",
        label_visibility="collapsed",
        help="Enter the complete URL. No network requests are made during analysis.",
        key="url_input_field",
    )
with btn_col:
    analyze_clicked = st.button(
        "Analyze", type="primary", use_container_width=True
    )

st.markdown(
    """
    <div class="wt-notice" style="margin-top:0.5rem;margin-bottom:0.8rem;">
        <strong>Notice:</strong>
        URL validation checks structure and destination restrictions only.
        A syntactically valid URL or an HTTPS scheme does not prove the destination
        is trustworthy — phishing sites routinely obtain valid certificates.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Run analysis and store in session state
# ---------------------------------------------------------------------------
# Analysis is run when the button is clicked and the result is cached in
# session state so that switching between tabs does not re-run validation
# or wipe the URL input.

_SK_URL      = "wt_analysis_url"
_SK_RESULT   = "wt_analysis_result"
_SK_FEATURES = "wt_analysis_features"

if analyze_clicked:
    if not url_input or not url_input.strip():
        st.error(
            "No URL entered. Please type a URL in the field above and click **Analyze**."
        )
        st.stop()

    _vr: ValidationResult = validate_url(url_input)
    _fr: FeatureResult | None = extract_features(_vr) if _vr.is_valid else None

    st.session_state[_SK_URL]      = url_input.strip()
    st.session_state[_SK_RESULT]   = _vr
    st.session_state[_SK_FEATURES] = _fr

# Retrieve whatever is stored (may be None on first load)
_stored_url: str | None                = st.session_state.get(_SK_URL)
result: ValidationResult | None        = st.session_state.get(_SK_RESULT)
features: FeatureResult | None         = st.session_state.get(_SK_FEATURES)

# Nothing to show yet
if result is None:
    st.stop()

st.markdown('<hr class="wt-divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Summary strip — always visible once analysis has run
# ---------------------------------------------------------------------------

_v_badge  = '<span class="badge badge-valid">Valid</span>'   if result.is_valid \
            else '<span class="badge badge-invalid">Invalid</span>'

# Domain legitimacy: not assessed — URL structural validation never implies
# domain ownership or brand authenticity.
_leg_badge = '<span class="badge badge-notchk">Not Assessed</span>'

# ML classification: not yet integrated.
_ml_badge  = '<span class="badge badge-notchk">Not Available</span>'

# Destination status: read the actual value returned by the validator.
# The validator sets this to "not_checked" by default and only changes it
# when a DNS check is explicitly requested.  Never override with a
# hardcoded "verified" label.
_dest_strip_meta = {
    "not_checked":            ("badge-notchk",  "Not Checked"),
    "blocked":                ("badge-blocked",  "Blocked"),
    "destination_unverified": ("badge-unverif",  "Unverified"),
    "verified_for_policy":    ("badge-verified", "Verified for Policy"),
}
_dest_strip_cls, _dest_strip_label = _dest_strip_meta.get(
    result.destination_status,
    ("badge-notchk", result.destination_status),
)
_dest_strip_badge = (
    f'<span class="badge {_dest_strip_cls}">{_dest_strip_label}</span>'
)

st.markdown(
    f"""
    <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:10px;
                padding:0.9rem 1.4rem;margin-bottom:1.2rem;
                display:flex;gap:2rem;flex-wrap:wrap;align-items:center;">
        <div>
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.08em;
                        text-transform:uppercase;color:#64748B;margin-bottom:0.3rem;">
                URL Validation
            </div>
            {_v_badge}
        </div>
        <div>
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.08em;
                        text-transform:uppercase;color:#64748B;margin-bottom:0.3rem;">
                Destination Status
            </div>
            {_dest_strip_badge}
        </div>
        <div>
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.08em;
                        text-transform:uppercase;color:#64748B;margin-bottom:0.3rem;">
                Domain Legitimacy
            </div>
            {_leg_badge}
        </div>
        <div>
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.08em;
                        text-transform:uppercase;color:#64748B;margin-bottom:0.3rem;">
                ML Phishing Classification
            </div>
            {_ml_badge}
        </div>
        <div style="margin-left:auto;font-size:0.8rem;color:#64748B;
                    font-family:'Consolas','Courier New',monospace;
                    overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
                    max-width:280px;" title="{_stored_url or ''}">
            {_stored_url or ''}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# If validation failed, show errors and stop — do not show tabs
if not result.is_valid:
    if result.errors:
        for err in result.errors:
            st.markdown(
                f'<div class="wt-alert wt-alert-error">'
                f'<span class="wt-alert-label">Validation error:</span>{err}</div>',
                unsafe_allow_html=True,
            )
    if result.warnings:
        for warn in result.warnings:
            st.markdown(
                f'<div class="wt-alert wt-alert-warn">'
                f'<span class="wt-alert-label">Warning:</span>{warn}</div>',
                unsafe_allow_html=True,
            )
    st.markdown(
        """
        <div class="wt-notice" style="margin-top:0.6rem;">
            The URL did not pass validation. Analysis cannot proceed for an invalid
            or prohibited URL. Correct the URL and try again.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# Validation warnings (non-fatal) shown above the tabs for valid URLs
if result.warnings:
    for warn in result.warnings:
        st.markdown(
            f'<div class="wt-alert wt-alert-warn">'
            f'<span class="wt-alert-label">Warning:</span>{warn}</div>',
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# Four-tab analysis interface
# ---------------------------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    ["🔗 URL Components", "📊 Traditional Features", "🔒 Website Security", "🤖 ML Detection"]
)

# ============================================================================
# TAB 1 — URL Components
# ============================================================================

with tab1:

    port_display = (
        f'<span class="wt-field-value">{result.port}</span>'
        if result.port is not None
        else '<span class="wt-field-value muted">Not specified</span>'
    )
    path_display = (
        f'<span class="wt-field-value">{result.path}</span>'
        if result.path
        else '<span class="wt-field-value muted">/</span>'
    )
    https_badge = (
        '<span class="badge badge-https">HTTPS</span>'
        if result.uses_https
        else '<span class="badge badge-http">HTTP — unencrypted</span>'
    )
    host_type_badge = (
        '<span class="badge badge-ip">IP address</span>'
        if result.is_ip_address
        else '<span class="badge badge-host">Hostname</span>'
    )

    _status_meta = {
        "not_checked":            ("badge-notchk",  "Not checked",
                                   "No destination verification has been performed."),
        "blocked":                ("badge-blocked",  "Blocked",
                                   "Destination falls within a prohibited address range."),
        "destination_unverified": ("badge-unverif",  "Unverified",
                                   "A DNS check was attempted but could not confirm the destination."),
        "verified_for_policy":    ("badge-verified", "Verified for policy",
                                   "DNS check passed policy — not a safety certificate."),
    }
    dest_cls, dest_label, dest_explain = _status_meta.get(
        result.destination_status,
        ("badge-notchk", result.destination_status, ""),
    )
    dest_badge = f'<span class="badge {dest_cls}">{dest_label}</span>'

    st.markdown(
        f"""
        <div class="wt-card">
            <p class="wt-card-title">URL Components</p>
            <div class="wt-grid">
                <div class="wt-field">
                    <div class="wt-field-label">Scheme</div>
                    <div class="wt-field-value">{result.scheme or '—'}</div>
                </div>
                <div class="wt-field">
                    <div class="wt-field-label">Hostname</div>
                    <div class="wt-field-value">{result.hostname or '—'}</div>
                </div>
                <div class="wt-field">
                    <div class="wt-field-label">Port</div>
                    {port_display}
                </div>
                <div class="wt-field">
                    <div class="wt-field-label">Path</div>
                    {path_display}
                </div>
                <div class="wt-field">
                    <div class="wt-field-label">Encryption</div>
                    {https_badge}
                </div>
                <div class="wt-field">
                    <div class="wt-field-label">Host type</div>
                    {host_type_badge}
                </div>
                <div class="wt-field" style="grid-column: span 2;">
                    <div class="wt-field-label">Destination status</div>
                    <div class="wt-dest-row">
                        {dest_badge}
                        <span class="wt-dest-explain">{dest_explain}</span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="wt-card">
            <div class="wt-status-row">
                <span class="wt-status-label">Domain legitimacy</span>
                <span class="badge badge-notchk">Not Assessed</span>
            </div>
            <span style="font-size:0.85rem;color:#475569;">
                URL structural validation does not verify domain ownership, brand
                authenticity, or registration history. A well-formed hostname is not
                evidence of legitimacy.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================================
# TAB 2 — Traditional Features
# ============================================================================

with tab2:

    if features is None:
        st.info("Feature extraction requires a valid URL.")
    else:
        num  = features.numeric
        desc = features.descriptive

        # ── URL length and structure ────────────────────────────────────────
        st.markdown(
            f"""
            <div class="wt-card">
                <p class="wt-card-title">URL Length and Structure</p>
                <div class="wt-grid">
                    <div class="wt-field">
                        <div class="wt-field-label">Total URL length</div>
                        <div class="wt-field-value">{num["url_length"]} characters</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Path length</div>
                        <div class="wt-field-value">{num["url_path_length"]} characters</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Query string length</div>
                        <div class="wt-field-value">
                            {"Not present" if not num["flag_has_query"] else f'{num["url_query_length"]} characters'}
                        </div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Query parameters</div>
                        <div class="wt-field-value">{num["url_num_query_params"]}</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Fragment</div>
                        <div class="wt-field-value">
                            {"Present" if num["flag_has_fragment"] else "Not present"}
                        </div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Port</div>
                        <div class="wt-field-value">
                            {"Non-default (" + str(result.port) + ")" if num["flag_has_non_default_port"] else
                             (str(result.port) + " (default)" if result.port else "Not specified")}
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Character counts ────────────────────────────────────────────────
        st.markdown(
            f"""
            <div class="wt-card">
                <p class="wt-card-title">Character Counts</p>
                <div class="wt-grid">
                    <div class="wt-field">
                        <div class="wt-field-label">Dots (.)</div>
                        <div class="wt-field-value">{num["char_count_dot"]}</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Hyphens (-)</div>
                        <div class="wt-field-value">{num["char_count_hyphen"]}</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Underscores (_)</div>
                        <div class="wt-field-value">{num["char_count_underscore"]}</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Slashes (/)</div>
                        <div class="wt-field-value">{num["char_count_slash"]}</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Percent-encoded (%)</div>
                        <div class="wt-field-value">{num["char_count_percent"]}</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">At-sign (@)</div>
                        <div class="wt-field-value">{num["char_count_at"]}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Hostname and domain features ────────────────────────────────────
        _reg_dom_display = (
            desc["registered_domain"]
            if desc["registered_domain"] != "unknown"
            else "Could not be determined"
        )
        _sub_display = (
            str(num["host_subdomain_count"])
            if num["host_subdomain_count"] >= 0
            else "N/A"
        )

        st.markdown(
            f"""
            <div class="wt-card">
                <p class="wt-card-title">Hostname and Domain Features</p>
                <div class="wt-grid">
                    <div class="wt-field">
                        <div class="wt-field-label">Hostname length</div>
                        <div class="wt-field-value">{num["url_hostname_length"]} characters</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Hostname labels</div>
                        <div class="wt-field-value">{num["host_num_labels"]}</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Subdomain labels</div>
                        <div class="wt-field-value">{_sub_display}</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Registered domain</div>
                        <div class="wt-field-value">{_reg_dom_display}</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Direct IP address</div>
                        <div class="wt-field-value">{"Yes" if num["flag_is_ip_address"] else "No"}</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">Punycode / IDN</div>
                        <div class="wt-field-value">{"Detected" if num["flag_has_punycode"] else "Not detected"}</div>
                    </div>
                    <div class="wt-field">
                        <div class="wt-field-label">URL shortener</div>
                        <div class="wt-field-value">{"Detected" if num["flag_is_url_shortener"] else "Not detected"}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Keyword indicators ──────────────────────────────────────────────
        _kw_list_display = (
            ", ".join(f"<code>{kw}</code>" for kw in features.keywords_matched)
            if features.keywords_matched
            else "None"
        )
        st.markdown(
            f"""
            <div class="wt-card">
                <p class="wt-card-title">Keyword Indicators</p>
                <p style="font-size:0.83rem;color:#475569;margin:0 0 0.8rem;line-height:1.55;">
                    Potentially relevant keywords found in the URL (case-insensitive).
                    Legitimate websites frequently use these terms — a match is a
                    structural observation, not a phishing verdict.
                </p>
                <div class="wt-field" style="margin-bottom:0.5rem;">
                    <div class="wt-field-label">Keywords matched ({num["kw_num_matched"]})</div>
                    <div class="wt-field-value" style="margin-top:0.25rem;">
                        {_kw_list_display}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Feature extraction warnings (e.g. registered-domain ambiguity)
        if features.warnings:
            for w in features.warnings:
                st.markdown(
                    f'<div class="wt-alert wt-alert-warn">'
                    f'<span class="wt-alert-label">Note:</span>{w}</div>',
                    unsafe_allow_html=True,
                )

        st.markdown(
            """
            <div class="wt-notice">
                <strong>Feature extraction notice:</strong>
                These structural observations are extracted from the URL string and hostname.
                They do not classify this URL as phishing or legitimate. They will supply
                inputs to a machine-learning model when that module is integrated.
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================================
# TAB 3 — Website Security
# ============================================================================

with tab3:
    st.markdown(
        """
        <div class="wt-card" style="border-style:dashed;background:#FAFAFA;">
            <div class="wt-status-row">
                <span class="wt-status-label">Website security analysis</span>
                <span class="badge badge-notchk">Not Available</span>
            </div>
            <p style="font-size:0.83rem;color:#64748B;margin:0 0 0.6rem;line-height:1.55;">
                Website security analysis is not yet integrated. No security-header,
                cookie, or TLS assessment has been performed for this URL.
            </p>
            <p style="font-size:0.82rem;color:#94A3B8;margin:0;line-height:1.5;">
                When this module is integrated it will examine:
                HTTP security headers (HSTS, CSP, X-Frame-Options, …),
                cookie security attributes (Secure, HttpOnly, SameSite), and
                TLS certificate validity and issuer information.
                No findings will be shown until a real analysis has been performed.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================================
# TAB 4 — ML Detection
# ============================================================================

with tab4:
    st.markdown(
        """
        <div class="wt-card" style="border-style:dashed;background:#FAFAFA;">
            <div class="wt-status-row">
                <span class="wt-status-label">ML phishing classification</span>
                <span class="badge badge-notchk">Not Available</span>
            </div>
            <p style="font-size:0.83rem;color:#64748B;margin:0 0 0.6rem;line-height:1.55;">
                Machine-learning phishing classification is not yet available.
                URL validation and traditional feature extraction do not independently
                determine whether a website is legitimate or malicious.
            </p>
            <p style="font-size:0.82rem;color:#94A3B8;margin:0;line-height:1.5;">
                No risk scores, phishing labels, or confidence values will be displayed
                until a validated model produces a real result for this URL.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Overall analyst reminder — shown below the tabs
# ---------------------------------------------------------------------------

st.markdown(
    """
    <div class="wt-notice" style="margin-top:1rem;">
        <strong>Analyst reminder:</strong>
        The findings above are structured technical observations from currently
        integrated modules. They support your investigation but do not independently
        determine whether this URL is legitimate or malicious. Always apply
        professional judgement and additional verification steps as appropriate.
    </div>
    """,
    unsafe_allow_html=True,
)
