"""Simulation experiment of the study Duedahl2005."""

from typing import ClassVar, override

import numpy as np
from pkpdsim.metadata import Coadministration, Dosing, Fasting, Health, Route, Tissue
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Change, Simulation

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    fig_single,
    hide_xaxis_label,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Duedahl2005(DexSimulationExperiment):
    """Simulation experiment of Duedahl2005.

    24 healthy men (79 kg, 55-110 kg), crossover against saline: 0.5 mg/kg
    dextromethorphan as an intravenous infusion over 30 min (10 mg/ml prepared
    by the hospital pharmacy, the salt is not named and the dose is taken as
    the base). Venous blood of the non-dominant arm up to 3 hr, serum
    dextromethorphan (Fig 3, mean +- SD of 23 subjects). The metabolizer status
    was not determined; dextrorphan was below or near the limit of
    quantification. The authors fitted a lag time of 5 min (median), which
    the simulation does not have.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3"]:
            df = self.load_dataframe(fig_id)
            dset = DataSet.from_df(df, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.dxm)
            dsets[self.to_sid(f"{fig_id}_dex")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        bodyweight = Q(79, "kg")

        changes = {
            **self.default_changes(),
            # mean weight of subjects is 79 kg.
            # 30 min continuous injection
            "BW": bodyweight,
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
            "Ri_dxm": Q(0.5, "mg/kg") * bodyweight / Q(30, "min"),
        }
        for activity_score in self.activity_scores:
            # 30 min infusion, then 3 hr
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="min",
                end=30 + 60 * 3,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
                changes=[Change(30, {"Ri_dxm": Q(0.0, "mg/min")})],
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        return {
            "fm_duedahl2005_dxm_iv": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig3_dex",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_cyp2d6_activity_2", xid="time", yid="[Cve_dxm]"
                ),
                metadata=DexMappingMetaData(
                    diplotype=None,
                    tissue=Tissue.SERUM,
                    genetic_phenotype=None,
                    metabolic_phenotype=None,
                    route=Route.IV,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.NONE,
                ),
            ),
        }

    @override
    def figures(self) -> dict[str, Figure]:
        scale = "log"

        fig, plot = fig_single(
            experiment=self,
            fig_id="Fig3",
            scale=scale,
            name=self.label_dxm,
            unit=self.unit_dxm,
        )
        if plot.yaxis is not None:
            plot.yaxis.min = 10e-3
        gstyle = GenotypeStyle(
            activities=np.array([self.activity_scores[0], self.activity_scores[-1]])
        )
        for activity_score in self.activity_scores:
            task_id = f"task_cyp2d6_activity_{activity_score}"
            # simulations
            plot.add_data(
                task=self.to_sid(task_id),
                xid="time",
                yid="[Cve_dxm]",
                label=f"AS:{activity_score}",
                color=gstyle.color(activity_score),
            )

        # data
        plot.add_data(
            dataset="Fig3_dex",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="DXM 0.5 mg/kg iv",
            color="black",
        )

        # dextromethorphan in the compartments of the blood: the data are
        # sampled from a vein of the non-dominant arm, the model has no
        # sampling site of its own; the venous and arterial plasma of the
        # model do not differ during the infusion
        compartments = {
            "Cve_dxm": "venous blood",
            "Car_dxm": "arterial blood",
            "Chv_dxm": "hepatic vein",
        }
        fig2 = Figure(
            experiment=self,
            sid="Fig3_blood",
            name=f"{self.sid}_Fig3_blood",
            num_cols=1,
            num_rows=len(compartments),
        )
        plots = fig2.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        for k, compartment in enumerate(compartments.values()):
            plots[k].set_yaxis(f"DXM {compartment}\n", unit=self.unit_dxm)
            if k < len(compartments) - 1:
                hide_xaxis_label(plots[k])
        # data
        for plot in plots:
            plot.add_data(
                dataset="Fig3_dex",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="DXM 0.5 mg/kg iv",
                color="black",
            )
        for activity_score in self.activity_scores:
            task_id = f"task_cyp2d6_activity_{activity_score}"
            for k, key in enumerate(compartments):
                plots[k].add_data(
                    task=self.to_sid(task_id),
                    xid="time",
                    yid=f"[{key}]",
                    label=f"AS:{activity_score}",
                    color=gstyle.color(activity_score),
                )

        return {
            "fig3": fig,
            "fig3_blood": fig2,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Duedahl2005, output_dir="test", save_results=True)
