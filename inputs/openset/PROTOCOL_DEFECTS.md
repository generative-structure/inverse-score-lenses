# Open-set protocol — defects in the sealed text

`openset/PROTOCOL.md` is sealed before any of its analyses ran. If a flaw is
found **in the sealed text itself**, it is recorded here and never amended into
the protocol.

Two versions have been sealed, and this ledger spans both:

| version | seal commit | GitHub-confirmed | status |
|---|---|---|---|
| v1.0 (`openset/v1.0/PROTOCOL.md`) | `8eb6111` | 2026-08-05T14:05:23Z | **superseded on D-O1**, retained, never executed |
| v2.0 (`openset/PROTOCOL.md`) | `2dcf7a6` | 2026-08-05T18:48:44Z | **governing**; executed 2026-08-05 |

D-O1 is a defect of v1.0 and the reason v2.0 exists. D-O2 is a defect of v2.0,
found after execution and before any sentence was selected.

## Convention

Following `sid/PROTOCOL_DEFECTS.md`, `rid/PROTOCOL_DEFECTS.md` and
`addendum/PROTOCOL_DEFECTS.md`: each defect gets a numbered `D-O<n>` section
stating what the protocol says, what the defect is, a demonstration by
measurement where measurement is possible, what was adjudicated and why, the
effect on the verdicts including "none", and the sentence the manuscript owes
a reader.

---

## D-O1 — outcome (4)'s gate is unreachable, because the only held-in instances the protocol defines are the ones the rule is calibrated on

*Logged 2026-08-05, **before any execution**, during implementation of the
sealed text. **Execution did not start.** No result under this protocol
exists.*

**What the protocol says.** §4.1 partitions the training rows exactly two
ways: a **fit** portion and a **calibration split** of 20%, "grouped, disjoint
from fit". No third partition is defined anywhere in the document.

§5.5 then requires that "every metric is computed on held-in instances too",
and names `A_in`, the pooled held-in abstention rate, as **the gate for
outcome (4)**.

§6 outcome (4) triggers on `A_in > 2α = 0.20`, on the reasoning that
"abstention on calibration-consistent data at twice the nominal level means
the mechanism is not functioning as designed".

**The defect.** The only held-in instances the protocol makes available are
the calibration split itself — and that is precisely the set `q_y` is fitted
on. Classwise conformal calibration chooses `q_y` so that the true-class score
falls at or below threshold for a `1 − α` fraction of calibration instances of
class `y`. Abstention requires the emitted set to be empty, which requires
*every* candidate — including the true class — to exceed its threshold. On the
calibration split that can happen for at most about an `α` fraction, and in
practice far less, because a wrong class frequently falls inside its own
threshold even when the true class does not.

So `A_in` measured where the protocol allows it to be measured is bounded
above by roughly `α = 0.10`, and the gate is set at `2α = 0.20`. **The trigger
cannot fire.** Outcome (4) is unreachable as written, and the degenerate
regime it was added to catch would pass the gate silently.

**Demonstration by measurement.** One LOPO fold, S-ID, `autopsy_mix`, sealed
logistic decoder, sealed grouping, `α = 0.10`, calibration split per §4.1
(seed `20260805001`), held-out cell `ae__full__robust`:

| quantity | value |
|---|---|
| gate trigger (§6 outcome 4) | `A_in > 0.2000` |
| measured `A_in` on the calibration split | **0.0005** |
| gate reachable | **no** |
| mean emitted set size | 2.37 |

The measured rate is roughly **400×** below the trigger. This is not a
marginal miss that a different fold might reverse; it is the structural
consequence of measuring an abstention rate on the sample the abstention
threshold was fitted to.

**This is a defect of SPECIFICATION in the sealed text, not an error in the
conformal rule.** The rule is correct and its guarantee holds. What is wrong is
that §5.5 and §6 require a held-in evaluation set that §4.1 never creates.

**What it blocks.** Outcome (4) was added in the pre-seal amendment
specifically to prevent outcomes (1)–(3) being read off a non-functioning
mechanism. As written it provides no such protection. Running the protocol
would produce an `A_in` near zero on every fold, pass the gate on every fold,
and license outcomes (1)–(3) without the check they were gated on ever having
been performed. The gate would appear in the report as satisfied, which is
worse than its absence.

**Why execution stopped rather than proceeding on a reading.** The obvious
repair — reserve a third partition, so held-in evaluation happens on instances
used neither for fitting nor for calibration — is a **design change to a
committed threshold's measurement basis**, made after sealing and after the
defect was visible. Precedent exists for taking literal readings where a
sealed protocol is merely enumerative (`sid/substrate.py` logs several), but
this is not enumerative underspecification: it determines whether a committed
gate can fire at all, and any choice made here is a choice made with the
knowledge that the gate is currently inert.

Choosing it silently is exactly the failure this project's discipline exists
to prevent, and it would be the first time in the program that a threshold's
basis was set after seal. **Execution therefore did not start**, and the
ruling is left to the author.

**Options, stated without recommendation.**

1. **Three-way split.** Amend by ruling — not by editing the sealed text — so
   that training rows partition into fit / calibration / held-in evaluation,
   with the held-in evaluation fraction and seed fixed in the ruling. Outcome
   (4) becomes reachable and means what it was drafted to mean. Cost: one
   additional partition, no additional fit; the run cost in §7.2 is unchanged.
2. **Retire outcome (4).** Rule that the gate is inert as sealed, record it as
   unreachable, and adjudicate outcomes (1)–(3) without it — with the
   manuscript stating plainly that the intended degeneracy check could not be
   performed under the sealed text.
3. **Re-seal.** Treat the protocol as void, correct §4.1/§5.5/§6 together, and
   seal v2.0 with a fresh anchor. Cleanest logically, and it costs the current
   chain — which is the strongest in the project — its status as the thing
   that was sealed before its numbers existed.

**Effect on the verdicts.** None. Nothing has run; no sealed verdict anywhere
in the project is touched.

**Carry into the manuscript.** If option 1 or 2 is taken, one sentence: the
open-set protocol committed a degeneracy gate whose trigger was unreachable as
specified, the defect was found before execution and logged, and the gate was
either repaired by ruling or reported as inert — with the reader told which.

**Not a reason to amend the sealed file.** `openset/PROTOCOL.md` stays exactly
as sealed whatever is decided. The seal, its hash, and its anchors remain
valid; what they attest is that this text was fixed before its numbers
existed, and that remains true — including the part of it that turned out to
be wrong.

### RULING — 2026-08-05, author. Option 3: re-seal as v2.0.

Recorded **before** any v2.0 text was drafted and before any further execution.

Option 3 was taken over option 1 because the repair is not enumerative. A
protocol whose gate cannot fire is not a protocol with an ambiguous clause; it
is a protocol that does not do what its own text says it does. Repairing that
by ruling would leave a sealed document permanently at odds with the analysis
actually run under it, and every future reader would have to hold the ruling
alongside the seal to know what was measured. Re-sealing costs the chain its
"strongest in the project" status and buys a sealed text that is true.

**The four conditions under which the re-seal is permitted.** These are the
conditions that make a re-seal a correction rather than a do-over, and each is
checkable by a reader:

1. **No committed outcome quantity was computed under v1.** The only execution
   that ever touched v1 is the single diagnostic LOPO fold logged above, which
   measured `A_in` **on the defective basis only** — the calibration split — to
   establish that the gate was unreachable. No value of `A`, `C`, the
   absorption structure, the family-level rates, or the per-institution
   breakdown exists. The re-seal therefore cannot be selecting a protocol to
   fit a result, because no result exists to fit. This is the condition that
   does the real work, and it is why the defect had to be found before
   execution for option 3 to be available at all.
2. **The defect was logged first.** This section existed, with its measurement
   and its options, before the ruling was made and before v2.0 was drafted.
   The record of the flaw is not reconstructed after the fact.
3. **v1 is retained and cited as superseded.** `openset/v1.0/` keeps the sealed
   v1 text, its hash and both OTS receipts byte-identical, so v1 still
   verifies and still anchors. v2.0 cites it. Nothing is deleted, and the
   history is not made to look like v2.0 was the first thing sealed.
4. **The change is scoped to the defect.** v2.0 differs from v1.0 only in the
   D-O1 failure mode — the measurement basis for held-in quantities — plus
   whatever the generalized sweep below turns up in that same class. No
   threshold is retuned, no outcome is re-partitioned, no licensed sentence is
   rewritten to a different meaning, and nothing unrelated is improved along
   the way. A diff against v1.0 is the check.

**What v2.0 changes.** §4.1 partitions training rows three ways — **fit |
calibration | held-in evaluation** — with sizes and seeds fixed in the text.
§5.5 measures held-in quantities on the held-in evaluation partition, which is
used for neither fitting nor calibration. §6's trigger `A_in > 2α = 0.20`
**stands unchanged**: on a genuine held-in evaluation partition, conformal
validity puts a functioning mechanism's abstention at or below `α`, so the
threshold is meaningful once the basis is right. What was wrong was never the
number; it was the sample the number was read off.

**Generalized sweep required before sealing v2.0.** The D-O1 failure mode is
not specific to outcome (4): any committed threshold can be pinned by the
construction of the sample it is evaluated on. Before v2.0 is sealed, every
committed threshold in it is checked against three questions — is the quantity
**computable as specified**, is it computed **on the partition specified**, and
**can it actually vary**. Results are recorded in v2.0 §11. A threshold that
fails any of the three is repaired before sealing or the seal does not happen.

**Effect on the verdicts.** Still none. Nothing has run.

**Carry into the manuscript.** One sentence, now determinate: the open-set
protocol's first sealed version committed a degeneracy gate whose trigger was
unreachable as specified; the defect was found before any execution, logged,
and the protocol re-sealed as v2.0 with the gate's measurement basis corrected,
with v1.0 retained and superseded.

---

## D-O2 — region (3)'s licensed sentence is not instantiable at the corner the R-ID arm actually landed on

*Logged 2026-08-05, **after execution, before any sentence was selected**.
Execution completed in full; every committed quantity was measured. What
stopped is the **reporting** of the R-ID arm, not its measurement.*

**What the protocol says.** §9 establishes that the partition on `(A_in, A, C)`
is total: gate first, then `A ≥ 0.60` → (1); `A ≤ 0.30 ∧ C ≥ 0.50` → (2);
"every remaining combination" → (3). Region (3) is defined as a **residual**.

Its licensed sentence, drafted in §6, reads:

> The decoder abstains on [A] overall, **but the behaviour splits**: [families
> or facets X] are predominantly abstained on, [families or facets Y]
> predominantly absorbed. We name both directions and headline neither.

**What was realised.** R-ID, LOPO-22, pooled over 88 fold-tasks
(2 representations × 2 decoders × 22 folds):

| quantity | value |
|---|---|
| `A_in` (held-in evaluation, the gate) | **0.0000** → (4b) functioning |
| `A` (held-out abstention) | **0.0000** — on every fold, every representation, every decoder, every institution |
| `C` (median confidence of non-abstaining) | **0.2401 – 0.2812** |
| region selected by the partition | **(3)**, since `A ≤ 0.30` but `C < 0.50` |

**The defect.** The point `(A = 0.0000, C ≈ 0.25)` is inside region (3), and
the partition is total exactly as §9 claims. But region (3)'s sentence asserts
a **split** — a set X of families or facets that are "predominantly abstained
on". With `A = 0` exactly, X is **empty**. There is no fold, no facet, no
family and no institution with any abstention at all. The sentence cannot be
instantiated without naming an empty set as though it were populated, which
would be a false statement about the data.

So the outcome space is exhaustive in coordinates and **not exhaustive in
sentences**. Region (3) licenses one narrative — a split — for a region that
contains at least two qualitatively different worlds: a genuine split, and the
corner where the decoder simply never abstains and misattributes *diffidently*.
R-ID landed in the second.

**This is the D-O1 failure mode one dimension over, and §11 did not catch it.**
§11 asked whether each committed *quantity* was computable, on the right
partition, and free to vary. All three hold here: `A` was free to vary, and on
S-ID it did (0.0112 to 0.1379 pooled; one fold reached 0.6225). What §11 never
asked is whether each licensed *sentence* is true throughout the region it
licenses. A protocol can partition its outcome space totally, verify every
threshold reachable, and still own a region whose only sentence is false in
part of it.

**Why this is not a misfire under §0.4.** Nothing failed to fit. No fold
degenerated. `misfire_min_cal = 0` and `misfire_tau = 0` across all 440
fold-tasks; the smallest calibration class held 240 rows (S-ID) and 475 (R-ID).
The machinery worked exactly as sealed. The gap is in the drafted prose.

**The substantive reason `A = 0`, which is itself the interesting part.**
Empty-set abstention requires *every* candidate to be excluded. A decoder whose
posterior is diffuse keeps many candidates inside their conformal thresholds,
so it abstains **less**. R-ID's closed-set accuracy is materially lower than
S-ID's (0.452 / 0.437 against 0.770 / 0.807, §7.4), and its conformal sets are
correspondingly wider. **The abstention mechanism fails to trigger precisely
where the decoder is least certain** — the opposite of what an abstention rule
is for. That is a result, and a more uncomfortable one than either drafted
direction, which is why it must not be quietly filed under a sentence about
splits.

**What is unaffected.** The **S-ID arm adjudicates cleanly and completely**:
`A_in = 0.0101` → (4b) functioning; `A` pooled 0.0112–0.1379 ≤ 0.30 and `C`
pooled 0.5048–0.6694 ≥ 0.50 on all four representation × decoder cells →
**outcome (2), confident misattribution**, whose sentence is instantiable
verbatim. No ruling is needed for S-ID and none is anticipated here.

The committed reporting was produced in full and is not in question:
§5.6's per-institution table (all twelve, `A = 0` uniformly, `C` spanning
0.2425–0.3035, a **1.25×** spread against the 2.7× the protocol expected — the
uniformity is the finding, as §5.6 committed it would be); §6's facet null
(same-algorithm absorption 0.3649 observed against 0.1645 under uniform
absorption, **2.22×**, R-ID; 0.2785 against 0.1655, 1.68×, S-ID); §5.4's family
decoder; and both secondary sweeps.

**Effect on the verdicts.** None outside this protocol. No sealed verdict
elsewhere in the project is touched. Within it: S-ID stands adjudicated;
**R-ID is measured but unreported pending a ruling**.

**Options, stated without recommendation.**

1. **Report R-ID descriptively under (3), without the split clause.** Rule that
   region (3)'s sentence has an unlicensed corner, state the realised numbers
   plainly, and say in the manuscript that the drafted sentence did not fit and
   was not used. Costs nothing but the admission; licenses no interpretation
   the protocol did not commit to.
2. **Extend region (3) by ruling, with a second drafted sentence** for the
   no-abstention corner, written now and marked as post-hoc — dated, logged,
   and flagged in the manuscript as drafted after the numbers existed. Honest
   only if the post-hoc status is stated everywhere the sentence appears.
3. **Re-seal as v3.0** with the corner licensed in advance. This time the cost
   is real and different in kind from D-O1's: the numbers now exist, so a v3.0
   could not claim to have been sealed before them, and the chain's central
   property would be gone for this arm.

**Carry into the manuscript.** One sentence either way: the open-set protocol's
residual outcome carried a single drafted sentence describing a split, the
R-ID arm landed on a corner of that region where no split exists, and the arm
was reported [descriptively / under a post-hoc sentence] with the gap logged.

**Not a reason to amend the sealed file.** `openset/PROTOCOL.md` v2.0 stays
exactly as sealed. Its hash and anchors remain valid.

### RULING — 2026-08-05, author. Option 1: report R-ID descriptively.

Recorded after the forensic pass (`notes/RUN_REPORT_INCIDENTS.md` I1) confirmed
that the committed run is the run, and that the figures of the contradicting
report were absorption and a pre-seal synthetic demonstration misread as
abstention. The ruling therefore adjudicates a defect whose underlying numbers
have been independently recomputed from the persisted parquets.

**Region (3)'s sentence has an unlicensed corner. The R-ID arm is reported
descriptively, without the split clause.** The drafted sentence did not fit
the corner the arm landed on and was not used.

**Rationale.** Licensed sentences are **selected, never written**. Option 2
writes one after the numbers exist, which is the discipline's central
prohibition however carefully the post-hoc status is flagged. Option 3 buys a
licensed corner at the price of the property that makes the chain worth
anything — and unlike D-O1, where nothing had run, a v3.0 could not claim to
precede its numbers. Option 1 follows the pattern **D-A5** and **§B.4**
already set: an outcome that falls outside the sentence space is reported
plainly, with the defect cited, and nothing is licensed that the protocol did
not commit to. D-O2 stands as written above; this ruling adds no sentence to
the protocol and removes none.

**What the manuscript carries wherever the R-ID arm is reported.**

1. The realised numbers plainly: abstention `A = 0` on every fold,
   representation, decoder and all twelve institutions; `C` spanning
   0.2425–0.3035 across institutions — a **1.25×** spread against the 2.7×
   §5.6 anticipated, with the uniformity reported as the finding §5.6
   committed it would be.
2. The mechanism at full strength: empty-set abstention requires excluding
   *every* candidate; a diffuse posterior keeps candidates inside their
   conformal thresholds; therefore **the abstention mechanism fails to trigger
   precisely where the decoder is least certain** — the opposite of what
   abstention is for.
3. One sentence on the gap: the protocol's residual region carried a single
   drafted sentence describing a split, the arm landed where no split exists,
   the arm is reported descriptively, and the gap is logged as D-O2.

**S-ID is unaffected** and adjudicates to **outcome (2)** with its committed
sentence selected verbatim.

**No safe-degradation framing anywhere.** The honest two-arm reading is that on
synthetic data the decoder misattributes unseen pipelines confidently, and on
real data the abstention mechanism never fires at all. The facet null is
reported alongside: same-algorithm absorption **2.22×** uniform on R-ID and
**1.68×** on S-ID.

**Carry into the methods finding.** §11 verified that every committed quantity
was computable, on the partition specified, and free to vary — and never asked
whether each licensed *sentence* is true throughout the region it licenses.
The preregistration lesson now has three clauses: **derive the outcome space;
partition it totally; and verify that each region's sentence holds across the
whole of that region.** D-A5 taught the first, §9 the second, D-O2 the third.
