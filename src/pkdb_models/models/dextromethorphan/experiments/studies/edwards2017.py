"""Simulation experiment of the study Edwards2017."""

from typing import ClassVar, override

import numpy as np
from pkpdsim.metadata import Coadministration, Dosing, Fasting, Health, Route, Tissue
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import fig_dex
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GeneticPhenotype,
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Edwards2017(DexSimulationExperiment):
    """Simulation experiment of Edwards2017.

    Study III of the interactions of obeticholic acid (OCA): healthy subjects
    (76.2 +- 11.8 kg), genetic poor metabolizers of CYP2D6 excluded, randomized
    to OCA 10 mg (N = 23) or 25 mg (N = 24) once daily from day 5 to 28. A
    single dose of 30 mg dextromethorphan in a capsule (the salt is not named,
    the strength of an oral product is the hydrobromide) fasted on day 1 alone
    and on day 18 with OCA; omeprazole was given on other days (day 4 and
    21-28), not with dextromethorphan. Fig 4 gives the mean + SD of plasma
    dextromethorphan up to 72 hr. The curation labels the curves with
    omeprazole 30 mg (the publication gives 20 mg on day 4).

    OCA does not change the pharmacokinetics of dextromethorphan (AUC GMR
    0.89 and 0.90, Tab 3), so the days are the same simulation; the days with
    OCA validate it. The means mix extensive and intermediate metabolizers:
    the terminal phase of the means (1.0-1.8 ng/ml at 24 hr, 0.3-0.5 ng/ml at
    72 hr) is the one of the slow metabolizers among the subjects.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]
    #: the curves by their label in the curation
    curves: ClassVar[dict[str, str]] = {
        "Fig4_group1_dex30_ome30": "Fig4_oca10arm_day1",
        "Fig4_group1_dex30_ome30_OCA10": "Fig4_oca10arm_day18_oca10",
        "Fig4_group2_dex30_ome30": "Fig4_oca25arm_day1",
        "Fig4_group2_dex30_ome30_OCA25": "Fig4_oca25arm_day18_oca25",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig4")
        for label, df_label in df.groupby("label"):
            dset = DataSet.from_df(df_label, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.dxm)
            dsets[self.to_sid(self.curves[str(label)])] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        changes = {
            **self.default_changes(),
            # 30 mg dextromethorphan hydrobromide
            "PODOSE_dxm": Q(30, "mg") * self.f_dxmhbr_to_dxm(),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=80,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for curve in self.curves.values():
            key = curve.removeprefix("Fig4_")
            mappings[self.to_sid(f"fm_edwards2017_dxm_{key}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(curve),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_cyp2d6_activity_2",
                    xid="time",
                    yid="[Cve_dxm]",
                ),
                metadata=DexMappingMetaData(
                    tissue=Tissue.PLASMA,
                    # the genetic poor metabolizers are excluded
                    genetic_phenotype=GeneticPhenotype.gEM,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    # obeticholic acid has no member of the vocabulary
                    coadministration=(
                        Coadministration.COMEDICATION
                        if "oca" in key.split("_")[-1]
                        else Coadministration.NONE
                    ),
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        gstyle = GenotypeStyle(
            activities=np.array([self.activity_scores[0], self.activity_scores[-1]])
        )
        fig, plot = fig_dex(experiment=self, fig_id="Fig4", scale="log")
        if plot.yaxis is not None:
            plot.yaxis.min = 1e-5
        for activity_score in self.activity_scores:
            plot.add_data(
                task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                xid="time",
                yid="[Cve_dxm]",
                label=f"AS:{activity_score}",
                color=gstyle.color(activity_score),
            )
        styles = {
            "Fig4_oca10arm_day1": ("OCA 10 mg arm, day 1", "s", "black"),
            "Fig4_oca10arm_day18_oca10": ("day 18, OCA 10 mg", "s", "dimgrey"),
            "Fig4_oca25arm_day1": ("OCA 25 mg arm, day 1", "^", "black"),
            "Fig4_oca25arm_day18_oca25": ("day 18, OCA 25 mg", "^", "dimgrey"),
        }
        for curve, (label, marker, color) in styles.items():
            plot.add_data(
                dataset=self.to_sid(curve),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=label,
                marker=marker,
                color=color,
            )
        return {
            "fig4": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Edwards2017, output_dir="test", save_results=True)
