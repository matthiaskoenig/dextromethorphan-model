"""Parameter fit problems for dextromethorphan.

The data of a fit is selected from the fit mappings of the studies in three
steps, see `sbmlsim.fit.helpers`: the filters on the metadata of the mappings
select the training data of the fit and exclude the rest, the outliers are
named once for all mappings and are the training data which is not usable, and
the validation data is the part of the training data a fit is evaluated on but
not fitted to. The metadata of a mapping describes its curve, what a fit does
with the curve is decided here.

The training data are healthy subjects without an interacting drug, of every
CYP2D6 phenotype: the activity score of the diplotype of a curve sets the
activity of CYP2D6 of its simulation (`LI__cyp2d6_activity`), so poor,
intermediate, extensive and ultrarapid metabolizers identify one set of
parameters. The validation data has four parts, each a different question: the
interactions (`INTERACTION_VALIDATION`, the arms with a coadministered drug,
simulated with the documented activity factors `cyp2d6_inhibition` and
`cyp3a4_inhibition` of the base of the experiments, which are not fitted), the
doses (`DOSE_VALIDATION`), the populations (`POPULATION_VALIDATION`, the
cross-sectional genotype-phenotype cohorts, whose means mix the activity
scores) and the limitations (`LIMITATION_VALIDATION`, data of a process the
model does not describe, e.g. a sustained release formulation). The summaries
of data which is fitted one by one are excluded (`AGGREGATE_MAPPINGS`).

Besides the vocabulary of pkpdsim a dextromethorphan curve is described by the
CYP2D6 status of its subjects (`DexMappingMetaData`): the diplotype (genotype)
with the genetic phenotype and the activity score which follow from it, and
the metabolic phenotype which was determined by phenotyping (e.g. the urinary
metabolic ratio). The experiments are imported inside the functions.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pkpdsim.fit import mapping_metadata, observable_filter
from pkpdsim.metadata import Coadministration, PKPDMappingMetaData
from sbmlsim.console import console
from sbmlsim.fit import FitMapping, FitMappingCollection, MappingKind
from sbmlsim.fit.helpers import FitMappings, MappingFilter

from pkdb_models.models.dextromethorphan import DATA_PATHS, DEXTROMETHORPHAN_PATH
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GeneticPhenotype,
    GenotypeScoring,
    MetabolicPhenotype,
)

if TYPE_CHECKING:
    from sbmlsim.experiment import SimulationExperiment


@dataclass(kw_only=True)
class DexMappingMetaData(PKPDMappingMetaData):
    """Metadata for a fit mapping of the dextromethorphan model.

    The genetic phenotype and the activity score of a given diplotype are
    calculated from the diplotype (e.g. *4/*4 -> gPM, 0.0) unless given.
    """

    diplotype: str | None = None
    genetic_phenotype: GeneticPhenotype | None = None
    metabolic_phenotype: MetabolicPhenotype | None = None
    activity_score: float = math.nan

    def __post_init__(self) -> None:
        """Calculate the genetic phenotype and the activity score of the diplotype."""
        if self.diplotype and not self.genetic_phenotype:
            self.genetic_phenotype = GenotypeScoring.genetic_phenotype_for_diplotype(
                diplotype=self.diplotype
            )
        if self.diplotype and math.isnan(self.activity_score):
            self.activity_score = GenotypeScoring.activity_score_for_diplotype(
                diplotype=self.diplotype
            )


#: the keys of fit mappings by study: the keys of the mappings are SIds of
#: their experiment, which two studies can share, so a named mapping is named
#: with its study
type NamedMappings = dict[str, set[str]]

#: coadministrations which do not interact with dextromethorphan: their arms
#: are training data like the arms without a coadministration. Guaifenesin does
#: not change the pharmacokinetics of dextromethorphan (Demirbas1998), the
#: substances of a phenotyping cocktail are given at probe doses
CONTROL_COADMINISTRATION: frozenset[Coadministration] = frozenset(
    {
        Coadministration.NONE,
        Coadministration.COCKTAIL,
        Coadministration.GUAIFENESIN,
    }
)

#: the individuals of the studies A, C, D (healthy, reference period) and E
#: (patients with HIV) of Frank2009 which have a CYP2D6 genotype
FRANK2009_INDIVIDUALS: dict[str, tuple[str, ...]] = {
    "A": tuple(f"A{k:02d}" for k in range(1, 17)),
    "C": tuple(f"C{k:02d}" for k in (1, 2, 3, 4, 6, 8, 10, 11, 12, 14, 15)),
    "D": tuple(f"D{k:02d}" for k in (1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12)),
    "E": tuple(f"E{k:02d}" for k in (*range(1, 19), *range(20, 29), 30)),
}

#: mappings which are not fitted, the data is not usable
OUTLIER_MAPPINGS: NamedMappings = {
    # the total dextrorphan of Fig3 is 5-6 fold the maximum of Tab1 in every
    # group of the publication, a scale error of the figure
    "Capon1996": {
        "fm_capon1996_dxo_total_plasma_em",
        "fm_capon1996_dxo_total_plasma_pm",
        "fm_capon1996_dxo_total_plasma_em_qui",
    },
    # the dextromethorphan of the extensive and intermediate metabolizers of
    # the studies A, C and D: plasma 5-20 fold and urine 10-30 fold below the
    # model at its start values, which describes the dextromethorphan of the
    # other studies of the same dose (plasma: Capon1996, Doroshyenko2013 with
    # the same capsule, Nakashima2007; urine: Schadel1995, Nagai1996, the
    # median 0.2 % of the dose in 0-4 hr of 95 subjects of Chladek2000); the
    # dextrorphan of the same subjects and the dextromethorphan of the poor
    # metabolizer A08 agree with the model. As training data the 66 curves set
    # the dextromethorphan of extensive metabolizers 4 fold below the other
    # studies
    "Frank2009": {
        f"fm_frank2009_{study}_{tissue}_dex_{individual}"
        for study in ("A", "C", "D")
        for tissue in ("plasma", "urine")
        for individual in FRANK2009_INDIVIDUALS[study]
        if individual != "A08"
    },
    # the cumulative ratios of the poor metabolizers of Fig3 B (0-72 hr)
    # contradict Fig3 D (0-14 days) and the amounts of Tab1, which agree
    "Jones1996": {
        "fm_jones1996_Fig3_mr_pm1",
        "fm_jones1996_Fig3_mr_pm2",
        "fm_jones1996_Fig3_mr_pm3",
    },
}

#: the validation of the interactions: the arms with a coadministered drug
#: which changes the activity of CYP2D6 or CYP3A4, simulated with a documented
#: activity factor which is not fitted (`cyp2d6_inhibition`,
#: `cyp3a4_inhibition` of the base of the experiments or of the study)
INTERACTION_VALIDATION: NamedMappings = {
    # terbinafine, CYP2D6 (urinary ratio 97 fold in extensive metabolizers)
    "Abdelrahman1999": {
        f"fm_abdelrahman1999_mr_urine_{diplotype}_ter"
        for diplotype in ("1_1", "1_2", "2_2", "1_4", "4_5", "4_6", "5_13")
    },
    # osilodrostat, CYP2D6 (AUC ratio 1.48)
    "Armani2017": {"fm_armani2017_dxm_plasma_osi"},
    # quinidine, CYP2D6
    "Capon1996": {"fm_capon1996_dxm_plasma_em_qui"},
    # silexan, no interaction (AUC ratio 1.05)
    "Doroshyenko2013": {"fm_doroshyenko2013_dxm_silexan"},
    # tipranavir/ritonavir, CYP2D6 and CYP3A4, first dose and steady state
    "Dumond2010": {
        "fm_dumond2010_dxm_tpvr_first_dose",
        "fm_dumond2010_dxm_tpvr_steady_state",
    },
    # obeticholic acid, no interaction (AUC ratio 0.9)
    "Edwards2017": {
        "fm_edwards2017_dxm_oca10arm_day18_oca10",
        "fm_edwards2017_dxm_oca25arm_day18_oca25",
    },
    # cinacalcet, CYP2D6 (AUC ratio 11.5)
    "Nakashima2007": {
        "fm_nakashima2007_dxm_cinacalcet",
        "fm_nakashima2007_dxo_cinacalcet",
    },
    # quinidine, repeated doses of dextromethorphan with quinidine
    "Pope2004": {
        f"fm_pope2004_{observable}_{phenotype}"
        for observable in ("dxm", "dxo_total", "mr")
        for phenotype in ("em", "pm")
    },
    # Zuojin pill, CYP2D6 (AUC ratio 3.0 in *1/*1)
    "Qiu2016": {f"fm_qiu2016_dxm_group{k}_zuojin" for k in (1, 2, 3)},
    # quinidine, CYP2D6
    "Schadel1995": {
        "fm_schadel1995_tab3_dxm_em_qui",
        "fm_schadel1995_tab3_dxo_em_qui",
        "fm_schadel1995_tab3_dxoglu_em_qui",
        "fm_schadel1995_tab3_mm_em_qui",
        "fm_schadel1995_fig2_dxm_em_qui",
        "fm_schadel1995_fig2_dxoglu_em_qui",
        "fm_schadel1995_fig2_mm_em_qui",
        "fm_schadel1995_fig4_dxm_em2_qui",
        "fm_schadel1995_fig4_dxoglu_em2_qui",
    },
    # quinidine (dextromethorphan/quinidine) and paroxetine, CYP2D6
    "Schoedel2012": {"fm_schoedel2012_dxm_dmq", "fm_schoedel2012_dxm_dmq_paroxetine"},
    # chloroguanide, CYP2D6 (urinary ratio 3.2 fold)
    "Tenneze1999": {
        "fm_tenneze1999_fig1_dxm_dex_chlo",
        "fm_tenneze1999_fig1_dxo_total_dex_chlo",
        "fm_tenneze1999_tab2_dxm_dex_chlo",
        "fm_tenneze1999_tab2_dxo_total_dex_chlo",
        "fm_tenneze1999_tab2_mm_dex_chlo",
    },
    # isavuconazole, CYP3A4 (AUC ratio 1.19)
    "Yamazaki2016": {
        "fm_yamazaki2016_dxm_im_isa",
        "fm_yamazaki2016_dxm_em_isa",
        "fm_yamazaki2016_dxo_total_all_isa",
    },
    # quinidine, CYP2D6
    "Zawertailo2010": {
        "fm_zawertailo2010_dxm_qui",
        "fm_zawertailo2010_dxo_qui",
        "fm_zawertailo2010_dxo_total_qui",
        "fm_zawertailo2010_mm_qui",
    },
}

#: the validation of the doses: doses which the training data predict
DOSE_VALIDATION: NamedMappings = {
    # a microdose of 2 mg in a cocktail, not phenotyped
    "Oh2012": {"fm_oh2012_dxm", "fm_oh2012_dxo"},
}

#: the validation of the populations: the means of cohorts which mix the
#: CYP2D6 activity scores of their subjects, which one simulation cannot
#: describe, and the cross-sectional genotype-phenotype cohorts (one ratio per
#: subject, more points than all time courses together, alleles whose activity
#: the studies dispute), which the model evaluates by activity score
POPULATION_VALIDATION: NamedMappings = {
    # mean of 17 extensive and 2 poor metabolizers
    "Armani2017": {"fm_armani2017_dxm_plasma"},
    # means of 4 extensive and 1 intermediate metabolizer
    "Barnhart1980": {
        "fm_barnhart1980_dxo_urine",
        "fm_barnhart1980_dxo_total_urine",
        "fm_barnhart1980_mm_urine",
    },
    "Dorado2017": {
        f"fm_dorado2017_mr_total_urine_{diplotype}"
        for diplotype in (
            "4_4",
            "4_5",
            "4_17",
            "41_41",
            "29_41",
            "17_29",
            "17_17",
            "6_35",
            "2_6",
            "2_4",
            "1_6",
            "1_5",
            "1_4",
            "17_35",
            "2_41",
            "1_41",
            "2_17",
            "1_29",
            "1_17",
            "1x2_4",
            "35_35",
            "2_2",
            "1_35",
            "1_2",
            "1_1",
            "1x2_17",
            "1x2_35",
            "2_2x2",
            "1_2x2",
            "1_1x2",
        )
    },
    # mean of 1 poor and intermediate metabolizers
    "Dumond2010": {"fm_dumond2010_dxm_baseline"},
    # means of extensive and intermediate metabolizers
    "Edwards2017": {
        "fm_edwards2017_dxm_oca10arm_day1",
        "fm_edwards2017_dxm_oca25arm_day1",
    },
    # patients with HIV on two nucleoside reverse transcriptase inhibitors
    "Frank2009": {
        f"fm_frank2009_E_plasma_{observable}_{individual}"
        for observable in ("dex", "dor", "dxo_total")
        for individual in FRANK2009_INDIVIDUALS["E"]
    },
    # the cumulative urinary ratios of single extensive metabolizers which
    # were phenotyped but not genotyped (Jones1996 Fig3, Nagai1996 Fig3): the
    # ratio is the phenotype itself, its 20 fold spread among the extensive
    # metabolizers is the variability of the activity of CYP2D6, which the
    # activity score 2 of the simulation does not carry (as Hou1991)
    "Jones1996": {f"fm_jones1996_Fig3_mr_em{k}" for k in range(1, 8)},
    "Nagai1996": {f"fm_nagai1996_mr_urine_study1_{k}" for k in range(1, 8)},
    # phenotype groups classified by the measured ratio itself
    "Hou1991": {
        "fm_hou1991_Fig5_mr_urine_em",
        "fm_hou1991_Fig5_mr_urine_im",
        "fm_hou1991_Fig5_mr_urine_pm",
    },
    # 3 healthy controls and 2 medicated patients in one group
    "Koehler1997": {"fm_koehler1997_fig2_dxm_pm", "fm_koehler1997_fig2_dxo_total_pm"},
    # extensive metabolizers of unknown genotype (activity scores 1 and 2)
    "Lenuzza2016": {
        f"fm_lenuzza2016_{observable}_{k}"
        for observable in ("dxm", "dxo")
        for k in range(2, 11)
    },
    "Lopez2005": {
        f"fm_lopez2005_{diplotype}"
        for diplotype in (
            "1_1",
            "1_10",
            "1_2",
            "1_4",
            "1x2_1",
            "1x2_10",
            "1x2_4",
            "2_10",
            "2_17",
            "2_2",
            "2_4",
            "2x2_1",
            "2x2_4",
            "3_4",
            "4_10",
            "4_4",
        )
    },
    "Montane2013": {
        f"fm_montane2013_{diplotype}"
        for diplotype in (
            "10_10",
            "10_17",
            "10_41",
            "10_41x2",
            "13_1_4",
            "17_17",
            "17_29",
            "17_41",
            "17_42",
            "1_1",
            "1_10",
            "1_17",
            "1_1x2",
            "1_2",
            "1_29",
            "1_2x2",
            "1_3",
            "1_36",
            "1_4",
            "1_41",
            "1_42",
            "1_4x2",
            "1_5",
            "1_9",
            "1x2_17",
            "1x2_41",
            "29_29",
            "2_10",
            "2_17",
            "2_2",
            "2_29",
            "2_2x2",
            "2_36_10x2",
            "2_4",
            "2_41",
            "2_5",
            "2x2_17",
            "2x2_5",
            "4_10",
            "4_17",
            "4_4",
            "4_41",
            "4_5",
            "4x2_17",
            "5_10",
            "5_17",
            "5_29",
            "5_5",
        )
    },
    "Myrand2008": {
        f"fm_myrand2008_{diplotype}"
        for diplotype in (
            "10_10",
            "10_10x2",
            "10_14",
            "10_36",
            "1_1",
            "1_10",
            "1_10x2",
            "1_1x2",
            "1_2",
            "1_21",
            "1_2x2",
            "1_3",
            "1_36",
            "1_4",
            "1_4x2",
            "1_5",
            "1_6",
            "1x2_5",
            "2_10",
            "2_14",
            "2_2",
            "2_21",
            "2_3",
            "2_4",
            "2_4x2",
            "2_5",
            "2_6",
            "2x2_5",
            "3_4",
            "4_10",
            "4_36",
            "4_4",
            "5_10",
            "5_14",
        )
    },
    # genotype classes of the publication which mix activity scores
    "Yamazaki2016": {
        "fm_yamazaki2016_dxm_im",
        "fm_yamazaki2016_dxm_em",
        "fm_yamazaki2016_dxo_total_all",
    },
}

#: the validation of the limitations of the model: valid data of a process the
#: model does not describe
LIMITATION_VALIDATION: NamedMappings = {
    # the free dextrorphan of poor metabolizers: the plasma ratio
    # dextromethorphan/dextrorphan is 6-60 against 500 in the model, which
    # forms all dextrorphan in the liver, where it is glucuronidated before it
    # reaches the plasma (the total dextrorphan of poor metabolizers fits)
    "Chladek2000": {"fm_chladek2000_dor_plasma_pm"},
    # sustained release products
    "Demirbas1998": {
        f"fm_demirbas1998_dxo_total_{arm}_{day}"
        for arm in ("A", "B")
        for day in ("day1", "day6")
    },
    # the venous serum of the arm during and after an infusion of 30 min: the
    # concentration rises over the infusion and falls within 30 min after it,
    # the arteriovenous difference of the forearm, which the model (one venous
    # plasma) does not describe: its venous plasma reaches the plateau of the
    # infusion within minutes, 20 fold the data at 3 min
    "Duedahl2005": {"fm_duedahl2005_dxm_iv"},
    # an optimized formulation which dissolves faster, not described
    "Eichhold2007": {
        f"fm_eichhold2007_{analyte}_{phenotype}_optimized"
        for analyte in ("dex", "dor")
        for phenotype in ("em", "pm")
    },
    # the incomplete deglucuronidation of the urine (total over free 5-10
    # fold, about 20 fold in the model and the other studies)
    "Frank2009": {
        f"fm_frank2009_{study}_urine_dor_total_{individual}"
        for study in ("A", "C", "D")
        for individual in FRANK2009_INDIVIDUALS[study]
    },
    # the same incomplete deglucuronidation
    "Hou1991": {
        "fm_hou1991_Fig8_mrtot_urine_em",
        "fm_hou1991_Fig8_mrtot_urine_im",
        "fm_hou1991_Fig8_mrtot_urine_pm",
    },
    # sustained release tablets
    "Hu2011": {"fm_hu2011_dxo_total_floating", "fm_hu2011_dxo_total_conventional"},
}

#: the summaries of data which the fits use one by one, excluded from every
#: fit: a mean of subjects would count the subjects twice
AGGREGATE_MAPPINGS: NamedMappings = {
    # the ratio of the two mapped series of the subject
    "Eichhold1997": {"fm_eichhold1997_mr_em"},
    # the free ratios of the 19 subjects of Fig8 are among the 61 of Fig5
    "Hou1991": {
        "fm_hou1991_Fig8_mr_urine_em",
        "fm_hou1991_Fig8_mr_urine_im",
        "fm_hou1991_Fig8_mr_urine_pm",
    },
    # the end points of the curves of Fig2 of the same subjects
    "Jones1996": {"fm_jones1996_Tab1_dxm_em", "fm_jones1996_Tab1_dxm_pm"},
    # the subjects EM2 and PM3 of Fig4 are in the means of Tab3
    "Schadel1995": {
        "fm_schadel1995_fig4_dxoglu_em2",
        "fm_schadel1995_fig4_dxm_pm3",
        "fm_schadel1995_fig4_dxoglu_pm3",
    },
}

#: the validation data
VALIDATION_QUESTIONS: dict[str, NamedMappings] = {
    "interactions": INTERACTION_VALIDATION,
    "doses": DOSE_VALIDATION,
    "populations": POPULATION_VALIDATION,
    "limitations": LIMITATION_VALIDATION,
}
VALIDATION_MAPPINGS: NamedMappings = {
    study: set().union(
        *(mappings.get(study, set()) for mappings in VALIDATION_QUESTIONS.values())
    )
    for mappings in VALIDATION_QUESTIONS.values()
    for study in mappings
}


def experiment_classes() -> list[type[SimulationExperiment]]:
    """Get the experiments of the studies, the registry of the model."""
    from pkdb_models.models.dextromethorphan.simulations import EXPERIMENTS

    return list(EXPERIMENTS.get("studies", []))


def study(fit_mapping: FitMapping) -> str:
    """Get the study of a fit mapping, the id of its experiment."""
    return fit_mapping.reference.experiment.sid


def named(
    mappings: NamedMappings, fit_mapping_key: str, fit_mapping: FitMapping
) -> bool:
    """Check whether a fit mapping is one of the named mappings of its study."""
    return fit_mapping_key in mappings.get(study(fit_mapping), set())


def check_named(mappings: NamedMappings, fit_mappings: FitMappings) -> None:
    """Check that the named mappings are fit mappings of their studies.

    Raises:
        ValueError: for a study which is no experiment, or a key which is no
            fit mapping of its study.
    """
    for sid, keys in mappings.items():
        experiment = fit_mappings.experiments.get(sid)
        if experiment is None:
            raise ValueError(f"'{sid}' is no experiment of the fits.")
        if unknown := sorted(keys - set(experiment._fit_mappings)):
            raise ValueError(f"'{unknown}' are no fit mappings of '{sid}'.")


def filter_aggregates(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """No summaries of data which is fitted one by one, see `AGGREGATE_MAPPINGS`."""
    return not named(AGGREGATE_MAPPINGS, fit_mapping_key, fit_mapping)


def filter_validation(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Data without an interacting drug, besides the named validation data."""
    if named(VALIDATION_MAPPINGS, fit_mapping_key, fit_mapping):
        return True
    # the coadministration is a field of the base of the metadata
    return mapping_metadata(fit_mapping).coadministration in CONTROL_COADMINISTRATION


def mapping_collections(
    filters: MappingFilter | list[MappingFilter],
    validation: NamedMappings = VALIDATION_MAPPINGS,
) -> dict[str, list[FitMappingCollection]]:
    """Select the data of a fit from the fit mappings of the studies.

    The filters select the training data, the mappings which fail them are
    excluded, and so are the summaries of data which is fitted one by one
    (`AGGREGATE_MAPPINGS`) and the arms with an interacting drug
    (`filter_validation`). The outliers are `OUTLIER_MAPPINGS`, the validation
    data is `VALIDATION_MAPPINGS`. Neither kind enters the cost; both are
    simulated and evaluated with the training data, so a report says how the
    fitted parameters describe data they were not fitted on.

    Args:
        filters: filters of the training data.
        validation: the keys of the validation data by study.

    Returns:
        The fit mapping collections of all kinds by experiment id.

    Raises:
        ValueError: if an outlier is a mapping of no study or of several.
    """
    fit_mappings = FitMappings(
        experiment_classes=experiment_classes(),
        base_path=DEXTROMETHORPHAN_PATH,
        data_path=DATA_PATHS,
    )
    for mappings in [OUTLIER_MAPPINGS, AGGREGATE_MAPPINGS, validation]:
        check_named(mappings, fit_mappings)
    # sbmlsim selects the outliers by their keys alone, which must name one
    # mapping of all studies
    outliers = {key for keys in OUTLIER_MAPPINGS.values() for key in keys}
    for key in outliers:
        studies = [
            sid
            for sid, experiment in fit_mappings.experiments.items()
            if key in experiment._fit_mappings
        ]
        if len(studies) != 1:
            raise ValueError(f"The outlier '{key}' is a mapping of {studies}.")
    selection = fit_mappings.select(
        filters=[
            *(filters if isinstance(filters, list) else [filters]),
            filter_aggregates,
            filter_validation,
        ],
        outliers=outliers,
        validation=lambda key, fit_mapping: named(validation, key, fit_mapping),
        print_info=False,
    )
    # the counts per experiment and kind, not the single mappings
    selection.print(detail=False)
    # the validation mappings by the question they answer
    selected = {
        (sid, key)
        for sid, kinds in selection.kinds.items()
        for key, kind in kinds.items()
        if kind is MappingKind.VALIDATION
    }

    def pairs(mappings: NamedMappings) -> set[tuple[str, str]]:
        return {(sid, key) for sid, keys in mappings.items() for key in keys}

    console.print(
        "validation: "
        + ", ".join(
            f"{len(selected & pairs(mappings))} {question}"
            for question, mappings in VALIDATION_QUESTIONS.items()
        )
    )
    return selection.collections


#: the observables of the data (the index of the data, without the brackets of
#: a concentration): the plasma concentrations, the urinary amounts and the
#: metabolic ratios of the plasma and of the urine
OBSERVABLES_PK: tuple[str, ...] = (
    "Cve_dxm",
    "Cve_dxo",
    "Cve_dxo_glu",
    "Cve_mm",
    "dxo_total",
    "dxm_dxo",
    "dxm_dxo_total",
    "Aurine_dxm",
    "Aurine_dxo",
    "Aurine_dxo_glu",
    "Aurine_dxo_total",
    "Aurine_mm",
    "dxm_dxo_urine",
    "dxm_dxo_total_urine",
)


def f_collections_pk() -> dict[str, list[FitMappingCollection]]:
    """Pharmacokinetic data of dextromethorphan and its metabolites."""
    return mapping_collections(observable_filter(OBSERVABLES_PK))


if __name__ == "__main__":
    console.rule(title="PK", align="left", style="white")
    f_collections_pk()
