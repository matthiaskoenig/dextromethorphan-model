"""Simulation experiment of the study Schoedel2012."""

from typing import ClassVar, override

import numpy as np
from pkpdsim.metadata import Coadministration, Dosing, Fasting, Health, Route, Tissue
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import fig_dex
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Schoedel2012(DexSimulationExperiment):
    """Simulation experiment of Schoedel2012.

    Group 2 of an interaction study (evaluable n = 10, 9 extensive, one
    intermediate (*4/*17) and one poor metabolizer (*3/*4) of CYP2D6), fasted
    about 8 hr before the doses of the PK days: dextromethorphan hydrobromide
    30 mg with quinidine sulfate 30 mg (DMQ) twice daily for 8 days, then
    paroxetine 20 mg once daily added from day 9 to day 20. Fig4 is the plasma
    dextromethorphan over the 12 hr after the morning dose of day 8 (DMQ, at
    steady state) and of day 20 (DMQ + paroxetine), mean +- SD. The
    simulation doses DMQ every 12 hr with the constant CYP2D6 activity of
    quinidine (15 doses, the data are the 15th); the paroxetine arm uses the
    same protocol with the CYP2D6 activity of quinidine and paroxetine (the
    steady state of day 20).
    """

    activity_scores: ClassVar[list[float]] = [0, 1.0, 2]

    #: the CYP2D6 activity of the study besides quinidine: paroxetine 20 mg
    #: once daily at steady state is a strong mechanism based inhibitor of
    #: CYP2D6, it raises the AUC of desipramine (fraction metabolized by
    #: CYP2D6 about 0.9) 5.2 fold (Alderman1997), i.e. about 10 % of the
    #: activity; the inhibitions of quinidine and paroxetine are multiplied.
    #: Observed in this study: the AUC12 of dextromethorphan under DMQ rises
    #: 1.46 fold with paroxetine (914.6 to 1335.9 ng*h/ml, Tab III), the
    #: validation of the factor
    cyp2d6_inhibition: ClassVar[dict[str, float]] = {
        **DexSimulationExperiment.cyp2d6_inhibition,
        "paroxetine": 0.1,
    }
    #: the arms: the CYP2D6 activity of the coadministered drugs
    arms: ClassVar[dict[str, tuple[str, ...]]] = {
        "DMQ": ("quinidine",),
        "DMQ_paroxetine": ("quinidine", "paroxetine"),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig4"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.dxm)
                dsets[self.to_sid(f"{fig_id}_{label}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        # 30 mg of the hydrobromide monohydrate, 22 mg of the base
        PODOSE = Q(30, "mg") * self.f_dxmhbr_to_dxm()
        SUBSEQUENT_DOSING_REPETIONS = 7 * 2
        # first dose, subsequent doses every 12 hr, then 15 hr post simulation
        dose_times = [12 * (k + 1) for k in range(SUBSEQUENT_DOSING_REPETIONS)]
        end = 12 * (SUBSEQUENT_DOSING_REPETIONS + 1) + 15
        tcsims = {}

        for arm, inhibitors in self.arms.items():
            f_cyp2d6 = float(np.prod([self.cyp2d6_inhibition[i] for i in inhibitors]))
            for activity_score in self.activity_scores:
                changes = {
                    **self.default_changes(),
                    "PODOSE_dxm": PODOSE,
                    "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
                    "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                    "LI__f_cyp2d6": Q(f_cyp2d6, "dimensionless"),
                }
                tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}_{arm}")] = (
                    Simulation(
                        time_unit="hr",
                        end=end,
                        # 0.1 hr
                        preinit_changes=changes,
                        changes=[self.add_doses(dose_times, {"PODOSE_dxm": PODOSE})],
                    )
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for arm in self.arms:
            mappings[self.to_sid(f"fm_schoedel2012_dxm_{arm.lower()}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig4_{arm}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_cyp2d6_activity_2_{arm}"),
                    xid="time",
                    yid="[Cve_dxm]",
                ),
                metadata=DexMappingMetaData(
                    diplotype=None,
                    tissue=Tissue.PLASMA,
                    genetic_phenotype=None,
                    # 8 extensive, one intermediate and one poor metabolizer
                    metabolic_phenotype=None,
                    route=Route.PO,
                    dosing=Dosing.MULTIPLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.QUINIDINE,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plot = fig_dex(experiment=self, fig_id="Fig4")
        plot.xaxis = Axis(self.label_time, unit=self.unit_time, min=160, max=195)
        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        labels = {"DMQ": "DMQ", "DMQ_paroxetine": "DMQ + paroxetine"}
        linestyles = {"DMQ": "-", "DMQ_paroxetine": "--"}
        for arm in self.arms:
            for activity_score in self.activity_scores:
                plot.add_data(
                    task=self.to_sid(f"task_cyp2d6_activity_{activity_score}_{arm}"),
                    xid="time",
                    yid="[Cve_dxm]",
                    label=f"AS:{activity_score} {labels[arm]}",
                    color=gstyle.color(activity_score),
                    linestyle=linestyles[arm],
                )
        # data
        plot.add_data(
            dataset="Fig4_DMQ",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="DMQ",
            color="black",
        )
        plot.add_data(
            dataset="Fig4_DMQ_paroxetine",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="DMQ + paroxetine",
            color="dimgrey",
            marker="^",
        )

        return {
            "fig1": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Schoedel2012, output_dir="test", save_results=True)
