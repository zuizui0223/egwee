#!/usr/bin/env python3
"""Longitudinal Heliconia follow-up: absorbing death and reversible non-detection.

Exploratory extension of the same published Heliconia programme. It neither
identifies a fragmentation causal effect nor adds a programme to EGWEE.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from audit_heliconia_cohort_observation import (
    COHORT_START, UPSTREAM_COMMIT, BLOBS, exact_permutation, mean, rows
)

YEAR_END = 2006
HORIZONS = (1, 2, 3)


def run(source_dir: Path | None) -> dict:
    census = rows("HDP_survey.csv", source_dir)
    metadata = rows("HDP_plots.csv", source_dir)
    details = {x["plot_id"]: x for x in metadata}
    assert len(details) == 13 and len(census) == 66396
    history: dict[tuple[str, str], dict[int, dict[str, str]]] = defaultdict(dict)
    present = set()
    for x in census:
        site, y, individual = x["plot_id"], int(x["year"]), x["plant_id"]
        assert site in details
        key = (site, individual)
        assert y not in history[key]
        assert x["census_status"] in {"measured", "missing", "dead"}
        history[key][y] = x
        present.add((site, y))
    assert len(history) == 8586

    output = {}
    for horizon in HORIZONS:
        summaries = defaultdict(lambda: {
            "cohort": 0, "alive": 0, "ever_dead": 0, "unknown": 0,
            "dead_reported_at_target": 0, "missing_then_observed_alive": 0,
            "dead_then_observed_alive": 0,
        })
        for (plot, _), records in history.items():
            births = [y for y, x in records.items() if x["recorded_sdlg"] == "TRUE"]
            assert len(births) <= 1
            if not births:
                continue
            birth = births[0]
            assert birth == min(records)
            if not COHORT_START <= birth <= YEAR_END - horizon:
                continue
            if (plot, birth + horizon) not in present:
                continue
            states = [records.get(y, {}).get("census_status", "absent")
                      for y in range(birth + 1, birth + horizon + 1)]
            r = summaries[plot]
            r["cohort"] += 1
            if states[-1] == "dead":
                r["dead_reported_at_target"] += 1
            if "dead" in states:
                r["ever_dead"] += 1
                if states[-1] == "measured":
                    r["dead_then_observed_alive"] += 1
            elif states[-1] == "measured":
                r["alive"] += 1
                if "missing" in states[:-1]:
                    r["missing_then_observed_alive"] += 1
            else:
                r["unknown"] += 1

        plots = []
        for plot, desc in sorted(details.items()):
            c = summaries[plot]
            assert c["cohort"] == c["alive"] + c["ever_dead"] + c["unknown"]
            assert c["cohort"] > 0 and c["alive"] + c["ever_dead"] > 0
            assert c["dead_then_observed_alive"] == 0
            a, dead, uncertain = c["alive"], c["ever_dead"], c["unknown"]
            plots.append({
                "plot": plot, "ranch": desc["ranch"],
                "group": "continuous" if desc["habitat"] == "forest" else "fragment",
                "habitat": desc["habitat"], **c,
                "known_fate_survival": a / (a + dead),
                "alive_lower_bound": a / c["cohort"],
                "alive_upper_bound": (a + uncertain) / c["cohort"],
                "wrong_endpoint_only_survival":
                    a / (a + c["dead_reported_at_target"])
                    if a + c["dead_reported_at_target"] else None,
            })
        group_counts = {}
        for group in ("continuous", "fragment"):
            ss = [p for p in plots if p["group"] == group]
            group_counts[group] = {
                "plots": len(ss),
                **{k: sum(p[k] for p in ss) for k in (
                    "cohort", "alive", "ever_dead", "unknown",
                    "dead_reported_at_target", "missing_then_observed_alive")},
                "mean_plot_known_survival": mean([p["known_fate_survival"] for p in ss]),
                "mean_plot_wrong_endpoint_only_survival":
                    mean([p["wrong_endpoint_only_survival"] for p in ss]),
                "mean_plot_lower_bound": mean([p["alive_lower_bound"] for p in ss]),
                "mean_plot_upper_bound": mean([p["alive_upper_bound"] for p in ss]),
            }
        unblocked = exact_permutation(plots, "known_fate_survival", False)
        ranch_blocked = exact_permutation(plots, "known_fate_survival", True)
        assert unblocked["total"] == 1716 and ranch_blocked["total"] == 240
        lo = (group_counts["fragment"]["mean_plot_lower_bound"]
              - group_counts["continuous"]["mean_plot_upper_bound"])
        hi = (group_counts["fragment"]["mean_plot_upper_bound"]
              - group_counts["continuous"]["mean_plot_lower_bound"])
        output[str(horizon)] = {
            "birth_years": f"{COHORT_START}-{YEAR_END - horizon}",
            "group_summaries": group_counts,
            "plots": plots,
            "permutation": {"unblocked": unblocked, "ranch_blocked": ranch_blocked},
            "unknown_fate_difference_bounds": {"min": lo, "max": hi},
        }

    # Do not allow a future upstream source revision or code change to silently
    # turn the canonical source report into a different quantitative claim.
    assert output["1"]["group_summaries"]["continuous"]["cohort"] == 1551
    assert output["1"]["group_summaries"]["fragment"]["cohort"] == 1039
    assert output["2"]["group_summaries"]["continuous"]["cohort"] == 1437
    assert output["2"]["group_summaries"]["fragment"]["cohort"] == 932
    assert output["3"]["group_summaries"]["continuous"]["cohort"] == 1298
    assert output["3"]["group_summaries"]["fragment"]["cohort"] == 748
    for horizon, expected in (("2", (0.7434545024588616, 0.7679529480616828)),
                              ("3", (0.6945538125815242, 0.6926539081313187))):
        for group, v in zip(("continuous", "fragment"), expected):
            assert abs(output[horizon]["group_summaries"][group][
                "mean_plot_known_survival"] - v) < 1e-10
    return {
        "schema": 1,
        "status": "post_hoc_observation_sensitivity_only",
        "source_commit": UPSTREAM_COMMIT,
        "source_blob_shas": BLOBS,
        "independent_units": "13 plots in 3 ranch blocks",
        "estimand": "Mean plot-level probability of alive at t+h conditional on observed alive or a recorded death at/before t+h; not full unconditional survival",
        "death_rule": "dead is absorbing even after source rows cease",
        "unknown_rule": "missing or absent with no preceding death is unknown, not dead",
        "no_meta_inclusion": True,
        "horizons": output,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.source_dir)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for h, res in result["horizons"].items():
        c, f = (res["group_summaries"][g] for g in ("continuous", "fragment"))
        print(f"h={h} cf={c['mean_plot_known_survival']:.5f} "
              f"ff={f['mean_plot_known_survival']:.5f} "
              f"p_plot={res['permutation']['unblocked']['two_sided_permutation_p']:.5f} "
              f"p_ranch={res['permutation']['ranch_blocked']['two_sided_permutation_p']:.5f} "
              f"newly_relocated={c['missing_then_observed_alive'] + f['missing_then_observed_alive']}")
    print("HELICONIA_MULTYEAR_AUDIT: PASS")


if __name__ == "__main__":
    main()
