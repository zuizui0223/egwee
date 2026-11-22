"""CP002 scientific boundary fixtures; all records are synthetic."""
import contextlib
import csv
import importlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import audit_cp001_source_coverage as source
try:
    audit = importlib.import_module("audit_cp002_measurement_sources")
except ModuleNotFoundError:
    audit = None

def row(study="Synthetic_A_2001", group="G1", site="F1", **extra):
    return {
        "study_id": study, "study_id2": group, "site_id": site,
        "sampling_year": "2001", "crop": "synthetic_crop",
        "country": "synthetic_country", "yield": extra.pop("outcome", "20"),
        "yield_units": "kg per hectare", "use_visits_or_abundance": "use visits",
        "taxa_recorded": "all visitors", "sampling_visitation": "focal observations",
        "visitation_rate_units": "visits per 100 flowers and hour",
        "visitation_rate": "1", "management": "organic",
        "field_size": "2", "plant_density": "3", **extra,
    }

def csv_bytes(rows):
    out = io.StringIO(newline="")
    w = csv.DictWriter(out, fieldnames=source.EXPECTED_COLUMNS)
    w.writeheader()
    w.writerows(rows)
    return out.getvalue().encode()

class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(audit, "CP002 audit has not been implemented")

    def inspect(self, rows, dois=()):
        return audit.inspect_csv(csv_bytes(rows), allowed_dois=set(dois))

    def test_full_unit_label_overrides_misleading_prefix_and_secondary_is_separate(self):
        x=self.inspect([
            row(site="F1",yield_units="fruit set: weight in g of 100 randomly selected seeds"),
            row(site="F2",yield_units="Insect Pollination: Open pollination [control] - Self-pollination [Tulle bags]"),
            row(site="F3",yield_units="z-score Seeds produced"),
            row(site="F4",outcome="NA",yield2="6",yield2_units="kg per hectare"),
            row(site="F5",yield_units="fruit set (%)"),
        ])
        self.assertEqual(x["frames"]["primary_reviewed_direct"]["rows"],1)
        self.assertEqual(x["outcome_families"]["yield"]["organ_mass_or_quality_component"],1)
        self.assertEqual(x["outcome_families"]["yield"]["treatment_contrast"],1)
        self.assertEqual(x["outcome_families"]["yield"]["already_transformed"],1)
        self.assertEqual(x["outcome_families"]["yield2"]["harvest_mass_area"],1)

    def test_zero_is_observed_and_missing_visit_is_not_a_zero(self):
        x=self.inspect([row(site="F1",outcome="0",visitation_rate="0"),
                        row(site="F2",visitation_rate="NA"),
                        row(site="F3",outcome="NA")])
        self.assertEqual(x["frames"]["primary_reviewed_direct"]["rows"],2)
        self.assertEqual(x["frames"]["author_use_visits_direct_timed"]["rows"],1)

    def test_net_counts_and_unspecified_effort_do_not_enter_timed_observation_frame(self):
        x=self.inspect([
            row(site="F1"),
            row(site="F2",sampling_visitation="sweep net"),
            row(site="F3",visitation_rate_units="visits"),
            row(site="F4",visitation_rate_units="Insects per flower"),
            row(site="F5",use_visits_or_abundance="use abundance",sampling_abundance="sweep net",abundance="2"),
        ])
        self.assertEqual(x["frames"]["primary_direct_total_visit"]["rows"],5)
        self.assertEqual(x["frames"]["primary_direct_timed_observation"]["rows"],2)
        self.assertEqual(x["frames"]["author_use_visits_direct_timed"]["rows"],1)
        self.assertEqual(x["frames"]["author_use_abundance_direct"]["rows"],1)

    def test_drop_selector_is_an_annotation_not_universal_invalidity(self):
        x=self.inspect([row(use_visits_or_abundance="drop (HB not recorded)",taxa_recorded="wild bees")])
        self.assertEqual(x["frames"]["primary_direct_timed_observation"]["rows"],1)
        self.assertEqual(x["frames"]["author_use_visits_direct_timed"]["rows"],0)

    def test_source_links_are_transitive_but_generic_publication_is_not_a_link(self):
        x=self.inspect([
            row(study="Synthetic_A_2001",group="G1",site="F1",Publication="unpublished"),
            row(study="Synthetic_A_2002",group="G2",site="F2",sampling_year="2002",Publication="https://doi.org/10.1234/shared"),
            row(study="Synthetic_B_2003",group="G3",site="F3",sampling_year="2003",Publication="doi:10.1234/shared."),
            row(study="Synthetic_C_2004",group="G4",site="F4",sampling_year="2004",Publication="unpublished"),
        ],dois=("10.1234/shared",))
        self.assertEqual(x["grouping"]["provisional_study_id2_groups"],4)
        self.assertEqual(x["grouping"]["year_stem_components"],3)
        self.assertEqual(x["grouping"]["vetted_publication_components"],3)
        self.assertEqual(x["grouping"]["combined_components"],2)
        self.assertEqual(x["grouping"]["largest_component_study_id2_groups"],3)

    def test_unvetted_or_umbrella_doi_does_not_merge_sources(self):
        x=self.inspect([
            row(study="Synthetic_A_2001",group="G1",site="F1",Publication="10.1234/umbrella"),
            row(study="Synthetic_B_2002",group="G2",site="F2",Publication="10.1234/umbrella"),
        ])
        self.assertEqual(x["grouping"]["combined_components"],2)
        self.assertEqual(x["grouping"]["unvetted_distinct_doi_tokens"],1)

    def test_embedded_year_and_nonmatching_study_names_are_not_fuzzy_joined(self):
        x=self.inspect([
            row(study="Synthetic2001_A",group="G1",site="F1"),
            row(study="Synthetic_A",group="G2",site="F2"),
        ])
        self.assertEqual(x["grouping"]["year_stem_components"],2)

    def test_balanced_doi_parentheses_survive_citation_wrapper_normalization(self):
        x=self.inspect([
            row(study="Synthetic_A_2001",group="G1",site="F1",Publication="10.1234/a(2001)"),
            row(study="Synthetic_B_2001",group="G2",site="F2",Publication="(https://doi.org/10.1234/a(2001))."),
        ],dois=("10.1234/a(2001)",))
        self.assertEqual(x["grouping"]["vetted_publication_components"],1)

    def test_complete_constant_baseline_fails_variation_and_missing_management_is_not_conventional(self):
        constant=[row(site="F"+str(i)) for i in range(5)]
        varying=[row(study="Synthetic_B_2001",group="G2",site="V"+str(i),field_size=str(i+1)) for i in range(5)]
        missing=[row(study="Synthetic_C_2001",group="G3",site="M"+str(i),management="NA") for i in range(5)]
        x=self.inspect(constant+varying+missing)["baseline"]["harvest_mass_area_author_visits"]["all_three"]
        self.assertEqual(x["complete_rows"],10)
        self.assertEqual(x["blocks_at_least_five"],2)
        self.assertEqual(x["variable_blocks"],1)
        self.assertEqual(x["rows_in_variable_blocks"],5)
        self.assertEqual(x["components_with_variable_blocks"],1)

    def test_original_units_protocol_and_taxa_prevent_cross_block_ranking(self):
        records=[row(site="F"+str(i)) for i in range(3)]
        records += [row(site="T"+str(i),sampling_visitation="transects") for i in range(3)]
        records += [row(site="U"+str(i),yield_units="tonne per hectare") for i in range(3)]
        records += [row(site="B"+str(i),taxa_recorded="bees") for i in range(3)]
        b=self.inspect(records)["baseline"]["harvest_mass_area_author_visits"]["all_three"]
        self.assertEqual(b["complete_rows"],12)
        self.assertEqual(b["blocks"],4)
        self.assertEqual(b["blocks_at_least_five"],0)

    def test_duplicate_field_keys_are_flagged_not_counted_as_distinct_fields(self):
        x=self.inspect([row() for _ in range(5)])
        self.assertEqual(x["anomalies"]["duplicate_candidate_keys"],1)
        self.assertEqual(x["baseline"]["harvest_mass_area_author_visits"]["all_three"]["blocks_at_least_five"],0)

    def test_outcome_magnitudes_do_not_change_the_metadata_audit(self):
        a=[row(site="F"+str(i),field_size=str(i+1),outcome=str(i+1)) for i in range(5)]
        b=[{**r,"yield":str(10000-i*1000)} for i,r in enumerate(a)]
        self.assertEqual(self.inspect(a),self.inspect(b))

    def test_unknown_text_and_raw_identifiers_do_not_escape_in_output(self):
        x=self.inspect([row(study="PRIVATE_STUDY",site="PRIVATE_SITE",
            crop="PRIVATE_CROP",country="PRIVATE_COUNTRY",Publication="PRIVATE_REFERENCE",
            Email_contact="private@example.invalid",notes="PRIVATE_NOTE",
            yield_units="PRIVATE_UNIT",management="PRIVATE_MANAGEMENT")])
        out=json.dumps(x)
        for secret in ("PRIVATE_", "private@example.invalid"):
            self.assertNotIn(secret,out)
        self.assertEqual(x["frames"]["primary_reviewed_direct"]["rows"],0)

    def test_unknown_schema_is_rejected_before_row_processing(self):
        with self.assertRaises(ValueError):
            audit.inspect_csv(b"study_id,yield\nsecret,1\n")

    def test_nonfinite_numbers_are_not_admitted(self):
        x=self.inspect([row(site="F1",outcome="Infinity"),row(site="F2",visitation_rate="NaN"),
                        row(site="F3",field_size="Infinity")])
        self.assertEqual(x["frames"]["author_use_visits_direct_timed"]["rows"],1)
        self.assertEqual(x["baseline"]["harvest_mass_area_author_visits"]["all_three"]["complete_rows"],0)

    def test_access_stop_returns_nonzero_and_safe_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"receipt.json"
            with patch.object(audit.source,"fetch_verified_source",side_effect=TimeoutError("PRIVATE_DETAIL")), \
                 patch("sys.argv",["audit","--output",str(path)]),contextlib.redirect_stdout(io.StringIO()):
                code=audit.main()
            x=json.loads(path.read_text())
            self.assertEqual(code,2)
            self.assertFalse(x["model_admission"])
            self.assertEqual(x["status"],"SOURCE_ACCESS_OR_SCHEMA_STOP")
            self.assertNotIn("PRIVATE_DETAIL",json.dumps(x))

    def test_all_baseline_blocks_remain_visible_when_a_covariate_is_entirely_missing(self):
        x=self.inspect([row(site="F"+str(i),plant_density="NA") for i in range(5)])
        b=x["baseline"]["harvest_mass_area_author_visits"]["all_three"]
        self.assertEqual(b["blocks"],1)
        self.assertEqual(b["complete_rows"],0)
        self.assertEqual(b["block_size_distribution"],{"5":1})
        self.assertEqual(b["complete_case_block_size_distribution"],{"0":1})

    def test_invalid_physical_domains_are_distinguished_from_numeric_presence(self):
        x=self.inspect([
            row(site="F1",outcome="-1"),
            row(site="F2",visitation_rate="-1"),
            row(site="F3",use_visits_or_abundance="use abundance",sampling_abundance="sweep net",abundance="-1"),
            row(site="F4",outcome="101",yield_units="fruit set (%)"),
            row(site="F5",outcome="0",visitation_rate="0"),
        ])
        self.assertEqual(x["frames"]["primary_reviewed_direct"]["rows"],3)
        self.assertEqual(x["frames"]["author_use_visits_direct_timed"]["rows"],1)
        self.assertEqual(x["frames"]["author_use_abundance_direct"]["rows"],0)
        self.assertEqual(x["invalid_domains"],{
            "primary_direct_negative":1,"primary_percentage_above_100":1,
            "negative_visitation":1,"negative_abundance":1})

    def test_abundance_candidate_requires_a_documented_taxonomic_scope(self):
        x=self.inspect([row(use_visits_or_abundance="use abundance",
            sampling_abundance="sweep net",abundance="2",taxa_recorded="none")])
        self.assertEqual(x["frames"]["author_use_abundance_direct"]["rows"],0)

    def test_duplicate_key_audit_does_not_depend_on_crop_or_group_completeness(self):
        x=self.inspect([row(),row(crop="NA",group="")])
        self.assertEqual(x["anomalies"]["duplicate_candidate_keys"],1)

    def test_incomplete_duplicate_cannot_disappear_from_baseline_eligibility(self):
        records=[row(site="F"+str(i),field_size=str(i+1)) for i in range(5)]
        records.append(row(site="F0",plant_density="NA"))
        x=self.inspect(records)
        b=x["baseline"]["harvest_mass_area_author_visits"]["all_three"]
        self.assertEqual(b["complete_rows"],5)
        self.assertEqual(b["blocks_with_duplicate_candidate_keys"],1)
        self.assertEqual(b["blocks_at_least_five"],0)
        self.assertEqual(b["variable_blocks"],0)

    def test_missing_source_nodes_cannot_collide_with_real_source_ids(self):
        x=self.inspect([
            row(study="A_2001",group="",site="F1"),
            row(study="B_2001",group="_missing_0",site="F2"),
        ])
        g=x["grouping"]
        self.assertEqual(g["provisional_study_id2_groups"],1)
        self.assertEqual(g.get("unresolved_source_nodes"),1)
        self.assertEqual(g["components_including_unresolved_nodes"],2)
        self.assertEqual(g["combined_components"],1)
        self.assertEqual(g["largest_component_study_id2_groups"],1)

    def test_visit_unit_missing_tokens_share_one_missing_category(self):
        x=self.inspect([row(site="F"+str(i),visitation_rate_units=v)
                        for i,v in enumerate(["","NA","N/A"])])
        self.assertEqual(x["metadata_categories"]["visit_unit_family"],{"missing":3})

if __name__ == "__main__":
    unittest.main()
