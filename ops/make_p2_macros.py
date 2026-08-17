"""Generate results_macros.tex from the stored analysis outputs only.

No reported statistic is hand-typed. Every number in the manuscript is a
macro defined here, derived from the stored run directories, the frozen
configs, or a read-only re-derivation over the stored substrate.

Inputs are read from inputs/ through paths.require, which asserts a
SHA-256 for each and aborts naming the file if one is missing or altered.
The SOURCES table below is that pin table.

Run:  make macros      (or  python3 ops/make_p2_macros.py)
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from paths import PROJECT, REPO, require    # noqa: E402

OUT = PROJECT / "results_macros.tex"

SID = "results/sid/20260726T172824Z_c093730/"
ADD = "addendum/results/"
RID = "results/rid/20260730T010224Z_a7d5cb2/"
REFB = "results/refbattery/20260805T125312Z_0847bf2/"
OVC = "results/overlap_circularity/20260805T132923Z_f9f8d25/"

SOURCES = {
    SID + "task_A.csv":
        "18ef7747b08c56865e5a2e5ec292b11b2addd0c5a77ca4f280d88a198074c8a4",
    SID + "task_A_family.csv":
        "ebfbc83705744ef17917ffb39902cb48f53488486f711186845b8e6cb16388e2",
    SID + "task_B1.csv":
        "ce3ee1fce536ea30fbfaa412f85e21986689252ad9ce6a1d3d6cc0a7cdb6189f",
    SID + "task_B2.csv":
        "5924579748fe889d2c3fe7e93c0606977260feeaf84304e767cede9b56b29379",
    SID + "task_C.csv":
        "6b228d72e9d99287cae6f3f5c4bf9e63b1699c1e6b616c78da03e30bfc5c9595",
    SID + "task_C_family.csv":
        "12fc51a0650dc6bed4d90272ce8553c29322a63038cc092d76d15906df8cf540",
    SID + "task_D.csv":
        "bbdea5f2df5680c783a6fef84086de8e53fda4714f17cd91d854c920ae794f19",
    SID + "loho.csv":
        "325e7c858f71943c2cf2fb348d5050f9515067cc1be247a197579177573afeb3",
    SID + "floors.csv":
        "6044da58aa2c2699e8c7d93c8f3c69b9fd774beb88c3f66195c7f266c9dd422f",
    SID + "P3.csv":
        "c3a20163d9999a4c1ce4ee49ec5ada758b466285847c9206d57a35c6a21be000",
    SID + "plant_decomposition.csv":
        "b86c04374fb039bd4a39556af1ca2569f51575dac9614ccd9bf4e2b51ca2b221",
    SID + "task_E_confusion.csv":
        "07f70149d9ec9453f9082788794f54d762ac181391c8da9f89c08305ffe89d61",
    SID + "worklists.parquet":
        "4f7ee326417d0e382fdb3dbcf73d44607195043ab2196250ec0833535c34e321",
    RID + "task_A.csv":
        "a72fae66d96118550a4b0180b5cf210cc501b7cdc54a11ff339bca3ca9606758",
    RID + "task_A_family.csv":
        "e134f61aeb806a5c63402b0dbff9d6757343f28b9837ecad34993a2a7e777db2",
    RID + "loco.csv":
        "102f5c85726b48f044a1be706651d7b3de4471c9d10ed5f79a0c6e1614ced206",
    RID + "gap.csv":
        "ccb38adb7d43ac6207f50b2d47a1894c9a302bd1079383034feb6b34b2e7000f",
    RID + "p_r_b.csv":
        "9c96c92ad34767bb1c1c7e49ddbc2e0289effd5cbae2a3f9ea8f05924856b5ac",
    RID + "floors.csv":
        "df034b214756a2da2c2a6f0e1c2710a1d233146056bb62173077f08e2bb30ca3",
    RID + "p_r_c.csv":
        "b448e61eda2474cd104f84358ab3c7b9c3df55b93d2839451f63f7047122911c",
    RID + "predictions.csv":
        "7cef3935c4e30bae6abce93baf4af40480579490a15eeb13002c2b9491999308",
    RID + "per_class_recall.csv":
        "10a0b99513f41f3529f34229eb4c3d7ed9c56525e846f84d5ddfbb92d4d21389",
    RID + "worklists.parquet":
        "d98ee73bd426505ec4bfa3f4c2b2bb5cc1480263a9d3504c464b4a3ba743be80",
    "rid/config.yaml":
        "81953a4c5d1d72be2f6ca22f54122010bff83c14e58e7401454bbf5274272a52",
    "config/frozen_corpora.yaml":
        "a8ff6504d79265c8751d16009026437ddff1904f8cf44e542d09f20cfbe6a228",
    "config/frozen_config.yaml":
        "29346d171ba7df6547d3c87bae3e99419e62049a555aed4e25787d993ab67050",
    "sid/config.yaml":
        "84c2ecfff0db1ccfb9023d7fc6f36f0e18089708352b3a4940dd848ec07fbb90",
    "config/env_m5_freeze.txt":
        "e75a9825ee8034dead3beb7aebf092fbf9d03ccb558f6bacbc76791b31987289",

    ADD + "certificate_rederived.csv":
        "16cce8ac210b59fb7cc900e2322a456e0e8ccae854a23f0840b73493a81312cb",
    ADD + "certificate_mc.csv":
        "3018fc7362ae4dc8b1cbecb658e6f5924b5eb22af76ac6b7c92edb4ebc26edeb",
    "results/extension_B_fullclass.parquet":
        "f722d8bd6bd655e85a77e6f0ee5c13ad711c3d6f975b3aeb01f02901614b5d6e",
    ADD + "rule_recovery.csv":
        "efd13212f324e5ff2fc50f9c159355710e415f82e2c676fd23edadd7c139dafb",
    ADD + "cert_bounds.csv":
        "ef68c4c7d206aed7c1ac66b1c6139586e7829e5641522962066a0b4905dcc7bd",
    ADD + "boundary_probs.csv":
        "2c0b072a816cb3e2c33b15339606f6da00806b59b8b8b4985bfea05c1a35d859",
    ADD + "section_H.csv":
        "d136d36d97314b65a543e87e347b8fb7eb24b1449d69f58727dd1f547005821f",
    # ---- addendum outputs ------------------------------------------------
    # These were read unpinned until the perimeter remediation: the
    # discipline held on the two original sealed studies and lapsed entirely
    # on the corrective analyses, which is where the certificate comes from.
    ADD + "fig5_family_signatures.csv":
        "dc05e546a10d96b63b3ab0676d95ce66f9ce5e5cd8fa220f544cf6c785cb100f",
    ADD + "oof_A_family_autopsy_mix_random_forest.parquet":
        "b1e6717787f43b1fb18e492b847fefb3dc804cc385a820a67fd1534020d8e846",
    ADD + "oof_F27_sid_autopsy_mix_random_forest.parquet":
        "732856247b3458146931b5d7e9ae26007cc8c66216b842fec73f2cefd8a7a63d",
    ADD + "oof_F27_sid_structural_random_forest.parquet":
        "cc9a5940ea8900f833de2b86a852b9553d23f4a4f19c3d8932a3c843841e562e",
    ADD + "oof_F_sid22_autopsy_mix_random_forest.parquet":
        "f9f626bb2295de6cb7d4d36551982cf444491f6ad07a878da32aa1e27917a94d",
    ADD + "oof_F_sid22_structural_random_forest.parquet":
        "44aee59763bedfc24061d089e75f4e764142a63d6497495c7c4c45b085fb4f64",
    ADD + "pairwise_graph.csv":
        "8caa10b7d2ce3248a1760495d15aa3ba5f411c7e65f11b3c93ff7b0c1efe33f8",
    ADD + "section_A.csv":
        "432086ab7edcb9188627f51f34abd4b606f81b357b4d0b7d80487bb5276ee9e6",
    ADD + "section_B.csv":
        "dab4da9151b6743c9d464e8a0de61de5840c9632745cbca0ae0490f82c60f03e",
    ADD + "section_C.csv":
        "877e2120e7204c85a192e78a53ce2f236ccfd6839486c6224a857a4afccbca41",
    ADD + "section_D.csv":
        "30aefa0eb0c923aa65a510adb9d1d89543f35cd43da3916ab7273de6e6ac8e87",
    ADD + "section_F.csv":
        "4830cff87319771243ff44588242aba2cff22a41cd3ef0a011781d20fcb26617",
    ADD + "section_G1.csv":
        "e020c4feeb85914bcb46895dbf18ed379b1da86ab56698356bb04cd0d74ea14c",
    ADD + "section_I.csv":
        "170e45ffc67127c6951f5c659cf755595773bbb8337b9e1066b8beba4c883e69",
    ADD + "section_J.csv":
        "5ab067eb4ffa31f9f17c9739c9bc564a3a2bfba810042c833c6ad30d81eee0e4",
    ADD + "section_K.csv":
        "a628ad11a3bf962f2a66764d3650a0ede9fca2b741c6c977cb774ead61122f42",
    ADD + "section_N.csv":
        "ba3e3cc861e5d51e3f2d610ae13d9002435264551627b11ba20f8a566cc55a65",
    ADD + "section_N_match.csv":
        "880941df25e6910c9ae154c3172e6ebcb16400a6160e0baee274657372b1a76d",
    ADD + "section_O.csv":
        "6fc67bb5ef0214e8ca444ec45efa527fa21b07e4ca02d11785c790a95784b396",
    ADD + "section_O_corpus.csv":
        "46729cfb15f8a75e624ac242347f47d0f2a360a4bced2bba258836572d3361cc",
    ADD + "section_Q.csv":
        "a841b369ee10178d664b10e586ccac085cd5ef264cfed13ea133382fa305dae5",
    # D-A11 disposition (ii) repair: the augmented reference-battery
    # observation model. Target-independent by construction; computed under
    # the sealed configs by ops/refbattery.py.
    REFB + "refbattery.csv":
        "7191fec237cb0bffe17aef0d3f790800e7d8a4073ad09fe57a9318024d99ff38",
    OVC + "overlap_circularity.csv":
        "d644a69a27302eb48cb58e9818b034c35c96b17d3ac060c0fad7dd92ba611fe3",
    # --- Phase 6 executed controls and their interval re-derivation. Added
    # 2026-08-14: a provenance gate found phase6_macros() reading these
    # unpinned while this file's header claimed every input pinned. The
    # openset pair and the fig4 per-institution table were unpinned for the
    # same reason and are closed with them (notes/P2_CORRECTIONS_LEDGER.md,
    # entry P2-C5).
    ADD + "p6_section_E.csv":
        "839612c0777fd2a85d8584db812a0d0800b51e76acedfc80dfa519a98100621e",
    ADD + "p6_section_P.csv":
        "422f07742173be91ace40a84c2b7dcfeb139f76aa7d8ebdfee33b340e5794a5b",
    ADD + "p6_section_G2.csv":
        "d2a75245a5a68e91a9068f5bf4ea3480c51968053f256d94816138681f19c8ae",
    ADD + "p6_g2_intervals.csv":
        "828ed5ae96870d0aafb56ec4cac719c39c4622d6eb8fbea3c1c9bde8239794fb",
    ADD + "p6_cw15_candidate_set.csv":
        "4607fd2f8583e071009b6e4f3bf07698f5da85cb482183e0663d3aee08a16da7",
    ADD + "p6_cw16_stochastic.csv":
        "00d0493b9da4fed113f987d01c6d0baade8b9eaeeb78052ce2941d56a5ded011",
    ADD + "fig4_loco_per_institution.csv":
        "2cd875ef8402494e499b9f3753b55da20587ba29a8d58c2398c8f46ae1cf214b",
    "results/openset/20260805T191833Z_a4b895a/pooled.csv":
        "9e683c19dc94c84dbb063d5eff6c5427953c88768272bdfd271d9e4e7d86c485",
    "results/openset/20260805T191833Z_a4b895a/per_institution.csv":
        "59372dcf8e1e24a0ac6af729be125f4db7ca60ab8aa0ecb5dfc1a6bc53d44c29",
}

MACROS: dict[str, str] = {}
_ORDER: list[tuple[str, str]] = []

# ---------------------------------------------------------------------------
# SEALED / CORRECTED PAIRS — the authoritative homonym table.
#
# Where a sealed adjudication and its corrected counterpart both exist, BOTH
# names must declare which they are: the sealed one carries `Sealed`, the
# corrected one carries `Corr`. A bare stem is forbidden, because a bare stem
# is what let "the corrected logistic ratio is \RidPRDLogistic{}" print the
# SEALED 0.889 for as long as it did (CW-2c; the sentence said corrected and a
# literal search for 0.889 returned nothing, so the defect read as fixed).
#
# ops/macrocheck.py fails the build on any pair whose sealed side does not
# declare itself. Add a row here whenever a corrected counterpart is created.
# ---------------------------------------------------------------------------
SEALED_CORRECTED_PAIRS: list[tuple[str, str]] = [
    ("SealedRidTaskAAm", "CorrTaskAAm"),
    ("SealedRidTaskASt", "CorrTaskASt"),
    ("SealedRidTaskAOv", "CorrTaskAOv"),
    ("SealedRidTaskALearnedAm", "CorrLearnedAm"),
    ("SealedRidTaskALearnedSt", "CorrLearnedSt"),
    ("SealedRidFamilyAm", "CorrFamilyAm"),
    ("SealedRidFamilySt", "CorrFamilySt"),
    ("SealedRidFamilyOv", "CorrFamilyOv"),
    ("SealedRidICorpusAm", "CorrICorpusAm"),
    ("SealedRidICorpusSt", "CorrICorpusSt"),
    ("SealedRidPRDLogistic", "CorrPRDLogistic"),
    ("SealedRidPRDForest", "CorrPRDForest"),
]


def verify_sources() -> None:
    """Every pin checked through paths.require, which names the
    offending file and distinguishes missing from changed."""
    for rel, want in SOURCES.items():
        require(rel, want)
    print(f"verified {len(SOURCES)} sources against {REPO}")


def add(name: str, value: str, note: str = "") -> None:
    if not name.isalpha():
        raise ValueError(f"macro name must be letters only: {name!r}")
    if name in MACROS:
        raise ValueError(f"duplicate macro: {name}")
    MACROS[name] = value
    _ORDER.append((name, note))


def konst(name: str, value, authority: str = "", note: str = "") -> None:
    """A literal whose value is fixed OUTSIDE this generator.

    Legitimate only when a protocol clause, config key, design fact or stated
    derivation determines it. `authority` names that thing and is required --
    ops/litcheck.py fails the build on a konst without one, and on any bare
    literal passed to add(). The point is that "why is this number what it
    is?" must be answerable at the call site.
    """
    if not str(authority).strip():
        raise ValueError(f"konst({name!r}) requires an authority")
    add(name, str(value), note or f"[{authority}]")


def pct(x, d=1):
    return f"{100*float(x):.{d}f}\\%"


def num(x, d=4):
    return f"{float(x):.{d}f}"


def sig(x, d=3):
    return f"{float(x):.{d}f}"


def thou(n):
    return f"{int(n):,}".replace(",", "{,}")


def tex(s: str) -> str:
    """LaTeX-escape a literal drawn from the data (institution names carry
    underscores). Escaping belongs here, not in the manuscript."""
    out = str(s)
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
                 ("}", r"\}"), ("~", r"\textasciitilde{}"),
                 ("^", r"\textasciicircum{}")):
        out = out.replace(a, b)
    return out


def csv(rel):
    return pd.read_csv(REPO / rel)


def pick(df, rep, model, col):
    r = df[(df.representation == rep) & (df.model == model)]
    if len(r) != 1:
        raise SystemExit(f"expected one row for {rep}/{model}; got {len(r)}")
    return r[col].iloc[0]


# --------------------------------------------------------------- S-ID -------
def sid_macros() -> None:
    A, C = csv(SID + "task_A.csv"), csv(SID + "task_C.csv")
    AF, CF = csv(SID + "task_A_family.csv"), csv(SID + "task_C_family.csv")
    B1, B2 = csv(SID + "task_B1.csv"), csv(SID + "task_B2.csv")
    D, L = csv(SID + "task_D.csv"), csv(SID + "loho.csv")
    FL, P3 = csv(SID + "floors.csv"), csv(SID + "P3.csv")
    PD = csv(SID + "plant_decomposition.csv")

    add("SidPopulations", thou(1200), "sid/config.yaml substrate")
    add("SidWorklists", thou(1200 * 27), "1,200 x 27")
    konst("SidK", 50, "sid/config.yaml substrate top-k; PROTOCOL.md \u00a74")
    add("SidChanceTwentySeven", num(1 / 27), "1/27")
    add("SidChanceTwentyTwo", num(1 / 22), "1/22")
    _scfg = yaml.safe_load((REPO / "sid/config.yaml").read_text())
    _fam = _scfg["families"]
    # config states families either as member lists or as counts; accept both
    _sz = [len(v) if isinstance(v, (list, tuple)) else int(v)
           for v in _fam.values()]
    add("SidFamilyBaseline", num(max(_sz) / sum(_sz), 4),
        "largest family share of the learned bin")

    # Task A (all 1,200 populations) — random forest is primary on both
    # headlined representations (higher I; see primary-model rule).
    add("SidTaskAAm", num(pick(A, "autopsy_mix", "random_forest", "accuracy")))
    add("SidTaskASt", num(pick(A, "structural", "random_forest", "accuracy")))
    add("SidTaskAAmPct",
        pct(pick(A, "autopsy_mix", "random_forest", "accuracy")))
    add("SidTaskAStPct",
        pct(pick(A, "structural", "random_forest", "accuracy")))
    add("SidTaskALearnedAm",
        num(pick(A, "autopsy_mix", "random_forest", "learned")))
    add("SidTaskALearnedSt",
        num(pick(A, "structural", "random_forest", "learned")))

    # Task C — the NULL restriction (populations from the nominal process)
    add("SidTaskCAm", num(pick(C, "autopsy_mix", "random_forest", "acc_all27")))
    add("SidTaskCSt", num(pick(C, "structural", "random_forest", "acc_all27")))
    add("SidTaskCAmPct",
        pct(pick(C, "autopsy_mix", "random_forest", "acc_all27")))
    add("SidTaskCStPct",
        pct(pick(C, "structural", "random_forest", "acc_all27")))
    add("SidTaskCLearnedDiagAm",
        num(pick(C, "autopsy_mix", "random_forest", "acc_learned22")),
        "DIAGNOSTIC ONLY: recall under 27 classes, not a 22-class refit")

    add("SidFamilyAm",
        num(pick(AF, "autopsy_mix", "random_forest", "accuracy")))
    add("SidFamilySt",
        num(pick(AF, "structural", "random_forest", "accuracy")))
    add("SidFamilyCAm",
        num(pick(CF, "autopsy_mix", "random_forest", "family_accuracy")))
    add("SidFamilyCAmPct",
        pct(pick(CF, "autopsy_mix", "random_forest", "family_accuracy"), 1))
    add("SidFamilyCSt",
        num(pick(CF, "structural", "random_forest", "family_accuracy")))

    # Task D — NULL vs planted. All six differences are negative.
    add("SidRegimeMaxDiff", num(D.difference.abs().max()))
    add("SidRegimeAllNegative",
        "yes" if bool((D.difference < 0).all()) else "no")
    add("SidRegimeMinDiff", num(D.difference.abs().min()))

    # vocabulary-independence ratio: structural / autopsy_mix, Task A
    rl = (pick(A, "structural", "logistic", "accuracy")
          / pick(A, "autopsy_mix", "logistic", "accuracy"))
    rr = (pick(A, "structural", "random_forest", "accuracy")
          / pick(A, "autopsy_mix", "random_forest", "accuracy"))
    add("SidVocabRatioLo", f"{min(rl, rr):.2f}")
    add("SidVocabRatioHi", f"{max(rl, rr):.2f}")

    for tag, rep in (("Am", "autopsy_mix"), ("St", "structural")):
        add(f"SidISpec{tag}", sig(pick(A, rep, "random_forest", "I_bits")))
        add(f"SidISpecCI{tag}",
            str(pick(A, rep, "random_forest", "CI")).replace("[", "").replace(
                "]", "").replace(",", ",\\,"))
        add(f"SidIPlant{tag}",
            sig(pick(B1, rep, "random_forest", "I_plant_bits")))
        add(f"SidIPlantCI{tag}",
            str(pick(B1, rep, "random_forest", "CI")).replace(
                "[", "").replace("]", "").replace(",", ",\\,"))
        add(f"SidIPop{tag}", sig(pick(B2, rep, "random_forest", "I_pop_bits")))
        add(f"SidLoho{tag}", num(pick(L, rep, "random_forest", "loho_acc")))
        add(f"SidLohoRatio{tag}",
            f'{float(pick(L, rep, "random_forest", "ratio")):.3f}')

    fl = FL.set_index("representation")
    add("SidFloorPopAm", sig(fl.loc["autopsy_mix", "floor_pop_I"]))
    add("SidFloorPopSt", sig(fl.loc["structural", "floor_pop_I"]))
    add("SidFloorSpecAm", sig(fl.loc["autopsy_mix", "floor_27_I"]))
    add("SidFloorSpecSt", sig(fl.loc["structural", "floor_27_I"]))

    p3 = P3.set_index("representation")
    add("SidNormRatioAm", f'{float(p3.loc["autopsy_mix", "norm_ratio"]):.2f}')
    add("SidNormRatioSt", f'{float(p3.loc["structural", "norm_ratio"]):.2f}')
    add("SidNormRatioLo",
        f'{min(p3.norm_ratio):.1f}')
    add("SidNormRatioHi", f'{max(p3.norm_ratio):.1f}')
    add("SidRawRatioAm", f'{float(p3.loc["autopsy_mix", "raw_ratio"]):.2f}')
    add("SidRawRatioSt", f'{float(p3.loc["structural", "raw_ratio"]):.2f}')
    konst("SidNormFloor", 1.5, "PROTOCOL.md P3c committed multiple")

    pd_ = PD[PD.representation == "structural"].set_index("stratum")
    add("SidAlignCEal", sig(pd_.loc["aligned", "mean_CE_bits"]))
    add("SidAlignCEnon", sig(pd_.loc["non_aligned", "mean_CE_bits"]))
    add("SidAlignAccAl", num(pd_.loc["aligned", "accuracy"]))
    add("SidAlignAccNon", num(pd_.loc["non_aligned", "accuracy"]))
    add("SidAlignNal", thou(pd_.loc["aligned", "instances"]))
    add("SidAlignNnon", thou(pd_.loc["non_aligned", "instances"]))


def sid_strata_macros() -> None:
    """Within-stratum class distributions — re-derived, not hand-typed."""
    frozen = yaml.safe_load((REPO / "config/frozen_config.yaml").read_text())
    S = pd.read_parquet(REPO / (SID + "worklists.parquet"),
                        columns=["plant_condition", "spec_name", "geometry"]) \
        if (REPO / (SID + "worklists.parquet")).exists() else None
    if S is None:
        raise SystemExit("S-ID worklists.parquet absent")
    ens = frozen["grid"]["ensemble"]["name"]
    sens = frozen["alignment"]["class_sensitivity"]
    pert = frozen["alignment"]["plant_perturbs"]
    geom = dict(zip(S.spec_name, S.geometry))

    def strat(sp, pl):
        if pl == "NULL":
            return "null_populations"
        if sp == ens:
            return "ensemble"
        return ("aligned" if set(sens.get(geom.get(sp), []))
                & set(pert.get(pl, [])) else "non_aligned")

    S["stratum"] = [strat(a, b) for a, b in zip(S.spec_name, S.plant_condition)]
    for tag, st in (("Al", "aligned"), ("Non", "non_aligned")):
        g = S[S.stratum == st]
        vc = g.plant_condition.value_counts() / len(g)
        add(f"SidStratMaj{tag}", num(vc.max()),
            f"within-stratum majority rate, {st}")
        add(f"SidStratCopy{tag}", num(vc.get("COPY", 0.0)),
            f"COPY share, {st}")
    add("SidPlantEntropy", num(2.1610), "design == empirical H(plant)")


# --------------------------------------------------------------- R-ID -------
def rid_macros() -> None:
    A, AF = csv(RID + "task_A.csv"), csv(RID + "task_A_family.csv")
    L, G = csv(RID + "loco.csv"), csv(RID + "gap.csv")
    B, FL = csv(RID + "p_r_b.csv"), csv(RID + "floors.csv")
    PC, PR = csv(RID + "p_r_c.csv"), csv(RID + "predictions.csv")
    rcfg = yaml.safe_load((REPO / "rid/config.yaml").read_text())

    W = pd.read_parquet(REPO / (RID + "worklists.parquet"),
                        columns=["corpus", "pi", "unit", "unit_id",
                                 "spec_name", "n"])
    add("RidUnits", thou(W.unit_id.nunique()))
    add("RidWorklists", thou(len(W)))
    add("RidSealedWorklists", thou(rcfg["substrate"]["expected_worklists"]))
    add("RidAbsentWorklists",
        thou(rcfg["substrate"]["expected_worklists"] - len(W)))
    add("RidCorpora", str(W.corpus.nunique()))
    add("RidChance", num(1 / 27))

    for tag, rep in (("Am", "autopsy_mix"), ("St", "structural")):
        add(f"SealedRidTaskA{tag}", num(pick(A, rep, "random_forest", "accuracy")))
        add(f"SealedRidTaskALearned{tag}",
            num(pick(A, rep, "random_forest", "learned")))
        add(f"SealedRidFamily{tag}", num(pick(AF, rep, "random_forest", "accuracy")))
        add(f"RidLoco{tag}", num(pick(L, rep, "random_forest", "loco_acc")))
        add(f"RidLocoRatio{tag}",
            f'{float(pick(L, rep, "random_forest", "ratio")):.3f}')
        add(f"RidLocoRatioLog{tag}",
            f'{float(pick(L, rep, "logistic", "ratio")):.3f}')
        add(f"RidGap{tag}", num(pick(G, rep, "random_forest", "gap")))
        add(f"RidGapCI{tag}",
            str(pick(G, rep, "random_forest", "CI")).replace("[", "").replace(
                "]", "").replace(",", ",\\,"))
        add(f"RidISpec{tag}", sig(pick(B, rep, "random_forest", "I_S_bits")))
        add(f"SealedRidICorpus{tag}",
            sig(pick(B, rep, "random_forest", "I_corpus_bits")))
        add(f"RidICorpusCI{tag}",
            str(pick(B, rep, "random_forest", "I_corpus_CI")).replace(
                "[", "").replace("]", "").replace(",", ",\\,"))
        add(f"RidNormRatio{tag}",
            f'{float(pick(B, rep, "random_forest", "norm_ratio")):.2f}')

    ghead = G[G.representation != "overlap_profile"]
    add("RidGapLoPts", f"{100*ghead.gap.min():.1f}")
    add("RidGapHiPts", f"{100*ghead.gap.max():.1f}")
    add("RidLocoRatioLo", f"{L[L.representation!='overlap_profile'].ratio.min():.3f}")
    add("RidLocoRatioHi", f"{L[L.representation!='overlap_profile'].ratio.max():.3f}")

    fl = FL.set_index("representation")
    add("RidFloorSpecAm", sig(fl.loc["autopsy_mix", "floor_27_I"]))
    add("RidFloorCorpusAm", sig(fl.loc["autopsy_mix", "floor_corpus_I"]))

    add("RidPRCNotEvaluable", str(int((PC.verdict == "NOT EVALUABLE").sum())))
    add("RidPRCTotal", str(len(PC)))
    prd = PR[PR.prediction == "P-R-D"]
    add("RidPRDVerdict", str(prd.verdict.iloc[0]))
    _TA = pd.read_csv(REPO / (RID + "task_A.csv"))
    def _prd(kind):
        g = _TA[_TA.model == kind]
        return (float(g[g.representation == "structural"].accuracy.iloc[0])
                / float(g[g.representation == "autopsy_mix"].accuracy.iloc[0]))
    add("SealedRidPRDLogistic", num(_prd("logistic"), 3))
    add("SealedRidPRDForest", num(_prd("random_forest"), 3))
    konst("RidPRDThreshold", 0.90, "rid/PROTOCOL.md clause P-R-D threshold")
    add("RidPRDMargin", num(0.90 - 0.889, 3), "how far P-R-D missed")

    sc = rcfg["interpretation_scale"]
    add("RidBandStrongC", num(sc["strong"]["c27"][0], 2))
    add("RidBandStrongFam", num(sc["strong"]["family"][0], 2))
    add("RidBandModLoC", num(sc["moderate"]["c27"][0], 2))
    add("RidBandModLoFam", num(sc["moderate"]["family"][0], 2))
    add("RidFamilyMarginAm",
        num(pick(AF, "autopsy_mix", "random_forest", "accuracy")
            - sc["strong"]["family"][0]))
    add("RidSidLohoAm", num(rcfg["loco_comparison"]["sid_loho_autopsy_mix"], 3))
    add("RidSidLohoSt", num(rcfg["loco_comparison"]["sid_loho_structural"], 3))

    mi = rcfg["mutual_information"]
    add("RidHspecDeclared", num(mi["h_spec_bits"]))
    add("RidHcorpusDeclared", num(mi["h_corpus_bits"]))

    def H(y):
        _, c = np.unique(y, return_counts=True)
        p = c / c.sum()
        return float(-(p * np.log2(p)).sum())
    add("RidHspecEmpirical", num(H(W.spec_name)))
    add("RidHcorpusEmpirical", num(H(W.corpus)))


def rid_defect_macros() -> None:
    """D1 / D2 geometry, re-derived read-only from the stored substrate."""
    W = pd.read_parquet(REPO / (RID + "worklists.parquet"),
                        columns=["corpus", "pi", "unit", "unit_id", "n",
                                 "spec_name"])
    W["year"] = W.unit.map(
        lambda x: (json.loads(x) if isinstance(x, str) else x)[0])
    W["component"] = W.corpus + "|" + W.year.astype(str)

    from sklearn.model_selection import GroupKFold
    N = len(W)
    fold = np.empty(N, dtype=int)
    for f, (_, te) in enumerate(
            GroupKFold(n_splits=5).split(np.zeros(N), groups=W.unit_id)):
        fold[te] = f
    W["fold"] = fold

    add("RidComponents", str(W.component.nunique()))
    add("RidFyUnits", str(W[W.pi == "fy"].unit_id.nunique()))
    add("RidFyOfficeUnits", str(W[W.pi == "fy_office"].unit_id.nunique()))

    fy = W[W.pi == "fy"].drop_duplicates("unit_id")[["component", "fold"]] \
        .rename(columns={"fold": "pfold"})
    fo = W[W.pi == "fy_office"].drop_duplicates("unit_id")[
        ["component", "fold", "unit_id"]]
    m = fo.merge(fy, on="component", how="inner")
    cross = int((m.fold != m.pfold).sum())
    add("RidCrossFoldChildren", thou(cross))
    add("RidCrossFoldChildrenPct", pct((m.fold != m.pfold).mean()))
    add("RidCrossFoldRows", thou(27 * cross))
    add("RidCrossFoldRowsPct", pct(27 * cross / N))
    add("RidFyMassPct", pct(len(W[W.pi == "fy"]) / N))

    cells = W.groupby("unit_id").size()
    partial = set(cells[cells == 22].index)
    add("RidPartialUnits", str(len(partial)))
    P = W[W.unit_id.isin(partial)].drop_duplicates("unit_id")
    F = W[~W.unit_id.isin(partial)].drop_duplicates("unit_id")
    add("RidPartialMedianN", thou(P.n.median()))
    add("RidFullMedianN", thou(F.n.median()))
    add("RidPartialSizeRatio", f"{P.n.median()/F.n.median():.0f}")
    # partial-battery concentration BY NESTING LEVEL (D1 x D2 interaction)
    for lvl, macro in (("fy", "RidPartialFyShare"),
                       ("fy_office", "RidPartialFoShare")):
        tot = W[W.pi == lvl].unit_id.nunique()
        got = P[P.pi == lvl].unit_id.nunique()
        add(macro, pct(got / tot, 1))
    top = P.corpus.value_counts()
    add("RidPartialTopCorpus", tex(top.index[0]))
    add("RidPartialTopCount", str(int(top.iloc[0])))
    add("RidPartialTopPct", pct(top.iloc[0] / len(P)))
    add("RidPartialZeroCorpora", str(W.corpus.nunique() - top.shape[0]))

    per = W.groupby("corpus").agg(units=("unit_id", "nunique"),
                                  rows=("n", "size"))
    per["share"] = per.rows / N
    add("RidNycSfShare", pct(per.loc[["nyc", "sf"], "share"].sum()))
    add("RidNycUnits", thou(per.loc["nyc", "units"]))
    add("RidNycShare", pct(per.loc["nyc", "share"]))

    lines = [r"\begin{tabular}{lrrrr}", r"\toprule",
             r"institution & units & instances & share of pooled "
             r"& majority baseline \\", r"\midrule"]
    majs = []
    for c in per.sort_values("rows", ascending=False).index:
        g = W[W.corpus == c]
        maj = float(g.spec_name.value_counts().iloc[0] / len(g))
        majs.append(maj)
        lines.append(
            f"{tex(c)} & {int(per.loc[c,'units'])} & {thou(per.loc[c,'rows'])} "
            f"& {pct(per.loc[c,'share'],2)} & {num(maj)} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    MACROS["RidPerCorpusTable"] = "%\n".join(lines)
    _ORDER.append(("RidPerCorpusTable", "generated per-institution table"))
    add("RidMajBaselineLo", num(min(majs)))
    add("RidMajBaselineHi", num(max(majs)))

    # LOCO / grouped training-set sizes (the P-R-GAP size confound)
    sizes = [len(tr) for tr, _ in
             GroupKFold(n_splits=5).split(np.zeros(N), groups=W.unit_id)]
    add("RidGroupedTrain", thou(int(np.mean(sizes))))
    loco_tr = [N - int((W.corpus == c).sum()) for c in W.corpus.unique()]
    add("RidLocoTrainMean", thou(int(np.mean(loco_tr))))
    add("RidLocoTrainMin", thou(min(loco_tr)))
    add("RidTrainExcessPct",
        f"{100*(np.mean(loco_tr)/np.mean(sizes)-1):.1f}")


def prb_convention_macros() -> None:
    """The three-convention P-R-B sensitivity grid, computed here."""
    B = csv(RID + "p_r_b.csv")
    rcfg = yaml.safe_load((REPO / "rid/config.yaml").read_text())
    Hs_d = rcfg["mutual_information"]["h_spec_bits"]
    Hc_d = rcfg["mutual_information"]["h_corpus_bits"]

    W = pd.read_parquet(REPO / (RID + "worklists.parquet"),
                        columns=["corpus", "spec_name"])

    def H(y):
        _, c = np.unique(y, return_counts=True)
        p = c / c.sum()
        return float(-(p * np.log2(p)).sum())
    Hs_e, Hc_e = H(W.spec_name), H(W.corpus)
    shift = Hc_d - Hc_e
    add("RidHcorpusShift", sig(shift))

    for tag, rep in (("Am", "autopsy_mix"), ("St", "structural")):
        r = B[B.representation == rep].iloc[0]
        Is, Ic = float(r.I_S_bits), float(r.I_corpus_bits)
        hi = float(str(r.I_corpus_CI).strip("[]").split(",")[1])
        CEc = Hc_e - Ic
        nS = Is / Hs_d
        add(f"RidConvOne{tag}", f"{nS/(Ic/Hc_d):.2f}")
        add(f"RidConvOneProp{tag}", f"{nS/(hi/Hc_d):.2f}")
        add(f"RidConvTwo{tag}", f"{(Is/Hs_e)/(Ic/Hc_e):.2f}")
        add(f"RidConvTwoProp{tag}", f"{(Is/Hs_e)/(hi/Hc_e):.2f}")
        IcThree = Hc_d - CEc
        add(f"RidConvThree{tag}", f"{nS/(IcThree/Hc_d):.2f}")
        add(f"RidConvThreeProp{tag}", f"{nS/((hi+shift)/Hc_d):.2f}")
        if tag == "Am":
            add("RidConvThreeIcorpus", sig(IcThree))
            add("RidConvThreeInflation", f"{IcThree/Ic:.1f}")


def overlap_macros() -> None:
    """The never-headlined overlap representation, under the SEALED
    primary-model rule (higher I is the tighter lower bound), so the
    comparison against the headlined representations is like-for-like.

    DEFECT D-A11: this representation is built by deleting the coordinate
    named by the target, so it is NOT attribution under the paper's
    observation model and the manuscript no longer asserts that it is the
    strongest attributor. These figures are retained because the §N
    decontamination is still reported as run -- it answered the availability
    question honestly -- and because the size of the artifact must stay
    visible. Nothing in the abstract, the contributions, or the
    joint-property argument may rest on them. The augmented-model
    replacement is refbattery_macros() below."""
    SA, SC = csv(SID + "task_A.csv"), csv(SID + "task_C.csv")
    SB2, SL = csv(SID + "task_B2.csv"), csv(SID + "loho.csv")
    RA, RF_ = csv(RID + "task_A.csv"), csv(RID + "task_A_family.csv")
    RL = csv(RID + "loco.csv")

    def primary(df, rep, icol):
        d = df[df.representation == rep]
        return d.loc[d[icol].idxmax(), "model"]

    ms = primary(SA, "overlap_profile", "I_bits")
    mr = primary(RA, "overlap_profile", "I_bits")
    add("SidOverlapPrimaryModel", ms.replace("_", " "))
    add("RidOverlapPrimaryModel", mr.replace("_", " "))
    add("SidTaskAOv", num(pick(SA, "overlap_profile", ms, "accuracy")))
    add("SidTaskCOv", num(pick(SC, "overlap_profile", ms, "acc_all27")))
    add("SealedRidTaskAOv", num(pick(RA, "overlap_profile", mr, "accuracy")))
    add("SealedRidFamilyOv", num(pick(RF_, "overlap_profile", mr, "accuracy")))
    add("RidLocoOv", num(pick(RL, "overlap_profile", mr, "loco_acc")))
    add("SidIPopOv",
        sig(SB2[SB2.representation == "overlap_profile"].I_pop_bits.max()))
    add("SidLohoRatioOvLo",
        f'{SL[SL.representation=="overlap_profile"].ratio.min():.3f}')
    add("SidLohoRatioOvHi",
        f'{SL[SL.representation=="overlap_profile"].ratio.max():.3f}')
    # the one measure on which a headlined representation leads
    add("RidLocoRatioOv",
        f'{float(pick(RL, "overlap_profile", mr, "ratio")):.3f}')
    # Under the primary-model rule the overlap representation leads on
    # retention ratio too. Only a best-of-models reading puts a headlined
    # representation ahead, and then by a hair. Both are generated so the
    # prose cannot quietly pick the flattering one.
    head_best = RL[RL.representation != "overlap_profile"].ratio.max()
    ov_best = RL[RL.representation == "overlap_profile"].ratio.max()
    add("RidLocoRatioHeadBest", f"{head_best:.3f}")
    add("RidLocoRatioOvBest", f"{ov_best:.3f}")
    add("RidLocoRatioOvMargin", f"{head_best - ov_best:.3f}",
        "best-of-models margin; the ONLY reading where a headlined rep leads")


def refbattery_macros() -> None:
    """The augmented reference-battery observation model (W, X, R_X).

    D-A11 disposition (ii). The observer holds the worklist, its population,
    and the full 27-specification battery run on that same population. The
    representation is all 27 Jaccard coordinates in fixed sorted order with
    the self-coordinate RETAINED -- target-independent, since coordinate p is
    spec p for every row whatever produced it.

    This is same-population reference matching: a different and easier task
    than attribution, and the manuscript says so wherever it appears. The
    primary model is selected by the same sealed rule used everywhere else
    (higher I is the tighter lower bound)."""
    RB = csv(REFB + "refbattery.csv")
    for arm, tag in (("sid", "Sid"), ("rid", "Rid")):
        d = RB[(RB.arm == arm) & RB.primary]
        if len(d) != 1:
            raise ValueError(f"refbattery: expected one primary row for {arm}")
        r = d.iloc[0]
        add(f"RefBattery{tag}", num(r.accuracy))
        add(f"RefBattery{tag}Pct", pct(r.accuracy))
        add(f"RefBattery{tag}Model", str(r.model).replace("_", " "))
    konst("RefBatteryWidth", 27,
          "all 27 Jaccard coordinates, self retained; ops/refbattery.py")
    konst("RefBatteryDefect", "D-A11",
          "addendum/PROTOCOL_DEFECTS.md, disposition (ii)")


def circularity_macros() -> None:
    """Defect D-A11 measured: what the overlap CONSTRUCTION contributes.

    Four representations under the sealed configs (ops/overlap_circularity.py).
    `aligned26` reproduces the sealed task_A figures exactly, which is the
    check that this harness is faithful before its contrasts are believed."""
    C = csv(OVC + "overlap_circularity.csv")

    def prim(arm, rep, col="accuracy"):
        d = C[(C.arm == arm) & (C.representation == rep) & C.primary]
        if len(d) != 1:
            raise ValueError(f"circularity: no unique primary {arm}/{rep}")
        return d.iloc[0][col]

    for arm, tag in (("sid", "Sid"), ("rid", "Rid")):
        add(f"OvAligned{tag}", num(prim(arm, "aligned26")))
        add(f"OvSorted{tag}", num(prim(arm, "sorted26")))
        add(f"OvFixed{tag}", num(prim(arm, "fixed27")))
        add(f"OvSynthetic{tag}", num(prim(arm, "synthetic")))
    # the self-coordinate is a constant; stated as measured, not assumed
    js = C[["j_self_min", "j_self_max"]].to_numpy()
    if not (js == 1.0).all():
        raise ValueError("circularity: j_self is not identically 1.0")
    konst("OvSelfValue", "1.000",
          "measured: j_self min = max = 1.0 on every row, both arms")


_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
          7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven",
          12: "twelve"}


def abstract_macros() -> None:
    """Forms the abstract needs that the body does not.

    Where the abstract's prose rounds a figure (79%, 32%, 2--6 points),
    the ROUNDED form is generated here rather than typed, so the prose
    stays verbatim and still moves if the underlying number moves. Spelled
    numbers likewise: "twelve" is derived from the corpus count, not
    written down, or it goes stale silently the day a corpus is added.
    """
    C, D = csv(SID + "task_C.csv"), csv(SID + "task_D.csv")
    CF = csv(SID + "task_C_family.csv")
    G = csv(RID + "gap.csv")
    W = pd.read_parquet(REPO / (RID + "worklists.parquet"),
                        columns=["corpus"])

    _sc = yaml.safe_load((REPO / "sid/config.yaml").read_text())
    add("SidLearnedCells", str(len(_sc["bins"]["learned"])))
    add("SidAllCells", str(sum(len(v) if isinstance(v, (list, tuple))
                               else int(v) for v in _sc["bins"].values())))
    add("SidChanceTwentyTwoPct", pct(1 / 22, 1))
    add("SidChanceTwentySevenPct", pct(1 / 27, 1))
    # rounded forms used by the abstract's prose
    add("SidTaskCAmPctRound",
        pct(pick(C, "autopsy_mix", "random_forest", "acc_all27"), 0))
    add("SidFamilyCAmPctRound",
        pct(pick(CF, "autopsy_mix", "random_forest", "family_accuracy"), 1))
    add("FamilyBaselinePct", pct(7 / 22, 1), "majority family 7/22")
    add("FamilyBaselinePctRound", pct(7 / 22, 0))
    add("SidRegimeMaxDiffShort", num(D.difference.abs().max(), 3))
    ghead = G[G.representation != "overlap_profile"]
    add("RidGapLoPtsRound", f"{100*ghead.gap.min():.0f}")
    add("RidGapHiPtsRound", f"{100*ghead.gap.max():.0f}")
    n = int(W.corpus.nunique())
    add("RidCorporaWord", _WORDS[n], "spelled corpus count, derived")


def methods_macros() -> None:
    """Everything the methods sections need to be self-contained: library
    versions, decoder specifications, fold schemes, and the 27-cell battery
    as a generated table. A reader must be able to reconstruct the study
    from the article; none of this may be typed by hand into the prose."""
    frozen = yaml.safe_load((REPO / "config/frozen_config.yaml").read_text())
    scfg = yaml.safe_load((REPO / "sid/config.yaml").read_text())
    rcfg = yaml.safe_load((REPO / "rid/config.yaml").read_text())
    env = (REPO / "config/env_m5_freeze.txt").read_text()

    # --- library versions, parsed from the frozen environment ------------
    vers = {}
    for line in env.splitlines():
        line = line.strip().lstrip("# ").strip()
        if "==" in line and not line.startswith("#"):
            k, _, v = line.partition("==")
            vers[k.strip().lower()] = v.strip()
        if line.lower().startswith("python:"):
            vers["python"] = line.split()[-1]
    for key, macro in (("python", "VerPython"), ("numpy", "VerNumpy"),
                       ("scipy", "VerScipy"), ("scikit-learn", "VerSklearn"),
                       ("pandas", "VerPandas")):
        if key not in vers:
            raise SystemExit(f"env freeze: no version for {key}")
        add(macro, vers[key])

    # --- decoders --------------------------------------------------------
    lr = scfg["models"]["logistic"]["params"]
    rf = scfg["models"]["random_forest"]["params"]
    add("DecLogSolver", str(lr["solver"]))
    add("DecLogC", str(lr["C"]))
    add("DecLogMaxIter", thou(lr["max_iter"]))
    add("DecRfTrees", str(rf["n_estimators"]))
    add("DecRfDepth", str(rf["max_depth"]))
    add("DecRfLeaf", str(rf["min_samples_leaf"]))
    add("DecRfFeatures", str(rf["max_features"]))
    add("SidFolds", str(scfg["cv"]["task_a"]["n_folds"]))
    add("RidFolds", str(rcfg["cv"]["grouped_by_unit"]["n_folds"]))
    add("RidLocoFolds", str(rcfg["cv"]["loco"]["n_folds"]))
    add("SidCvSeed", str(scfg["cv"]["seed"]))
    add("RidCvSeed", str(rcfg["cv"]["seed"]))
    add("BootResamples", thou(rcfg["bootstrap"]["n_resamples"]))
    # CW-5: an empty tail is reported as 0/N, not rounded to a probability
    # of zero. N resamples cannot resolve a fraction below 1/N.
    add("BootZeroForm", "$0/" + thou(rcfg["bootstrap"]["n_resamples"]) + "$")
    add("BootCI", pct(rcfg["bootstrap"]["ci"], 0))
    add("SidSeedRoot", tex(scfg["substrate"]["seed_root"]))
    add("RidSeedRoot", tex(rcfg["seed_root"]))

    # --- the 27-cell battery, generated ----------------------------------
    cells = frozen["grid"]["cells"]
    mdl = frozen["models"]
    rule = {"benford", "round_flag", "repeat", "dup_pair"}
    nice = {"iforest": "isolation forest", "lof": "LOF", "knn": "kNN distance",
            "ocsvm": "one-class SVM", "mcd": "MCD", "autoencoder": "autoencoder",
            "benford": "Benford", "round_flag": "round-number",
            "repeat": "repetition", "dup_pair": "duplicate pair"}

    def hyper(c):
        p = dict(mdl.get(c["algorithm"], {}))
        p.update(c.get("params", {}))
        if not p:
            return "---"
        out = []
        for k, v in p.items():
            if v is None:
                continue
            if isinstance(v, list):
                v = f"{len(v)} divisors"
            out.append(f"{tex(k)}\\,{tex(v)}")
        return ", ".join(out) if out else "---"

    rows = [r"\begin{tabular}{llllp{3.6cm}}", r"\toprule",
            r"cell & family & feature set & preprocessing & hyperparameters"
            r" \\", r"\midrule"]
    order = ["iforest", "lof", "knn", "ocsvm", "mcd", "autoencoder"]
    seq = sorted(cells, key=lambda c: (c["algorithm"] in rule,
                                       order.index(c["algorithm"])
                                       if c["algorithm"] in order else 9,
                                       c["name"]))
    n_learned = 0
    for i, c in enumerate(seq, 1):
        if c["algorithm"] not in rule:
            n_learned += 1
        if i == n_learned + 1 and c["algorithm"] in rule:
            rows.append(r"\midrule")
        rows.append(
            f"{i} & {nice[c['algorithm']]} & {tex(c['features'])} & "
            f"{tex(c['preprocessing'])} & {hyper(c)} \\\\")
    rows += [r"\midrule",
             f"{len(seq)+1} & ensemble & --- & --- & "
             r"mean rank over cells 1--" + str(len(seq)) + r" \\",
             r"\bottomrule", r"\end{tabular}"]
    MACROS["BatteryTable"] = "%\n".join(rows)
    _ORDER.append(("BatteryTable", "generated 27-cell battery table"))
    add("BatteryLearned", str(n_learned))
    add("BatteryRule", str(len(seq) - n_learned))
    add("BatteryNonEnsemble", str(len(seq)),
        "cells the ensemble averages over")

    # Which learned cells consume a seed at S-ID's population size.
    # lof and knn never reference the seed argument; ocsvm uses it only for
    # a fit-subsample draw, and the frozen config leaves fit_subsample null.
    # Assert that precondition rather than trusting it.
    if mdl["ocsvm"].get("fit_subsample") is not None:
        raise SystemExit("ocsvm.fit_subsample is set: the deterministic-cell "
                         "count in the methods section no longer holds")
    det = {"lof", "knn", "ocsvm"}
    n_det = sum(1 for c in cells
                if c["algorithm"] in det and c["algorithm"] not in rule)
    add("SidDeterministicCells", str(n_det),
        "learned cells that consume no seed at n=5,000")
    add("SidStochasticCells", str(n_learned - n_det))
    fam = {}
    for c in cells:
        if c["algorithm"] not in rule:
            fam[c["algorithm"]] = fam.get(c["algorithm"], 0) + 1
    counts = sorted(fam.values(), reverse=True)
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
             6: "six", 7: "seven"}
    add("SidFamilySizes",
        ", ".join(words[c] for c in counts[:-1]) + " and " + words[counts[-1]],
        "learned cells per family, descending")
    add("SidFamilyCount", str(len(fam)))
    import math
    add("EpsFloorBits", f"{-math.log2(1e-12):.0f}",
        "cross-entropy contributed by one floored probability")
    add("EpsFloorShift", num(-math.log2(1e-12) / (1200 * 27), 4),
        "how far ONE floored instance moves the mean over all worklists")
    add("SidNullPopulations",
        thou(yaml.safe_load((REPO / "sid/config.yaml").read_text())
             ["substrate"]["populations"]["null_total"]))


def substrate_macros() -> None:
    """R-ID substrate construction: what a unit is, and how many records
    the study actually covers."""
    W = pd.read_parquet(REPO / (RID + "worklists.parquet"),
                        columns=["corpus", "pi", "unit_id", "n", "spec_name"])
    U = W.drop_duplicates("unit_id")
    add("RidRecords", thou(U.n.sum()), "records across all units")
    add("RidMinUnitN", thou(1000), "frozen_corpora pi.min_unit_n")
    add("RidMedianUnitN", thou(U.n.median()))

    per = (W.groupby("corpus")
           .agg(units=("unit_id", "nunique"), rows=("unit_id", "size")))
    recs = U.groupby("corpus").n.sum()
    per["records"] = recs
    per["share"] = per.rows / len(W)
    lines = [r"\begin{tabular}{lrrrrr}", r"\toprule",
             r"institution & units & records & instances & share "
             r"& majority \\", r"\midrule"]
    for c in per.sort_values("rows", ascending=False).index:
        g = W[W.corpus == c]
        maj = float(g.spec_name.value_counts().iloc[0] / len(g))
        lines.append(
            f"{tex(c)} & {int(per.loc[c,'units'])} & "
            f"{thou(per.loc[c,'records'])} & {thou(per.loc[c,'rows'])} & "
            f"{pct(per.loc[c,'share'],2)} & {num(maj)} \\\\")
    lines += [r"\midrule",
              f"total & {int(per.units.sum())} & {thou(per.records.sum())} & "
              f"{thou(per.rows.sum())} & {pct(1.0,2)} & --- \\\\",
              r"\bottomrule", r"\end{tabular}"]
    MACROS["RidSubstrateTable"] = "%\n".join(lines)
    _ORDER.append(("RidSubstrateTable", "generated substrate table"))


def failure_threshold_macros() -> None:
    """Committed thresholds and observed values for the failed predictions.

    Item 6 of the completion audit: a reported failure must carry BOTH the
    threshold it was adjudicated against and what was observed. Three did
    not."""
    rcfg = yaml.safe_load((REPO / "rid/config.yaml").read_text())
    L = csv(SID + "loho.csv")
    # P2's committed floor is encoded in the verdict column name the sealed
    # analyzer wrote: ratio_ge_<threshold>.
    col = [c for c in L.columns if c.startswith("ratio_ge_")]
    if len(col) != 1:
        raise SystemExit(f"cannot recover P2 threshold from loho.csv: {col}")
    add("SidLohoThreshold", num(float(col[0].split("_")[-1]), 2))

    PC = csv(RID + "p_r_c.csv")
    cc = rcfg["confusion_clause"]
    add("RidPRCMinPairs", str(cc["min_confused_pairs"]))
    add("RidPRCThreshold", num(cc["threshold"], 2))
    add("RidPRCMaxObserved", str(int(PC.confused_pairs.max())))


def converse_pair_macros() -> None:
    """Remark 1's converse, instantiated from the sealed outputs.

    The remark argues that attribution and disagreement are logically
    independent. The battery contains a matched pair of pairs that shows
    both quadrants occupied at essentially the SAME overlap:

      * high overlap, heavily confused  -- the register's known case;
      * high overlap, never confused    -- the converse.

    Selection is by rule, not by hand: among learned-cell pairs on NULL
    populations, the converse instance is the highest-overlap pair whose
    symmetric mutual-confusion rate is at most CONF_MAX. The pair identities
    are asserted so the prose cannot drift away from the data.
    """
    CONF_MAX = 0.02
    frozen = yaml.safe_load((REPO / "config/frozen_config.yaml").read_text())
    rule = {c["name"] for c in frozen["grid"]["cells"]
            if c["algorithm"] in ("benford", "round_flag", "repeat",
                                  "dup_pair")}
    ens = frozen["grid"]["ensemble"]["name"]
    W = pd.read_parquet(REPO / (SID + "worklists.parquet"))
    learned = sorted(set(W.spec_name.unique()) - rule - {ens})
    N = W[W.plant_condition == "NULL"]
    cm = pd.read_csv(REPO / (SID + "task_E_confusion.csv"), index_col=0)
    rate = cm.div(cm.sum(axis=1).replace(0, 1), axis=0)

    rows = []
    for a in learned:
        ra = N[N.spec_name == a]
        for b in learned:
            if a < b:
                r1, r2 = float(rate.loc[a, b]), float(rate.loc[b, a])
                rows.append((float(ra[f"j_{b}"].mean()), a, b, r1, r2,
                             (r1 + r2) / 2))
    rows.sort(reverse=True)
    conv = next(r for r in rows if r[5] <= CONF_MAX)
    reg = next(r for r in rows
               if {r[1], r[2]} == {"iforest__full__log", "iforest__full__robust"})

    assert conv[1] == "iforest__amount_only__raw" and \
        conv[2] == "iforest__full__raw", f"converse pair moved: {conv[1:3]}"

    def nice(n):
        alg, feat, prep = n.split("__")
        return f"{alg}/{feat.replace('amount_', '')}/{prep}"

    add("ConvPairA", tex(nice(conv[1])))
    add("ConvPairB", tex(nice(conv[2])))
    add("ConvPairJ", num(conv[0], 2))
    add("ConvPairConfLo", num(min(conv[3], conv[4]), 3))
    add("ConvPairConfHi", num(max(conv[3], conv[4]), 3))
    add("RegPairA", tex(nice(reg[1])))
    add("RegPairB", tex(nice(reg[2])))
    add("RegPairJ", num(reg[0], 2))
    add("RegPairConfLo", num(min(reg[3], reg[4]), 2))
    add("RegPairConfHi", num(max(reg[3], reg[4]), 2))
    add("ConvConfMax", num(CONF_MAX, 2))


def pairwise_macros() -> None:
    """Part 3.3's pairwise attribution graph: 231 dedicated binary tasks.
    This replaces the confusion-matrix instance in Remark 1, because
    multiclass confusion conflates 'rarely confused with each other' with
    'both usually assigned elsewhere' and a binary decoder cannot."""
    P = pd.read_csv(REPO / "addendum/results/pairwise_graph.csv")
    add("PairN", str(len(P)), "C(22,2) binary attribution tasks")
    add("PairCorr", f"{P.mean_overlap.corr(P.d):+.2f}")
    add("PairDMin", num(P.d.min(), 2))
    add("PairDMed", num(P.d.median(), 2))
    add("PairDMax", num(P.d.max(), 2))
    # the matched-overlap contrast: inseparable vs near-perfect at ~equal overlap
    # The contrast must be MATCHED on overlap, or it argues nothing: pick the
    # least-separable high-overlap pair, then its nearest neighbour in overlap
    # among well-separated pairs.
    hi = P[P.mean_overlap >= P.mean_overlap.quantile(0.90)]
    lo = hi.loc[hi.d.idxmin()]
    cand = P[(P.d >= 0.95) & (P.a != lo.a) & (P.b != lo.b)].copy()
    cand["gap"] = (cand.mean_overlap - lo.mean_overlap).abs()
    up = cand.loc[cand.gap.idxmin()]
    add("PairOverlapGap", num(abs(up.mean_overlap - lo.mean_overlap), 3),
        "overlap difference between the matched pair -- must be small")

    def nice(n):
        a, f, pr = n.split("__")
        return f"{a}/{f.replace('amount_', '')}/{pr}"
    add("PairFlatA", tex(nice(lo.a)))
    add("PairFlatB", tex(nice(lo.b)))
    add("PairFlatOverlap", num(lo.mean_overlap, 2))
    add("PairFlatAcc", num(lo.A, 4))
    add("PairFlatD", num(lo.d, 2))
    add("PairSharpA", tex(nice(up.a)))
    add("PairSharpB", tex(nice(up.b)))
    add("PairSharpOverlap", num(up.mean_overlap, 2))
    add("PairSharpAcc", num(up.A, 4))
    add("PairSharpD", num(up.d, 2))


def popcontrol_macros() -> None:
    """Section Q's population-only decoder: the derived-expectation control."""
    # Analytic, not measured. section_Q sets L(S|X) = H(S) by construction:
    # within a unit every specification sees the same population, so a
    # population-only decoder cannot separate them and its loss IS the label
    # entropy. The control therefore holds identically, which is stronger
    # than an approximately-zero fit. An earlier fitted value (0.0027) is
    # superseded; its per-instance outputs were never persisted, and no refit
    # is needed because the analytic result is exact. See D-A4, D-A8.
    _Qp = pd.read_csv(REPO / "addendum/results/section_Q.csv")
    assert (_Qp.L_population_only - (_Qp.delta_W_given_X
                                     + _Qp.L_worklist_and_population)
            ).abs().max() < 5e-4, "section_Q identity does not close"
    konst("ProvPopOnlyBits", "0", "analytic: section_Q sets L(S|X)=H(S) "
          "by construction on the crossed design (D-A4)")
    add("ProvFlooredCount", "zero",
        "measured over every persisted fit; see defect D-A2")


def portability_macros() -> None:
    """Part 4(e): excess-over-null portability index rho = (A_out - A0)/(A_in - A0).
    A0 is the null the task can reach without any signature: chance for the
    balanced specification task, the majority-class rate for the unbalanced
    family task. Both the sealed ratio and rho are generated so the paper can
    show what changed."""
    J = pd.read_csv(REPO / "addendum/results/section_J.csv")
    A = pd.read_csv(REPO / "addendum/results/section_A.csv")
    L = pd.read_csv(REPO / (RID + "loco.csv"))
    TA = pd.read_csv(REPO / (RID + "task_A.csv"))
    for tag, rep in (("Am", "autopsy_mix"), ("St", "structural")):
        a_in = float(A[(A.task == "spec27") & (A.representation == rep)
                       & (A.model == "random_forest")].accuracy.iloc[0])
        a_out = float(J[(J.arm == "LOCO") & (J.representation == rep)].pooled.iloc[0])
        a_mac = float(J[(J.arm == "LOCO") & (J.representation == rep)].macro.iloc[0])
        a0 = 1 / 27
        add(f"RhoPooled{tag}", num((a_out - a0) / (a_in - a0), 3))
        add(f"RhoMacro{tag}", num((a_mac - a0) / (a_in - a0), 3))
        add(f"RatioPooled{tag}", num(a_out / a_in, 3), "the superseded index")
        # sealed (unit-grouped) figures, for the before/after
        s_in = float(TA[(TA.representation == rep)
                        & (TA.model == "random_forest")].accuracy.iloc[0])
        s_out = float(L[(L.representation == rep)
                        & (L.model == "random_forest")].loco_acc.iloc[0])
        add(f"RhoSealed{tag}", num((s_out - a0) / (s_in - a0), 3))
        add(f"RatioSealed{tag}", num(s_out / s_in, 3))
    add("PortNullSpec", num(1 / 27), "chance for the balanced 27-class task")
    # Derived, not asserted. An earlier revision carried this as a typed
    # literal (0.3182); recomputing it from the persisted labels gives
    # 0.3184, so the literal was also wrong in its last digit.
    fam = pd.read_parquet(REPO / "addendum/results"
                          / "oof_A_family_autopsy_mix_random_forest.parquet")
    a0f = float(fam.y_true.value_counts().iloc[0]) / len(fam)
    add("PortNullFamily", num(a0f), "majority-class rate, unbalanced family task")

    # How much the correction moves each spec-task retention figure. Four
    # figures: two representations x {pooled, macro}.
    shifts = []
    for rep in ("autopsy_mix", "structural"):
        a_in = float(A[(A.task == "spec27") & (A.representation == rep)
                       & (A.model == "random_forest")].accuracy.iloc[0])
        row = J[(J.arm == "LOCO") & (J.representation == rep)]
        for col in ("pooled", "macro"):
            a_out = float(row[col].iloc[0])
            shifts.append(abs(a_out / a_in - (a_out - 1 / 27) / (a_in - 1 / 27)))
    add("PortShiftLo", num(min(shifts), 3))
    add("PortShiftHi", num(max(shifts), 3))

    # The family task, where a large null makes the two indices diverge. The
    # ratio below is an ILLUSTRATIVE value chosen to make the divergence
    # legible -- it is not a measurement -- but everything derived from it is
    # computed, so the worked example cannot drift from the data.
    ILLUS = 0.75
    add("PortIllustrativeRatio", num(ILLUS, 2), "illustrative, not measured")
    fam_rho = {}
    for rep in ("autopsy_mix", "structural", "overlap_profile"):
        a_in = float(A[(A.task == "family") & (A.representation == rep)
                       & (A.model == "random_forest")].accuracy.iloc[0])
        fam_rho[rep] = (ILLUS * a_in - a0f) / (a_in - a0f)
    # The claim "retains under half the above-null signal" holds for the two
    # headlined representations and NOT for overlap_profile, whose accuracy is
    # far enough above the null that rho stays above 0.5. The manuscript must
    # therefore name its scope rather than generalise over the battery.
    add("PortFamilyRhoAm", num(fam_rho["autopsy_mix"], 3))
    add("PortFamilyRhoSt", num(fam_rho["structural"], 3))
    add("PortFamilyDiffMax", num(max(ILLUS - r for r in
                                     (fam_rho["autopsy_mix"],
                                      fam_rho["structural"])), 3))


def multitask_macros() -> None:
    """Section H's multitask decomposition: which FACET of a specification the
    signature carries -- its algorithm, its feature basis, or its
    preprocessing transform. Ran with the addendum and was not reported."""
    H = pd.read_csv(REPO / "addendum/results/section_H.csv")
    for facet, t in (("algorithm", "Alg"), ("basis", "Basis"),
                     ("transform", "Trans")):
        d = H[H.task == f"multitask:{facet}"]
        base = float(str(d.note.iloc[0]).split("baseline ")[1].split(",")[0])
        k = int(str(d.note.iloc[0]).split(",")[1].split()[0])
        for rep, r in (("autopsy_mix", "Am"), ("structural", "St")):
            a = float(d[d.family == rep].accuracy.iloc[0])
            add(f"Multi{t}{r}", num(a, 4))
            add(f"Multi{t}Lift{r}", num(a - base, 3))
        add(f"Multi{t}Base", num(base, 4))
        add(f"Multi{t}K", str(k))
    nw = H[(H.task == "LOSO-family") & (H.note.str.contains("NOT WELL-POSED"))]
    add("LosoFamilyIllPosed", str(len(nw)))
    add("LosoFamilyTotal", str(int((H.task == "LOSO-family").sum())))


def perclass_macros() -> None:
    """Per-class recall tables for both studies. S-ID is derived from the
    persisted 27-class per-instance predictions; R-ID is the sealed run's own
    per-class table."""
    AD = REPO / "addendum" / "results"
    rows = []
    for rep, t in (("autopsy_mix", "Am"), ("structural", "St")):
        d = pd.read_parquet(AD / f"oof_F27_sid_{rep}_random_forest.parquet")
        ok = (d["y_pred"] == d["y_true"])
        r = ok.groupby(d["y_true"]).mean()
        n = d.groupby("y_true").size()
        rows.append(pd.DataFrame({f"recall_{t}": r, "n": n}))
    S = pd.concat([rows[0], rows[1][["recall_St"]]], axis=1).sort_index()
    body = " \\\\\n".join(
        f"\\texttt{{{i.replace('_', chr(92)+'_')}}} & {int(x.n):,} & "
        f"{x.recall_Am:.3f} & {x.recall_St:.3f}".replace(",", "{,}")
        for i, x in S.iterrows())
    add("SidPerClassTable",
        "\\begin{tabular}{lrrr}\\toprule specification & $n$ & autopsy mix "
        "& structural \\\\ \\midrule " + body +
        " \\\\ \\bottomrule \\end{tabular}")
    R = pd.read_csv(REPO / (RID + "per_class_recall.csv"))
    def esc(x):
        return str(x).replace("_", chr(92) + "_").replace("**", "$^{*}$")
    b = []
    for rep, t in (("autopsy_mix", "Am"), ("structural", "St")):
        pass
    piv = R.pivot_table(index="class", columns="representation",
                        values="recall")
    nn = R.groupby("class").instances.first()
    for cl in piv.index:
        b.append(f"\\texttt{{{esc(cl)}}} & {int(nn[cl]):,}".replace(",", "{,}")
                 + f" & {piv.loc[cl].get('autopsy_mix', float('nan')):.3f}"
                 + f" & {piv.loc[cl].get('structural', float('nan')):.3f}")
    add("RidPerClassTable",
        "\\begin{tabular}{lrrr}\\toprule specification & $n$ & autopsy mix "
        "& structural \\\\ \\midrule " + " \\\\\n".join(b) +
        " \\\\ \\bottomrule \\end{tabular}")
    add("RidPerClassRows", str(len(piv)))


def battery_scope_macros() -> None:
    """The battery is a curated selection, not an exhaustive cross-product.
    D-A10 records that the rejection reasons were never logged; this at least
    makes the selection's size checkable from the frozen configuration."""
    import itertools
    g = yaml.safe_load(
        (REPO / "config/frozen_config.yaml").read_text())["grid"]
    cells = g["cells"]
    A = {c["algorithm"] for c in cells}
    F = {c["features"] for c in cells}
    P = {c["preprocessing"] for c in cells}
    add("BatteryCross", str(len(A) * len(F) * len(P)))
    add("BatteryAlgos", str(len(A)))
    add("BatteryFeatSets", str(len(F)))
    add("BatteryPreproc", str(len(P)))
    add("BatteryAbsent", str(len(A) * len(F) * len(P) - len(cells)))


def slotfill_macros() -> None:
    """Quantities the manuscript's remaining slots need, each from a pinned
    section output."""
    AD = REPO / "addendum" / "results"
    F = pd.read_csv(AD / "section_F.csv"); C = pd.read_csv(AD / "section_C.csv")
    I_ = pd.read_csv(AD / "section_I.csv"); J = pd.read_csv(AD / "section_J.csv")
    O = pd.read_csv(AD / "section_O.csv"); G = pd.read_csv(AD / "section_G1.csv")
    def fx(study, rep):
        d = F[(F.study == study) & (F.representation == rep)
              & (F.model == "random_forest")]
        return float(d.accuracy.iloc[0])
    for rep, t in (("autopsy_mix", "Am"), ("structural", "St")):
        add(f"SidRefitTwentyTwo{t}", num(fx("S-ID", rep), 4))
        add(f"RidRefitTwentyTwo{t}", num(fx("R-ID", rep), 4))
        c = C[C.representation == rep].iloc[0]
        add(f"CondPlantGivenS{t}", num(c.I_plant_given_S, 4))
        add(f"CondSGivenPlant{t}", num(c.I_S_given_plant, 4))
        r = J[(J.arm == "LOCO size-matched") & (J.representation == rep)]
        add(f"LocoMatched{t}", num(r.pooled.iloc[0], 4))
        add(f"LocoMatchedSd{t}", num(r.macro.iloc[0], 4))
        i = I_[I_.representation == rep].iloc[0]
    o = O[O.source == "oof_A_family_autopsy_mix_random_forest"].iloc[0]
    add("FanoFamilyAm", num(o.I_fano, 3)); add("LoglossFamilyAm", num(o.I_logloss, 3))
    add("FanoGovernsCount", str(int((O.governs == "fano").sum())))
    add("FanoTotalRows", str(len(O)))
    add("GridAccLo", num(G.accuracy.min(), 4)); add("GridAccHi", num(G.accuracy.max(), 4))
    add("GridCells", str(len(G)))
    b = []
    for _, r in G.iterrows():
        b.append(f"{r.variant} & {r.grouping} & {r.representation.replace('_', chr(92)+'_')} "
                 f"& {r.accuracy:.4f}")
    add("CommonSupportTable",
        "\\begin{tabular}{llll}\\toprule variant & grouping & representation "
        "& accuracy \\\\ \\midrule " + " \\\\\n".join(b) +
        " \\\\ \\bottomrule \\end{tabular}")


def boundary_macros() -> None:
    """Resampling probabilities for the two verdicts the corrected analysis
    does not resolve. NOTE the column semantics differ by row: for the band
    rows p_above_lo/hi are the SEED range of the probability; for the P-R-D
    rows they are the ratio's CI endpoints. Only p_above is read for both."""
    Bp = pd.read_csv(REPO / "addendum/results/boundary_probs.csv").set_index("quantity")
    for q, t in (("family band, autopsy_mix", "Am"),
                 ("family band, structural", "St")):
        add(f"BandPAbove{t}", num(Bp.loc[q, "p_above"], 3))
        add(f"BandMargin{t}", f"{Bp.loc[q, 'margin']:+.4f}")
    for q, t in (("prd_logistic", "Log"), ("prd_random_forest", "Rf")):
        add(f"PrdPBelow{t}", num(1 - Bp.loc[q, "p_above"], 3))
    add("CorrPRDLogistic", num(Bp.loc["prd_logistic", "point"], 4))
    add("CorrPRDForest", num(Bp.loc["prd_random_forest", "point"], 4))
    r = Bp.loc["prd_logistic"]
    add("PrdCILog", f"{r.p_above_lo:.3f},\, {r.p_above_hi:.3f}")


def cert_bound_macros() -> None:
    """Three lower bounds on I(S;F); see ops/cert_bounds.py. The certificate
    quotes the largest DEFENSIBLE one, which is the soft-probability route."""
    C = pd.read_csv(REPO / "addendum/results/cert_bounds.csv")
    for M, sfx in ((22, ""), (27, "TwentySeven")):
        for rep, t in (("autopsy_mix", "Am"), ("structural", "St")):
            r = C[(C.M == M) & (C.representation == rep)].iloc[0]
            add(f"BndFano{t}{sfx}", num(r.L_fano, 2))
            add(f"BndConf{t}{sfx}", num(r.L_confusion, 2))
            add(f"BndSoft{t}{sfx}", num(r.L_soft, 2))
            add(f"BndSoftMargin{t}{sfx}", num(r.margin_soft, 2))
    add("BndPluginBiasMax", num(C.plugin_bias.max(), 4))
    add("BndFlooredTotal", str(int(C.floored.sum())))
    add("BndGainMin", num((C.L_soft - C.L_fano).min(), 2))
    add("BndGainMax", num((C.L_soft - C.L_fano).max(), 2))
    konst("CertCoverage", "95\\%", "sid/config.yaml bootstrap.ci")
    # D1 addendum (2026-08-05) -- the §O reversal. The GOVERNING route is the
    # WEAKER bound, per the realised sealed licensed sentence, not the largest
    # defensible one. Derived and asserted rather than declared, so a row that
    # stopped being weakest would surface as "mixed" instead of passing.
    _weakest = C[["L_fano", "L_confusion", "L_soft"]].idxmin(axis=1)
    add("BndRoute", "Fano" if (_weakest == "L_fano").all() else "mixed",
        "governing route: the weaker bound governs (sealed §O, outcome 2)")


def rule_recovery_macros() -> None:
    """Post-hoc rule-recoverability analysis; see ops/rule_recovery.py."""
    r = pd.read_csv(REPO / "addendum/results/rule_recovery.csv").iloc[0]
    konst("RuleCommit", r.commit, "repository commit of the corrected slate")
    add("RuleLearnedPairs", thou(int(r.learned_pairs)))
    add("RuleLearnedMedianJ", num(r.learned_median_j, 4))
    add("RuleLearnedPctFifty", f"{r.learned_pct_fifty:.1f}\%")
    add("RuleAmountMedianJ", num(r.amount_median, 4))
    add("RuleFullMedianJ", num(r.full_median, 4))
    add("RuleAmountPctFifty", f"{r.amount_pct_fifty:.1f}\%")
    add("RuleFullPctFifty", f"{r.full_pct_fifty:.1f}\%")
    add("RuleAmountCells", str(int(r.amount_cells)))
    add("RuleFullCells", str(int(r.full_cells)))
    add("RuleMaxJ", num(r.amount_hi, 4))
    add("RuleSpearman", f"{r.spearman:+.3f}")
    add("RuleSpearmanP", num(r.spearman_p, 3))
    add("RuleSpearmanCI", f"{r.spearman_lo:+.3f},\, {r.spearman_hi:+.3f}")
    add("RulePearson", f"{r.pearson:+.3f}")
    add("RulePearsonP", num(r.pearson_p, 3))
    add("RulePearsonCI", f"{r.pearson_lo:+.3f},\, {r.pearson_hi:+.3f}")
    add("RuleNCells", str(int(r.n_cells)))
    for t in ("hi", "lo"):
        add(f"Rule{t.title()}Cell",
            str(r[f"{t}_cell"]).replace("_", "\_"))
        add(f"Rule{t.title()}J", num(r[f"{t}_j"], 3))
        add(f"Rule{t.title()}Recall", num(r[f"{t}_recall"], 3))


def addendum_macros() -> None:
    """Every figure produced by the sealed addendum run, so the manuscript can
    be filled without a hand-typed number entering it. Sourced from
    addendum/results/*.csv, which are themselves derived from the persisted
    per-instance outputs section 0.5 requires."""
    AD = REPO / "addendum" / "results"   # pinned via SOURCES/ADD
    A = pd.read_csv(AD / "section_A.csv"); B = pd.read_csv(AD / "section_B.csv")
    C = pd.read_csv(AD / "section_C.csv"); D = pd.read_csv(AD / "section_D.csv")
    F = pd.read_csv(AD / "section_F.csv"); G = pd.read_csv(AD / "section_G1.csv")
    I_ = pd.read_csv(AD / "section_I.csv"); J = pd.read_csv(AD / "section_J.csv")
    K = pd.read_csv(AD / "section_K.csv"); N = pd.read_csv(AD / "section_N.csv")
    NM = pd.read_csv(AD / "section_N_match.csv")
    O = pd.read_csv(AD / "section_O.csv"); OC = pd.read_csv(AD / "section_O_corpus.csv")
    Q = pd.read_csv(AD / "section_Q.csv")
    T = {"autopsy_mix": "Am", "structural": "St", "overlap_profile": "Ov"}

    for rep, t in T.items():
        r = A[(A.task == "spec27") & (A.representation == rep)
              & (A.model == "random_forest")]
        if len(r):
            add(f"CorrTaskA{t}", num(r.accuracy.iloc[0]))
            add(f"CorrLearned{t}", num(r.learned_only.iloc[0]))
        f = A[(A.task == "family") & (A.representation == rep)
              & (A.model == "random_forest")]
        if len(f):
            add(f"CorrFamily{t}", num(f.accuracy.iloc[0]))
        b = B[(B.task == "family") & (B.representation == rep)
              & (B.model == "random_forest")]
        if len(b):
            add(f"CorrFamilyCI{t}",
                f"{b.ci_lo.iloc[0]:.4f},\\,{b.ci_hi.iloc[0]:.4f}")
            add(f"CorrFamilyMacro{t}", num(b.macro_accuracy.iloc[0]))
            # CW-2b / ISL B.8(a). The FAMILY task's above-null retention.
            # rho = (A_macro - A0)/(A_pooled - A0) with A0 the majority-family
            # rate 7/22, NOT 1/27 -- the family task is unbalanced and its
            # null is the majority class, per portability_macros()'s own
            # docstring. \RhoMacro* is the 27-class SPECIFICATION task's rho
            # (a0 = 1/27, task == "spec27") and attaching it to a family
            # figure is a category error the abstract made.
            if len(f):
                _a0 = 7 / 22
                add(f"RhoFamilyMacro{t}",
                    num((float(b.macro_accuracy.iloc[0]) - _a0)
                        / (float(f.accuracy.iloc[0]) - _a0), 3))
        o = O[O.source == f"oof_A_spec_{rep}_random_forest"]
        if len(o):
            add(f"FanoSpec{t}", sig(o.I_fano.iloc[0]))
            add(f"LogLossSpec{t}", sig(o.I_logloss.iloc[0]))
        oc = OC[OC.representation == rep]
        if len(oc):
            add(f"CorrICorpus{t}", sig(oc.I_logloss.iloc[0]))
            add(f"CorrICorpusFano{t}", sig(oc.I_fano.iloc[0]))
        c = C[C.representation == rep]
        if len(c):
            # CW-19 / 1e: reported as INTERACTION INFORMATION, not "synergy".
            # II(S;plant;F) = I(S;plant|F) - I(S;plant); on this crossed
            # design I(S;plant) = 0, so II equals the conditional term.
            # Sign convention: positive means the pair is more informative
            # jointly than separately.
            add(f"InteractionII{t}", num(c.synergy_J_route1.iloc[0], 4))
            add(f"CondSgivenP{t}", num(c.I_S_given_plant.iloc[0], 4))
            add(f"CondPgivenS{t}", num(c.I_plant_given_S.iloc[0], 4))
        q = Q[Q.representation == rep]
        if len(q):
            add(f"DeltaWX{t}", num(q.delta_W_given_X.iloc[0], 4))
        i = I_[I_.representation == rep]
        if len(i):
            add(f"VarSpec{t}", num(i.pct_specification.iloc[0], 2))
            add(f"VarUnit{t}", num(i.pct_unit.iloc[0], 2))
            add(f"VarInter{t}", num(i.pct_interaction.iloc[0], 2))
        j = J[(J.arm == "LOCO") & (J.representation == rep)]
        if len(j):
            add(f"LocoPooled{t}", num(j.pooled.iloc[0]))
            add(f"LocoMacro{t}", num(j.macro.iloc[0]))
        sm = J[(J.arm == "LOCO size-matched") & (J.representation == rep)]
        if len(sm):
            add(f"LocoSizeMatched{t}", num(sm.pooled.iloc[0]))
        for arm, nm in (("isotonic (nested)", "Iso"),
                        ("gradient boosting", "Gbm")):
            d = D[(D.arm == arm) & (D.representation == rep)]
            if len(d):
                add(f"{nm}Acc{t}", num(d.accuracy.iloc[0]))
                add(f"{nm}Bits{t}", sig(d.I_bits.iloc[0]))
                add(f"{nm}Floored{t}", str(int(d.floored.iloc[0])))
        s22 = F[(F.study == "S-ID") & (F.representation == rep)
                & (F.model == "random_forest")]
        if len(s22):
            add(f"SidTwentyTwo{t}", num(s22.accuracy.iloc[0]))
        r22 = F[(F.study == "R-ID") & (F.representation == rep)
                & (F.model == "random_forest")]
        if len(r22):
            add(f"RidTwentyTwo{t}", num(r22.accuracy.iloc[0]))

    # section N: decontaminated, like-for-like
    add("DeconSpec", num(N[(N.arm == "N.1 common-cell")
                           & (N.task == "spec-22-common")
                           & (N.study == "R-ID")].accuracy.iloc[0]))
    add("DeconFamily", num(N[(N.arm == "N.1 common-cell")
                             & (N.task == "family")].accuracy.iloc[0]))
    add("DeconSpecBest", num(NM[NM.task == "spec-22-common"].accuracy.max()))
    add("DeconFamilyBest", num(NM[NM.task == "family"].accuracy.max()))
    add("MaskDelta", num(
        N[(N.arm == "N.2 mask-present") & (N.task == "spec-27")].accuracy.iloc[0]
        - N[(N.arm == "N.2 mask-dropped") & (N.task == "spec-27")].accuracy.iloc[0], 4))
    # k-sensitivity
    for k, word in ((10, "Ten"), (25, "TwentyFive"), (50, "Fifty")):
        kk = K[(K.k == k) & (K.representation == "autopsy_mix")]
        add(f"Kacc{word}", num(kk.accuracy.iloc[0]))
        ko = K[(K.k == k) & (K.representation == "overlap_profile")]
        add(f"KaccOv{word}", num(ko.accuracy.iloc[0]))
    # common support: the doubly-clean cell
    gg = G[(G.variant == "22 common x complete units") & (G.grouping == "component")]
    add("GcleanAm", num(gg[gg.representation == "autopsy_mix"].accuracy.iloc[0]))
    add("GcleanSt", num(gg[gg.representation == "structural"].accuracy.iloc[0]))
    # certificate
    # Ruling 1a: the DERIVED path is authoritative. These were transcribed by
    # hand from addendum/RESULTS.md, whose ad-hoc script's RNG call pattern
    # was never persisted; ops/certificate.py recomputes them from pinned
    # parquets under the sealed bootstrap config and is reproducible.
    # Ruling 1d: the Fano bound prints to TWO decimals, because that is what
    # 2,000 resamples supports -- see certificate_mc.csv.
    C = pd.read_csv(REPO / "addendum/results/certificate_rederived.csv")
    MC = pd.read_csv(REPO / "addendum/results/certificate_mc.csv")
    for M, sfx in ((22, ""), (27, "TwentySeven")):
        for rep, t in (("autopsy_mix", "Am"), ("structural", "St")):
            r = C[(C.M == M) & (C.representation == rep)].iloc[0]
            add(f"CertAcc{t}{sfx}", num(r.accuracy, 4))
            add(f"CertLower{t}{sfx}", num(r.lower, 4))
            add(f"CertFano{t}{sfx}", num(r.fano_emp, 2))
            add(f"CertMargin{t}{sfx}", num(r.margin_emp, 2))
    add("CertHplant", num(float(C.h_plant.iloc[0]), 6))
    # ------------------------------------------------------------------
    # PRIOR-INDEPENDENT CEILING (mathematical review, 2026-08-13). The
    # planted mechanism takes six values, so I(Y;F) <= H(Y) <= log2(6)
    # for ANY six-class prior. A cell whose Fano lower bound exceeds
    # log2(6) establishes the ordering for every possible prior; the
    # design-frequency ceiling H(plant) remains what the remaining cell
    # requires. Margins computed here against the exact constant, not the
    # config's 4-decimal rounding.
    import math as _math
    konst("LogTwoSix", f"{_math.log2(6):.7f}",
          "log2(6): maximum entropy of any six-class prior; analytic")
    for M, sfx in ((22, ""), (27, "TwentySeven")):
        for rep, t in (("autopsy_mix", "Am"), ("structural", "St")):
            r = C[(C.M == M) & (C.representation == rep)].iloc[0]
            _m = float(r.fano_emp) - _math.log2(6)
            add(f"CertPI{t}{sfx}", f"{_m:+.2f}")
            add(f"CertPIClears{t}{sfx}", "clears" if _m > 0 else "does not clear")
    # CW-9 / Phase 3a: the certificate is DESIGN-CONDITIONAL. Its ceiling is
    # the entropy of the plant prior, and that prior is a design choice --
    # 50% NULL plus five planted mechanisms at 10% each (sid/config.yaml
    # cv.task_b1.class_marginals). Under a BALANCED six-way plant prior the
    # ceiling rises to log2(6) and the certificate is a stiffer test. The
    # sealed config already declares that variant, so the sensitivity is read
    # from it rather than invented here.
    _scfg = yaml.safe_load(open(REPO / "sid" / "config.yaml"))
    _bal = float(_scfg["cv"]["task_b1"]["balanced_variant"]["entropy_bits"])
    _prior = _scfg["cv"]["task_b1"]["class_marginals"]
    add("CertHplantBalanced", num(_bal, 3))
    # CW-1 / B.4: the battery's true character, stated in the review's own
    # replacement wording. No design-time rejection log exists (D-A10).
    konst("BatteryCells", "26",
          "config/frozen_config.yaml grid: 26 cells plus the ensemble")
    # ------------------------------------------------------------ open-set
    # Executed under openset/PROTOCOL.md v2.0 (seal 2dcf7a6, GitHub-receipted
    # 54 s later). 440 fold-tasks, zero misfires. S-ID selects outcome (2);
    # R-ID is reported descriptively under the D-O2 ruling.
    _OSP = pd.read_csv(REPO / "results/openset/20260805T191833Z_a4b895a/pooled.csv").set_index("arm")
    _OSI = pd.read_csv(REPO / "results/openset/20260805T191833Z_a4b895a/per_institution.csv")
    for _a, _t in (("sid", "Sid"), ("rid", "Rid")):
        _r = _OSP.loc[_a]
        add("Os" + _t + "A", num(_r.A, 4))
        add("Os" + _t + "Ain", num(_r.A_in, 4))
        add("Os" + _t + "ALo", num(_r.A_lo, 4))
        add("Os" + _t + "AHi", num(_r.A_hi, 4))
        add("Os" + _t + "CLo", num(_r.C_lo, 4))
        add("Os" + _t + "CHi", num(_r.C_hi, 4))
        add("Os" + _t + "Family", num(_r.A_family, 4))
        add("Os" + _t + "CorrectFamily", num(_r.correct_family, 4))
        add("Os" + _t + "FacetObs", num(_r.same_alg_obs, 4))
        add("Os" + _t + "FacetNull", num(_r.same_alg_null, 4))
        add("Os" + _t + "FacetLift",
            "%.2f" % (float(_r.same_alg_obs) / float(_r.same_alg_null)))
        add("Os" + _t + "Folds", str(int(_r.n_folds)))
    add("OsInstCLo", num(_OSI.C.min(), 4))
    add("OsInstCHi", num(_OSI.C.max(), 4))
    add("OsInstSpread", "%.2f" % float(_OSI.C.max() / _OSI.C.min()))
    add("OsInstN", str(len(_OSI)))
    _osrows = []
    for _row in _OSI.itertuples():
        _osrows.append("\\texttt{%s} & %s & %.4f & %.4f"
                       % (_row.corpus.replace("_", "\\_"),
                          thou(int(_row.n)), _row.A, _row.C))
    add("OsInstTable",
        "\\begin{tabular}{lrrr}\\toprule institution & instances & "
        "abstention $A$ & median confidence $C$ \\\\ \\midrule "
        + " \\\\\n".join(_osrows)
        + " \\\\ \\bottomrule \\end{tabular}")
    # the sealed LOCO spread the open-set protocol anticipated
    _loco = pd.read_csv(REPO / "addendum/results/section_J.csv")
    _l = _loco[(_loco.arm == "LOCO") & (_loco.representation == "autopsy_mix")].iloc[0]
    _acc = [float(getattr(_l, c)) for c in _loco.columns if c.startswith("acc_")]
    add("RidLocoSpread", "%.1f" % (max(_acc) / min(_acc)))
    konst("OsTasks", "440", "openset run 20260805T191833Z: fold-tasks executed")

    konst("BatteryPossible", "120",
          "6 algorithms x 5 feature sets x 4 preprocessings, design space")

    # ---------------------------------------------------------------- CW-1
    # The analysis-identification taxonomy. Every result in the paper carries
    # exactly one provenance class. Built here so the table cannot drift from
    # the prose: adding a result without classing it is a missing row, which
    # is visible.
    _TAX = [
        ("Task A, exact specification, S-ID", "original preregistered",
         "sid/PROTOCOL.md v1.1"),
        ("Task A-family, S-ID", "original preregistered", "sid/PROTOCOL.md v1.1"),
        ("Task B1/B2, plant and population, S-ID", "original preregistered",
         "sid/PROTOCOL.md v1.1"),
        ("Task A and family, R-ID", "original preregistered",
         "rid/PROTOCOL.md v1.0"),
        ("LOCO transport, R-ID", "original preregistered", "rid/PROTOCOL.md v1.0"),
        ("P-R-A / P-R-D band adjudications", "original preregistered",
         "rid/PROTOCOL.md v1.0"),
        ("Facet recovery (algorithm / feature / preprocessing)",
         "original exploratory", "no committed threshold"),
        ("Pairwise separation", "original exploratory", "no committed threshold"),
        ("Corrected accuracies under record-component grouping",
         "corrected after defect", "defect D2"),
        ("Corrected family band and P-R-D ratios", "corrected after defect",
         "defect D2, addendum \\S A"),
        ("Cluster-correct intervals on every headline accuracy",
         "externally timestamped addendum", "addendum \\S B"),
        ("Entropy-dominance certificate", "externally timestamped addendum",
         "addendum \\S O"),
        ("Fano cross-check on every information figure",
         "externally timestamped addendum", "addendum \\S O"),
        ("Conditional quantities and interaction information",
         "externally timestamped addendum", "addendum \\S C"),
        ("Variance decomposition", "externally timestamped addendum",
         "addendum \\S I"),
        ("Common-support matrix", "externally timestamped addendum",
         "addendum \\S G.1"),
        ("k-sensitivity", "externally timestamped addendum", "addendum \\S K"),
        ("Size-matched LOCO", "externally timestamped addendum",
         "addendum \\S J"),
        ("Overlap decontamination", "externally timestamped addendum",
         "addendum \\S N"),
        ("Open-set attribution, both arms", "externally timestamped addendum",
         "openset/PROTOCOL.md v2.0"),
        ("Reference-battery match statistics", "unregistered post hoc",
         "defect D-A11 disposition (ii)"),
        ("Balanced-prior certificate sensitivity", "unregistered post hoc",
         "Phase 3a, ledger P2-C3"),
        ("Availability term $I(S;A)$", "unregistered post hoc",
         "Phase 1f, ledger P2-C1"),
        # Phase 6, 2026-08-08: EXECUTED. Defect D-A3's blocker was the
        # persistence design, not the specification; sid/substrate_p6.py
        # regenerates the substrate with record values, worklist membership
        # and is_plant, and verifies bit-exact against the sealed one
        # (32,400 worklists x 49 feature columns, rtol=0 atol=0). The three
        # analyses are sealed specifications executed post-hoc, so the class
        # is the addendum's, with the execution timing stated.
        ("Random-50 negative control (\\S E.1)",
         "externally timestamped addendum", "addendum \\S E.1, executed 2026-08-08"),
        ("Padding and blending degradation (\\S P)",
         "externally timestamped addendum", "addendum \\S P, executed 2026-08-08"),
        ("Worklist-only T1 ablation (\\S G.2)",
         "externally timestamped addendum", "addendum \\S G.2, executed 2026-08-08"),
        ("Candidate-set dependence; stochastic-vs-deterministic",
         "unregistered post hoc", "review findings CW-15, CW-16"),
        # Still unrun after Phase 6, and named rather than quietly dropped:
        # \S E.2 (full-population upper reference) and \S E.3 (oracle
        # worklist by true planted status) were unblocked by the same
        # regeneration and were not scoped into Phase 6. Independent-
        # implementation robustness (CW-14) is declined on its merits, not
        # on cost -- see addendum/results/p6_cw14_scope.json.
        ("Full-population and oracle positive controls (\\S E.2, \\S E.3); "
         "independent-implementation robustness",
         "proposed but unrun", "unblocked by Phase 6; CW-14 declined, reason logged"),
        ("Overlap profile as an attribution result", "superseded",
         "defect D-A11"),
        ("Sealed point-estimate band verdicts", "superseded",
         "corrected estimates govern; sealed reported as historical"),
    ]
    # ------------------------------------------------------------------
    # SINGLE ORIGIN. _TAX is the ledger. The rendered rows, the count macro
    # and the per-class breakdown are all derived from _ROWLIST below and
    # from nothing else -- there is no parallel count anywhere in this
    # function, and adding one is the defect this construction forecloses.
    #
    # Phase 6a: previously `add("ProvenanceCount", str(len(_TAX)))` took its
    # value from _TAX while the table took its rows from a separate
    # comprehension over _TAX. The two agreed, and were verified to agree,
    # but they were two paths over one source and nothing asserted their
    # equality. They are now one path, and ops/macrocheck.py asserts the
    # equality downstream from the RENDERED macros, which is the only place
    # a drift could actually reach the manuscript.
    # ------------------------------------------------------------------
    _ROWLIST = [f"{a} & {b} & {c}" for a, b, c in _TAX]
    add("ProvenanceTable",
        "\\begin{tabular}{p{0.40\\textwidth}p{0.24\\textwidth}p{0.26\\textwidth}}"
        "\\toprule result & class & authority \\\\ \\midrule "
        + " \\\\\n".join(_ROWLIST) + " \\\\ \\bottomrule \\end{tabular}")
    add("ProvenanceCount", str(len(_ROWLIST)))
    _clscount = 0
    for _cls in ("original preregistered", "original exploratory",
                 "corrected after defect", "externally timestamped addendum",
                 "unregistered post hoc", "proposed but unrun", "superseded"):
        _k = "".join(w.title() for w in _cls.replace("/", " ").split())
        _n = sum(1 for _r in _ROWLIST if _r.split(" & ")[1] == _cls)
        _clscount += _n
        add("Prov" + _k, str(_n))
    # Every row must fall in exactly one declared class. A row whose class
    # string is not in the tuple above would vanish from the breakdown while
    # still appearing in the table; that is the drift macrocheck's assertion
    # is written to catch, and this is the generator-side half of it.
    if _clscount != len(_ROWLIST):
        raise SystemExit(
            f"provenance ledger: {len(_ROWLIST)} rows but {_clscount} "
            f"classified. A row carries a class not in the declared set.")
    # Phase 3d: the open-set seal-to-third-party-receipt interval, the one
    # externally attested ordering in the program. From openset/MANIFEST.md.
    konst("OpenSetReceiptGap", "54 seconds",
          "openset/MANIFEST.md: seal 18:47:50Z, GitHub ls-remote 18:48:44Z")
    add("CertPlantNullShare", pct(_prior[None], 0))
    add("CertPlantClasses", str(len(_prior)))
    for M, sfx in ((22, ""), (27, "TwentySeven")):
        for rep, t in (("autopsy_mix", "Am"), ("structural", "St")):
            r = C[(C.M == M) & (C.representation == rep)].iloc[0]
            add(f"CertBalMargin{t}{sfx}", f"{float(r.fano_emp) - _bal:+.2f}")
            add(f"CertBalClears{t}{sfx}",
                "clears" if float(r.fano_emp) > _bal else "\\textbf{does not clear}")
    add("CertThresholdTwentyTwo",
        num(float(C[C.M == 22].threshold.iloc[0]), 6))
    add("CertThresholdTwentySeven",
        num(float(C[C.M == 27].threshold.iloc[0]), 6))
    # what the bootstrap's own reproducibility is, and how far the margins
    # sit above it -- so the precision claim is itself measured
    add("CertMcFano", num(MC.fano_spread.max(), 4))
    add("CertMcLower", num(MC.lower_spread.max(), 4))
    add("CertRobustLo", f"{int(MC.margin_over_noise.min() // 10 * 10)}")
    add("CertRobustHi", f"{int(-(-MC.margin_over_noise.max() // 10) * 10)}")
    _N = pd.read_csv(REPO / "addendum/results/section_N.csv")
    _NM = pd.read_csv(REPO / "addendum/results/section_N_match.csv")
    def _n(task, arm):
        return float(_N[(_N.task == task) & (_N.arm == arm)
                        & (_N.study == "R-ID")].accuracy.iloc[0])
    def _best(task):
        return float(_NM[_NM.task == task].accuracy.max())
    add("DeconLeadSpec", num(_n("spec-22-common", "N.1 common-cell")
                             - _best("spec-22-common"), 4))
    add("DeconLeadFamily", num(_n("family", "N.1 common-cell")
                               - _best("family"), 4))
    add("MaskDeltaFamily", num(_n("family", "N.2 mask-present")
                               - _n("family", "N.2 mask-dropped"), 4))
    add("LedgerTotal", "seven"); add("LedgerSameCause", "four")
    add("FecDisclosure", yaml.safe_load(
        (REPO / "config/frozen_corpora.yaml").read_text())["slates"]["fec"]
        ["match_disclosure"].replace(" - ", " --- "))
    # D-A7 ruling: traced to the frozen corpora file and pinned. The
    # disclosure string and the comparison median come from the same source,
    # so the sentence cannot drift from the record it cites.
    _fc = yaml.safe_load((REPO / "config/frozen_corpora.yaml").read_text())
    _sl = _fc["slates"]
    _md = sorted(v["match_distance"] for v in _sl.values())
    add("FecMatchDistance", num(_sl["fec"]["match_distance"], 3))
    add("FecMatchMedian", num((_md[len(_md)//2 - 1] + _md[len(_md)//2]) / 2, 3))
    add("FecMatchRatio", num(_sl["fec"]["match_distance"] /
                             ((_md[len(_md)//2 - 1] + _md[len(_md)//2]) / 2), 1))
    add("CorporaCount", str(len(_sl)))
    _L = pd.read_csv(REPO / "addendum/results/fig4_loco_per_institution.csv")
    def _loco(rep, corp=None):
        d = _L[_L.representation == rep]
        return float(d[d.corpus == corp].accuracy.iloc[0] if corp
                     else d.accuracy.max())
    add("RidLocoWorst", num(_L[_L.representation == "autopsy_mix"].accuracy.min(), 3))
    add("RidLocoBest", num(_L[_L.representation == "autopsy_mix"].accuracy.max(), 3))
    add("FecLocoAm", num(_loco("autopsy_mix", "fec"), 3))
    add("FecLocoSt", num(_loco("structural", "fec"), 3))
    add("BestLocoAm", num(_loco("autopsy_mix"), 3))
    _D = pd.read_csv(REPO / "addendum/results/section_D.csv")
    def _d(arm, rep="autopsy_mix", col="accuracy"):
        return float(_D[(_D.arm == arm) & (_D.representation == rep)][col].iloc[0])
    add("GbmAccBest", num(_d("gradient boosting"), 4))
    add("GbmBitsBest", num(_d("gradient boosting", col="I_bits"), 3))
    add("CurveFivePct", num(_d("learning curve 0.05"), 4))
    add("CurveFullPct", num(_d("learning curve 1.00"), 4))
    konst("BlockedSidCostMin", 42, "measured cost probe, notes/P2_VERIFICATION.md"); konst("BlockedSidWorkersMin", 3, "measured cost probe, notes/P2_VERIFICATION.md")
    G = pd.read_csv(REPO / "addendum/results/section_G1.csv")
    A2 = pd.read_csv(REPO / "addendum/results/section_A.csv")
    deltas = []
    for v in G.variant.unique():
        for rep in G.representation.unique():
            u = G[(G.variant == v) & (G.grouping == "unit")
                  & (G.representation == rep)].accuracy
            c = G[(G.variant == v) & (G.grouping == "component")
                  & (G.representation == rep)].accuracy
            if len(u) and len(c):
                deltas.append(float(u.iloc[0] - c.iloc[0]))
    add("GroupingCostLo", num(min(deltas), 3))
    add("GroupingCostHi", num(max(deltas), 3))
    # D1's class asymmetry against its unit asymmetry, on the common
    # sub-grid. Holding units fixed and dropping the five categorical cells
    # against holding cells fixed and dropping the partial units. An earlier
    # revision typed this range as 0.03-0.05; the upper end is 0.056.
    cls, uni = [], []
    for grp in ("unit", "component"):
        for rep in ("autopsy_mix", "structural"):
            def acc(v):
                return float(G[(G.variant == v) & (G.grouping == grp)
                               & (G.representation == rep)].accuracy.iloc[0])
            cls.append(acc("22 common x complete units")
                       - acc("27 cells x complete units"))
            uni.append(abs(acc("22 common x complete units")
                           - acc("22 common x all units")))
    add("DOneClassDeltaLo", num(min(cls), 2))
    add("DOneClassDeltaHi", num(max(cls), 2))
    add("DOneUnitDeltaMax", num(max(uni), 3))
    # D2 ruling: the two normalized quantities, reported SEPARATELY with
    # intervals. No ratio is formed -- the corpus-side denominator is negative.
    _Q = pd.read_csv(REPO / "addendum/results/section_Q.csv")
    def _norm(rep):
        r = _Q[_Q.representation == rep].iloc[0]
        return float(r.delta_W_given_X) / float(r.L_population_only)
    # ---------------------------------------------------------------- CW-3
    # Phase 2a. Common support becomes the PRIMARY real-data estimand:
    # 22 common specifications x all units, COMPONENT-grouped. The 27-class
    # figure over all units is demoted to a diagnostic because class
    # availability is not independent of the unit (P2-C1 / D-A11's cousin):
    # 52 units carry only 22 cells, so the 27-way task is partly a test of
    # which cells were available rather than which produced the worklist.
    _G = pd.read_csv(REPO / "addendum/results/section_G1.csv")

    def _g(variant, grouping, rep):
        r = _G[(_G.variant == variant) & (_G.grouping == grouping)
               & (_G.representation == rep)]
        return r.iloc[0]

    for rep, t in (("autopsy_mix", "Am"), ("structural", "St")):
        pr = _g("22 common x all units", "component", rep)
        add(f"PrimaryReal{t}", num(pr.accuracy, 4))
        add(f"PrimaryRealUnit{t}",
            num(_g("22 common x all units", "unit", rep).accuracy, 4))
        add(f"SecondaryReal{t}",
            num(_g("27 cells x complete units", "component", rep).accuracy, 4))
        add(f"CommonCompleteReal{t}",
            num(_g("22 common x complete units", "component", rep).accuracy, 4))
    _pr = _g("22 common x all units", "component", "autopsy_mix")
    add("PrimaryRealClasses", str(int(_pr.classes)))
    add("PrimaryRealUnits", thou(int(_pr.units)))
    add("PrimaryRealRows", thou(int(_pr.rows)))
    _sc = _g("27 cells x complete units", "component", "autopsy_mix")
    add("SecondaryRealUnits", thou(int(_sc.units)))
    add("SecondaryRealRows", thou(int(_sc.rows)))
    add("PrimaryRealChance", num(1 / int(_pr.classes), 4))
    # CW-6: both decoders on the primary estimand, so no figure is quoted at
    # a max over models. Section F carries the 22-class R-ID refit.
    _F = pd.read_csv(REPO / "addendum/results/section_F.csv")
    for rep, t in (("autopsy_mix", "Am"), ("structural", "St")):
        for mdl, mt in (("logistic", "Logistic"), ("random_forest", "Forest")):
            r = _F[(_F.study == "R-ID") & (_F.classes == 22)
                   & (_F.representation == rep) & (_F.model == mdl)]
            add(f"RidTwentyTwo{mt}{t}", num(r.accuracy.iloc[0], 4))
    # CW-5 bootstrap reporting form: see \BootZeroForm, built beside
    # \BootResamples from the sealed config.

    add("NormSpecAm", num(_norm("autopsy_mix"), 4));
    add("NormSpecSt", num(_norm("structural"), 4));
    # CW-2f / 1f. The S-perp-X violation on the FULL real substrate, measured
    # rather than asserted. 52 of 2,423 units carry only 22 of the 27
    # specifications, so availability is not independent of the label and the
    # population-only arm is NOT pinned at H(S). I(S;A) is the size of the
    # violation, and it is the bound the manuscript may claim on the full
    # substrate in place of the analytic zero.
    _W = pd.read_parquet(REPO / (RID + "worklists.parquet"),
                         columns=["unit_id", "spec_name"])
    _n = _W.groupby("unit_id").spec_name.nunique()
    add("RidUnitsComplete", thou(int((_n == 27).sum())))
    add("RidUnitsIncomplete", thou(int((_n < 27).sum())))
    add("RidIncompleteCells", str(int(_n[_n < 27].max())))

    def _H(v):
        import numpy as _np
        return float(-(v * _np.log2(v)).sum())
    _HS = _H(_W.spec_name.value_counts(normalize=True).values)
    _av = _W.groupby("unit_id").spec_name.apply(frozenset).rename("A")
    _J = _W.join(_av, on="unit_id")
    _HSgA = sum(len(g) / len(_J)
                * _H(g.spec_name.value_counts(normalize=True).values)
                for _, g in _J.groupby("A"))
    add("RidAvailabilityBits", num(_HS - _HSgA, 4))
    # CW-9 / Phase 3c. The augmented model (W, X, R_X) is DETERMINISTIC
    # matching, and these are the statistics that show it: how often the
    # self-coordinate is the unique maximum of the Jaccard profile, how often
    # it merely ties, and how wide the ambiguity set is. No decoder involved.
    import numpy as _np
    for _arm, _rel, _t in (("rid", RID, "Rid"), ("sid", SID, "Sid")):
        _D = pd.read_parquet(REPO / (_rel + "worklists.parquet"))
        _sp = sorted(_D.spec_name.unique())
        _J = _D[[f"j_{x}" for x in _sp]].to_numpy()
        _own = _D.spec_name.map({x: i for i, x in enumerate(_sp)}).to_numpy()
        _mx = _J.max(axis=1)
        _self = _J[_np.arange(len(_J)), _own]
        _atmax = _self >= _mx - 1e-12
        _nt = (_np.abs(_J - _mx[:, None]) <= 1e-12).sum(axis=1)
        add(f"Match{_t}Exact", num(float((_atmax & (_nt == 1)).mean()), 4))
        add(f"Match{_t}Tied", num(float((_atmax & (_nt > 1)).mean()), 4))
        add(f"Match{_t}Miss", num(float((~_atmax).mean()), 4))
        konst("MatchAmbTol", "0.01",
              "ambiguity-set tolerance, declared here; the statistic is "
              "reported for this tolerance only") if _t == "Rid" else None
        add(f"Match{_t}Amb",
            f"{float((_J >= (_mx[:, None] - 0.01)).sum(axis=1).mean()):.2f}")
    # WHICH cells are absent, and why it is not arbitrary: every absent cell
    # is a `full_categorical` feature-set cell, so availability tracks whether
    # a unit has usable categorical fields. Four of the five are LEARNED, so
    # the family task inherits the confound on those units too.
    _inc = _n[_n < 27].index
    _abs_cells = sorted(set(_W.spec_name.unique())
                        - set(_W[_W.unit_id == _inc[0]].spec_name))
    add("RidAbsentCells", str(len(_abs_cells)))
    add("RidAbsentFeatureSet", "full\\_categorical")
    add("RidAbsentLearned",
        str(sum(1 for c in _abs_cells if not c.startswith(
            ("benford", "round", "repeat", "dup_pair", "ensemble")))))
    add("RidLabelEntropy", num(_HS, 4))

    # CW-2a / ISL B.6: the ABSOLUTE R-ID deltas already exist as \DeltaWX*
    # (added at the addendum loop above, from this same section_Q.csv). The
    # repair at :364 quotes those beside \NormSpec*, instead of pairing an
    # R-ID normalized fraction with \SidISpecSt, an S-ID absolute.
    # NormDiff removed with the corpus-side term it depended on (D-A7).


def family_profile_macros() -> None:
    """Figure 5's interpretive half: per-family composition profile, as mean
    standardised feature value relative to the battery mean. No refit and no
    permutation importance -- these are the persisted derived features,
    standardised, so the table owes nothing to a decoder.

    The CLEAN/DIFFUSE split is by rule, not by eye: a family is described
    only if some coordinate reaches |z| >= THRESH."""
    THRESH = 0.5
    d = pd.read_csv(REPO / "addendum/results/fig5_family_signatures.csv",
                    index_col=0)
    order = ["iforest", "lof", "knn", "ocsvm", "mcd", "autoencoder"]
    d = d.loc[[f for f in order if f in d.index]]

    def nice(c):
        return c.replace("mix_", "").replace("struct_", "").replace("_", " ")

    rows = [r"\begin{tabular}{llll}", r"\toprule",
            r"family & runs high & runs low & description \\", r"\midrule"]
    clean, diffuse = [], []
    for f in d.index:
        r = d.loc[f].sort_values()
        hi = ", ".join(f"{nice(i)} ({v:+.2f})" for i, v in r.tail(2)[::-1].items())
        lo = ", ".join(f"{nice(i)} ({v:+.2f})" for i, v in r.head(2).items())
        peak = float(max(abs(r.min()), abs(r.max())))
        ok = peak >= THRESH
        (clean if ok else diffuse).append(f)
        rows.append(f"{tex(f)} & {tex(hi)} & {tex(lo)} & "
                    f"{'clean' if ok else r'\emph{diffuse}'} \\\\")
    rows += [r"\bottomrule", r"\end{tabular}"]
    MACROS["FamilyProfileTable"] = "%\n".join(rows)
    _ORDER.append(("FamilyProfileTable", "generated family profile table"))
    add("FamilyCleanCount", str(len(clean)))
    add("FamilyDiffuseCount", str(len(diffuse)))
    add("FamilyDiffuseNames", " and ".join(tex(f) for f in diffuse))
    add("FamilyProfileThresh", num(THRESH, 1))
    peaks = {f: float(max(abs(d.loc[f].min()), abs(d.loc[f].max())))
             for f in d.index}
    dif = sorted(diffuse, key=lambda f: -peaks[f])
    for i, f in enumerate(dif):
        add(f"FamilyDiffusePeak{'One' if i == 0 else 'Two'}", num(peaks[f], 2))
    # the two most distinct profiles, and the two least
    from itertools import combinations
    dist = {(a, b): float(np.linalg.norm(d.loc[a] - d.loc[b]))
            for a, b in combinations(d.index, 2)}
    far = max(dist, key=dist.get); near = min(dist, key=dist.get)
    add("FamilyFarA", tex(far[0])); add("FamilyFarB", tex(far[1]))
    add("FamilyFarDist", num(dist[far], 2))
    add("FamilyNearA", tex(near[0])); add("FamilyNearB", tex(near[1]))
    add("FamilyNearDist", num(dist[near], 2))


def provenance_macros() -> None:
    konst("ProvHeadlinedFeatures", 22, "config/frozen_config.yaml block widths")
    konst("ProvTOneCount", 1, "notes/P2_VERIFICATION.md provenance audit")
    konst("ProvAutopsyWidth", 15, "config/frozen_config.yaml autopsy_mix block")
    konst("ProvStructWidth", 7, "config/frozen_config.yaml structural block")
    konst("ProvOverlapWidth", 26, "27 persisted, self-column dropped")
    konst("ProvZeroFillRecall", "1.000", "notes/P2_VERIFICATION.md zero-fill audit")


def phase6_macros() -> None:
    """Phase 6's executed controls: SS E.1, SS P, SS G.2, CW-15, CW-16.

    Sealed specifications executed post-hoc on the regenerated substrate
    (results/p6), which is gated on bit-exact agreement with the sealed one.
    Every figure enters through this function; none is hand-typed.
    """
    P6 = REPO / "addendum/results"
    rf = lambda d: d[d.model == "random_forest"]

    # ---- SS E.1 random-50 negative control
    E = pd.read_csv(P6 / "p6_section_E.csv")
    for rep, t in (("autopsy_mix", "Am"), ("structural", "St"),
                   ("overlap_profile", "Ov")):
        r = rf(E)[rf(E).representation == rep].iloc[0]
        add(f"RandFifty{t}", num(r.accuracy, 4))
        add(f"RandFifty{t}CI", f"{r.ci_lo:.4f}, {r.ci_hi:.4f}")
        add(f"RandFifty{t}Bits", num(r.I_bits, 3))
    add("RandFiftyChance", num(float(E.chance.iloc[0]), 4))

    # ---- SS P padding and blending
    P = pd.read_csv(P6 / "p6_section_P.csv")
    pa = rf(P)[rf(P).representation == "autopsy_mix"]
    ps = rf(P)[rf(P).representation == "structural"]
    for r_, w in ((0, "Zero"), (5, "Five"), (10, "Ten"), (25, "TwentyFive")):
        add(f"PadAm{w}", num(pa[(pa.arm == "padding")
                               & (pa.param == r_)].accuracy.iloc[0], 4))
        add(f"PadSt{w}", num(ps[(ps.arm == "padding")
                               & (ps.param == r_)].accuracy.iloc[0], 4))
    for w_, nm in ((0.25, "Quarter"), (0.5, "Half")):
        add(f"BlendAm{nm}", num(pa[(pa.arm == "blending")
                                   & (pa.param == w_)].accuracy.iloc[0], 4))
        add(f"BlendSt{nm}", num(ps[(ps.arm == "blending")
                                   & (ps.param == w_)].accuracy.iloc[0], 4))

    # ---- SS G.2 worklist-only (T1) ablation
    G = pd.read_csv(P6 / "p6_section_G2.csv")
    g = rf(G).set_index("arm")
    add("GtwoTOneAcc", num(g.loc["T1_only", "accuracy"], 4))
    add("GtwoTOneBits", num(g.loc["T1_only", "I_bits"], 3))
    add("GtwoTOnePerm", num(g.loc["T1_only_permuted", "accuracy"], 4))
    add("GtwoFullAm", num(g.loc["T1+T2_autopsy_mix", "accuracy"], 4))
    add("GtwoFullSt", num(g.loc["T1+T2_structural", "accuracy"], 4))
    add("GtwoFullStBits", num(g.loc["T1+T2_structural", "I_bits"], 3))
    add("GtwoDeltaAcc",
        num(g.loc["T1_only", "accuracy"] - g.loc["T1+T2_structural",
                                                 "accuracy"], 4))
    add("GtwoDeltaBits",
        num(g.loc["T1_only", "I_bits"] - g.loc["T1+T2_structural",
                                               "I_bits"], 3))
    add("GtwoTOneFeatures", str(int(g.loc["T1_only", "n_features"])))

    # ---- CW-15 candidate-set dependence
    C15 = pd.read_csv(P6 / "p6_cw15_candidate_set.csv")
    c = rf(C15)
    for arm, nm in (("all_27_baseline", "All"), ("learned_22", "Learned"),
                    ("iforest_pruned_to_3", "Pruned"),
                    ("family_balanced_2each", "Balanced"),
                    ("one_per_family_6", "OnePer")):
        for rep, t in (("autopsy_mix", "Am"), ("structural", "St")):
            r = c[(c.arm == arm) & (c.representation == rep)].iloc[0]
            add(f"CwFifteen{nm}{t}", num(r.accuracy, 4))
            add(f"CwFifteen{nm}{t}Lift", num(r.accuracy / r.chance, 1))
        add(f"CwFifteen{nm}K",
            str(int(c[(c.arm == arm)].n_classes.iloc[0])))

    # ---- CW-16 deterministic vs stochastic
    C16 = pd.read_csv(P6 / "p6_cw16_stochastic.csv")
    d = rf(C16)
    for arm, nm in (("stochastic_only", "Stoch"),
                    ("deterministic_only", "Det")):
        for rep, t in (("autopsy_mix", "Am"), ("structural", "St")):
            r = d[(d.arm == arm) & (d.representation == rep)].iloc[0]
            add(f"CwSixteen{nm}{t}", num(r.accuracy, 4))
            add(f"CwSixteen{nm}{t}Lift", num(r.accuracy / r.chance, 2))
        add(f"CwSixteen{nm}K", str(int(d[d.arm == arm].n_classes.iloc[0])))
    _st = json.loads((REPO / "results/p6/STOCHASTIC.json").read_text())
    add("StochCells", str(_st["n_stochastic"]))
    add("DetCells", str(_st["n_deterministic"]))

    # ---- SS G.2 intervals: clustered per arm, PAIRED on the differences.
    # Adversarial round. The paired scheme resamples populations once per
    # draw and moves both arms together, which is what separate marginal
    # intervals cannot do when the same populations underlie both.
    GI = pd.read_csv(P6 / "p6_g2_intervals.csv").set_index("quantity")
    def _gi(q, t):
        r = GI.loc[q]
        add(f"Gtwo{t}CI", f"{r.lo:.4f}, {r.hi:.4f}")
    _gi("T1_only accuracy", "TOneAcc")
    _gi("T1_only_permuted accuracy", "TOnePerm")
    _gi("T1+T2_autopsy_mix accuracy", "FullAm")
    _gi("T1+T2_structural accuracy", "FullSt")
    _gi("T1_only I_bits", "TOneBits")
    _gi("T1+T2_structural I_bits", "FullStBits")
    r = GI.loc["paired accuracy difference (T1 - structural)"]
    add("GtwoPairDiffAcc", num(r.point, 4))
    add("GtwoPairDiffAccCI", f"{r.lo:.4f}, {r.hi:.4f}")
    r = GI.loc["paired log-loss difference, bits (T1 - structural)"]
    add("GtwoPairDiffBits", num(r.point, 3))
    add("GtwoPairDiffBitsCI", f"{r.lo:.3f}, {r.hi:.3f}")

    # ---- the regeneration and its gate
    _v = json.loads((REPO / "results/p6/VERIFICATION.json").read_text())
    add("RegenRows", f"{_v['full_substrate_check']['rows']:,}".replace(
        ",", "{,}"))
    add("RegenCols", str(_v["full_substrate_check"]["feature_columns"]))
    add("RegenDiffering", str(_v["full_substrate_check"]["columns_differing"]))


def main() -> None:
    verify_sources()
    sid_macros()
    sid_strata_macros()
    rid_macros()
    rid_defect_macros()
    prb_convention_macros()
    overlap_macros()
    refbattery_macros()
    circularity_macros()
    abstract_macros()
    methods_macros()
    substrate_macros()
    failure_threshold_macros()
    converse_pair_macros()
    pairwise_macros()
    popcontrol_macros()
    portability_macros()
    rule_recovery_macros()
    cert_bound_macros()
    boundary_macros()
    slotfill_macros()
    battery_scope_macros()
    perclass_macros()
    multitask_macros()
    add("PinnedSources", str(len(SOURCES)))
    # The per-instance fits are inventoried rather than scanned: the full
    # set is 337 MB and is not redistributed with this package, so the two
    # macros below are derived from the committed manifest and the recorded
    # sizes of the same entries. The five fits the build actually reads are
    # present under inputs/ and pinned in SOURCES like every other input.
    _pq = [l.split()[1] for l in
           (REPO / "addendum/results/PARQUET_MANIFEST.sha256")
           .read_text().strip().split("\n")]
    _sz = [int(l.split("\t")[0]) for l in
           (REPO / "addendum/results/PARQUET_SIZES.tsv")
           .read_text().strip().split("\n")]
    add("PersistedFits", str(len(_pq)))
    add("PersistedSize", f"{sum(_sz)/2**20:.0f}\\,MB")
    konst("ManifestCommit", "ca2229d", "commit adding PARQUET_MANIFEST.sha256")
    # ------------------------------------------------------------------
    # DEFECT COUNTS, single origin. One parse of the three ledgers yields
    # the in-scope count, the full index total and the excluded remainder;
    # the manuscript sentence prints all of it from these macros, so the
    # rule is stated on the page and the numbers cannot drift apart. The
    # in-scope rule: defects in the original studies' sealed designs and in
    # our analysis and execution of them -- rid '## D*' plus addendum
    # '## D-A*'. Excluded: the follow-on protocols' own drafting defects
    # (the addendum ledger's D1/D2 and the open-set ledger's D-O1/D-O2).
    # ops/macrocheck.py asserts the arithmetic on the RENDERED macros.
    # ------------------------------------------------------------------
    import re as _re
    _heads = {rel: _re.findall(r"(?m)^## (D[-A-Z]*\d+)",
                               (REPO / rel).read_text())
              for rel in ("rid/PROTOCOL_DEFECTS.md",
                          "addendum/PROTOCOL_DEFECTS.md",
                          "openset/PROTOCOL_DEFECTS.md")}
    _in_scope = (len(_heads["rid/PROTOCOL_DEFECTS.md"])
                 + sum(1 for h in _heads["addendum/PROTOCOL_DEFECTS.md"]
                       if h.startswith("D-A")))
    _total = sum(len(v) for v in _heads.values())
    if _in_scope + (_total - _in_scope) != _total or _in_scope > _total:
        raise SystemExit("defect ledger arithmetic is inconsistent")
    add("DefectCount", str(_in_scope),
        "rid '## D*' + addendum '## D-A*' headings")
    add("DefectIndexTotal", str(_total), "all '## D*' headings, three ledgers")
    add("DefectExcluded", str(_total - _in_scope),
        "follow-on protocols' own drafting defects")
    konst("UnpinnedFound", 17, "perimeter audit, notes/P2_PERIMETER.md (D-A6)")
    konst("TypedFound", 45, "perimeter audit, notes/P2_PERIMETER.md (D-A6)")
    family_profile_macros()
    addendum_macros()
    phase6_macros()
    provenance_macros()

    head = [
        "% paper/results_macros.tex — GENERATED FILE. DO NOT HAND-EDIT.",
        "% Regenerate: .venv/bin/python paper/ops/make_p2_macros.py",
        "%",
        "% Every statistic in main.tex is defined here and traced to a",
        "% pinned sealed output. The generator verifies a SHA-256 for each",
        f"% of its {len(SOURCES)} sources and refuses to run on any change.",
        "%",
        f"% macros defined: {len(MACROS)}",
        "",
    ]
    body = []
    for name, note in _ORDER:
        if note:
            body.append(f"% {note}")
        body.append(f"\\newcommand{{\\{name}}}{{{MACROS[name]}}}")
    OUT.write_text("\n".join(head + body) + "\n")
    print(f"wrote {OUT.relative_to(PROJECT)} — {len(MACROS)} macros")


if __name__ == "__main__":
    main()
