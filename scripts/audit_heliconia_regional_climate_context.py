#!/usr/bin/env python3
"""NASA POWER contextual climate check for the BDFFP region, 1998-2005.

Exploratory *regional climate context*, not site exposure, not a causal model,
and not a new EGWEE study. Fetch a single approximate BDFFP coordinate.
Monthly precipitation is mm/day; integrate by calendar month length.
"""
from __future__ import annotations
import argparse
import calendar
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from audit_heliconia_forward_lag_prediction import archive_rows

API="https://power.larc.nasa.gov/api/temporal/monthly/point"
ARGS={"parameters":"PRECTOTCORR,T2M", "community":"AG",
      "longitude":"-60", "latitude":"-2.5",
      "start":"1998", "end":"2005", "format":"JSON"}
URL=API+"?"+urlencode(ARGS)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    request=Request(URL,headers={"User-Agent":"egwee-empirical-climate-context/1.0"})
    with urlopen(request,timeout=70) as response:
        assert response.status==200,response.status
        raw=response.read()
    assert raw.startswith(b"{"),raw[:120]
    obj=json.loads(raw.decode("utf-8"))
    param=obj["properties"]["parameter"]
    assert "PRECTOTCORR" in param and "T2M" in param
    monthly={}
    for y in range(1998,2006):
        months=[]
        for m in range(1,13):
            key=f"{y}{m:02d}"
            rainfall=float(param["PRECTOTCORR"][key])
            temp=float(param["T2M"][key])
            assert -100<rainfall<1000 and -40<temp<65,(key,rainfall,temp)
            assert rainfall>=0,(key,rainfall)
            nday=calendar.monthrange(y,m)[1]
            months.append({"month":m,"days":nday,"rain_mm_day":rainfall,
                           "precipitation_mm":round(rainfall*nday,4),
                           "temperature_c":temp})
        monthly[str(y)]={
            "annual_precipitation_mm":round(sum(x["precipitation_mm"] for x in months),3),
            "mean_temperature_c":round(sum(x["temperature_c"]*x["days"] for x in months)/
                                         sum(x["days"] for x in months),3),
            "jan_may_precipitation_mm":round(sum(x["precipitation_mm"] for x in months[:5]),3),
            "jun_dec_precipitation_mm":round(sum(x["precipitation_mm"] for x in months[5:]),3),
            "months":months,
        }
    # The census archive records years, not dates. The same-study climate paper
    # refers to a February census. Do not use full current-year rainfall as a
    # prospective predictor without field-level visit dates.
    plant_rows, _ = archive_rows(None)
    years=range(2001,2006)
    common_plots=set.intersection(*[
        {r["plot"] for r in plant_rows if r["year"]==yr} for yr in years
    ])
    assert len(common_plots)==10
    compared={}
    for yr in (2002,2003):
        subset=[r for r in plant_rows if r["year"]==yr and r["plot"] in common_plots]
        assert len(subset)==10
        compared[str(yr)]={
            "mean_first_recorded_new_seedlings":sum(r["y"] for r in subset)/len(subset),
            "mean_previous_year_documented_flowering":sum(r["fl1"] for r in subset)/len(subset),
            "mean_previous_year_observed_stock":sum(r["stock"] for r in subset)/len(subset),
            "strictly_prior_calendar_year_rainfall_mm":monthly[str(yr-1)]["annual_precipitation_mm"],
            "strictly_prior_calendar_year_jan_may_rainfall_mm":monthly[str(yr-1)]["jan_may_precipitation_mm"],
            "strictly_prior_calendar_year_mean_temperature_c":monthly[str(yr-1)]["mean_temperature_c"],
            "same_calendar_year_jan_may_rainfall_mm_NOT_PROSPECTIVE":monthly[str(yr)]["jan_may_precipitation_mm"],
            "same_calendar_year_total_rainfall_mm_NOT_PROSPECTIVE":monthly[str(yr)]["annual_precipitation_mm"],
        }
    report={
        "status":"EXTERNAL_REGIONAL_CONTEXT_NO_CAUSAL_OR_SITE_CLAIM",
        "source_url":URL,
        "retrieved_json_sha256":hashlib.sha256(raw).hexdigest(),
        "metadata":{"header":obj.get("header"),
                    "parameter_units":obj.get("parameters"),
                    "site_latitude":-2.5,"site_longitude":-60.0},
        "monthly_climate":monthly,
        "biological_calendar_alignment":compared,
        "timing_guard":{
            "study_report_2022_doi":"10.1111/gcb.15900",
            "associated_later_study_mentions_February_census":True,
            "exact_archive_plot_year_survey_dates_available":False,
            "prohibition":"Do not use current-year Jan-May or annual rainfall as prior exposure for a possibly February census.",
            "counterexample":"2003 full-year rainfall falls strongly, but 2002 annual rainfall preceding that census differs very little from 2001. This rejects an automatic inference of prior-year drought from the same-year climate curve, not all precipitation-lag mechanisms."
        },
        "source_limits":[
            "Regional gridded climate around approximate BDFFP centroid, not exact site/ranch exposure.",
            "POWER meteorology MERRA-2 products and revisions; not observed local field rainfall.",
            "Annual point aggregate from monthly mean daily precipitation * calendar days.",
            "Data exist after response years, not necessarily available at earlier operational issue date.",
            "Observed recruitment may respond to different year, season, cue, soil microclimate and seed bank.",
            "Eight climate years, three ranches one studied landscape; no correlated-independent-year p values.",
            "Do not equate regional temperature/rainfall with local microhabitat conditions.",
            "This is an exploratory competitor, no climate causal mediator or demographic stage identified."
        ],
    }
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "annual_climate":{y:{k:v for k,v in x.items() if k!="months"}
                          for y,x in monthly.items()},
        "biological_calendar_alignment":compared,
        "timing_guard":report["timing_guard"],
    },indent=2))

if __name__=="__main__":
    main()
