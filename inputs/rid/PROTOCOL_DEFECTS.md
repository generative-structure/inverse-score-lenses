# R-ID — defects in the sealed protocol

**One defect recorded: D1 (Task A's 27-class scope).** Created empty at seal
time; D1 was found during implementation planning, before any R-ID code was
written and before any result existed.

`rid/PROTOCOL.md` is sealed (SHA-256 in `rid/PROTOCOL.sha256`) before any R-ID
substrate, code or result, and before the S4 re-score. If implementation or
execution reveals a flaw **in the sealed text itself**, it is recorded here.

## Why a defect log rather than an amendment

A post-seal amendment may correct an **implementation error** and never a
**design choice**. Editing `PROTOCOL.md` to fix a flaw in its own reasoning
would break the seal and destroy what the seal establishes. Such flaws are
recorded here, adjudicated in the open, and carried into the manuscript's
limitations.

An empty log at the end of a study is not evidence the protocol was perfect;
it is evidence about whether anyone looked. This one is empty because nothing
has been run — and R-ID may never be run (`PROTOCOL.md` status block).

## Convention

Following `sid/PROTOCOL_DEFECTS.md` and `s12/PROTOCOL_DEFECTS.md`: each defect
gets a numbered `D<n>` section stating what the protocol says, what the defect
is, a **demonstration by measurement** wherever measurement is possible, what
was adjudicated and why, the effect on the verdicts including "none", and the
sentence the manuscript's limitations owes a reader. A closing "Not defects"
section records what was checked and found sound, so the log distinguishes
*checked and clean* from *never looked at*.

## Note on inherited defects

R-ID **deliberately corrects** two defects logged against S-ID rather than
inheriting them — D1's degenerate floor and D2's capped confusion statistic —
with the reasons stated in `PROTOCOL.md` §4. Those corrections are design
choices made **before** sealing and are not amendments. They mean P-R-B's floor
and P-R-C are not directly comparable to S-ID's counterparts, which is intended
and stated.

## Scope

Defects in the **protocol**. Implementation errors are amendments, logged in
`DECISIONS.md`. A fault with both aspects appears in both places with a
cross-reference.


---

## D1 — Task A is defined as 27-class recovery, but 260 worklists do not exist

**What the protocol says.** §3 states the unit of analysis as
`2,423 units × 27 specifications = 65,421 worklists`, and §4 defines Task A as
predicting `cell_name` over **27 classes**.

**The defect.** 65,421 worklists do not exist. **52 units scored only 22
specifications**, having skipped their five `full_categorical` cells under the
frozen cardinality and byte bounds, so **260 worklists are absent** and the true
count is **65,161**. The sealed text describes a task that cannot be executed
exactly as written.

**This is a defect of SCOPE in the sealed description, not an error in the
substrate.** The 52 units are correctly scored; the skips are frozen policy
(`fullcat_above_onehot_max`, and the `FULLCAT_BYTES_MAX` bound added by Arm A/B
post-gate amendment 7, itself declared as a preregistration deviation). What is
wrong is the protocol's arithmetic and its implicit assumption that every unit
contributes every class.

**The affected units are systematically the largest and highest-cardinality,
not a random subset.** Measured:

| | units | median n | median vendor cardinality | min n |
|---|---|---|---|---|
| **skipped (22 cells)** | 52 | **1,249,063** | **31,346** | 56,446 |
| full (27 cells) | 2,371 | 4,339 | 471 | 1,000 |

The median skipped unit sits at the **98.7th percentile** of the n
distribution, and **all 52 lie above n = 56,446**, which exceeds 86.3% of
units. Skip reasons: 35 on cardinality, 17 on the byte bound. Concentrated in
`nyc` (33), `fec` (7), `ct` (7).

**Consequence, stated plainly.** Per-class estimates for the **five
`full_categorical` cells** — `iforest__full_categorical__robust`,
`lof__full_categorical__robust`, `knn__full_categorical__robust`,
`ae__full_categorical__robust`, `dup_pair__full_categorical__raw` — derive from
a **different unit population** than the other 22 classes: one from which the
largest and highest-cardinality units are entirely absent. Any comparison of
recall across classes is therefore not like-for-like.

**Handling, declared now, before any result exists:**

1. **All 27 classes retained.** None is dropped.
2. **No reweighting.** Class priors are left as the data gives them.
3. **No imputation or synthesis** of the missing worklists.
4. **Per-class recall is reported with per-class instance counts alongside**, so
   the imbalance is visible **in the output** rather than only in this log. A
   reader must be able to see that five classes rest on 2,371 units and 22 on
   2,423 without consulting a defect file.
5. The **five affected classes are named** wherever per-class figures appear.

**Effect on the verdicts.** Task A's headline accuracy is computed over all
available instances and is affected only to the extent that 0.4% of instances
are absent. The interpretation-scale bands of §4 are unchanged. What is affected
is the **comparability of per-class recall**, which is now reported with the
counts that make it legible.

**Carry into the manuscript.** One sentence: the identification task's class set
is not uniformly populated, because the largest units cannot run the
categorical-feature cells at all, and per-class figures for those five cells
therefore describe a smaller and systematically different population of units.

**Not a reason to amend.** The sealed text stays as written. Correcting "27
specifications" to "22 or 27 by unit" would be a design edit after sealing, and
the arithmetic error is visible here instead.

---

## D2 — the grouping unit is mis-specified relative to record independence

*Logged 2026-08-02, during the Paper 2 verification pass, **before the addendum
protocol was drafted** — the ordering is by construction: the corrective refit
specified in `notes/ADDENDUM_PROTOCOL_DRAFT.md` exists because this entry does,
not the other way round. (The header line at the top of this file, "One defect
recorded: D1", predates this entry; append-only convention leaves it standing.)*

**What the protocol says.** §4 commits Task A to grouped 5-fold
cross-validation with the **unit** as the grouping key. The implementation
follows it exactly: `groups = df.unit_id.to_numpy()` (`rid/analysis.py:230`,
and the parallel line at `:361` for Task A-family), where `unit_id` is
`corpus|pi|unit` (`rid/substrate.py:85`), handed to
`GroupKFold(n_splits=5)` (`rid/analysis.py:143-145`).

**The defect.** The unit is not the unit of record independence. Per
`config/frozen_corpora.yaml:16-53`, **eleven of twelve corpora carry units at
both Π levels** — `fy` and `fy_office`; `md` is the sole `fy`-only corpus — and
the file's own note at `:54-55` states the nesting: `fy_office = fiscal year x
office`. **129 `fy` units are parents of 2,294 `fy_office` units.** The nesting
is exact: in all eleven both-level corpora the set of fiscal years appearing at
`fy_office` is a subset of the years appearing at `fy`, so every `fy_office`
unit has a parent `fy` unit whose record set contains it. The
**record-connected components are therefore `corpus × fiscal year`, and there
are 129 of them** — one per `fy` unit.

Grouping on `unit_id` treats parent and child as independent groups. They are
not.

**Demonstration by measurement** (read-only, from
`results/rid/20260730T010224Z_a7d5cb2/worklists.parquet` under the same
`GroupKFold(n_splits=5)` the run used):

| quantity | measured |
|---|---|
| record-connected components | 129 |
| components spanning more than one fold | 93 (77 span all five) |
| units in a fold-spanning component | 2,385 / 2,423 (**98.4%**) |
| rows in a fold-spanning component | 64,145 / 65,161 (**98.4%**) |
| `fy_office` units in a different fold from their parent `fy` unit | **1,828 / 2,294 (79.7%)** |
| rows so affected | **49,356 / 65,161 (75.7%)** |

Record identity itself cannot be joined from the substrate — the `record_ids`
in `results/armAB_s4/unit_cache/*.json` are unit-local positional indices
(0…n−1), and `rid/guard.py` blocks reads of `data/raw/*/substrate/`. It does
not need to be: the Π hierarchy gives the components by construction.

**Magnitude is not predictable from the structure, and the log says so.** The
leaked *test* mass is large (75.7% of rows) but the leaking *training* mass is
small: the `fy` level is 129 units and 3,483 rows, **5.3% of the instance
count**, so in any fold roughly 2,800 parent rows are available to inform ~75%
of test rows. Sibling `fy_office` units within one corpus-year are **disjoint
in records and are not a leak at all**; separating them is exactly the
within-institution generalization Task A means to measure. The contamination
channel is narrow but broadly touching. Anyone asserting a direction for the
effect without running the refit is guessing.

**Affected.** Every within-corpus accuracy: Task A 27-class (0.4520 / 0.4368),
Task A learned-only (0.4087 / 0.3778), Task A-family (0.6012 / 0.6181), the
**P-R-A band adjudications** that rest on them, **P-R-D** (a ratio of two
grouped accuracies), and the **grouped side of P-R-GAP**.

**NOT affected.** **P-R-A-LOCO.** `loco_splits` (`rid/analysis.py:148-150`,
called at `:385`) partitions on `corpus`, and every Π view of a corpus carries
that corpus label, so all views of an institution leave together. The LOCO
figures (0.4176 / 0.3796) and the DEFEATED verdict do not rest on the leaking
boundary. The LOCO side of P-R-GAP is likewise clean; only the level of the gap
moves, not its LOCO arm.

**Adjudication.** The sealed verdicts **stand as adjudicated**. The corrective
component-grouped refit — `GroupKFold` on the 129 `corpus × fiscal-year`
components, identical decoders, features and fold count — is specified in the
addendum protocol and will be reported **beside** the sealed figures, never in
place of them. The sealed figures are re-read as an upper bound on
within-institution accuracy, not withdrawn.

**Carry into the manuscript.** One sentence: the within-corpus
cross-validation grouped on the analysis unit rather than on the set of records
an analysis unit draws from, and because eleven of twelve corpora publish the
same records at two nesting levels, roughly three-quarters of instances were
tested against folds that could contain a coarser view of their own records;
the corrected grouping is reported alongside.

**Not a reason to amend.** The sealed text stays as written. Changing the
grouping key after sealing would be a design edit; the corrected analysis lives
in the addendum, under its own protocol, with its own licensed sentences drafted
before its numbers exist.
