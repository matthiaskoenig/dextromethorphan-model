"""Simulation experiment of the study Gaedigk2013."""

from typing import ClassVar, override

import numpy as np
from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
    DataType,
    Dosing,
    Fasting,
    Health,
    PKPDData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
    jitter,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    fig_mrtot_urine,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeScoring,
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Gaedigk2013(DexSimulationExperiment):
    """Simulation experiment of Gaedigk2013.

    A review: Fig. 1 shows a cohort of 362 caucasian subjects phenotyped with
    dextromethorphan (adapted from Gaedigk et al. 2008), Fig. 1B the
    individual urinary metabolic ratio DM/DX (after deconjugation) of 143 of
    them by genotype. The 2013 article reports neither the dose nor the
    collection: the 0.3 mg/kg as a syrup (Tussin cough syrup, the hydrobromide)
    and the urine over 4 hr are those of the source studies (Gaedigk2008,
    Gaedigk2002). The body weight is not reported, the dose is given per kg of
    the body weight of the model.

    Every marker of Fig. 1B is one subject. The figure itself has fewer
    markers than subjects for `*1/*1` (6 of 33), `*1/*2A` (21 of 22) and
    `*1/*4` (41 of 46), identical ratios drawn on top of each other; the data
    are the markers of the vector paths of the figure.
    """

    #: the genotype groups of Fig. 1B: (diplotype, activity score, subjects);
    #: `*41/null` is a reduced and a non-functional allele (activity score 0.5)
    diplotypes: ClassVar[dict[str, tuple[str, float, int]]] = {
        "1_1": ("*1/*1", 2.0, 33),
        "1_2A": ("*1/*2", 2.0, 22),
        "2A_2A": ("*2/*2", 2.0, 7),
        "1_4": ("*1/*4", 1.0, 46),
        "2A_4": ("*2/*4", 1.0, 10),
        "41_null": ("*41/null", 0.5, 14),
        "4_4": ("*4/*4", 0.0, 11),
    }
    activity_scores: ClassVar[list[float]] = [0.0, 0.5, 1.0, 2.0]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for group, dset_group in dframes["(dmt)/(dtf+dtfglu)"].groupby("group"):
                dset_group["time_jitter"] = jitter(dset_group["time"], 0.1)
                dset_group["time_jitter_unit"] = dset_group["time_unit"]
                dsets[self.to_sid(f"{fig_id}_{group}")] = DataSet.from_df(
                    dset_group, self.ureg
                )
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": Q(0.3, "mg/kg") * self.f_dxmhbr_to_dxm() * Q(75, "kg"),
            "BW": Q(75, "kg"),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=5,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        for group, (diplotype, activity_score, _) in self.diplotypes.items():
            mappings[self.to_sid(f"fm_gaedigk2013_mrtot_urine_{group}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig1_{group}"),
                    xid="time",
                    yid="value",
                    count=1,
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                    xid="time",
                    yid="dxm_dxo_total_urine",
                ),
                metadata=DexMappingMetaData(
                    diplotype=diplotype,
                    genetic_phenotype=GenotypeScoring.genetic_phenotype_for_activity_score(
                        activity_score
                    ),
                    activity_score=activity_score,
                    metabolic_phenotype=None,
                    tissue=Tissue.URINE,
                    route=Route.PO,
                    application_form=ApplicationForm.SYRUP,
                    dosing=Dosing.SINGLE,
                    health=Health.NR,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.NONE,
                    data=PKPDData.PK,
                    data_type=DataType.INDIVIDUAL,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plots = fig_mrtot_urine(experiment=self, fig_id="Fig1")
        gstyle = GenotypeStyle(activities=np.array([0, 2]))
        for activity_score in self.activity_scores:
            plots[0].add_data(
                task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                xid="time",
                yid="dxm_dxo_total_urine",
                color=gstyle.color(activity_score),
                label=f"AS:{activity_score:g}",
            )
        for marker, (group, (diplotype, activity_score, n)) in zip(
            ["o", "s", "^", "o", "s", "o", "o"], self.diplotypes.items(), strict=True
        ):
            plots[0].add_data(
                dataset=self.to_sid(f"Fig1_{group}"),
                xid="time_jitter",
                yid="value",
                label=f"{diplotype} AS:{activity_score:g} (n={n})",
                color=gstyle.color(activity_score),
                marker=marker,
                linestyle="",
                alpha=1,
            )

        return {"fig1": fig}


if __name__ == "__main__":
    MODEL.run_experiments(Gaedigk2013, output_dir="test", save_results=True)
