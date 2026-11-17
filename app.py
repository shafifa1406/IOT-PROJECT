import requests
import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Pet Smart Collar", page_icon="🐾", layout="wide"
)


# ==========================================
# CUSTOM THEME: CREAM + BURGUNDY
# ==========================================

st.markdown(
    """
<style>

:root {
    --background: #F5F0E9;
    --card: #FFFCF8;
    --burgundy: #722F40;
    --burgundy-dark: #592333;
    --text: #35272A;
    --secondary: #8D7D7D;
    --border: #722F40;
}

/* Main Background & Header */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
header[data-testid="stHeader"] {
    background-color: var(--background) !important;
    color: var(--text) !important;
}

/* Sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background-color: var(--card) !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--burgundy) !important;
}

/* Sidebar Collapse & Expand Buttons */
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stSidebarCollapsedControl"] button,
[data-testid="stExpandSidebarButton"],
[data-testid="stExpandSidebarButton"] button,
header[data-testid="stHeader"] button[kind="header"],
header[data-testid="stHeader"] button[kind="headerNoPadding"] {
    background-color: var(--burgundy) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--burgundy) !important;
    border-radius: 8px !important;
    opacity: 1 !important;
    visibility: visible !important;
}

[data-testid="stSidebarCollapseButton"] button svg,
[data-testid="stSidebarCollapsedControl"] button svg,
[data-testid="stExpandSidebarButton"] svg,
header[data-testid="stHeader"] button svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}

/* Headings & Text */
h1, h2, h3, h4 {
    color: var(--burgundy) !important;
    font-weight: 700 !important;
}

h1 {
    font-size: 38px !important;
}

p, label, [data-testid="stWidgetLabel"] p {
    color: var(--text) !important;
    font-weight: 500;
}

.stCaption {
    color: var(--secondary) !important;
}

/* Inputs */
div[data-baseweb="input"] {
    background-color: var(--card) !important;
    border: 1px solid var(--burgundy) !important;
    border-radius: 8px !important;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}

[data-testid="stNumberInput"] button {
    background-color: var(--burgundy) !important;
    color: #FFFFFF !important;
    border: none !important;
}

[data-testid="stNumberInput"] button:hover {
    background-color: var(--burgundy-dark) !important;
}

/* Custom Location Locked Card (Theme Matched) */
.location-card {
    background-color: #722F40 !important;
    color: #F5F0E9 !important;
    border-radius: 10px;
    padding: 14px 16px;
    margin-top: 10px;
    margin-bottom: 10px;
    border: 1px solid #592333;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

/* KPI Cards & Custom Cards */
[data-testid="stMetric"] {
    background-color: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-top: 4px solid var(--burgundy) !important;
    padding: 20px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: var(--secondary) !important;
}

[data-testid="stMetricValue"] {
    color: var(--burgundy) !important;
    font-weight: 700 !important;
}

.custom-card {
    background-color: var(--card) !important;
    border: 1px solid var(--border);
    border-left: 4px solid var(--burgundy);
    border-radius: 12px;
    padding: 20px;
    min-height: 70px;
    color: var(--burgundy);
}

hr {
    border-color: var(--burgundy) !important;
}

#MainMenu, footer {
    visibility: hidden;
}

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================
# ACCURATE GEOCODING HELPER
# ==========================================


def get_fresh_lat_lon(query):
  if not query or len(query.strip()) < 2:
    return None, None

  url = "https://nominatim.openstreetmap.org/search"
  params = {
      "q": query.strip(),
      "format": "json",
      "limit": 1,
      "addressdetails": 1,
      "dedupe": 1,
  }
  headers = {"User-Agent": "PetSmartCollarApp/2.0"}

  try:
    res = requests.get(url, params=params, headers=headers, timeout=4)
    data = res.json()
    if data and len(data) > 0:
      return float(data[0]["lat"]), float(data[0]["lon"])
  except Exception:
    pass
  return None, None


# ==========================================
# DASHBOARD HEADER
# ==========================================

st.title("🐾 Pet Smart Collar")
st.caption("Real-time Pet Monitoring & Safety Dashboard")
st.divider()


# ==========================================
# SIDEBAR SETTINGS
# ==========================================

with st.sidebar:
  st.header("Settings")
  st.subheader("Geofence Location")

  search_query = st.text_input(
      "Home Address / Location",
      value="Connaught Place, New Delhi",
      placeholder="Type any area, city or landmark...",
  )

  if "current_lat" not in st.session_state:
    st.session_state.current_lat = 28.6139
  if "current_lon" not in st.session_state:
    st.session_state.current_lon = 77.2090
  if "last_query" not in st.session_state:
    st.session_state.last_query = ""

  if search_query and search_query != st.session_state.last_query:
    lat, lon = get_fresh_lat_lon(search_query)
    if lat is not None and lon is not None:
      st.session_state.current_lat = lat
      st.session_state.current_lon = lon
      st.session_state.last_query = search_query

  # Clean, perfectly positioned theme-matched card
  if st.session_state.current_lat and st.session_state.current_lon:
    st.markdown(
        f"""
        <div class="location-card">
            <div style="font-size: 13px; font-weight: 600; color: #F5F0E9; margin-bottom: 4px;">
                📍 Location 
            </div>
            <div style="font-size: 14px; font-weight: 700; color: #FFFFFF;">
                Lat: {st.session_state.current_lat:.4f} &nbsp;|&nbsp; Lon: {st.session_state.current_lon:.4f}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.warning("⚠️ Location not found. Try a more specific name.")

  st.write("")
  radius = st.number_input("Geofence Radius (metres)", value=100, step=10)


# ==========================================
# LIVE OVERVIEW
# ==========================================

st.subheader("Live Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Activity", "WAITING")
col2.metric("GPS Status", "Disconnected")
col3.metric("Speed", "0 km/h")
col4.metric("Alerts", "0")

st.divider()


# ==========================================
# MAIN DASHBOARD
# ==========================================

left, right = st.columns([1.5, 1])

with left:
  st.subheader("Live Location")
  st.markdown(
      """
    <div class="custom-card">
        <span style="color:#722F40; font-weight:600;">
            GPS map will appear here.
        </span>
    </div>
    """,
      unsafe_allow_html=True,
  )

with right:
  st.subheader("Activity Monitoring")
  st.markdown(
      """
    <div class="custom-card">
        <span style="color:#722F40; font-weight:600;">
            Live activity information will appear here.
        </span>
    </div>
    """,
      unsafe_allow_html=True,
  )

st.divider()


# ==========================================
# RECENT ALERTS
# ==========================================

st.subheader("Recent Alerts")

st.markdown(
    """
<div class="custom-card">
    <span style="color:#8D7D7D;">
        No alerts yet.
    </span>
</div>
""",
    unsafe_allow_html=True,
)


# ==========================================
# FOOTER
# ==========================================

st.markdown(
    """
<div style="
    text-align:center;
    color:#8D7D7D;
    font-size:12px;
    padding:20px;
">
    Pet Smart Collar | ESP32 Monitoring System
</div>
""",
    unsafe_allow_html=True,
)