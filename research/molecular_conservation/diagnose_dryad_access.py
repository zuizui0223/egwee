#!/usr/bin/env python3
"""Source-only Dryad download diagnosis. No phenotype/genotype data retained or printed."""
import argparse
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

BASE = "https://datadryad.org"
DOIS = ("10.5061/dryad.pnvx0k6zm", "10.5061/dryad.2pj0j")

def safe_api(href):
    url = urljoin(BASE, href)
    p = urlparse(url)
    if p.scheme != "https" or p.hostname != "datadryad.org" or not p.path.startswith("/api/v2/"):
        raise ValueError("Nonofficial API URL")
    return url

def json_request(url):
    with urlopen(Request(safe_api(url), headers={"Accept": "application/json", "User-Agent": "EGWEE-source-diagnostic/1.0"}), timeout=25) as r:
        return json.load(r)

def getlink(d, rel):
    obj = (d.get("_links") or {}).get(rel) or {}
    return obj.get("href")

def status_for_download(href):
    """Probe official advertised download URL, read at most one byte; no raw biological values output."""
    url = safe_api(href)
    req = Request(url, headers={"User-Agent": "EGWEE-source-diagnostic/1.0", "Range": "bytes=0-0"})
    try:
        with urlopen(req, timeout=25) as r:
            final = urlparse(r.geturl())
            # Some official file endpoints redirect to storage; never print signed URLs.
            r.read(1)
            return {"result": "reachable", "http_status": r.status,
                    "redirected": r.geturl() != url, "final_host": final.hostname}
    except HTTPError as e:
        return {"result": "http_stop", "http_status": e.code, "redirected": False}
    except URLError as e:
        return {"result": "network_stop", "error_type": type(e.reason).__name__}
    except ValueError:
        return {"result": "url_policy_stop"}

def diagnose(doi):
    from urllib.parse import quote
    api = BASE + "/api/v2/datasets/" + quote("doi:" + doi, safe="")
    dataset = json_request(api)
    version = json_request(getlink(dataset, "stash:version"))
    files = json_request(getlink(version, "stash:files"))
    listed = (files.get("_embedded") or {}).get("stash:files") or []
    candidates = [f for f in listed if str(f.get("path", "")).lower().endswith(".xlsx")]
    out = {"doi": doi, "declared_xlsx": len(candidates), "probe_results": []}
    for f in candidates[:2]:
        href = getlink(f, "stash:download")
        out["probe_results"].append({"file_type": "xlsx", "declared_size": f.get("size"),
                                     "probe": status_for_download(href) if href else {"result": "no_advertised_link"}})
    return out

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    args = p.parse_args()
    results = []
    for doi in DOIS:
        try:
            results.append(diagnose(doi))
        except (HTTPError, URLError, ValueError, KeyError, TypeError) as e:
            results.append({"doi": doi, "result": "metadata_stop", "error_type": type(e).__name__,
                            "http_status": e.code if isinstance(e, HTTPError) else None})
    with open(args.output, "w") as f:
        json.dump({"purpose": "source_access_diagnosis_only", "sources": results,
                   "raw_values_saved": False, "biological_join_verified": False,
                   "effect_estimated": False}, f, indent=2)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
