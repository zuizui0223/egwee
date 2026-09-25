from __future__ import annotations

import csv
import json
import math
import statistics as stats
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALUES = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_transect_values_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_direct_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_direct_covariance_v1.json"
CONTRACT = ROOT / "manuscript/CF01_SEVENELLO_2026_DIRECT_IF_RECOVERY_CONTRACT.md"
MISSING = ROOT / "manuscript/CF01_SEVENELLO_2026_MISSINGNESS_AMENDMENT_2026-09-25.md"
RESULT = ROOT / "manuscript/PHASE2_CF01_SEVENELLO_DIRECT_IF_RECOVERY_2026-09-25.md"
PAIR = ROOT / "evidence/meta_extraction/coverage_expansion_pair_coverage_v1.csv"
COMPLETION = ROOT / "manuscript/PHASE2_CF01_COVERAGE_COMPLETION_2026-09-25.md"

PROGRAMME = "P2_CF01_SEVENELLO_2026"
PRIMARY = ("GORO", "LARO", "POAR")
EXPECTED = {"GORO": (6, 6), "LARO": (8, 8), "POAR": (6, 6), "POGN": (6, 5)}
TOL = 5e-10


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pearson(x: list[float], y: list[float]) -> float:
    mx, my = stats.mean(x), stats.mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    return sum(a*b for a,b in zip(dx,dy)) / math.sqrt(
        sum(a*a for a in dx) * sum(b*b for b in dy)
    )


def centered(values: list[float], groups: list[str]) -> list[float]:
    means = {
        g: stats.mean(v for v, gg in zip(values, groups) if gg == g)
        for g in set(groups)
    }
    return [v - means[g] for v, g in zip(values, groups)]


def hedges(fragmented: list[float], reference: list[float]) -> tuple[float,float]:
    n1,n2=len(fragmented),len(reference)
    m1,m2=stats.mean(fragmented),stats.mean(reference)
    s1,s2=stats.stdev(fragmented),stats.stdev(reference)
    df=n1+n2-2
    pooled=math.sqrt(((n1-1)*s1*s1+(n2-1)*s2*s2)/df)
    d=(m1-m2)/pooled
    j=1-3/(4*df-1)
    g=j*d
    v=1/n1+1/n2+g*g/(2*(n1+n2))
    return g,v


def main() -> None:
    for p in (VALUES,EFFECTS,COV,CONTRACT,MISSING,RESULT,PAIR,COMPLETION):
        assert p.is_file(), p

    vals=rows(VALUES)
    assert all(r["programme_id"] == PROGRAMME for r in vals)
    by_sp: dict[str,list[dict[str,str]]] = defaultdict(list)
    for r in vals:
        by_sp[r["species"]].append(r)
        assert int(r["n_OP_planned"]) == 10
        assert 1 <= int(r["n_OP_nonmissing"]) <= 10

    assert set(by_sp) == {*PRIMARY, "POGN"}
    assert sum(int(r["n_OP_nonmissing"]) < 10 for r in vals) == 5
    assert not any(
        r["species"] == "POGN" and r["site"] == "Maya"
        and r["crop"] == "Wheat" and r["transect"] == "Core"
        for r in vals
    )

    eff={(r["species"],r["layer"]):r for r in rows(EFFECTS)}
    assert set(eff) == {(sp,layer) for sp in (*PRIMARY,"POGN") for layer in ("I","F")}

    cov=json.loads(COV.read_text(encoding="utf-8"))
    assert cov["programme_id"] == PROGRAMME
    assert cov["status"] == "direct_IF_three_panel_covariance_aware"
    assert cov["primary_species"] == list(PRIMARY)
    assert cov["sensitivity_species"] == ["POGN"]
    assert cov["direct_IF_programme_increment"] == 1
    assert cov["phase1_frozen_synthesis_increment"] == 0

    ps=[]
    for sp in (*PRIMARY,"POGN"):
        rr=by_sp[sp]
        groups=[r["transect"] for r in rr]
        iv=[float(r["I_all_bees"]) for r in rr]
        fv=[float(r["F_mean_total_seeds_OP"]) for r in rr]
        ie=[x for x,g in zip(iv,groups) if g=="Edge"]
        ic=[x for x,g in zip(iv,groups) if g=="Core"]
        fe=[x for x,g in zip(fv,groups) if g=="Edge"]
        fc=[x for x,g in zip(fv,groups) if g=="Core"]
        assert (len(ie),len(ic)) == EXPECTED[sp]

        gi,vi=hedges(ie,ic)
        gf,vf=hedges(fe,fc)
        for layer,g,v in (("I",gi,vi),("F",gf,vf)):
            e=eff[(sp,layer)]
            assert abs(float(e["hedges_g"])-g) < TOL
            assert abs(float(e["variance"])-v) < TOL

        rho=pearson(centered(iv,groups),centered(fv,groups))
        working=rho*math.sqrt(vi*vf)
        block=cov["panels"][sp]
        assert block["positive_definite"] is True
        assert abs(block["I_g"]-gi) < TOL
        assert abs(block["F_g"]-gf) < TOL
        assert abs(block["residual_correlation_IF"]-rho) < TOL
        assert abs(block["sampling_covariance_proxy_IF"]-working) < TOL
        assert block["covariance_determinant"] > 0
        if sp in PRIMARY:
            ps.append(block["I_minus_F"]["p_two_sided"])

    assert abs(cov["programme_internal_bonferroni_p"] - min(1.0,3*min(ps))) < TOL
    assert cov["programme_internal_bonferroni_p"] == 1.0

    contract=CONTRACT.read_text(encoding="utf-8")
    for token in (
        "Primary direct contrast = **Edge minus Core**",
        "Primary I =",
        "all_bees",
        "Primary F for each species = **mean total viable seeds per plant under natural open pollination**",
        "GORO: 6 Edge/Core",
        "LARO: 8 pairs",
        "POAR: 6 pairs",
        "POGN is **sensitivity only**",
        "direct I-F programme increment = **1**",
        "frozen Phase-1 five-cluster Fisher synthesis",
    ):
        assert token in contract, token

    missing=MISSING.read_text(encoding="utf-8")
    for token in (
        "literal",
        "NA",
        "never as zero",
        "at least one non-missing OP observation",
        "No arbitrary minimum-completeness threshold",
    ):
        assert token in missing, token

    result=RESULT.read_text(encoding="utf-8")
    for token in (
        "direct I-F three-panel covariance-aware",
        "programme count increment in pair-specific direct I-F coverage: **+1**",
        "internal three-panel Bonferroni p: **1**",
        "Phase-1 frozen five-cluster synthesis increment: **0**",
    ):
        assert token in result, token

    pair={r["pair_id"]:r for r in rows(PAIR)}
    assert int(pair["I-F"]["current_independent_direct_systems"]) == 2
    assert set(pair["I-F"]["current_system_ids"].split(";")) == {"ML020", PROGRAMME}

    completion=COMPLETION.read_text(encoding="utf-8")
    assert "I-F: **2 / 5 independent programmes**" in completion
    assert "Sevenello" in completion

    print(
        "PHASE2_CF01_SEVENELLO_CHECK_OK "
        "primary_panels=3 sensitivity_panels=1 covariance_blocks=4 all_PD=true "
        "programme_p=1 direct_IF=2/5 phase1_unchanged=true"
    )


if __name__ == "__main__":
    main()
