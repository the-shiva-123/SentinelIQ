# Raw Data Validation Report

**Status:** FAILED
**Run Date:** 2026-06-07T13:40:57Z
**Data Directory:** `data/raw`

## Summary of Dataset Metadata
- **Dataset Version:** `v001`
- **Client:** `NexaTel Communications Ltd.`
- **Service Provider:** `Asterion Digital Operations Services Pvt. Ltd.`

## File Counts & Validation Summary
| Category | Expected Extension | Valid Files Count | Status |
|---|---|---|---|
| Policies | `.pdf` | 38 | PASS |
| Release Notes | `.docx` | 20 | PASS |
| Logs | `.log` | 42 | PASS |
| Docs (Architecture & Decisions) | `.md`/`.docx` | 26 | PASS |

## Bad Files Detected
We detected the following files that violate extension rules, are zero-byte placeholders, or contain corrupted structure:
- `release_notes/deployment_checklist.txt` (invalid extension)
- `logs/session_events_recovery.json` (rejected due to invalid JSON content)
- `docs/escalation_runbook_scratch.md` (zero-byte file)

## Errors
- PDF Corruption: `policy_security_exceptions_v2.pdf` and `policy_vulnerability_management.pdf` are corrupted.
- DOCX Corruption: `release_notes_NXTEL_2023_Q2_v2.5.0_corrupted.docx` has a corrupted structure.
- Log Corruption: `session_events_recovery.json` contains invalid JSON.

## Warnings
- Log Corruption: 423 invalid JSON lines detected across operations log files.
- Duplicates: 3 sets of duplicate files found:
  1. `policies/policy_incident_response_v2.pdf` is a duplicate of `policies/policy_incident_response.pdf`
  2. `logs/nexatel_managed_ops_2023_09_ops.log` is a duplicate of `logs/nexatel_managed_ops_2023_09.log`
  3. `release_notes/release_notes_NXTEL_2024_Q2_v3.1.0_final.docx` is a duplicate of `release_notes/release_notes_NXTEL_2024_Q2_v3.1.0.docx`
