#!/usr/bin/env python3
"""Inspect ONLY file inventory and metadata accessibility of published Zenodo versions."""
import json
import urllib.request
import urllib.error

RECORD_IDS = ("20284225", "18376300", "18376299")
for record_id in RECORD_IDS:
    url = f"https://zenodo.org/api/records/{record_id}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "EGWEE-Zenodo-metadata-only/1.0 (+https://github.com/zuizui0223/egwee)",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=50) as response:
            obj = json.load(response)
        files = obj.get("files", None)
        info = {
            "record_id_requested": record_id, "record_id_returned": obj.get("id"),
            "doi": obj.get("doi"),
            "files_array_type": type(files).__name__,
            "num_attached_files": len(files) if isinstance(files, list) else None,
            "attached_names": sorted((f.get("key") or f.get("filename") or "")
                                     for f in files) if isinstance(files, list) else None,
            "access_metadata": obj.get("access"),
            "file_metadata": obj.get("files_metadata"),
            "links_available": sorted((obj.get("links") or {}).keys()),
            "conceptrecid": obj.get("conceptrecid"),
            "version": (obj.get("metadata") or {}).get("version"),
            "source_numeric_values_read": False,
        }
    except Exception as ex:
        info = {"record_id_requested": record_id,
                "metadata_error": type(ex).__name__ + ": " + str(ex)[:250],
                "source_numeric_values_read": False}
    print("ZENODO_VERSION_METADATA_ONLY " + json.dumps(info, sort_keys=True, ensure_ascii=False), flush=True)
