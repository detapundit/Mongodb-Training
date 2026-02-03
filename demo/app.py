
import streamlit as st
import requests
from datetime import datetime

# --------------------
# Configuration
# --------------------
AGGREGATOR_URL = "http://127.0.0.1:8080"

st.set_page_config(
    page_title="Mongo Observability AI",
    layout="wide",
)

# --------------------
# Helpers
# --------------------
def get_deployments():
    try:
        r = requests.get(f"{AGGREGATOR_URL}/deployments", timeout=5)
        return r.json().get("deployments", [])
    except Exception as e:
        st.error(f"Failed to fetch deployments: {e}")
        return []

def get_summary(deployment_id):
    r = requests.get(
        f"{AGGREGATOR_URL}/summary/{deployment_id}",
        timeout=15
    )
    r.raise_for_status()
    return r.json()

# --------------------
# Sidebar
# --------------------
st.sidebar.title("Mongo AI Observability")

deployments = get_deployments()
deployment_id = st.sidebar.selectbox(
    "Select Deployment",
    deployments
)

refresh = st.sidebar.button("🔄 Refresh")

auto_refresh = st.sidebar.checkbox("Auto refresh (30s)")

# --------------------
# Main
# --------------------
if not deployment_id:
    st.info("Select a deployment")
    st.stop()

try:
    summary = get_summary(deployment_id)
except Exception as e:
    st.error(f"Failed to load summary: {e}")
    st.stop()

st.title(f"Deployment: {deployment_id}")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --------------------
# AI Summary
# --------------------
st.subheader("🧠 AI Summary")
st.markdown(summary.get("ai_summary", "_No summary generated_"))

# --------------------
# Topology
# --------------------
st.subheader("🧩 Topology")
st.json(summary.get("topology", {}))

# --------------------
# Host Metrics
# --------------------
st.subheader("🖥️ Node Health")

hosts = summary.get("hosts", {})
for host, data in hosts.items():
    with st.expander(host, expanded=True):
        col1, col2, col3 = st.columns(3)
        col1.metric("CPU %", data.get("cpu", "N/A"))
        col2.metric("Memory %", data.get("memory", "N/A"))
        col3.metric("Replication Lag (sec)", data.get("replication_lag_sec", "N/A"))

# --------------------
# Slow Queries
# --------------------
st.subheader("🐢 Slow Queries")

slow = summary.get("slow_queries", [])
if slow:
    st.dataframe(slow, use_container_width=True)
else:
    st.success("No slow queries detected")

# --------------------
# Index Analysis
# --------------------
st.subheader("📚 Index Recommendations")

index_analysis = summary.get("index_analysis", {})
if index_analysis:
    st.json(index_analysis)
else:
    st.success("Indexes look good")

# --------------------
# Upgrade Advisor
# --------------------
st.subheader("⬆️ MongoDB Upgrade Advisor")
st.json(summary.get("upgrade_advisor", {}))

# --------------------
# Mongo CVE lookup
# --------------------
st.subheader("⬆️ MongoDB CVE lookup")
mongo_versions = summary.get("mongo_versions", [])
security = summary.get("security", {})
mongo_cves = summary.get("mongo_cves", [])

if isinstance(mongo_cves, dict):
    mongo_cves = [mongo_cves]

if not isinstance(mongo_cves, dict):
    mongo_cves = []


applicable_cves = [
        cve for cve in mongo_cves
        if cve.get("current_version") in mongo_versions
]
#print(applicable_cves)
#st.write("DEBUG mongo_cves:", applicable_cves)
if not applicable_cves:
    st.success("No MongoDB CVEs detected for this deployment")

else:
    for cve in applicable_cves[:3]:
        st.error(f"""
**CVE:** {cve.get('cve', 'N/A')}
**Severity:** {cve.get('severity', 'UNKNOWN')}
**Affected Range:** {cve.get('affeted_range', 'N/A')}
**Recommendation:** {cve.get('recommendation', 'N/A')}

{cve.get('description')}
""")
# --------------------
# Errors & Warnings
# --------------------
st.subheader("⚠️ MongoDB Errors / Warnings")

errors = summary.get("mongo_errors", [])
if errors:
    for e in errors:
        st.warning(e)
else:
    st.success("No errors found")
