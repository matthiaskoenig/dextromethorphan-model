"""Simulation experiment of the study Nagai1996."""

from typing import ClassVar, override

import numpy as np
import pandas as pd
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
from sbmlsim.units import Quantity

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
    MetabolicPhenotype,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Nagai1996(DexSimulationExperiment):
    """Simulation experiment of Nagai1996.

    Seven healthy Japanese volunteers (4 men, 3 women, 22-27 years, 45-67 kg),
    fasted 10 hr before and 4 hr after a single oral dose of 30 mg
    dextromethorphan hydrobromide (2 tablets of 15 mg, Medicon), which the
    publication gives as 81.0 µmole, the monohydrate of the salt factor
    `f_dxmhbr_to_dxm`. All seven are extensive metabolizers by the urinary
    metabolic ratio (cutoff 0.3).

    The assay hydrolyses the conjugates and quantifies the released dextrorphan
    and 3-hydroxymorphinan against the free substances, so the conjugates are
    equivalents of dextrorphan and of 3-hydroxymorphinan. Dextromethorphan and
    the free metabolites were not detectable in plasma (Fig1 has only the
    conjugates). The urinary recovery of Tab2 is the end of the cumulative
    excretion of Fig2 of the same subjects and is not mapped again. The body
    weight is the middle of the range of the subjects (the publication gives no
    mean; the 75 Japanese of its phenotyping part weigh 57.2 kg on average).

    Fig1: plasma dextrorphan and 3-hydroxymorphinan conjugates (mean, n=7).
    Fig2: cumulative urinary excretion of dextromethorphan, of free and
    conjugated dextrorphan and of free and conjugated 3-hydroxymorphinan
    (mean, n=7).
    Fig3: cumulative urinary metabolic ratio DXM/(DXO+DXOGLU) of the seven
    subjects.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]
    #: the body weight of the subjects, the middle of 45-67 kg
    bodyweight: ClassVar[Quantity] = Q(56, "kg")
    #: the molecular weight of 3-hydroxymorphinan (C16H21NO), the standard of
    #: the conjugated 3-hydroxymorphinan in plasma
    Mr_hm3: ClassVar[Quantity] = Q(243.35, "g/mole")
    #: the individuals of Fig3
    fig3_individuals: ClassVar[list[str]] = [f"study1_{k}" for k in range(1, 8)]
    #: the series of Fig1 by key: (substance of the data, observable)
    fig1_series: ClassVar[dict[str, tuple[str, str]]] = {
        "dxo_glu": ("dextrorphan-glucuronide", "[Cve_dxo_glu]"),
        "mm": ("3-hydroxymorphinan-glucuronide", "[Cve_mm]"),
    }
    #: the series of Fig2 by key: (substances of the data, observable); the
    #: free and conjugated 3-hydroxymorphinan are summed for the N-demethylated
    #: morphinans of the model (3-methoxymorphinan was not measured)
    fig2_series: ClassVar[dict[str, tuple[tuple[str, ...], str]]] = {
        "dxm": (("dextromethorphan",), "Aurine_dxm"),
        "dxo": (("dextrorphan",), "Aurine_dxo"),
        "dxo_glu": (("dextrorphan-glucuronide",), "Aurine_dxo_glu"),
        "mm": (("3-hydroxymorphinan", "3-hydroxymorphinan-glucuronide"), "Aurine_mm"),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        # Fig1: plasma conjugates in equivalents of the free substances
        fig1 = self.load_dataframes_by_substance("Fig1")
        for key, (substance, _) in self.fig1_series.items():
            dset = DataSet.from_df(fig1[substance], self.ureg)
            mr = self.Mr.dxo if key == "dxo_glu" else self.Mr_hm3
            dset.unit_conversion("mean", 1 / mr)
            dsets[f"Fig1_{key}"] = dset

        # Fig2: cumulative urinary excretion [µmole]
        fig2 = self.load_dataframes_by_substance("Fig2")
        for key, (substances, _) in self.fig2_series.items():
            dsets[f"Fig2_{key}"] = DataSet.from_df(
                self.sum_series([fig2[s] for s in substances]), self.ureg
            )

        # Fig3: urinary metabolic ratio of the individuals
        fig3 = self.load_dataframe("Fig3")
        for individual in self.fig3_individuals:
            dsets[f"Fig3_{individual}"] = DataSet.from_df(
                fig3[fig3.id == individual], self.ureg
            )
        return dsets

    @staticmethod
    def sum_series(frames: list[pd.DataFrame]) -> pd.DataFrame:
        """Sum series of a figure which are sampled at the same times.

        The standard deviation of the sum is the one of independent series.

        Raises:
            ValueError: if the series are sampled at different times.
        """
        frames = [df.sort_values("time").reset_index(drop=True) for df in frames]
        df = frames[0].copy()
        for other in frames[1:]:
            if not np.allclose(df.time, other.time):
                raise ValueError("The series are not sampled at the same times.")
        df["mean"] = sum(f["mean"] for f in frames)
        df["sd"] = np.sqrt(sum(f["sd"] ** 2 for f in frames))
        return df

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        changes = {
            **self.default_changes(),
            "BW": self.bodyweight,
            "PODOSE_dxm": Q(30, "mg") * self.f_dxmhbr_to_dxm(),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=36,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )
        return tcsims

    @staticmethod
    def metadata(tissue: Tissue, data_type: DataType) -> DexMappingMetaData:
        """Get the metadata of a mapping, the extensive metabolizers."""
        return DexMappingMetaData(
            diplotype=None,
            tissue=tissue,
            genetic_phenotype=None,
            metabolic_phenotype=MetabolicPhenotype.EM,
            route=Route.PO,
            application_form=ApplicationForm.TABLET,
            dosing=Dosing.SINGLE,
            health=Health.HEALTHY,
            fasting=Fasting.FASTED,
            coadministration=Coadministration.NONE,
            data=PKPDData.PK,
            data_type=data_type,
        )

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        series: list[tuple[str, str, str, Tissue]] = [
            ("Fig1", key, observable, Tissue.PLASMA)
            for key, (_, observable) in self.fig1_series.items()
        ] + [
            ("Fig2", key, observable, Tissue.URINE)
            for key, (_, observable) in self.fig2_series.items()
        ]
        for fig_id, key, observable, tissue in series:
            mappings[f"fm_nagai1996_{key}_{tissue.name.lower()}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"{fig_id}_{key}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_cyp2d6_activity_2", xid="time", yid=observable
                ),
                metadata=self.metadata(tissue=tissue, data_type=DataType.MEAN),
            )
        for individual in self.fig3_individuals:
            mappings[f"fm_nagai1996_mr_urine_{individual}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig3_{individual}",
                    xid="time",
                    yid="value",
                    count=1,
                ),
                observable=FitData(
                    self,
                    task="task_cyp2d6_activity_2",
                    xid="time",
                    yid="dxm_dxo_total_urine",
                ),
                metadata=self.metadata(
                    tissue=Tissue.URINE, data_type=DataType.INDIVIDUAL
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        # Fig1 (plasma) and Fig2 (urine): (dataset, observable, label, unit)
        panels: list[tuple[str, str, str, str]] = [
            ("Fig1_dxo_glu", "[Cve_dxo_glu]", self.label_dxoglu, self.unit_dxo),
            ("Fig1_mm", "[Cve_mm]", self.label_mm, self.unit_mm),
            ("Fig2_dxm", "Aurine_dxm", self.label_dxm_ur, self.unit_dxm_ur),
            ("Fig2_dxo", "Aurine_dxo", self.label_dxo_ur, self.unit_dxo_ur),
            ("Fig2_dxo_glu", "Aurine_dxo_glu", self.label_dxoglu_ur, self.unit_dxo_ur),
            ("Fig2_mm", "Aurine_mm", self.label_mm_ur, self.unit_mm_ur),
        ]
        fig = Figure(
            experiment=self,
            sid="Fig1_Fig2",
            name=f"{self.sid}_Fig1|Fig2",
            num_rows=3,
            num_cols=2,
            # the panels share their curves, one legend per row
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis("time", unit=self.unit_time), legend=True)
        for plot, (dset_id, observable, label, unit) in zip(plots, panels, strict=True):
            plot.set_yaxis(label, unit=unit)
            for activity_score in self.activity_scores:
                plot.add_data(
                    task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                    xid="time",
                    yid=observable,
                    label=f"AS:{activity_score}",
                    color=gstyle.color(activity_score),
                )
            plot.add_data(
                dataset=dset_id,
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="EM",
                color=gstyle.color(2),
            )
        for plot in plots[:4]:
            hide_xaxis_label(plot)

        # Fig3: the urinary metabolic ratio of the individuals
        fig3, plot3 = fig_single(
            experiment=self,
            fig_id="Fig3",
            name=self.label_mrtot_urine,
            unit=self.unit_dimless,
            scale="log",
        )
        for activity_score in self.activity_scores:
            plot3.add_data(
                task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                xid="time",
                yid="dxm_dxo_total_urine",
                label=f"AS:{activity_score}",
                color=gstyle.color(activity_score),
            )
        for k, individual in enumerate(self.fig3_individuals):
            plot3.add_data(
                dataset=f"Fig3_{individual}",
                xid="time",
                yid="value",
                count=1,
                # the individuals have one legend entry
                label="EM" if k == 0 else None,
                color=gstyle.color(2),
            )

        return {
            "fig1_fig2": fig,
            "fig3": fig3,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Nagai1996, output_dir="test", save_results=True)
