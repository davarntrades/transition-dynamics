# VF onset programme — Phase 0 dataset verification (SDDB v1.0.0)

> **Status: PHASE 0 RECORD. Metadata only.**
>
> - Read: headers, annotation files, the checksum manifest and PhysioNet's
>   own description page for the dataset.
> - **No ECG sample was read or decoded.** The 23 signal files were
>   SHA-256-hashed in-stream and never stored.
> - **No pre-VF physiological feature was computed or inspected.**
>   Annotations were read only under the sealed-zone policy in §2.
> - Nothing here changes any hypotension result, `CANONICAL_STATUS.md`, any
>   frozen protocol, or any source mathematics.
> - The VF protocol is **not frozen** and **no VF experiment was run**.
>
> Code: [`analysis/vf/phase0_verify.py`](../analysis/vf/phase0_verify.py) ·
> Output: [`analysis/results/vf_phase0_metadata.json`](../analysis/results/vf_phase0_metadata.json)

---

## 1. Access path, blocker and provenance

| Item | Evidence |
|---|---|
| **Blocker** | `physionet.org:443` is refused by this session's egress proxy: HTTP 403 to CONNECT, logged as `connect_rejected … policy denial`. The PhysioNet project page itself was therefore **not** read |
| **Configuration that removes it** | Add `physionet.org` to the environment's *Allowed domains* (environment settings → Network access; see the Claude Code cloud-environment docs, "network access"). The proxy has no other restriction on this host |
| **Path actually used** | PhysioNet's open-data mirror on AWS, `https://physionet-open.s3.amazonaws.com/sddb/1.0.0/` (bucket `physionet-open`). It is reachable, and it carries the project's own `SHA256SUMS.txt`, `RECORDS`, `ANNOTATORS` and the original PhysioBank description page (`index.shtml.shtml`) |
| Dataset / version | Sudden Cardiac Death Holter Database (`sddb`), **v1.0.0** |
| Files in the mirror | 110: 23 × {`.dat`, `.hea`, `.hea-`, `.ari`}, 12 × `.atr`, plus `RECORDS`, `ANNOTATORS`, `SHA256SUMS.txt`, `index.shtml.shtml`, `index.shtml-wz`, `vf-30.png` |
| Manifest | `SHA256SUMS.txt`, 109 entries. SHA-256 of the manifest itself: `03196bc43c2d751bd902414c388c392849349509fe20d7f5f510700c903e1f7a` |
| Checksum verification | **109 / 109 match.** 86 non-signal files were verified locally. All 23 `.dat` files were verified by streaming SHA-256 without storing them. Every `.dat` size equals header samples × 3 bytes (format 212, 2 signals); 49.dat is +1 byte (odd-sample padding) |
| Residual provenance limit | The manifest and the files came from the same mirror. They were **not** cross-checked against physionet.org, which is unreachable. Mirror–origin identity is assumed, not verified |
| Retrieval date | 2026-11-03 |

**Search snippets were not used as evidence anywhere in this document.**
Where an earlier design document relied on them, the verified value replaces
them. See §7.

---

## 2. Read policy (enforced in code)

| Rule | What may be read | Why it is outcome-blind |
|---|---|---|
| P1 | Format: annotation counts, first/last time, presence of rhythm annotations. Code vocabularies pooled across records only | file-format verification |
| P2 | VF-type event markers (`[`, `!`, `(VF…`) | these are the event label itself |
| P3 | Baseline zone [15, 45) min, only when it ends ≥ 60 min before onset: beat count, rhythm labels, `.ari`/`.atr` agreement | the protocol's baseline is outcome-blind by construction |
| P4 | **Nothing else before onset.** No ectopy counts, VT runs or rhythm changes in the remote, grey or warning-bin zones | sealed |
| P5 | Beat annotations in [onset, onset + 180 s): **post-onset only** | corroborates the event label without touching pre-VF data |

---

## 3. Record-level verification

The page column heading reads "VF Onset Time (**elapsed**)", and the
header `#vfon` comments match the page table exactly for all 20 VF records.

Column notes:

- **Base time** comes from the header. "(?)" marks the `12:00:00` value,
  which is probably a placeholder (§4.4).
- **Remote zone** is minutes of remote zone available under the v2
  geometry: onset − 15 − 30 − 5 − 60.
- **2h20 … 4h** are the eligibility rules.
- **Baseline beats** are `.ari` beat annotations in [15, 45) min.

| rec | duration | base time | xform offset | gain (adu/mV) | rhythm (page) | VF onset (elapsed) | remote zone (min) | 2h20 | 2h50 | 3h | 4h | analysis | `.atr` | baseline beats |
|---|---|---|---|---|---|---|--:|:--:|:--:|:--:|:--:|:--:|:--:|--:|
| 30 | 24:33:17 | 12:00:00 (?) | 26:35 | 800/800 | Sinus | 07:54:33 | 365 | ✓ | ✓ | ✓ | ✓ | A | yes | 2592 |
| 31 | 13:58:40 | 10:15:00 | 13:20 | 800/800 | Sinus | 13:42:24 | 712 | ✓ | ✓ | ✓ | ✓ | A | yes | 2262 |
| 32 | 24:20:00 | 5:04:00 | 18:00 | 800/800 | Sinus + intermittent demand V pacing | 16:45:18 | 895 | ✓ | ✓ | ✓ | ✓ | A | yes | 2627 |
| 33 | 24:33:00 | 10:38:00 | 7:00 | 800/800 | Sinus | 04:46:19 | 176 | ✓ | ✓ | ✓ | ✓ | A | no | 1766 |
| 34 | 07:05:20 | 12:00:00 (?) | 0 | 800/800 | Sinus | 06:35:44 | 286 | ✓ | ✓ | ✓ | ✓ | A | yes | 1848 |
| 35 | 24:52:00 | 12:00:00 (?) | 0 | 800/800 | AF | 24:34:56 | 1365 | ✓ | ✓ | ✓ | ✓ | B | yes | 2479 |
| 36 | 20:21:20 | 15:09:00 | 8:40 | 800/800 | AF | 18:59:01 | 1029 | ✓ | ✓ | ✓ | ✓ | B | yes | 1947 |
| 37 | 25:08:00 | 14:29:00 | 10:00 | 800/800 | AF | 01:31:13 | 0 | ✗ | ✗ | ✗ | ✗ | (B) | no | sealed |
| 38 | 18:18:25 | 12:00:00 (?) | 8:55 | 800/800 | Sinus | 08:01:54 | 372 | ✓ | ✓ | ✓ | ✓ | A | no | 2973 |
| 39 | 05:47:00 | 12:00:00 (?) | 0 | **200/200** | Sinus | 04:37:51 | 168 | ✓ | ✓ | ✓ | ✓ | A | no | 2349 |
| 40 | 24:53:00 | 9:50:00 | 0 | 800/800 | **Paced (continuous)** | — no VF | — | | | | | — | no | 2293 |
| 41 | 03:56:00 | 11:45:00 | 0 | 800/800 | Sinus | 02:59:24 | 69 | ✓ | ✓ | ✗ | ✗ | A | yes | 2707 |
| 42 | 25:08:10 | 12:00:00 (?) | 18:10 | 800/800 | Sinus | — no VF | — | | | | | — | no | 2747 |
| 43 | 23:07:50 | 12:00:00 (?) | 1:20 | 800/800 | Intermittent V pacing | 15:37:11 | 827 | ✓ | ✓ | ✓ | ✓ | A | **no** | 2185 |
| 44 | 23:20:00 | 14:51:00 | 0 | 800/800 | Sinus | 19:38:45 | 1069 | ✓ | ✓ | ✓ | ✓ | A | no | 2296 |
| 45 | 24:09:20 | 12:00:00 (?) | 0:40 | 800/800 | Sinus | 18:09:17 | 979 | ✓ | ✓ | ✓ | ✓ | A | yes | 2096 |
| 46 | 04:15:10 | 10:20:00 | 9:50 | 800/800 | Sinus | 03:41:47 | 112 | ✓ | ✓ | ✓ | ✗ | A | yes | 2411 |
| 47 | 23:35:50 | 12:00:00 (?) | **44:10** | **200/200** | Sinus | 06:13:01 | 263 | ✓ | ✓ | ✓ | ✓ | A | no | 1838 |
| 48 | 24:36:15 | 10:15:00 | 7:45 | 800/800 | Sinus | 02:29:40 | 40 | ✓ | ✗ | ✗ | ✗ | A | no | 2933 |
| 49 | 24:52:04 † | 13:40:00 | 6:05 | 800/800 | Sinus + intermittent pacing | — no VF | — | | | | | — | yes | 1666 |
| 50 | 23:07:38 | 21:50:00 | 0:22 | 800/800 | AF | 11:45:43 | 596 | ✓ | ✓ | ✓ | ✓ | B | no | 1468 |
| 51 | 25:08:30 | 12:00:00 (?) | 0 | 800/800 | Sinus + intermittent pacing | 22:58:23 | 1268 | ✓ | ✓ | ✓ | ✓ | A | yes | 1508 |
| 52 | 07:31:05 | 12:00:00 (?) | 5:55 | 800/800 | Sinus | 02:32:40 | 43 | ✓ | ✗ | ✗ | ✗ | A | yes | 2895 |

† The page lists 25:01:40 for record 49. The header samples give 24:52:04.
A 9.6-min discrepancy in a no-VF record.

---

## 4. Verified properties against the protocol's needs

### 4.1 Counts

| Quantity | Verified value | v1/v2 assumption |
|---|---|---|
| Records / patients | **23 / 23** (one record per patient; page clinical table) | 23 ✓ |
| Records with VF onset | **20**. No VF: **40** (continuously paced), **42** (sinus), **49** (sinus + intermittent pacing) | 20 ✓. v1 called 49 "paced, no VF", but the page says **intermittent** pacing |
| Rhythm | 14 sinus; 4 sinus with intermittent pacing (32, 43, 49, 51); 1 continuously paced (40); 4 AF (35, 36, 37, 50) | matches the page summary "18 sinus (4 intermittent pacing), 1 paced, 4 AF" |
| Sampling | **250 Hz, 2 channels, format 212, 12-bit, every record** | 250 Hz ✓ (now verified) |
| Gain | 800 adu/mV, except records **39 and 47 at 200 adu/mV** (4× coarser amplitude quantisation) | not previously known |
| Leads | signal description is "ECG" only. **Lead identity is not recorded** | v2 assumed "lead 1 primary". That is not anatomically meaningful |
| Duration | 3:56:00 to 25:08:30. 18 of 23 are ≥ 18 h | ✓ |
| Clinical data | age and sex mostly present; history and medication "Unknown" for most; several on digoxin/quinidine (pro-arrhythmic class) | — |
| Recording era | "mainly obtained in the 1980s in Boston area hospitals" (page) | ✓ |

### 4.2 VF onset annotations and their reliability

- **The onset exists only as the header comment `#vfon` and the page table.**
  No annotation file contains any VF-type marker. Across all 43 annotation
  files, the pooled `.ari` symbol vocabulary is `+ ? E N Q S V r s`, and its
  rhythm vocabulary is only `(N`, `(AFIB` and ST-episode labels. `.atr` files
  carry beat labels and no rhythm annotations. No annotator, method or
  precision is documented for `#vfon`.
- **Units are verified as elapsed time in the distributed record.** The page
  says "elapsed". Record 35's `24:34:56` cannot be a clock time. Every onset
  lies within its record's duration.
- **Post-onset corroboration (P5).** In all **10** VF records whose audited
  `.atr` covers the onset (30, 31, 32, 34, 36, 41, 45, 46, 51, 52), the
  audited beat stream within 60 s after `#vfon` either stops or becomes
  high-rate non-normal complexes. Record 35 also has an `.atr`, but it ends
  at 24:00:00, before its onset (24:34:56), so its zero count reflects
  coverage, not VF. Examples: 30, 31 and 32 show 7–9 beats in the first
  minute and then none; 41 shows 226 non-N per minute. This is consistent
  with a ventricular tachyarrhythmia beginning near the label. It also argues
  against a large shift from the xform extraction offsets in 30, 31 and 32,
  whose offsets are 13–27 min. Record 36 is mixed: 32 of 103 complexes are
  labelled N.
- **In the 10 VF records without a covering `.atr`** (33, 35, 37, 38, 39,
  43, 44, 47, 48, 50), the labels **cannot be corroborated** from the files. The unaudited
  `.ari` keeps annotating "beats" after onset, mostly as normal `N`. Record
  48 has 134 in the first minute and 286 in the next two minutes, 284 of
  them N. **The automated analyser labels ventricular-tachyarrhythmia
  complexes as normal beats.**
- **Pre-onset precision is not verifiable without reading pre-onset signal**,
  which is prohibited in this phase. Two things remain unknown: whether VF
  began earlier than the label, and whether earlier VF or VT episodes exist
  in the remote zone. A separately approved Phase 0b would be needed.

### 4.3 Beat annotations

| Property | Finding |
|---|---|
| Coverage | `.ari`: whole record (first annotation ≤ 3.7 s). `.atr`: 12 records. Several end at exactly 86,399 s, i.e. truncated at 24 h. Record 35's `.atr` ends before its onset |
| Baseline agreement, `.ari` vs `.atr` (11 records with both, ±150 ms) | detection sensitivity 0.967–1.000; PPV 0.912–1.000 (record 30: `.ari` has 9% extra detections). Normal-vs-other class agreement ≥ 0.97 in 9 records, **0.834 in record 51** (intermittent pacing), **0.001 in record 36** (AF: incompatible labelling conventions) |
| Paced beats | the `.ari` vocabulary has **no paced-beat code** (`/`). Paced-beat removal (Analysis A) is possible from `.atr` for 32 and 51. **Not possible from annotations for 43** (no `.atr`) |
| Rhythm labels | `.ari` `(AFIB` appears in the baseline of **sinus** records 30, 33, 44 and 52. The AF records 35, 36 and 50 carry no AF label in their baseline. **`.ari` rhythm labels are not usable for rhythm classification** |
| Near onset | `.ari` labels post-onset tachyarrhythmia complexes as `N` (§4.2). **`.ari` beat classes are unreliable exactly where ventricular ectopy and VT matter** |
| Baseline beat yield | ≥ 1,466 annotated beats in [15, 45) min in every eligible record. The v2 floor of ≥ 600 complete panel beats is not binding at the annotation level. Panel completeness needs signal and was not assessed |

### 4.4 Clock time

- **No header has a date.** 11 of 23 headers give exactly `12:00:00`, which
  is almost certainly a placeholder.
- 12 give other times, but it is unclear whether these refer to the
  distributed record or the original tape: every header states "Produced by
  xform … beginning at mm:ss", with offsets of 0–44 min.
- Among the 16 Analysis-A-eligible patients, only **7** (31, 32, 33, 41, 44,
  46, 48) have a non-placeholder start time.
- **Verdict:** clock time is **unavailable for 9 of 16** eligible patients
  and **unverified** for the other 7. Under provisional decision D6,
  circadian confounding remains **unresolved**. A clock-time-matched control
  would have 7 subjects, below the v2 minimum of 8, so it is non-evaluable.

### 4.5 Eligibility (provisional decisions D1, D5 applied)

| Rule (onset ≥) | Analysis A (sinus + intermittent pacing; primary) | Analysis B (+ AF; secondary, D1) | excluded VF records |
|---|:--:|:--:|---|
| **2 h 20 min** (primary, $R_{\min}$ = 30) | **16** | **19** | 37 |
| 2 h 50 min ($R_{\min}$ = 60, mandatory sensitivity under D5) | 14 | 17 | 37, 48, 52 |
| 3 h | 13 | 16 | 37, 41, 48, 52 |
| 4 h | 12 | 15 | 37, 41, 46, 48, 52 |

- Record 41 misses the 3-h rule by 36 s (onset 02:59:24).
- Records 48 and 52 (onsets 02:29:40 and 02:32:40) sit 10 and 13 min above
  the 2 h 20 rule.
- **Their inclusion therefore depends on D5, and the 60-min sensitivity
  analysis removes them.**
- No VF patient is continuously paced; record 40 has no VF. So the
  "continuous pacing" exclusion removes nobody from either analysis.

### 4.6 Window feasibility (geometry only)

- Under the primary rule, every eligible patient can supply the full zone
  geometry: settling, a 30-min baseline, a remote zone of ≥ 30 min, the
  grey zone, and all four bins.
- Remote zones range from **40 min (48) and 43 min (52)** to 1,268 min (51).
- **Positive windows per patient per bin:** 3 (B5), 5 (B10), 5 (B15) and 15
  (B30), before any VT/ectopy exclusion. For Analysis A that totals
  16 × 28 = 448 positive windows. Because of the ~15–20-min correlation length
  ([`VF_DESIGN_SIMULATION.md`](VF_DESIGN_SIMULATION.md) §3.1), this is about
  **one effective observation per patient per bin**.
- **Unknown until execution (sealed):** how many bin windows the sustained-VT
  rule removes. It cannot be computed from annotations anyway: no VT rhythm
  annotations exist, and `.ari` labels tachyarrhythmia complexes as N.
- Pseudo-onset availability (onset ≥ 5 h 20 min for one 3-h offset):
  Analysis A has 10 VF patients (30, 31, 32, 34, 38, 43, 44, 45, 47, 51).
  The no-VF records 42 and 49 are also usable for Analysis A; 40 is
  continuously paced. That gives **12 ≥ 8**, so the control is evaluable.

---

## 5. Findings, ranked

| # | Severity | Finding | Consequence for the protocol |
|:--:|:--:|---|---|
| P0-1 | **CRITICAL** | The event label is an undocumented header comment, with no VF annotation anywhere. Post-onset corroboration is possible for only **9 of 16** Analysis-A patients | onset precision and possible earlier episodes are unverified. Labels for 7 eligible A patients (33, 38, 39, 43, 44, 47, 48) are not corroborated |
| P0-2 | **CRITICAL** | The unaudited `.ari` labels ventricular-tachyarrhythmia complexes as normal beats | v2's NN series, ectopy features (M1), sustained-VT exclusion and NSVT sensitivity cannot use `.ari` labels near onset. **Repair required** |
| P0-3 | **MAJOR** | No paced-beat code in `.ari`; no `.atr` for record 43 | Analysis A's "paced beats removed" is not implementable for 43 from annotations |
| P0-4 | **MAJOR** | `.ari` AF rhythm labels contradict the clinical table | AF episodes within sinus records cannot be identified from annotations, so NN features may be contaminated |
| P0-5 | **MAJOR** | Clock time unavailable (9/16) or unverified (7/16) | circadian confounding unresolved (D6). The clock-matched control is non-evaluable |
| P0-6 | **MAJOR** | Lead identity unrecorded; two records at 4× coarser gain | "lead 1 primary" is arbitrary across patients. Morphology (Tamp, ST, TWA) precision is lower in 39 and 47 |
| P0-7 | MODERATE | Verified eligible n = 16 (A) / 19 (B), not the simulated 20 | power and MDE must be recomputed on the verified set (see the independent review) |
| P0-8 | MODERATE | Two eligible records (48, 52) carry ≈ 40 min of remote zone | the precision cost is modest, but these records decide the D5 sensitivity |
| P0-9 | MINOR | Record 49's duration differs between header and page (9.6 min) | no-VF record. The header governs |
| P0-10 | MINOR | Provenance verified against the mirror's manifest, not physionet.org | allowlisting physionet.org would close it |

---

## 6. What Phase 0 did not do (by restriction)

- Read no ECG sample.
- Computed no feature.
- Inspected no annotation in the remote, grey or bin zones.
- Did not count sustained-VT episodes, earlier VF episodes or ectopy.

These require either execution of a frozen protocol or a separately approved,
pre-specified **Phase 0b label-verification step** (see
[`VF_READINESS_ASSESSMENT.md`](VF_READINESS_ASSESSMENT.md)).

## 7. Corrections to earlier design documents

| Earlier statement (search-snippet based) | Verified |
|---|---|
| "250 Hz (secondary source only)" | 250 Hz, all records |
| "49: paced, no VF" | 49: sinus with **intermittent** pacing, no VF. 40 is the continuously paced record |
| "18 sinus / 4 AF / 1 paced — sources conflict" | the page states exactly this. Per-record mapping in §3 |
| "audited `.atr` for an incomplete subset (reported as 12)" | 12 ✓. Some are truncated at 24 h, and record 35's does not reach onset |
| "≈ 12–18 eligible (A)" | **16** (A) / **19** (B) under 2 h 20 |
| "rhythm annotations may mark VT before VF" | **no VT or VF rhythm annotations exist** |

---

© 2026 Davarn Morrison · Transition Dynamics
