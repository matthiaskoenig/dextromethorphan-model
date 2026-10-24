"""Simulation experiment of the study Doroshyenko2013."""

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


class Doroshyenko2013(DexSimulationExperiment):
    """Simulation experiment of Doroshyenko2013.

    Healthy men and women (16 completed), double blind crossover: 160 mg
    silexan (lavender oil) or placebo once daily on days 1 to 11, on day 11
    the phenotyping cocktail of 150 mg caffeine, 125 mg tolbutamide, 20 mg
    omeprazole, 30 mg dextromethorphan hydrobromide (one capsule Hustenstiller
    ratiopharm) and 2 mg midazolam iv, fasted from 9 hr before until 6 hr
    after the dose. Fig 1 gives the median plasma dextromethorphan of both
    periods. One subject was a genetic poor metabolizer of CYP2D6 and was
    excluded from the analysis of CYP2D6 (N = 15), no other subject carried two
    null alleles: the subjects are extensive and intermediate metabolizers.

    Silexan does not change the pharmacokinetics of dextromethorphan (AUC0-t
    ratio 1.046, 90 % CI 0.838-1.305), so both periods are the same
    simulation; the silexan period validates it.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]
    #: the periods by the label of their data: the key of the period and the
    #: coadministration
    periods: ClassVar[dict[str, tuple[str, Coadministration]]] = {
        "dex": ("placebo", Coadministration.COCKTAIL),
        "dex_silexan": ("silexan", Coadministration.SILEXAN),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        dframes = self.load_dataframes_by_substance("Fig1")
        for label, df in dframes["dextromethorphan"].groupby("label"):
            dsets[self.to_sid(f"Fig1_{label}")] = DataSet.from_df(df, self.ureg)
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        changes = {
            **self.default_changes(),
            # 30 mg dextromethorphan hydrobromide (Hustenstiller ratiopharm)
            "PODOSE_dxm": Q(30, "mg") * self.f_dxmhbr_to_dxm(),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=24,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        for label, (period, coadministration) in self.periods.items():
            mappings[self.to_sid(f"fm_doroshyenko2013_dxm_{period}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig1_{label}"),
                    xid="time",
                    yid="median",
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
                    # the genetic poor metabolizer is excluded
                    genetic_phenotype=GeneticPhenotype.gEM,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=coadministration,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plot = fig_dex(experiment=self, fig_id="Fig1", scale="log")
        gstyle = GenotypeStyle(
            activities=np.array([self.activity_scores[0], self.activity_scores[-1]])
        )
        for activity_score in self.activity_scores:
            plot.add_data(
                task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                xid="time",
                yid="[Cve_dxm]",
                label=f"AS:{activity_score}",
                color=gstyle.color(activity_score),
            )
        styles = {
            "dex": ("placebo (median)", "o", "black"),
            "dex_silexan": ("silexan (median)", "s", "dimgrey"),
        }
        for label, (curve_label, marker, color) in styles.items():
            plot.add_data(
                dataset=self.to_sid(f"Fig1_{label}"),
                xid="time",
                yid="median",
                count="count",
                label=curve_label,
                marker=marker,
                color=color,
            )
        return {
            "fig1": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Doroshyenko2013, output_dir="test", save_results=True)
