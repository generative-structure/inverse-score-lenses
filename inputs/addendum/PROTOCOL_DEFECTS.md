# Addendum protocol — defects in the sealed text

`addendum/PROTOCOL.md` is sealed (SHA-256 in `addendum/PROTOCOL.sha256`,
commit `dba5cb7`, received by GitHub 2026-08-03T08:43:19Z) before any of its
analyses ran. If execution reveals a flaw **in the sealed text itself**, it is
recorded here and never amended into the protocol.

## Convention

Following `sid/PROTOCOL_DEFECTS.md` and `rid/PROTOCOL_DEFECTS.md`: each defect
gets a numbered `D<n>` section stating what the protocol says, what the defect
is, a demonstration by measurement where measurement is possible, what was
adjudicated and why, the effect on the verdicts including "none", and the
sentence the manuscript owes a reader.

---

## D1 — §O's governing rule is written without scope, and reaches into a sealed clause it cannot adjudicate

*Logged 2026-08-03, during execution, immediately on §O returning outcome (2).
Ruling received from the author the same day and recorded below.*

**What the protocol says.** §O commits, for the case where the two estimator
routes disagree materially, the licensed sentence:

> The log-loss and Fano routes give [X] and [Y] bits, differing by [D]. The
> disagreement is reported and **the weaker bound governs every claim** in
> the paper.

**What was measured.** §O ran on the twelve persisted §A fits and returned
outcome (2) on every one. The gap is large and one-directional:

| task | representation | I (log-loss) | I (Fano) | gap |
|---|---|---|---|---|
| 27-class | autopsy_mix | 2.110 | **1.173** | 0.937 |
| 27-class | structural | 2.160 | **1.106** | 1.054 |
| 27-class | overlap_profile | 3.073 | **2.402** | 0.671 |
| family | autopsy_mix | 0.849 | **0.535** | 0.314 |
| family | structural | 0.945 | **0.583** | 0.362 |

**The defect.** The phrase *"every claim in the paper"* has no scope
qualifier. Read literally it reaches backwards into **P-R-B**, a clause
sealed in `rid/PROTOCOL.md` under a different protocol, adjudicated against
the log-loss estimator on the sealed unit-grouping, and already PASSED. P-R-B's
levels clause requires I(S;F) ≥ 1.5 bits on both headlined representations;
the log-loss route gives 2.137 and 2.200 sealed (2.110 and 2.160 corrected)
and passes, while the Fano bound gives **1.173 and 1.106** and would not be
met.

An addendum cannot re-adjudicate a clause sealed in a prior protocol. Doing so
would make a post-hoc analysis retroactively govern a prospective one, which
inverts the entire ordering these protocols exist to establish. But §O's
sentence, as written, instructs exactly that.

**This is a defect of SCOPE in the sealed addendum text, not an error in
either estimator.** Both bounds are correct. Fano is the tighter constraint
here because it uses only the error rate and discards the probability
information the log-loss route uses; that it is lower is expected, not
anomalous. What is wrong is that §O's governing rule was written without
saying what it governs.

**Adjudication (author ruling, 2026-08-03).**

1. **Sealed adjudications stand as adjudicated.** P-R-B PASSED on the
   estimator, grouping and data it was sealed against. That verdict is not
   reopened, not recomputed, and not annotated as provisional.
2. **§O governs forward-facing claims only** — every claim the manuscript
   makes in its own voice about how much information a worklist carries,
   as opposed to reports of what a sealed clause adjudicated.
3. **The paper will not claim the ≥1.5-bit levels result on real data.**
   The sealed P-R-B PASS is reported as what it was; the manuscript does not
   restate the bits threshold as a finding of its own.

**Effect on the verdicts.** None on any sealed verdict. P-R-B (levels) and
P-R-B (normalized) stand exactly as adjudicated in the R-ID report. The effect
is on the manuscript's forward-facing prose, which loses a claim it had been
entitled to make under the log-loss route alone.

**Carry into the manuscript.** One sentence: the information estimates carry
two bounds, the error-based bound is materially lower than the cross-entropy
bound, the paper's own claims are stated against the lower one, and the sealed
P-R-B adjudication — which used the cross-entropy route, as its protocol
specified — is reported as the prospective verdict it was rather than restated
as a present claim.

**Not a reason to amend.** The sealed §O text stays as written. Adding "of
this paper's own forward-facing claims" after "every claim" would be a design
edit after sealing. The scope is fixed here instead, in the open, before any
manuscript prose depends on it.

### D1, addendum 2026-08-05 — a later ruling contradicted the realised sealed sentence and is reversed in its favour

*The discipline applied to its own author. Recorded because the reversal is
the record, not a tidy-up of it.*

**What happened.** §O returned outcome (2) on every fit, realising the sealed
licensed sentence: where the routes disagree materially, **the weaker bound
governs every claim in the paper**. D1 above then scoped that rule — correctly
— to the manuscript's forward-facing claims, leaving sealed adjudications as
adjudicated. A **later** ruling by the author went further and held that the
certificate should quote the *largest defensible bound*, promoting the
soft-probability and confusion-region routes to governing status.

**The conflict.** That later ruling contradicts the realised sealed sentence
on its own territory. The certificate is a forward-facing claim in the
paper's own voice — precisely the class D1 assigned to §O — so §O governs it,
and §O says the weaker bound wins. A post-seal ruling cannot displace a
licensed sentence that the protocol drafted before the result existed and that
execution then realised. That ordering is the whole point of sealing.

**Ruling: reversed. The sealed sentence stands.**

1. The certificate's governing figures are the **Fano** column, as already
   carried in `addendum/RESULTS.md`: **2.5390 / 2.8339** at M=22, clearing
   H(plant) = 2.160964 by **0.3780 / 0.6730**; correspondingly **2.8696 /
   3.1146** at M=27, clearing by **0.7086 / 0.9537**. No figure in this
   repository changes — the results file already reports Fano at the one-sided
   95% lower bound. What changes is the manuscript prose that had been
   rewritten to quote the larger route as governing.
2. The soft-probability and confusion-region routes are reported as
   **secondary** — what richer held-out outputs support — with the
   calibration-asymmetry sentence retained and an explicit note that §O's
   weaker-bound rule is why they do not govern.
3. Abstract, §4, contributions and the conclusion are corrected wherever the
   larger figures were quoted as governing. The abstract's two-figure form
   survives; the emphasis flips.

**Effect on the verdicts.** None. No sealed clause is touched, and the
certificate's numbers were already the Fano ones. The correction is to prose
that had drifted off them.

**Why it is logged rather than quietly fixed.** A ruling made after seeing
results lost to a sentence written before them. That is the ordering working
as designed, against the author's own later preference, and it belongs in the
ledger on the same terms as every defect found in the protocol.

---

## D2 — the normalized-ratio machinery presupposes a positive denominator, and the corrected data-side term is negative

*Logged 2026-08-03 during execution. **Execution stopped at this point**, per
the standing rule that an outcome falling outside every committed direction is
a protocol defect and is reported rather than written around.*

**What the protocol says.** §B.4 outcome (3) re-keys P-R-B to two defensible
entropy conventions and commits three directions:

- **(i)** both conventions pass propagated;
- **(ii)** convention 1 passes propagated, convention 2 fails;
- **(iii)** both conventions fail propagated.

All three presuppose that the ratio
`[I(S;F)/H(S)] / [I(corpus;F)/H(corpus)]` is computable — that is, that
`I(corpus;F) > 0`.

**What was measured.** The data-side target was fitted under the corrected
component grouping (§A.2), primary model, both headlined representations,
persisted as `oof_Ocorpus_*`:

| representation | route | I(S;F) | I(corpus;F) | norm_S | norm_corpus | ratio |
|---|---|---|---|---|---|---|
| autopsy_mix | log-loss | 2.110 | **−1.124** | 0.4438 | −0.3135 | **undefined** |
| autopsy_mix | Fano | 1.173 | **−0.151** | 0.2467 | −0.0421 | **undefined** |
| structural | log-loss | 2.160 | **−1.061** | 0.4543 | −0.2960 | **undefined** |
| structural | Fano | 1.106 | **−0.158** | 0.2326 | −0.0441 | **undefined** |

**The defect.** `I(corpus;F)` is **negative on both headlined representations
under both estimators**, so the ratio has a non-positive denominator and none
of §B.4(3)'s three directions applies. There is no committed sentence for this
outcome.

**Why the term went negative, stated as measurement not inference.** Under the
sealed unit grouping the same quantity was **+0.556** and **+0.615**. The swing
is **−1.680** and **−1.676**. The mechanism is the one defect D2 of the R-ID
protocol describes: with grouping on `unit_id`, the year-by-office units of an
institution-year were split across folds, so a decoder predicting *corpus* saw
other views of the same institution-year in training. Component grouping
removes exactly that, and corpus identity then fails to be recoverable at all —
the decoder is worse than the marginal, which is what a negative plug-in
estimate means.

**The substantive reading, offered and flagged as interpretation.** The
dissociation P-R-B was written to detect is not weakened by this; it is
strengthened to a degree the clause cannot express. Specification information
remains substantially positive (1.106–2.160 bits depending on route) while
corpus information is nil or below. The clause asks whether specification
information exceeds corpus information by 1.5×; the corrected answer is that
corpus information is not measurably present, so the multiple is unbounded
rather than 2.90. **A ratio statistic cannot report that.**

**Consequence for the sealed verdict — none.** P-R-B (normalized) was
adjudicated on the sealed unit grouping with the log-loss estimator and the
declared constants, where the ratio is 2.90 and 2.70 and the clause PASSES.
That adjudication stands, and it is not reopened here. What this defect
records is that the **corrected** analysis cannot be reported in the same
currency.

**Adjudication (author ruling, 2026-08-03).** **Reading 1 is adopted.** The
corrected data-side term is negative, which is consistent with **no
recoverable corpus information under the corrected grouping**; the ratio is
undefined and **none is reported**. The two normalized quantities are reported
separately with intervals, per the manuscript's rule on unstable denominators.
The sealed 2.90 / 2.70 remain in the verdict table as the sealed adjudication
on the sealed grouping, and are not restated as present claims.

Measured, corrected grouping, corpus-clustered bootstrap:

| representation | I(S;F)/H(S) | 95% interval | I(corpus;F)/H(corpus) | 95% interval |
|---|---|---|---|---|
| autopsy_mix | **0.4438** | [0.3793, 0.4693] | **−0.3136** | [−1.8723, 0.1940] |
| structural | **0.4543** | [0.3717, 0.4873] | **−0.2959** | [−1.6651, 0.2049] |

The corpus-side interval spans zero from far below it; the specification-side
interval is comfortably positive and excludes zero. That is the dissociation,
stated without forming a quotient.

*The three readings considered, for the record:*

1. **Report the components, not the ratio.** State `I(S;F)` and
   `I(corpus;F)` separately with their routes, and say the ratio is undefined
   because the denominator is not positive. Most conservative; loses the
   headline multiple.
2. **Clamp the denominator at zero and report the multiple as unbounded.**
   Defensible — a negative plug-in estimate of a non-negative quantity is
   conventionally read as zero — but it converts an estimation artifact into a
   rhetorical maximum, which is the opposite of this project's habit.
3. **Report the sealed ratio as the adjudicated figure and the corrected
   components beside it**, with the sign inversion in the data-side term
   stated as the finding it is.

**Effect on the manuscript.** Larger than D1's. D1 costs a footnote: sealed
adjudications stand, forward-facing claims use the weaker bound, the paper
declines the ≥1.5-bit levels claim. **D2 restructures §5's bits discussion**,
because the data-side term does not merely shrink under correction — it
inverts sign, and the sealed +0.556 is revealed to have been substantially an
artifact of the grouping defect rather than a measurement of institutional
signal.

**Carry into the manuscript, pending the ruling.** One sentence at minimum:
under the corrected grouping the institution-identity term is not
distinguishable from zero and is estimated below it, so the dissociation the
sealed clause measured as a 2.9× multiple is better described as
specification information against no measurable institution information.

**Not a reason to amend.** The sealed §B.4 text stays as written. The missing
fourth direction is recorded here.

---

## D-A1 — §C's conditional comparison is not an independent test of the marginal ordering

*Logged 2026-08-03, on mathematical review, before §C was implemented.*

**What the protocol says.** §C commits I(plant;F|S) and I(S;F|plant) as a
conditional check on the marginal dissociation, with licensed sentences for a
"claim-strengthening" direction (pipeline still dominates after conditioning)
and a "claim-narrowing" one (plant information rises sharply once the detector
is known).

**The defect.** On the crossed synthetic design those sentences cannot
discriminate, because the conditional difference is algebraically identical to
the marginal one. Specification and plant are independent by construction —
every specification scores every population exactly once — so I(S;plant) = 0.
The interaction identity
`I(A;B|C) − I(A;B) = I(A;C|B) − I(A;C)` then gives

    I(S;F | plant)  = I(S;F)     + I(S;plant | F)
    I(plant;F | S)  = I(plant;F) + I(S;plant | F)

and subtracting,

    I(S;F|plant) − I(plant;F|S)  =  I(S;F) − I(plant;F).

The conditional ordering equals the marginal ordering identically. No outcome
of §C can confirm or overturn what §C was written to test.

**Demonstration by measurement.** On the sealed S-ID substrate,
I(S;plant) = **3.2 × 10⁻¹⁶ bits** — zero to floating-point precision — and
each of the 27 specifications scores each of the 1,200 populations exactly
once. The independence premise is exact, not approximate.

**Adjudication.** The sealed text stands unamended. **§C is reinterpreted as
measuring the synergy term J = I(S;plant | F)** — how much the representation
entangles pipeline and plant — which is a real quantity, is not determined by
the marginals, and is the informative thing this design can say. §C's licensed
sentences are reported as realised with this defect cited beside them, and
**no claim of independent confirmation of the marginal ordering is drawn from
them.**

**Implementation consequence.** §C is implemented with one coherent joint
decoder q(S, plant | F), from whose predicted joint I_dec(S;F),
I_dec(plant;F) and I_dec(S;plant|F) are all derived, so that the two
chain-rule routes to I(S,plant;F) can be checked against each other for
numerical coherence. Both routes are reported.

**Effect on the verdicts.** None. §C is an addendum analysis; no sealed
verdict depends on it. The effect is that the manuscript may not cite §C as
an independent test of the dissociation, which is what its licensed sentences
were drafted to support.

**Carry into the manuscript.** One sentence: on a crossed design where
specification and plant are independent, conditioning cannot reorder the
marginal comparison, so the conditional analysis is reported as a measurement
of pipeline–plant entanglement in the representation rather than as
corroboration of the ordering.

---

## D-A2 — the EPS floor is not the defect it was thought to be; the sealed estimator is sound on this data

*Logged 2026-08-03. Recorded because the concern was raised, investigated, and
found not to apply — a checked-and-clean entry, not a defect.*

**What was suspected.** That the `EPS = 1e-12` floor is applied coordinatewise
to the predicted distribution without renormalising the row, so that q is not
a valid conditional distribution and the identity
`R(q) = I(Y;F) − E[KL(P(Y|F) ‖ q(Y|F))] ≤ I(Y;F)` fails, undermining every
"lower bound" claim built on it.

**What the code does.** Not that. In `rid/analysis.py:108-114` and
`sid/analysis.py:68-73` the floor is applied to a **single scalar read-out** at
the point of taking the logarithm — `np.log2(max(p, EPS))` — where `p` is the
true class's entry in a row returned by `predict_proba`. **The predicted
distribution itself is never modified.**

**Demonstration by measurement**, over the persisted per-instance probability
vectors (§0.5):

| fit | rows | row-sum min | row-sum max | floored instances |
|---|---|---|---|---|
| S-ID 22-class, autopsy_mix | 26,400 | 1.000000 | 1.000000 | **0** |
| S-ID 22-class, structural | 26,400 | 1.000000 | 1.000000 | **0** |
| S-ID 22-class, overlap_profile | 26,400 | 1.000000 | 1.000000 | **0** |
| R-ID 27-class, autopsy_mix | 65,161 | 1.000000 | 1.000000 | **0** |

Every row is a valid distribution, and **the floor never fires on this data**:
no instance has a true-class probability at or below EPS.

**Where it could still matter, stated so it is not forgotten.** The floor
exists for the case where the true class is absent from a training fold
(`i is None` → `p = 0.0`). There, q assigns zero mass to a label in the support
of Y, the KL term diverges, and the floor substitutes an arbitrary finite
constant. Grouped CV with every class present in every fold prevents this, and
the measurement above confirms it did not occur. A future section that
subsets classes or strata more aggressively could reach that regime, and
should re-run this check.

**Additive-smoothing sensitivity**, reported as required rather than
substituted for the primary estimator:

| fit | δ = 0 | δ = 1e-6 | δ = 1e-4 | δ = 1e-2 |
|---|---|---|---|---|
| S-ID 22-class, autopsy_mix | 3.3496 | 3.3495 | 3.3468 | 3.1017 |
| S-ID 22-class, structural | 3.6264 | 3.6264 | 3.6236 | 3.3715 |
| R-ID 27-class, autopsy_mix | 2.1100 | 2.1100 | 2.1080 | 1.9079 |

Smoothing shrinks q toward uniform and therefore lowers every estimate
monotonically; at δ ≤ 1e-4 the shift is ≤ 0.003 bits, and at δ = 1e-2 it is
0.20–0.25 bits. **The primary estimator is unchanged.**

**Effect on the verdicts.** None. No bound in either study rests on a floored
instance, because there are none.

---

## D-A3 — §G.2's T1 feature set cannot be built from the persisted substrates

*Logged 2026-08-03 during execution, before §G.2 was run. **§G.2 is not
executed**; §G.1 ran and is reported.*

**What the protocol says.** §G.2 declares the T1-only arm as
`struct_share_grid` *plus* five further worklist-only statistics, and says
explicitly why they are declared in advance:

> share on the dollar grid, share with psych endings, share on Benford-rare
> lead digits, and the mean and s.d. of log amount **within the worklist**.
> These are all computable from the 50 selected records without their
> population, and they are declared now so the T1 arm is **not a strawman
> built from a single coordinate**.

**The defect.** Those five statistics are computable from the selected
*records*, and **neither persisted substrate carries the records**:

| substrate | what it stores | record values available? |
|---|---|---|
| S-ID `worklists.parquet` | derived features only; **no record identifiers of any kind** | no |
| R-ID `unit_cache/*.json` | `record_ids` — unit-local positional indices | no; amounts are not stored |

`struct_share_grid` is the one T1 coordinate that survives into the derived
features, which is exactly the single-coordinate strawman §G.2 forbids. The
section therefore cannot be executed as sealed from stored data.

**Why this was not visible at seal time.** The provenance audit established
which features *are* T1 by reading the feature-builder code. It did not ask
whether the T1 features could be *rebuilt* from what was persisted. Those are
different questions and only the first was answered before sealing.

**Adjudication.** §G.2 is **not run, not approximated, and not run in the
degenerate one-coordinate form.** Running the strawman the protocol names and
forbids would be worse than not running it. The manuscript's
`\pending{G.2: T1-only ablation}` slot remains unfilled, and §2's statement
that the worklist-only condition is "a secondary condition we specify but do
not yet report" remains accurate.

**Cost to unblock, so the deferral is priced rather than open-ended.**
S-ID needs regeneration *and* re-scoring, because worklist membership is not
stored: 2.10 s/population × 1,200 = **≈ 42 min single-threaded, ≈ 3 min on 14
workers** (probed rate). R-ID needs the record values joined to the cached
`record_ids` from the raw substrates, which `rid/guard.py` blocks by design;
that join is a separate substrate task and is **not costed here**.

**Effect on the verdicts.** None. No sealed verdict depends on §G.2. The
effect is that the paper's central phrase — "the worklist and its host
population" — remains licensed by the provenance audit's *code reading* rather
than by a measured T1 ablation, which is what §G.2 was written to supply.

**Carry into the manuscript.** The existing wording already says the
worklist-only condition is specified but not reported. That stays true and
needs no change; what changes is that the reason is now "the substrate does
not retain what the measurement needs", not "we have not got to it yet".

---

## D-A4 — §Q.1's decomposition is an identity on this design, not a measurement

*Logged 2026-08-03 during execution of §Q. **Execution continued**: the
outcome falls inside a committed direction, so the stop rule does not fire.
What is defective is the evidentiary status of the sentence, not the number.*

**What the protocol says.** §Q.1 makes

    Delta_{W|X} = L(p̂(S|X)) − L(p̂(S|W,X))

"the headline provenance decomposition", and drafts two licensed sentences:
one for Delta large ("the selection carries the signature") and one for Delta
small ("the signature is *relational* … this is a finding, not a failure").

**The defect.** On this design the two sentences cannot compete, because
Delta is not free to be small. **Within a unit, every specification is applied
to the same population**, so the population-only decoder sees identical
features for all 22 or 27 labels and cannot separate them. Its loss is
therefore the label entropy, and

    Delta_{W|X}  =  H(S) − L(p̂(S|W,X))  =  Î(S;F)

identically. §Q.1 recovers the quantity §A already reports, under a different
name.

**Demonstration by measurement.** A population-only decoder was fitted from
unit-level features alone (institution, log unit size, fiscal year), grouped
by component:

| quantity | value |
|---|---|
| H(S) | 4.7548 bits |
| measured L(S \| X) | 4.7521 bits |
| information about S recoverable from X alone | **+0.0027 bits** |

Two and a half thousandths of a bit — the decoder is at the marginal, as the
crossed design forces. Consequently the reported decompositions

| representation | L(S\|X) | L(S\|W,X) | Delta |
|---|---|---|---|
| autopsy_mix | 4.7548 | 2.6448 | **2.1100** |
| structural | 4.7548 | 2.5949 | **2.1600** |
| overlap_profile | 4.7548 | 1.6821 | **3.0727** |

reproduce §A's Î(S;F) exactly (2.110, 2.160, 3.073).

**Same family as D-A1.** Both defects are the crossed design making an
intended comparison analytic. D-A1: specification ⟂ plant, so conditioning
cannot reorder the marginals. D-A4: specification ⟂ population *within a
unit*, so the population-only arm is pinned at chance. In each case the
protocol drafted two competing sentences for a quantity that only one of them
could ever describe.

**Adjudication.** The sealed text stands unamended. §Q.1's outcome (1) is
realised and reported, **with this defect cited beside it**, and the
manuscript does not present Delta as independent evidence — it is Î(S;F)
renamed. What §Q.1 does establish, and this is worth stating positively, is
that the decomposition is *exhaustive*: none of the recoverable information
is attributable to the population alone, because there is none to attribute.
That is a real property of the design and it makes the population-only arm a
**sharp negative control with a derived expectation** — which is precisely
what Part 4(b) of the review asked the manuscript to claim.

**Effect on the verdicts.** None. No sealed verdict depends on §Q.

**Carry into the manuscript.** One sentence: because every specification in a
unit is applied to the same population, a population-only decoder is pinned at
the label entropy by construction (measured: 0.0027 bits recovered), so the
whole of the recoverable information is attributable to the selection, and the
decomposition is exhaustive rather than contingent.

### D-A3, extended 2026-08-03 — the same gap blocks §E and §P, and half of §K

The finding generalises: **the persisted substrates retain derived features and
worklist membership, but not the records themselves**, so any section that
needs to *re-derive* a representation from a different or perturbed selection
is affected. Each was checked individually rather than assumed.

| section | arm | executable? | why |
|---|---|---|---|
| **§E** | random-50 negative control, `autopsy_mix` / `structural` | **no** | needs the waterfall category and the population-relative statistics of 50 *unselected* records; only the 50 flagged ones are stored |
| §E | random-50, `overlap_profile` | yes in principle | Jaccard needs only ids; not run, because the control is only meaningful on the headlined representations |
| §E | full-population and oracle positive controls | **no** | need the full record set and per-record `is_plant`; S-ID discards the population frame |
| **§P** | padding (replace r of k with random records) | **no** | the substituted records' categories and values are not stored |
| §P | blending (rank-weighted combination) | **no** | needs the full ranking; only the top-50 is retained |
| **§K** | `autopsy_mix` at k = 10 / 25, R-ID | **YES — run** | per-flag categories are stored in worklist order (verified: 50 ids, 50 categories, aligned), so truncation is exact |
| §K | `overlap_profile` at k = 10 / 25, R-ID | **YES — run** | truncate `record_ids`, recompute Jaccard |
| §K | `structural` at any k | **no** | percentile rank, density rank and duplicate share are population-relative and need record values |
| §K | any arm on S-ID | **no** | S-ID stores no record identifiers at all |

**§K was NOT declared blocked wholesale**, because checking showed two of its
three representations are exactly reconstructible. Declaring a section blocked
without checking each arm would have discarded a result that was available.

**Price to unblock the rest — unchanged and measured.** S-ID needs regeneration
*and* re-scoring, since worklist membership is not stored: **≈ 42 min
single-threaded, ≈ 3 min on 14 workers** at the probed 2.10 s/population.
R-ID needs the record values joined to the cached `record_ids` from the raw
substrates; `rid/guard.py` blocks that join by design, so it is a separate
substrate task and **is not costed here**.

**Effect on the verdicts.** None. The affected slots stay unfilled and the
manuscript's existing hedges remain accurate.

### D-A3, resolved 2026-08-12/13 — the blockage was lifted by substrate regeneration

The deferral priced above was paid. The S-ID substrate was regenerated with
re-scoring (`sid/substrate_p6.py`, 1,200 populations), verified **bit-exact**
against the sealed `worklists.parquet`
(`4f7ee326417d0e382fdb3dbcf73d44607195043ab2196250ec0833535c34e321`) before
anything consumed it — `results/p6/VERIFICATION.json`, `all_bit_exact: true`,
and every consumer calls `substrate_p6.verify_gate` first. The previously
blocked sections then ran as **labelled post-hoc analyses of sealed
specifications**:

| section | executed | artifact | commit |
|---|---|---|---|
| §G.2 T1-only arm | yes | `addendum/results/p6_section_G2.csv` | `9541c56`, 2026-08-12 |
| §G.2 per-instance + paired intervals | yes | `addendum/results/oof_g2_*.parquet`, `p6_g2_intervals.csv` | `0f9286d`, 2026-08-13 |
| §E random-50 negative control | yes | `addendum/results/p6_section_E.csv` | `9541c56` |
| §P padding / blending | yes | `addendum/results/p6_section_P.csv` | `9541c56` |
| §K structural arm | **still blocked** | needs record values the R-ID guard withholds; not regenerable | — |

The T1-only headline figures from the regenerated run: accuracy 0.6773
against 1/27 chance, 3.333 bits, permutation baseline 0.0359; refit
re-derivation reproduced the persisted summaries exactly before intervals
were computed (`results/p6/g2_intervals.log`). The manuscript reports these
as post-hoc, labelled, with this defect cited at each site. The entries
above this one record the blockage as it stood; this entry records that it
no longer stands, except for §K's structural arm, which remains impossible
from persisted data.

### D-A2, addendum 2026-08-03 — the named residual case fired, in §D

D-A2 recorded that the floor never fires on the sealed estimator, and named
the regime where it could: *"A future section that subsets classes or strata
more aggressively could reach that regime, and should re-run this check."*

**§D's isotonic arm reached it.** Isotonic regression maps some inputs to
exactly zero, so a calibrated conditional can assign zero mass to a class the
uncalibrated forest gave small positive mass:

| §D arm | representation | floored instances |
|---|---|---|
| isotonic (nested) | autopsy_mix | **27** |
| isotonic (nested) | structural | **10** |
| gradient boosting | autopsy_mix | 0 |
| gradient boosting | structural | 0 |
| every sealed / uncalibrated fit | — | 0 |

27 and 10 instances out of 65,161. At the per-instance magnitude established
in the manuscript (~0.0012 bits each across a substrate of this size), that is
a shift of order 0.03 bits — not negligible, and it moves in the direction of
*understating* the calibrated estimate. The calibrated figures below are
therefore reported with their floored counts attached, as the manuscript's
corrected EPS sentence requires.

**No change to the adjudication.** The sealed estimator remains unaffected;
what fires is an addendum arm, and it fires visibly because §0.5 persists the
counts. This is the check working, not failing.


---

## D-A5 — §B.4's three directions were drafted on an unstated positivity assumption

*Logged 2026-08-03 alongside the D2 ruling. Distinct from D2: **D2 is the data
outcome** (the corrected data-side term is negative); **D-A5 is the drafting
defect** (the sealed sentences could not have described that outcome whatever
the data had done).*

**What the protocol says.** §B.4 outcome (3) commits three directions —
(i) both conventions pass propagated, (ii) convention 1 passes and convention 2
fails, (iii) both fail propagated — and instructs that the realised one be
quoted verbatim.

**The defect.** All three are statements about the *value* of a ratio
`[I(S;F)/H(S)] / [I(corpus;F)/H(corpus)]`, and therefore silently assume the
denominator is positive. Nothing in §B.4 says so, and no fourth direction
covers a denominator at or below zero. The assumption is not a modelling
choice made and defended; it is one that was never noticed, which is why it
was never written down.

**Why it is worth a separate entry from D2.** D2 could have been avoided only
by different *data*. D-A5 could have been avoided by different *drafting* —
a fourth direction, or a stated precondition, costing one sentence at seal
time. The two failure modes call for different corrections, and a ledger that
merges them teaches neither lesson.

**This is the fifth instance of one pattern.** With D-A1 (conditioning cannot
reorder marginals on a crossed design), D-A4 (the population-only arm is
pinned at chance by construction), and D1 (a governing rule written without
scope), the count of defects arising from *sentences drafted before the
algebra was worked* is now four of seven. The manuscript owes a methods
paragraph on this: writing licensed sentences in advance is the right
discipline, and it is not sufficient — the outcome space they partition has to
be derived, not assumed, or the partition can miss the region the data lands
in.

**Adjudication.** The sealed §B.4 text stands unamended. The missing fourth
direction is recorded here, and the manuscript reports the two normalized
quantities separately with intervals rather than any ratio.

**Effect on the verdicts.** None. P-R-B's sealed adjudication is untouched.

**Carry into the manuscript.** One sentence in the methods: where a
committed decision rule is a function of a ratio, the protocol should state
the domain on which that ratio is defined; ours did not, and the corrected
analysis landed outside it.

---

## D-A6 — the macro perimeter was enforced on one side of a boundary only

*Logged 2026-08-04. An instrumentation defect, not an analysis defect.*

**The finding.** The generation path was enforced rigorously on the two
original sealed studies — 27 pinned sources, no typed statistics — and not at
all on the addendum: 17 unpinned inputs and roughly 45 typed measured
statistics, including the entropy-dominance certificate, transcribed by hand
from `addendum/RESULTS.md`, a file that was itself unpinned. The manuscript
asserted the opposite in two places.

**Why it survived.** A typed string and a computed value are indistinguishable
at the generator's call site, so the lapse was invisible at the point of use.
Every check built to enforce the discipline inspected the *manuscript*, one
layer downstream of where the discipline actually lapsed.

**How it was found.** By a check built at reviewer suggestion, which failed
its own first validation: it exempted inline mathematics, the exact form both
observed violations had taken, and would have missed the errors it was built
for. It caught the lapse only after being validated against the failure it
targeted rather than the failure imagined.

**Substantive corrections surfaced.** Three. D1's class-asymmetry range had an
understated upper bound (0.056, reported as 0.05). `PortNullFamily` was typed
as 0.3182 against a computed 0.3184, having been confused with the design
quantity 7/22. The rho = 0.75 scope claim was true for the two headlined
representations and false for the overlap profile, where rho is 0.611.

**Adjudication.** No sealed result is affected; no verdict moves. The addendum
generation path was rebuilt rather than patched. Practice codified in
`PROVENANCE.md`.

---

## D-A7 — eight reported values cannot be traced to any pinned source

*Logged 2026-08-04, during the rebuild. Open.*

**The finding.** After the rebuild, eight values still have no derivation from
a pinned source, because they came from the same ad-hoc path as the
certificate and their inputs were never persisted:
`NormCorpAm`, `NormCorpSt`, their two confidence intervals, the two
specification-side intervals `NormSpecCIAm` / `NormSpecCISt`,
`FecMatchDistance`, and `ProvPopOnlyBits`.

`NormSpecAm` and `NormSpecSt` re-derive exactly from `section_Q.csv`
(2.11 / 4.7548 = 0.4438). The corpus-side quantities do not: `section_O_corpus.csv`
gives I(corpus;F)/H(corpus) = -1.124 / 2.8211 = -0.3984, against the reported
-0.3136. The reported pair is internally consistent with `NormDiff`, so it is
not a transcription slip; it is a different computation whose inputs are gone.
`ProvPopOnlyBits` falls below the rounding of `section_Q.csv` and cannot be
recovered from it.

**Why it is not simply fixed.** Recomputing the corpus-side quantities
requires a corpus decoder whose per-instance outputs were not persisted —
that is a refit, which is not available.

**Status.** Flagged in the generator with `konst(..., authority="UNTRACED")`,
so every occurrence is greppable. These values appear in a live table in the
dissociation section. **Awaiting a ruling**: report with the limitation
stated, replace with the traceable specification-side quantities alone, or
drop the corpus-side column.

---

## D-A8 — §Q's negative control was reported as a measurement; it is an identity

*Logged 2026-08-04. Closed by ruling; no refit required.*

**The finding.** The population-only control was reported as "recovers 0.0027
bits," implying a fit that came out near zero. It is not a measurement:
`section_Q` sets `L_population_only = H(S)` by construction, because within a
unit every specification sees the same population and a population-only
decoder therefore cannot separate them. The control holds **identically**.

**Disposition.** The fitted 0.0027 is dropped. Its per-instance outputs were
never persisted, but no refit is required because the analytic result is exact
and strictly stronger — no fit could have made the control come out otherwise.
The manuscript now states the identity. The generator asserts that
`section_Q`'s decomposition closes before emitting the macro, so the claim is
checked rather than asserted.

**Effect on D-A7.** D-A7 now covers only the corpus-side normalized values,
which remain untraceable and are no longer reported.

---

## D-A9 — a cap argument was reported from a realized count, not an alphabet

*Logged 2026-08-04. Caught in review before reaching prose.*

**The finding.** A deflation defence was reported resting on the cap
`A_R <= q/M`, using `q = 15`, the number of rules that ever won a
nearest-rule assignment. The cap bounds accuracy by the **alphabet** a decoder
could emit, which is the rule class as specified: 8 single-field top-50 rules,
1 trivial-extremeness, 38 percentile-band rules and 1 vendor-restricted rule,
so `|R| = 48`. At `48/22 = 2.18` and `48/27 = 1.78` the cap exceeds one and
constrains nothing. Using the realized count would make the bound
data-dependent and is not valid.

**Compounding error.** The accuracies compared against the cap were S-ID
figures while the rule slate is R-ID only, so the comparison was also
cross-substrate.

**Adjudication.** The cap argument is withdrawn in full. Nothing derived from
it entered the manuscript or the macro set.

---

## D-A10 — the excluded-cell log referenced by the supplement was never kept

*Logged 2026-08-04. A record-keeping loss, not an analysis defect.*

**What was referenced.** The supplement's structure reserved a section for an
excluded-cell log: configurations considered and rejected at battery-design
time, with the reason each was rejected, so that the battery reads as an
enumeration rather than a selection.

**The search.** Exhaustive and negative. Filename search across the whole
repository including untracked files; content search for `excluded.cell`,
`considered and rejected`, `rejected at battery` across all Markdown, YAML,
text and Python; `git log --all --diff-filter=D` for deleted files;
`git log -S` on distinctive strings; `git stash`; `git fsck --lost-found`
dangling blobs; all branches; and the manuscript project directory. The only
occurrences of the phrase are in documents written during this preparation.
No such log exists or ever existed in a recoverable form.

**What does exist.** `sid/PROTOCOL.md` §4 states a *leakage* rule — "any
feature that only one specification can produce by construction is excluded" —
but that governs **features**, not battery cells, and is a different object
from the one the supplement referenced. `config/frozen_config.yaml` enumerates
the 26 frozen cells plus `ensemble_meanrank`, and the protocol states which
bins are never headlined. Nothing records which *other* configurations were
weighed and set aside.

**Why it is not reconstructed.** The grid contains 26 cells out of 120
possible (algorithm x features x preprocessing = 10 x 4 x 3), so 94
combinations are absent. Their absence is recoverable by arithmetic; the
*reason* each was rejected is not. Writing plausible reasons after the fact
and presenting them as a design log would manufacture a contemporaneous record
that never existed, which is a worse fault than the missing section.

**Disposition (b).** The supplement slot is dropped. The battery section
instead states what is true: the frozen configuration enumerates the cells,
the protocol states the leakage rule and the never-headlined bins, and the
battery is 26 of 120 possible combinations — a curated selection whose
rejection reasons were not recorded. A reader can check every one of those
claims against the sealed sources.

**Carry into the manuscript.** One clause in the battery description
disclosing the 26-of-120 selection, so no reader infers an exhaustive
cross-product.

---

## D-A11 — `overlap_profile` is built by deleting the coordinate named by the target; it is not attribution under the paper's observation model

*Logged 2026-08-05, on an external audit's formal objection. Settled from the
feature-builder code and the persisted substrates, as instructed, before any
disposition was chosen.*

**What the representation is.** `sid/substrate.py:21-23` states it: "the
worklist's Jaccard against the other 26 worklists in fixed sorted
specification order with the self-entry removed. The full 27-vector is
persisted; the self column is dropped at analysis time."

**The construction, verbatim** (`sid/analysis.py:140-150`, identically at
`rid/analysis.py:153-162` and `addendum/run.py:130`):

```python
def overlap_matrix(df, j_cols, specs):
    J = df[j_cols].to_numpy()
    own = df.spec_name.map({s: i for i, s in enumerate(specs)}).to_numpy()
    out = np.empty((len(df), len(specs) - 1))
    for i in range(len(df)):
        out[i] = np.delete(J[i], own[i])
    return out
```

`df.spec_name` is the Task A **target** — `fit_oof(X, spec, splits_a, ...)` at
`sid/analysis.py:210`, with `spec = df.spec_name.to_numpy()` at line 179. The
deletion index is therefore the true label. The feature vector cannot be
constructed without already knowing the answer.

**The four construction facts, as asked.**

- **(a)** 27 coordinates persisted; **26** presented to the model
  (`len(specs) - 1`), verified on both substrates.
- **(b)** The self-cell's Jaccard is **excluded** from the model input. Where
  it is retained it is **identically 1.0** — measured min = max = 1.000000
  across all 32,400 S-ID and 65,161 R-ID rows. It is a constant, and its
  position is the label.
- **(c)** The exclusion is indexed **by the row's own cell label**, not by any
  fixed scheme. This is target-dependent by inspection.
- **(d)** **Yes.** Coordinate order depends on which cell is self. The
  docstring concedes it: "column p holds spec p for p < own index and spec p+1
  above -- the positional shift is inherent to the protocol's definition."
  Coordinate p denotes a *different specification* depending on the target.

**Demonstration by measurement.** Four representations, same folds
(GroupKFold by population / unit), random forest. These are a re-fit at
`n_estimators=200`, **not** the sealed config's hyperparameters, so the
aligned column runs slightly above the sealed report (0.9387 here against the
sealed 0.9119); the contrasts, not the levels, carry the argument. The
`synthetic` row is hyperparameter-independent.

| representation | S-ID 27-class | S-ID family | R-ID 27-class | R-ID family |
|---|---|---|---|---|
| aligned-26 (the paper's `overlap_profile`) | 0.9387 | 0.9927 | 0.7463 | 0.9257 |
| sorted-26 (same magnitudes, alignment destroyed) | 0.4893 | 0.6446 | 0.2173 | 0.4671 |
| fixed-27 (all coordinates, fixed order — target-independent) | 0.9777 | 0.9732 | 0.9708 | 0.9922 |
| **synthetic (identical profile every row, then delete index k)** | **1.0000** | **1.0000** | **1.0000** | **1.0000** |

The `synthetic` control is decisive. Every row is given the *same* 27-vector —
the column mean, carrying no information whatsoever about that row's worklist —
and index k is then deleted. The label is recovered at **100.00%** on all four
task/arm combinations. The construction alone, with all measured signal
removed, is an invertible encoding of the target.

The `sorted-26` control locates where the paper's accuracy actually comes
from. Destroy the label-dependent alignment while keeping all 26 genuine
Jaccard magnitudes and S-ID 27-class falls 0.9387 → 0.4893, R-ID 0.7463 →
0.2173 — the latter *below* both headlined representations (0.452 `autopsy_mix`,
0.437 `structural`). The representation's lead is the alignment, not the
overlap content.

**The defect.** The overlap results are not single-artifact attribution. Under
the paper's stated observation model — an analyst holds one worklist W and asks
which pipeline produced it — the feature vector is not computable. Either the
self-coordinate is retained, in which case argmax identifies the source
(**97.77%** S-ID, **97.08%** R-ID, measured) and the task is reference
matching; or it is deleted, in which case the true label built the predictor.
There is no third reading: the audit's dichotomy is exhaustive and the code
takes the second horn.

**§N does not answer this and could not.** §N.1 removes the availability
channel by restricting to the 22 universally-available cells — and the sealed
text itself records the residue: "the same 22 (**21 after self-removal**)
coordinates" (`addendum/PROTOCOL.md:1091`). The target-indexed deletion
survives decontamination unchanged. §N.2's mask arm isolates the availability
signal, which is a different channel. Both arms are honest answers to a
different objection.

**Disposition — (ii), the audit is right.** Not mixed: the exclusion is
target-indexed *and* the order is target-indexed, and both point the same way,
so no ruling is owed before proceeding. The repair is as specified:

1. An augmented **reference-battery observation model** is defined explicitly —
   the observer holds the worklist W, the population X, and the battery R_X of
   all 27 specifications run on that same population. Every overlap result
   moves under it and is labelled a different and easier task.
2. Overlap comes out of the abstract, the contributions, and the
   joint-property argument. The joint-property thesis is not entitled to lean
   on a representation whose leading coordinate structure is the label.
3. §5.8 is rewritten accordingly. The §N decontamination remains reported: it
   answered the availability objection honestly and that result stands.
4. Under the reference-battery model the result is real and worth stating:
   **an auditor who can run the full battery on the same population attributes
   strongly** — 0.9777 (S-ID) and 0.9708 (R-ID) at 27 classes on the
   target-independent fixed-27 representation. That is a useful operational
   finding for an auditor with battery access. It is not the paper's claim.

**Effect on the verdicts.** No sealed clause is reopened. `overlap_profile` is
never headlined in any sealed adjudication — `sid/analysis.py:236` restricts
headlines to the `learned` column and the protocol names the never-headlined
bins — so no PASS or FAIL turns on it. The effect is on the manuscript's
forward-facing prose, which loses the overlap lead as evidence for the
joint-property claim.

**Carry into the manuscript.** Where the representation is defined, the
construction is stated plainly: the vector is the worklist's Jaccard against
the other 26 worklists on the same population, with the self-coordinate
removed by index, and it therefore presupposes the reference battery and the
source label. The objection is recorded as having been raised and conceded,
because it will recur in review regardless of how the section is worded.

**Not a reason to amend the sealed text.** §N stays as written. The scope of
what its arms established is fixed here, in the open.

## D-A12 — the §P blending partner was drafted as a deterministic function of the target

*Logged 2026-08-12, retroactively recording a defect found and repaired on
2026-08-08 during the Phase 6 execution of §P. The Phase 6 report described
this entry as already logged; it was not, and the citation in the manuscript
pointed at nothing until now. Both the defective and repaired outputs were
retained from the start.*

*Id note: first logged under the id D-P1, which collides with an unrelated
Paper 1 defect of the same name in `notes/CORRECTIONS_LEDGER.md` (entry E,
2026-08-05, the D\* implementation). Renamed to D-A12 the same day the
collision was found, before any external copy carried the old id; commit
`b325bcb` and the Phase 6 session record refer to it as D-P1.*

**What the execution did.** §P's blending arm forms a worklist from the
rank-weighted combination of two specifications' rankings and asks the decoder
for the dominant one. The first implementation chose the partner as
`specs[(i + 1) % n]` — the lexicographic successor of the target
specification. The successor is a deterministic function of the target, so
the blended worklist encoded both the target and a second, perfectly
label-correlated signal.

**How it surfaced.** Accuracy under a w = 0.25 blend came out *above* the
unperturbed baseline (0.8191 against 0.7696). A contamination probe that
improves attribution is measuring its own construction. This is structurally
D-A11 — the label building the predictor — in a new site.

**The repair.** The partner is drawn uniformly at random from the other
specifications (seeded; `addendum/p6_controls.py`, blending arm). The section
was re-run in full before any figure was reported.

**What is retained.** The defective output is kept beside the corrected one as
`addendum/results/p6_section_P_DEFECTIVE_BLEND.csv`, so the correction is
checkable rather than asserted. No reported figure derives from the defective
run.

**Sealed text unaffected.** §P specifies "two specifications' rankings" and
does not fix the partner choice; the defect is in the execution, not the
protocol. The sealed text stays as written.
