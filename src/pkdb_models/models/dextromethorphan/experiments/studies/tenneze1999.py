"""Simulation experiment of the study Tenneze1999."""

import math
from typing import ClassVar, override

import numpy as np
import pandas as pd
from pkpdsim.metadata import Coadministration, Dosing, Fasting, Health, Route, Tissue
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    fig_dex_dor_plasma,
    hide_xaxis_label,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeStyle,
    MetabolicPhenotype,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Tenneze1999(DexSimulationExperiment):
    """Simulation experiment of Tenneze1999.

    36 healthy white men (73 +- 9 kg), extensive metabolizers of CYP2D6 and
    CYP2C19, fasted overnight; three-period crossover of a single oral dose of
    80 mg dextromethorphan (a capsule of the hospital pharmacy from a powder,
    the salt is not named, the dose is taken as the base like the curation),
    200 mg chloroguanide (proguanil) hydrochloride (two tablets of 100 mg) and
    both together. Plasma dextromethorphan and total dextrorphan (after
    enzymatic hydrolysis) (Fig1, mean +- SD) and the urinary recoveries over
    24 hr in % of the dextromethorphan dose (Tab2, mean +- SD). The
    N-demethylated morphinans of the model are the sum of 3-methoxymorphinan
    and 3-hydroxymorphinan (free and conjugated) of Tab2.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]

    #: the CYP2D6 activity of the study besides the base: chloroguanide 200 mg
    #: lowers the partial metabolic clearance of dextromethorphan to
    #: dextrorphan by 65 +- 41 % (the apparent oral clearance by 61 +- 55 %,
    #: the urinary metabolic ratio rises 3.2 fold) in this study, i.e. 35 % of
    #: the activity of CYP2D6
    cyp2d6_inhibition: ClassVar[dict[str, float]] = {
        **DexSimulationExperiment.cyp2d6_inhibition,
        "chloroguanide": 0.35,
    }

    #: the arms by intervention of the data
    arms: ClassVar[dict[str, str]] = {
        "dex80mg": "dex",
        "dex80mg, chloroguanide": "dex_chlo",
    }
    #: the plasma substances of the data and their observables
    plasma: ClassVar[dict[str, tuple[str, str]]] = {
        "dextromethorphan": ("dxm", "[Cve_dxm]"),
        "dtf+dtfglu": ("dxo_total", "dxo_total"),
    }
    #: the urinary substances of the data and their observables; the
    #: N-demethylated morphinans are the sum of the parts
    urine: ClassVar[dict[str, tuple[str, str]]] = {
        "dextromethorphan": ("dxm", "Aurine_dxm"),
        "dtf+dtfglu": ("dxo_total", "Aurine_dxo_total"),
        "mm": ("mm", "Aurine_mm"),
    }
    mm_parts: ClassVar[set[str]] = {"3-methoxymorphinan", "hm3+hm3glu"}

    #: the dose of the base
    dose: ClassVar[Quantity] = Q(80, "mg")

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        # plasma
        for substance, df in self.load_dataframes_by_substance("Fig1").items():
            sid, _ = self.plasma[substance]
            mr = self.Mr.dxm if substance == "dextromethorphan" else self.Mr.dxo
            for intervention, df_arm in df.groupby("intervention"):
                dset = DataSet.from_df(df_arm, self.ureg)
                # total dextrorphan in dextrorphan equivalents
                dset.unit_conversion("mean", 1 / mr)
                arm = self.arms[str(intervention)]
                dsets[self.to_sid(f"Fig1_{sid}_{arm}")] = dset

        # urinary recoveries [% of the dextromethorphan dose] -> amount
        df = self.load_dataframe("Tab2")
        df = df[df.measurement == "recovery"]
        df_mm = self.sum_mm(df[df.substance.isin(self.mm_parts)])
        df = pd.concat([df[~df.substance.isin(self.mm_parts)], df_mm])
        for (substance, intervention), df_arm in df.groupby(
            ["substance", "intervention"]
        ):
            sid, _ = self.urine[str(substance)]
            dset = DataSet.from_df(df_arm, self.ureg)
            dset.unit_conversion("mean", self.dose / self.Mr.dxm / Q(100, "percent"))
            arm = self.arms[str(intervention)]
            dsets[self.to_sid(f"Tab2_{sid}_{arm}")] = dset
        return dsets

    @staticmethod
    def sum_mm(df: pd.DataFrame) -> pd.DataFrame:
        """Get the N-demethylated morphinans, the sum of the parts per arm.

        The standard deviations and errors are added in quadrature.
        """
        rows = []
        for _, df_arm in df.groupby("intervention"):
            row = df_arm.iloc[0].copy()
            row["substance"] = "mm"
            row["mean"] = df_arm["mean"].sum()
            for err in ["sd", "se"]:
                row[err] = math.sqrt(float((df_arm[err] ** 2).sum()))
            rows.append(row)
        return pd.DataFrame(rows)

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": self.dose,
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            changes_as = {
                **changes,
                "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
            }
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=25,
                preinit_changes=changes_as,
            )
        tcsims["cyp2d6_activity_2_chlo"] = Simulation(
            time_unit="hr",
            end=25,
            preinit_changes={
                **changes,
                "LI__cyp2d6_ac": Q(2, "dimensionless"),
                "LI__f_cyp2d6": Q(
                    self.cyp2d6_inhibition["chloroguanide"], "dimensionless"
                ),
            },
        )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for arm in self.arms.values():
            chloroguanide = arm == "dex_chlo"
            task = (
                "task_cyp2d6_activity_2_chlo"
                if chloroguanide
                else ("task_cyp2d6_activity_2")
            )
            for fig_id, substances, tissue in [
                ("Fig1", self.plasma, Tissue.PLASMA),
                ("Tab2", self.urine, Tissue.URINE),
            ]:
                for sid, observable in substances.values():
                    key = f"fm_tenneze1999_{fig_id.lower()}_{sid}_{arm}"
                    mappings[self.to_sid(key)] = FitMapping(
                        self,
                        reference=FitData(
                            self,
                            dataset=self.to_sid(f"{fig_id}_{sid}_{arm}"),
                            xid="time",
                            yid="mean",
                            yid_sd="mean_sd",
                            count="count",
                        ),
                        observable=FitData(self, task=task, xid="time", yid=observable),
                        metadata=DexMappingMetaData(
                            diplotype=None,
                            tissue=tissue,
                            genetic_phenotype=None,
                            metabolic_phenotype=MetabolicPhenotype.EM,
                            route=Route.PO,
                            dosing=Dosing.SINGLE,
                            health=Health.HEALTHY,
                            fasting=Fasting.FASTED,
                            # pkpdsim has no term of chloroguanide (proguanil)
                            coadministration=(
                                Coadministration.COMEDICATION
                                if chloroguanide
                                else Coadministration.NONE
                            ),
                        ),
                    )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        scale = "log"
        fig, plots = fig_dex_dor_plasma(experiment=self, fig_id="Fig1", scale=scale)
        # the lower end of the axes, the mean - SD of the data is below zero
        plots[0].set_yaxis(self.label_dxm, unit=self.unit_dxm, scale=scale, min=1e-4)
        plots[1].set_yaxis(
            self.label_dxo_total, unit=self.unit_dxo, scale=scale, min=1e-3
        )
        fig_tab2 = Figure(
            experiment=self, sid="Tab2", name=f"{self.sid}_Tab2", num_rows=3
        )
        plots_tab2 = fig_tab2.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        # the unchanged dextromethorphan spans the phenotypes on a log scale
        for k, (plot, (label, unit, tab2_scale)) in enumerate(
            zip(
                plots_tab2,
                [
                    (self.label_dxm_ur, self.unit_dxm_ur, "log"),
                    (self.label_dxo_total_ur, self.unit_dxo_total_ur, "linear"),
                    (self.label_mm_ur, self.unit_mm_ur, "linear"),
                ],
                strict=True,
            )
        ):
            plot.set_yaxis(
                label.replace(" (", "\n(", 1),
                unit=unit,
                scale=tab2_scale,
                min=1e-2 if tab2_scale == "log" else None,
            )
            if k < len(plots_tab2) - 1:
                hide_xaxis_label(plot)

        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        for activity_score in self.activity_scores:
            task_id = self.to_sid(f"task_cyp2d6_activity_{activity_score}")
            for k, (_, observable) in enumerate(self.plasma.values()):
                plots[k].add_data(
                    task=task_id,
                    xid="time",
                    yid=observable,
                    label=f"AS:{activity_score}",
                    color=gstyle.color(activity_score),
                )
            for k, (_, observable) in enumerate(self.urine.values()):
                plots_tab2[k].add_data(
                    task=task_id,
                    xid="time",
                    yid=observable,
                    label=f"AS:{activity_score}",
                    color=gstyle.color(activity_score),
                )
        for k, (_, observable) in enumerate(self.plasma.values()):
            plots[k].add_data(
                task="task_cyp2d6_activity_2_chlo",
                xid="time",
                yid=observable,
                label="AS:2 + chloroguanide",
                color="black",
            )
        for k, (_, observable) in enumerate(self.urine.values()):
            plots_tab2[k].add_data(
                task="task_cyp2d6_activity_2_chlo",
                xid="time",
                yid=observable,
                label="AS:2 + chloroguanide",
                color="black",
            )

        # data
        for fig_id, substances, fig_plots in [
            ("Fig1", self.plasma, plots),
            ("Tab2", self.urine, plots_tab2),
        ]:
            for k, (sid, _) in enumerate(substances.values()):
                fig_plots[k].add_data(
                    dataset=self.to_sid(f"{fig_id}_{sid}_dex"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label="EM",
                    color=gstyle.color(2),
                )
                fig_plots[k].add_data(
                    dataset=self.to_sid(f"{fig_id}_{sid}_dex_chlo"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label="EM + chloroguanide",
                    marker="^",
                    color="black",
                )

        return {
            "fig1": fig,
            "tab2": fig_tab2,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Tenneze1999, output_dir="test", save_results=True)
