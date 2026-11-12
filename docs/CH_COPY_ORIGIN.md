# CH Copy Origin

- Source repository: `Hiroyuki-Kawasaki20/CH`
- Source commit: `539970e6d35425fd0e4b59b463fd7af81507b6aa`
- Copy date: 2026-11-12
- Git history was not copied. This project starts with a new repository and history.

## Intentional exclusions

- `_archive/` and `docs/_archive/`: archived material was not needed for the project baseline. This includes `_archive/入車時間マスタ_pre_switch_20260730.xlsx.bak`, an archived operational master.
- `tests/fixtures/issue42/nyusha_master_snapshot.xlsx` and `tests/fixtures/issue42/spo_upload_snapshot.xlsx`: verified as operational-data snapshots, not synthetic test data.
- `tests/fixtures/issue97/nyusha_master_snapshot.xlsx`, `tests/fixtures/issue97/spo_upload_snapshot.xlsx`, and `tests/fixtures/issue97/output_snapshot_20260824_1954.xlsx`: the source commit describes these as real-data fixtures.
- `tests/fixtures/issue_edf_20260820.json` and `tests/fixtures/issue_edf_20260820_v2.json`: the source commits identify these as captured from real operational runs.
- The following test modules depend on excluded fixtures and were omitted to avoid broken tests: `tests/unit/test_main_assignment_inspection_delay.py`, `tests/unit/test_relief_declined_keeps_current.py`, `tests/unit/test_relief_earliest_start.py`, `tests/test_issue97_followup_front_pack.py`, `tests/test_issue97_unneeded_overflow.py`, `tests/test_issue_edf_integration.py`, `tests/test_issue_edf_lane_assignment.py`, and `tests/unit/test_issue94_lane_priority.py`.

## Current status

This is a copy of CH logic only. N8-specific settings separation, process assignment, and input reconciliation are not implemented. The three-process-plus-relief workflow is also not implemented.

Do not launch the normal GUI yet. It may access CH settings or shared master files because N8-specific storage and workflow isolation have not been implemented.