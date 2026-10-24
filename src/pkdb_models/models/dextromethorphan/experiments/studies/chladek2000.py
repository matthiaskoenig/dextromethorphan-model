"""Simulation experiment of the study Chladek2000."""

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
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
    jitter,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    hide_xaxis_label,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeStyle,
    MetabolicPhenotype,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Chladek2000(DexSimulationExperiment):
    """Simulation experiment of Chladek2000.

    101 healthy Caucasian volunteers (58 men, 43 women, 20-35 years) took a
    single oral dose of 30 mg dextromethorphan hydrobromide as cough syrup
    (Wick Formel 44 Plus), without food 4 hr before and 4 hr after the dose.
    The urine was collected 0-4 hr after the dose, the plasma was sampled at
    3 hr (95 subjects). 6 subjects are poor metabolizers by the urinary
    metabolic ratio (antimode 0.3).

    The metabolic ratios of single subjects by phenotype (Fig4): the urinary
    ratio DXM/(DXO + DXO glucuronide) of 0-4 hr (Fig4B x), the plasma ratio
    DXM/(DXO + DXO glucuronide) at 3 hr (Fig4A y) and the plasma ratio DXM/DXO
    at 3 hr (Fig4B y). The urinary ratio of Fig4A (x) is the same measurement
    as the one of Fig4B in another subset of the subjects and is not used.
    The salt is the monohydrate of the hydrobromide of the model (the
    85 µmole of the publication are the anhydrous conversion, 5 % apart).
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        # NOTE: additional information in Fig3 and Fig4, the tables Tab1 and Tab2
        # are not used
        # the urinary ratio of Fig4A is the one of Fig4B in another subset
        datasets_used = {("Fig4A", "y_"), ("Fig4B", "x_"), ("Fig4B", "y_")}
        for fig_id in ["Fig4A", "Fig4B"]:
            df = self.load_dataframe(fig_id)
            prefix_rearange = {"x_": "y_", "y_": "x_"}
            for prefix, exclude_prefix in prefix_rearange.items():
                if (fig_id, prefix) not in datasets_used:
                    continue
                this_df = df.copy()
                this_columns = []
                rename_columns = {}
                for column in this_df.columns:
                    if column.startswith(prefix):
                        rename_columns[column] = column[2:]

                    if not column.startswith(exclude_prefix):
                        this_columns.append(column)

                this_df = this_df[this_columns].rename(columns=rename_columns)
                for phenotype, df_phenotype in this_df.groupby("phenotype"):
                    df_phenotype["time_jitter"] = jitter(df_phenotype["time"], 0.1)
                    df_phenotype["time_unit"] = df_phenotype["time_u"]
                    df_phenotype["time_jitter_unit"] = df_phenotype["time_u"]
                    df_phenotype["count"] = 1

                    dsets[self.to_sid(f"{fig_id}_{prefix}{phenotype}")] = (
                        DataSet.from_df(df_phenotype, self.ureg)
                    )

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        PODOSE = Q(30, "mg") * self.f_dxmhbr_to_dxm()  # DEX-HBr

        tcsims = {}
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": PODOSE,
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
        mappings = {}
        for phenotype, activity_score in {"em": 2, "pm": 0}.items():
            if phenotype == "em":
                metabolic_phenotype = MetabolicPhenotype.EM
            else:
                metabolic_phenotype = MetabolicPhenotype.PM

            mappings[self.to_sid(f"fm_chladek2000_dor_total_urine_{phenotype}")] = (
                FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(
                            f"Fig4B_x_{phenotype}"
                        ),  # dex / total dor urine
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
                        diplotype=None,
                        tissue=Tissue.URINE,
                        genetic_phenotype=None,
                        metabolic_phenotype=metabolic_phenotype,
                        route=Route.PO,
                        application_form=ApplicationForm.SYRUP,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                        data=PKPDData.PK,
                        data_type=DataType.INDIVIDUAL,
                    ),
                )
            )

            mappings[self.to_sid(f"fm_chladek2000_dor_total_plasma_{phenotype}")] = (
                FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(
                            f"Fig4A_y_{phenotype}"
                        ),  # dex / total dor plasma
                        xid="time",
                        yid="value",
                        count=1,
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                        xid="time",
                        yid="dxm_dxo_total",
                    ),
                    metadata=DexMappingMetaData(
                        diplotype=None,
                        tissue=Tissue.PLASMA,
                        genetic_phenotype=None,
                        metabolic_phenotype=metabolic_phenotype,
                        route=Route.PO,
                        application_form=ApplicationForm.SYRUP,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                        data=PKPDData.PK,
                        data_type=DataType.INDIVIDUAL,
                    ),
                )
            )

            mappings[self.to_sid(f"fm_chladek2000_dor_plasma_{phenotype}")] = (
                FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig4B_y_{phenotype}"),  # dex / dor plasma
                        xid="time",
                        yid="value",
                        count=1,
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                        xid="time",
                        yid="dxm_dxo",
                    ),
                    metadata=DexMappingMetaData(
                        diplotype=None,
                        tissue=Tissue.PLASMA,
                        genetic_phenotype=None,
                        metabolic_phenotype=metabolic_phenotype,
                        route=Route.PO,
                        application_form=ApplicationForm.SYRUP,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                        data=PKPDData.PK,
                        data_type=DataType.INDIVIDUAL,
                    ),
                )
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(experiment=self, sid="Fig4", name=f"{self.sid}_Fig4", num_rows=3)
        plots = fig.create_plots(xaxis=Axis("time", unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_mrtot_urine, unit=self.unit_dimless, scale="log")

        plots[1].set_yaxis(self.label_mrtot_plasma, unit=self.unit_dimless, scale="log")

        plots[2].set_yaxis(self.label_mr_plasma, unit=self.unit_dimless, scale="log")
        hide_xaxis_label(plots[0])
        hide_xaxis_label(plots[1])

        gstyle = GenotypeStyle(
            activities=np.array([self.activity_scores[0], self.activity_scores[-1]])
        )
        for activity_score in self.activity_scores:
            # simulation
            task_id = f"task_cyp2d6_activity_{activity_score}"
            plots[0].add_data(
                task=self.to_sid(task_id),
                xid="time",
                yid="dxm_dxo_total_urine",
                label=f"AS:{activity_score}",
                color=gstyle.color(activity_score),
            )
            plots[1].add_data(
                task=self.to_sid(task_id),
                xid="time",
                yid="dxm_dxo_total",
                label=f"AS:{activity_score}",
                color=gstyle.color(activity_score),
            )
            plots[2].add_data(
                task=self.to_sid(task_id),
                xid="time",
                yid="dxm_dxo",
                label=f"AS:{activity_score}",
                color=gstyle.color(activity_score),
            )
        for phenotype, activity_score in {"em": 2, "pm": 0}.items():
            plots[0].add_data(
                dataset=self.to_sid(f"Fig4B_x_{phenotype}"),  # dex / total dor urine
                xid="time_jitter",
                yid="value",
                single_lines=True,
                label=phenotype.upper(),
                color=gstyle.color(activity_score),
                linestyle="",
                alpha=1,
            )

            plots[1].add_data(
                dataset=self.to_sid(f"Fig4A_y_{phenotype}"),  # dex / total dor plasma
                xid="time_jitter",
                yid="value",
                single_lines=True,
                label=phenotype.upper(),
                color=gstyle.color(activity_score),
                linestyle="",
                alpha=1,
            )
            plots[2].add_data(
                dataset=self.to_sid(
                    f"Fig4B_y_{phenotype}"
                ),  # dex / unconjugated dor plasma
                xid="time_jitter",
                yid="value",
                single_lines=True,
                label=phenotype.upper(),
                color=gstyle.color(activity_score),
                linestyle="",
                alpha=1,
            )

        return {
            "fig4": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Chladek2000, output_dir="test", save_results=True)
