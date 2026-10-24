"""Simulation experiment of the study Hou1991."""

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
    fig_mr_urine,
    hide_xaxis_label,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeStyle,
    MetabolicPhenotype,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Hou1991(DexSimulationExperiment):
    """Simulation experiment of Hou1991.

    62 unrelated normal volunteers (white, Chinese, Japanese, Korean, african,
    hispanic), a single oral dose of 50 mg dextromethorphan hydrobromide as a
    powder in a gelatin capsule, urine collected over 0 to 8 hr and saliva at
    3 hr. Fig. 5 is a quantile plot of the urinary (free) and the salivary
    metabolic ratio of 61 subjects, the x and y of a point are not one subject;
    only the urinary ratios are used (the model has no saliva). Fig. 8 gives
    the free and the deconjugated urinary ratio of 19 of the subjects (9
    extensive, 5 intermediate and 5 poor metabolizers), whose free ratio is in
    Fig. 5 as well.

    The phenotypes are those of the free urinary ratio with the antimodes of
    the publication: extensive < 0.25 < intermediate < 4.0 < poor. The
    subjects were not genotyped; a phenotype is simulated with the activity
    score of its typical diplotype: EM 2, IM 0.5 (the intermediate ratios of
    0.29 to 2.5 are those of the activity score 0.5 of the model), PM 0.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]
    #: the activity score of a phenotype
    phenotypes: ClassVar[dict[str, tuple[MetabolicPhenotype, float]]] = {
        "em": (MetabolicPhenotype.EM, 2),
        "im": (MetabolicPhenotype.IM, 0.5),
        "pm": (MetabolicPhenotype.PM, 0),
    }
    #: the urinary metabolic ratios of the figures: (figure, column, key, observable)
    ratios: ClassVar[list[tuple[str, str, str, str]]] = [
        ("Fig5", "y_value", "mr", "dxm_dxo_urine"),
        ("Fig8", "y_value", "mr", "dxm_dxo_urine"),
        ("Fig8", "x_value", "mrtot", "dxm_dxo_total_urine"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id, column, key, _ in self.ratios:
            df = self.load_dataframe(fig_id)
            df = df.drop(
                columns=[c for c in df.columns if c[:2] in {"x_", "y_"}]
            ).assign(value=df[column], unit="dimensionless")
            # the urine is collected over 0 to 8 hr, the curation stores the
            # time of the saliva (3 hr)
            df["time"] = 8.0
            df["time_unit"] = "hr"
            for phenotype, df_phenotype in df.groupby("phenotype"):
                df_phenotype["time_jitter"] = jitter(df_phenotype["time"], 0.1)
                df_phenotype["time_jitter_unit"] = df_phenotype["time_unit"]
                dsets[self.to_sid(f"{fig_id}_{key}_{phenotype}")] = DataSet.from_df(
                    df_phenotype, self.ureg
                )
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": Q(50, "mg") * self.f_dxmhbr_to_dxm(),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=9,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for fig_id, _, key, observable in self.ratios:
            for phenotype, (
                metabolic_phenotype,
                activity_score,
            ) in self.phenotypes.items():
                dataset = self.to_sid(f"{fig_id}_{key}_{phenotype}")
                if dataset not in self._datasets:
                    continue
                mappings[
                    self.to_sid(f"fm_hou1991_{fig_id}_{key}_urine_{phenotype}")
                ] = FitMapping(
                    self,
                    reference=FitData(
                        self, dataset=dataset, count=1, xid="time", yid="value"
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                        xid="time",
                        yid=observable,
                    ),
                    metadata=DexMappingMetaData(
                        diplotype=None,
                        tissue=Tissue.URINE,
                        genetic_phenotype=None,
                        metabolic_phenotype=metabolic_phenotype,
                        route=Route.PO,
                        application_form=ApplicationForm.CAPSULE,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.NR,
                        coadministration=Coadministration.NONE,
                        data=PKPDData.PK,
                        data_type=DataType.INDIVIDUAL,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig5, plots_5 = fig_mr_urine(experiment=self, fig_id="Fig5")

        fig8 = Figure(experiment=self, sid="Fig8", name=f"{self.sid}_Fig8", num_rows=2)
        plots_8 = fig8.create_plots(
            xaxis=Axis("time", unit=self.unit_time), legend=True
        )
        plots_8[0].set_yaxis(self.label_mr_urine, unit=self.unit_dimless, scale="log")
        plots_8[1].set_yaxis(
            self.label_mrtot_urine, unit=self.unit_dimless, scale="log"
        )
        hide_xaxis_label(plots_8[0])

        gstyle = GenotypeStyle(
            activities=np.array([self.activity_scores[0], self.activity_scores[-1]])
        )
        for activity_score in self.activity_scores:
            task_id = f"task_cyp2d6_activity_{activity_score}"
            for plots in [plots_5, plots_8]:
                # simulations
                plots[0].add_data(
                    task=self.to_sid(task_id),
                    xid="time",
                    yid="dxm_dxo_urine",
                    color=gstyle.color(activity_score),
                    label=f"AS:{activity_score}",
                )
                if len(plots) == 2:
                    plots[1].add_data(
                        task=self.to_sid(task_id),
                        xid="time",
                        yid="dxm_dxo_total_urine",
                        color=gstyle.color(activity_score),
                        label=f"AS:{activity_score}",
                    )

        # data
        for phenotype, (_, activity_score) in self.phenotypes.items():
            for plot, fig_id, key in [
                (plots_5[0], "Fig5", "mr"),
                (plots_8[0], "Fig8", "mr"),
                (plots_8[1], "Fig8", "mrtot"),
            ]:
                plot.add_data(
                    dataset=self.to_sid(f"{fig_id}_{key}_{phenotype}"),
                    xid="time_jitter",
                    yid="value",
                    label=phenotype.upper(),
                    linestyle="",
                    alpha=1,
                    color=gstyle.color(activity_score),
                )

        return {
            "fig5": fig5,
            "fig8": fig8,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Hou1991, output_dir="test", save_results=True)
