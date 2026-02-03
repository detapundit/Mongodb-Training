#!/usr/bin/env python3

# =========================================================
# IMPORTS
# =========================================================
import json
import yaml
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone
from collections import defaultdict
from typing import Dict, List
from collections import defaultdict
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken
from packaging import version as pv

# =========================================================
# CONFIG LOAD
# =========================================================
CONFIG_PATH = "/opt/agg-monsum/config.yaml"

with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f)

# =========================================================
# LOGGING
# =========================================================
def setup_logging(cfg: dict):
    log_cfg = cfg.get("logging")

    if not log_cfg:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        return

    level = getattr(logging, log_cfg.get("level", "INFO").upper())
    log_file = log_cfg.get("file", "/opt/monsum/logs/aggregator.log")
    max_mb = log_cfg.get("max_size_mb", 20)
    backups = log_cfg.get("backup_count", 5)
    fmt = log_cfg.get("format")

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    handler = RotatingFileHandler(
        log_file,
        maxBytes=max_mb * 1024 * 1024,
        backupCount=backups
    )
    handler.setFormatter(logging.Formatter(fmt))

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)

    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


setup_logging(CONFIG)
logger = logging.getLogger("aggregator")

# =========================================================
# AGGREGATOR CONFIG
# =========================================================
AGG = CONFIG["aggregator"]

AGGREGATOR_ID = AGG["id"]
OPENAI_MODEL = AGG["ai"]["model"]
MAX_AI_TOKENS = AGG["ai"]["max_tokens"]
AI_TEMPERATURE = AGG["ai"]["temperature"]
MONGO_CVE_FEED = AGG["feeds"]["mongo_cve"]
SUPPORTED_MAJORS = AGG["mongo"]["supported_majors"]
PREFERRED_MAJOR = AGG["mongo"]["preferred_major"]
TRIM_FIELDS = set(AGG["trimming"]["drop_fields"])

logger.info("Aggregator starting | id=%s", AGGREGATOR_ID)

# =========================================================
# APP INIT
# =========================================================
app = Flask(__name__)
load_dotenv("/opt/agg-monsum/aggregator.env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DEPLOYMENTS: Dict[str, dict] = {}

# =========================================================
# TOKEN CONTROL
# =========================================================
def count_tokens(text: str) -> int:
    enc = tiktoken.encoding_for_model(OPENAI_MODEL)
    return len(enc.encode(text))

def trim_payload(payload: dict) -> dict:
    if count_tokens(json.dumps(payload)) <= MAX_AI_TOKENS:
        return payload
    trimmed = payload.copy()
    for f in TRIM_FIELDS:
        trimmed.pop(f, None)
    return trimmed

# =========================================================
# TOPOLOGY
# =========================================================
def detect_topology(agent_payload: dict) -> dict:
    topo = agent_payload.get("topology", {})
    if topo.get("sharded"):
        return {"type": "sharded", "cluster": topo.get("cluster")}
    if topo.get("replicaSet"):
        return {"type": "replicaset", "rs": topo.get("replicaSet")}
    return {"type": "standalone"}

# =========================================================
# MONGODB CVE LOOKUP VIA NVD
# =========================================================

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def fetch_nvd_mongo_cves() -> list:
    """
    Fetch MongoDB-related CVEs from NVD
    """
    params = {
        "keywordSearch": "mongodb",
        "resultsPerPage": 200
    }

    try:
        r = requests.get(NVD_API, params=params, timeout=15)
        if not r.ok:
            logger.warning("NVD API request failed")
            return []
        return r.json().get("vulnerabilities", [])
    except Exception as e:
        logger.warning("NVD API error: %s", e)
        return []


def version_in_range(version: str, start: str | None, end: str | None) -> bool:
    try:
        v = Version(version)
        if start and v < Version(start):
            return False
        if end and v >= Version(end):
            return False
        return True
    except InvalidVersion:
        return False

########################################

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def lookup_mongo_cves_for_versions(mongo_versions: list[str]) -> list[dict]:
    """
    Lookup MongoDB CVEs from NVD and return only those applicable
    to the given MongoDB versions.
    """

    results = []
    seen = set()

    for mongo_ver in mongo_versions:
        try:
            mongo_version = pv.parse(mongo_ver)
        except Exception:
            continue

        params = {
            "keywordSearch": "MongoDB Server",
            "resultsPerPage": 200
        }

        try:
            resp = requests.get(NVD_API, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            return [{
                "error": f"NVD lookup failed: {e}"
            }]

        vulns = data.get("vulnerabilities", [])

        for item in vulns:
            cve = item.get("cve", {})
            cve_id = cve.get("id")

            if not cve_id or cve_id in seen:
                continue

            configs = cve.get("configurations", [])
            if not isinstance(configs, list):
                continue

            affected = False
            affected_range = "unknown"

            for cfg in configs:
                for node in cfg.get("nodes", []):
                    for match in node.get("cpeMatch", []):
                        if not match.get("vulnerable", False):
                            continue

                        cpe = match.get("criteria", "")
                        if "mongodb" not in cpe.lower():
                            continue

                        v_start = match.get("versionStartIncluding") or match.get("versionStartExcluding")
                        v_end = match.get("versionEndIncluding") or match.get("versionEndExcluding")

                        try:
                            if v_start and mongo_version < pv.parse(v_start):
                                continue
                            if v_end and mongo_version > pv.parse(v_end):
                                continue
                        except Exception:
                            continue

                        affected = True
                        affected_range = f"{v_start or '*'} → {v_end or '*'}"

            if not affected:
                continue

            severity = (
                cve.get("metrics", {})
                   .get("cvssMetricV31", [{}])[0]
                   .get("cvssData", {})
                   .get("baseSeverity", "UNKNOWN")
            )

            description = next(
                (d["value"] for d in cve.get("descriptions", [])
                 if d.get("lang") == "en"),
                "No description available"
            )

            results.append({
                "cve": cve_id,
                "severity": severity,
                "affected_range": affected_range,
                "recommendation": "Upgrade to a MongoDB version where this CVE is fixed",
                "description": description
            })

            seen.add(cve_id)

    return results

'''
def lookup_mongo_cves_for_versions(mongo_versions: list[str]) -> list[dict]:
    findings = []
    cves = fetch_nvd_mongo_cves()

    for version in mongo_versions:
        for item in cves:
            cve = item.get("cve", {})
            cve_id = cve.get("id")
            descriptions = cve.get("descriptions", [])
            metrics = cve.get("metrics", {})

            desc = next(
                (d["value"] for d in descriptions if d["lang"] == "en"),
                ""
            )

            severity = (
                metrics.get("cvssMetricV31", [{}])[0]
                .get("cvssData", {})
                .get("baseSeverity")
            )

            configs = cve.get("configurations", [])

            if isinstance(configs,dict):
                nodes = configs.get("nodes", [])
            elif isinstance(configs, list):
                nodes = []
                for cfg in configs:
                    nodes.extend(cfg.get("nodes",[]))

            else:
                nodes = []

            for node in nodes:
                for match in node.get("cpeMatch", []):
                    cpe = match.get("criteria", "")
                    if "mongodb" not in cpe.lower():
                        continue

                    start = match.get("versionStartIncluding")
                    end = match.get("versionEndExcluding")

                    if version_in_range(version, start, end):
                        findings.append({
                            "cve": cve_id,
                            "severity": severity or "UNKNOWN",
                            "description": desc,
                            "current_version": version,
                            "affected_range": f">={start} <{end}",
                            "recommendation": (
                                f"Upgrade to {end} or later"
                                if end else "Upgrade recommended"
                            )
                        })
                        break

    return findings
'''

'''
# =========================================================
# MONGO CVE FEED LOADER
# =========================================================

def load_mongo_cve_feed() -> list:
    try:
        r = requests.get(MONGO_CVE_FEED, timeout=10)
        if not r.ok:
            logger.warning("Mongo CVE feed fetch failed")
            return []
        return r.json()
    except Exception as e:
        logger.warning("Mongo CVE feed error: %s", e)
        return []

def extract_version_ranges(affected_block: dict) -> list:
    """
    Converts MongoDB CVE 'events' into version ranges
    Example:
      introduced: 8.0.0 → fixed: 8.0.17
    """
    ranges = []

    for r in affected_block.get("ranges", []):
        events = r.get("events", [])
        introduced = None

        for e in events:
            if "introduced" in e:
                introduced = e["introduced"]
            elif "fixed" in e and introduced:
                ranges.append((introduced, e["fixed"]))
                introduced = None

    return ranges

def lookup_mongo_cves_for_versions(mongo_versions: List[str]) -> List[dict]:
    findings = []
    feed = load_mongo_cve_feed()

    for version in mongo_versions:
        try:
            v = Version(version)
        except Exception:
            continue

        for item in feed:
            for affected in item.get("affected", []):
                if affected.get("package") != "mongodb":
                    continue

                ranges = extract_version_ranges(affected)

                for introduced, fixed in ranges:
                    if Version(introduced) <= v < Version(fixed):
                        findings.append({
                            "cve": item.get("cve"),
                            "severity": item.get("severity"),
                            "description": item.get("description"),
                            "affected_range": f">={introduced}, <{fixed}",
                            "current_version": version,
                            "fixed_version": fixed
                        })
                        break

    return findings

# ========================================================
# VERSION CHECK
# =======================================================
def version_in_range(version: str, range_expr: str) -> bool:
    try:
        v = Version(version)
    except Exception:
        return False

    for part in range_expr.split(","):
        part = part.strip()

        if part.startswith(">=") and v < Version(part[2:]):
            return False
        elif part.startswith(">") and v <= Version(part[1:]):
            return False
        elif part.startswith("<=") and v > Version(part[2:]):
            return False
        elif part.startswith("<") and v >= Version(part[1:]):
            return False
        elif part.startswith("==") and v != Version(part[2:]):
            return False

    return True

# =========================================================
# CVE lookup
# =========================================================

def lookup_mongo_cves_for_versions(mongo_versions: List[str]) -> List[dict]:
    findings = []

    try:
        r = requests.get(MONGO_CVE_FEED, timeout=10)
        if not r.ok:
            logger.warning("Mongo CVE feed fetch failed")
            return []
        data = r.json()
    except Exception as e:
        logger.warning("Mongo CVE feed error: %s", e)
        return []

    for version in mongo_versions:
        for item in data:
            for rng in item.get("affected_versions", []):
                if version_in_range(version, rng):
                    findings.append({
                        "cve": item.get("cve"),
                        "severity": item.get("severity"),
                        "description": item.get("description"),
                        "affected_range": rng,
                        "current_version": version,
                        "fixed_version": (
                            item.get("fixed_versions", ["unknown"])[0]
                        )
                    })
                    break

    return findings
'''
# =========================================================
# SUMMARIZERS
# =========================================================
def summarize_host_metrics(hosts: dict) -> dict:
    cpu, mem = [], []
    for h in hosts.values():
        m = h.get("host_metrics", {})
        cpu.append(m.get("cpu_percent", 0))
        mem.append(m.get("memory", {}).get("percent", 0))
    return {
        "cpu_avg": round(sum(cpu)/len(cpu), 2) if cpu else None,
        "cpu_max": max(cpu) if cpu else None,
        "memory_avg": round(sum(mem)/len(mem), 2) if mem else None
    }

def summarize_server_status(hosts: dict) -> dict:
    conns, queues = [], []

    for h in hosts.values():
        ss = h.get("server_status", {})
        if ss.get("connections"):
            conns.append(ss["connections"].get("current"))
        if ss.get("queues"):
            queues.append(sum(ss["queues"].values()))

    return {
        "connections_avg": round(sum(conns)/len(conns), 2) if conns else None,
        "queues_max": max(queues) if queues else None
    }

def summarize_replication(hosts: dict) -> dict:
    lags = []
    for h in hosts.values():
        for lag in h.get("replication_lag", {}).values():
            lags.append(lag)
    return {
        "max_lag_seconds": max(lags) if lags else 0,
        "healthy": max(lags) < 10 if lags else True
    }

def summarize_log_health(hosts):
    errors, warnings = 0, 0
    for h in hosts.values():
        mh = h.get("mongo_log_health", {})
        errors += len(mh.get("errors",[]))
        warnings += len(mh.get("warnings",[]))

    return {
        "errors": errors,
        "warnings": warnings
    }

def extract_slow_queries(host_payload: dict) -> list:
    """
    Normalize slow queries from different agent payload formats
    """
    # Case 1: direct
    if isinstance(host_payload.get("slow_queries"), list):
        return host_payload["slow_queries"]

    # Case 2: under logs
    logs = host_payload.get("logs", {})
    if isinstance(logs.get("slow_queries"), list):
        return logs["slow_queries"]

    # Case 3: under mongo_logs
    mongo_logs = host_payload.get("mongo_logs", {})
    if isinstance(mongo_logs.get("slow_queries"), list):
        return mongo_logs["slow_queries"]

    return []

def summarize_slow_queries(hosts: dict) -> list:
    agg = defaultdict(list)
    for h in hosts.values():
        slow_queries = extract_slow_queries(h)

        for q in slow_queries:
            ns = q.get("ns") or q.get("namespace")
            dur = q.get("duration_ms") or q.get("durationMillis")

            if not ns or not dur:
                continue

            agg[ns].append(dur)

    return [
        {
            "ns": ns,
            "count": len(v),
            "avg_ms": round(sum(v) / len(v), 2),
            "max_ms": max(v)
        }
        for ns, v in agg.items()
    ]

def analyze_indexes(slow_queries: List[dict], indexes: dict) -> dict:
    recommendations, redundant = [], []
    seen = set()

    for q in slow_queries:
        shape = tuple(q.get("filter", []))
        if shape and shape not in seen:
            seen.add(shape)
            recommendations.append({
                "namespace": q["ns"],
                "suggested_index": list(shape),
                "reason": "Seen in slow query filter"
            })

    idx_map = defaultdict(list)
    for ns, idxs in indexes.items():
        for idx in idxs:
            key = tuple(idx["key"].keys())
            idx_map[(ns, key)].append(idx["name"])

    for (ns, key), names in idx_map.items():
        if len(names) > 1:
            redundant.append({
                "namespace": ns,
                "index_keys": list(key),
                "indexes": names
            })

    return {"recommended_indexes": recommendations, "redundant_indexes": redundant}

def mongo_upgrade_advisor(version: str) -> dict:
    if not version:
        return {"status": "unknown"}
    major = ".".join(version.split(".")[:2])
    if major == PREFERRED_MAJOR:
        return {"status": "optimal", "current": version}
    if major in SUPPORTED_MAJORS:
        return {"status": "supported_not_preferred", "current": version}
    return {"status": "upgrade_required", "current": version, "recommended": PREFERRED_MAJOR}

# =========================================================
# AI SUMMARY
# =========================================================
def generate_ai_summary(summary: dict) -> str:
    trimmed = trim_payload(summary)
    try:
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            temperature=AI_TEMPERATURE,
            messages=[
                {"role": "system", "content": "You are a senior MongoDB SRE."},
                {"role": "user", "content": json.dumps(trimmed, indent=2)}
            ]
        )
        return resp.choices[0].message.content
    except Exception:
        logger.exception("AI summary failed")
        return "AI summary unavailable"

# =========================================================
# INGEST
# =========================================================
@app.route("/ingest", methods=["POST"])
def ingest():
    payload = request.json
    if not payload:
        return jsonify({"error": "empty payload"}), 400

    did = payload.get("deployment_id")
    host = payload.get("host")

    if not did or not host:
        logger.warning("Invalid payload: %s", payload)
        return jsonify({"error": "invalid payload"}), 400

    DEPLOYMENTS.setdefault(did, {"hosts": {}, "created": datetime.now(timezone.utc).isoformat()})
    DEPLOYMENTS[did]["hosts"][host] = payload

    logger.info("Payload ingested | deployment=%s | host=%s", did, host)
    return jsonify({"status": "ok", "aggregator": AGGREGATOR_ID})

# =========================================================
# SUMMARY
# =========================================================
@app.route("/summary/<deployment_id>")
def summary(deployment_id):
    d = DEPLOYMENTS.get(deployment_id)
    if not d:
        return jsonify({"error": "unknown deployment"}), 404

    hosts = d["hosts"]
    versions = {h.get("mongo_version") for h in hosts.values()}

    deployment_summary = {
        "deployment_id": deployment_id,
        "topology": detect_topology(next(iter(hosts.values()))),
        "mongo_versions": list(versions),
        "host_metrics": summarize_host_metrics(hosts),
        "replication": summarize_replication(hosts),
        "slow_queries": summarize_slow_queries(hosts),
        "mongo_metrics": summarize_server_status(hosts),
        "log_health": summarize_log_health(hosts),
        "index_analysis": analyze_indexes(
            summarize_slow_queries(hosts),
            {k: v for h in hosts.values() for k, v in h.get("indexes", {}).items()}
        ),
        "security": {
            "mongo_cves": lookup_mongo_cves_for_versions(list(versions))
        },
        "upgrade_advisor": mongo_upgrade_advisor(next(iter(versions)))
    }

    deployment_summary["ai_summary"] = generate_ai_summary(deployment_summary)
    return jsonify(deployment_summary)

# =========================================================
# DEPLOYMENTS
# =========================================================
@app.route("/deployments", methods=["GET"])
def list_deployments():
    logger.info("Deployments list requested")

    return jsonify({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "deployments": list(DEPLOYMENTS.keys())

        })

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    app.run(
        host=AGG["server"]["bind_host"],
        port=AGG["server"]["port"]
    )
