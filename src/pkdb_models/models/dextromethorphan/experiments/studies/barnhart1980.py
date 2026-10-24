"""Simulation experiment of the study Barnhart1980."""

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


class Barnhart1980(DexSimulationExperiment):
    """Simulation experiment of Barnhart1980.

    Five healthy men (21 to 41 yr, 50 to 84 kg), fasted overnight through 2
    hr, a single oral dose of 30 mg dextromethorphan hydrobromide in a
    commercial formulation, "equivalent to 22 mg" of the base (the monohydrate).
    Urine in intervals to 48 hr, gas chromatography of dextromethorphan,
    dextrorphan and 3-hydroxymorphinan, free and after hydrolysis (total).
    Tab2: the cumulative urinary dextromethorphan of every subject; Fig4 and
    Fig5: the free and the total dextrorphan and 3-hydroxymorphinan, mean +-
    SEM of the five subjects. 3-methoxymorphinan was detected in some samples
    in amounts below those of dextromethorphan, so the total
    3-hydroxymorphinan is the N-demethylated morphinans of the model.

    Subjects 1 to 4 are extensive metabolizers (0.18 % of the dose as
    dextromethorphan, 45.6 % as total dextrorphan). Subject 5 is no poor
    metabolizer: 3.9 % of the dose as dextromethorphan and 38.8 % as total
    dextrorphan are a urinary metabolic ratio of 0.10, an intermediate
    metabolizer by the cutoffs 0.03 and 0.3 (Gaedigk2013), simulated with the
    activity score 0.5.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]
    #: the subjects of Tab2 with their phenotype and activity score
    subjects: ClassVar[dict[str, tuple[MetabolicPhenotype, float]]] = {
        "S1": (MetabolicPhenotype.EM, 2),
        "S2": (MetabolicPhenotype.EM, 2),
        "S3": (MetabolicPhenotype.EM, 2),
        "S4": (MetabolicPhenotype.EM, 2),
        "S5": (MetabolicPhenotype.IM, 0.5),
    }
    #: the means of the five subjects (Fig4, Fig5) by observable
    mean_data: ClassVar[dict[str, tuple[str, str]]] = {
        "dxo_urine": ("Fig4", "dextrorphan"),
        "dxo_total_urine": ("Fig5", "dtf+dtfglu"),
        "mm_urine": ("Fig5", "3-hydroxymorphinan"),
    }
    mean_observables: ClassVar[dict[str, str]] = {
        "dxo_urine": "Aurine_dxo",
        "dxo_total_urine": "Aurine_dxo_total",
        "mm_urine": "Aurine_mm",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        dframes = self.load_dataframes_by_substance("Tab2")
        for individual, df in dframes["dextromethorphan"].groupby("individual"):
            dset = DataSet.from_df(df, self.ureg)
            dset.unit_conversion("value", 1 / self.Mr.dxm)
            dsets[self.to_sid(f"Tab2_{individual}")] = dset

        # free (Fig4) and total (Fig5) dextrorphan and 3-hydroxymorphinan in mg
        # of the free base, the total dextrorphan is 45.6 % of the dose
        mrs = {"dextrorphan": self.Mr.dxo, "dtf+dtfglu": self.Mr.dxo}
        mrs["3-hydroxymorphinan"] = self.Mr.mm
        for key, (fig_id, substance) in self.mean_data.items():
            df = self.load_dataframes_by_substance(fig_id)[substance]
            dset = DataSet.from_df(df, self.ureg)
            dset.unit_conversion("mean", 1 / mrs[substance])
            dsets[self.to_sid(f"{fig_id}_{key}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        changes = {
            **self.default_changes(),
            # 30 mg of the hydrobromide, 22 mg of the base
            "PODOSE_dxm": Q(30, "mg") * self.f_dxmhbr_to_dxm(),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=50,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )
        return tcsims

    def metadata(
        self, phenotype: MetabolicPhenotype | None, data_type: DataType
    ) -> DexMappingMetaData:
        """Get the metadata of a mapping."""
        return DexMappingMetaData(
            metabolic_phenotype=phenotype,
            tissue=Tissue.URINE,
            route=Route.PO,
            application_form=ApplicationForm.NR,
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
        for subject, (phenotype, activity_score) in self.subjects.items():
            mappings[self.to_sid(f"fm_barnhart1980_dxm_urine_{subject}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Tab2_{subject}"),
                    xid="time",
                    yid="value",
                    count=1,
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                    xid="time",
                    yid="Aurine_dxm",
                ),
                metadata=self.metadata(phenotype, DataType.INDIVIDUAL),
            )
        # the means of four extensive and one intermediate metabolizer
        for key, (fig_id, _) in self.mean_data.items():
            mappings[self.to_sid(f"fm_barnhart1980_{key}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"{fig_id}_{key}"),
                    xid="time",
                    yid="mean",
                    yid_se="mean_se",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_cyp2d6_activity_2",
                    xid="time",
                    yid=self.mean_observables[key],
                ),
                metadata=self.metadata(None, DataType.MEAN),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        gstyle = GenotypeStyle(activities=np.array([0.0, 3]))
        fig = Figure(
            experiment=self,
            sid="Tab2_Fig4_Fig5",
            name=f"{self.sid}_Tab2_Fig4_Fig5",
            num_rows=2,
            num_cols=2,
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_dxm_ur, unit=self.unit_dxm_ur, scale="log")
        plots[1].set_yaxis(self.label_dxo_ur, unit=self.unit_dxo_ur, scale="log")
        plots[2].set_yaxis(self.label_dxo_total_ur, unit=self.unit_dxo_total_ur)
        plots[3].set_yaxis("morphinans (3MM + 3HM) urine\n", unit=self.unit_mm_ur)
        for plot in plots[:2]:
            hide_xaxis_label(plot)

        yids = ["Aurine_dxm", "Aurine_dxo", "Aurine_dxo_total", "Aurine_mm"]
        for activity_score in self.activity_scores:
            for k, yid in enumerate(yids):
                plots[k].add_data(
                    task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                    xid="time",
                    yid=yid,
                    label=f"AS:{activity_score}",
                    color=gstyle.color(activity_score),
                )

        for subject, (phenotype, activity_score) in self.subjects.items():
            plots[0].add_data(
                dataset=self.to_sid(f"Tab2_{subject}"),
                xid="time",
                yid="value",
                label=f"{subject} ({phenotype})",
                color=gstyle.color(activity_score),
                linestyle="",
            )
        for k, (key, (fig_id, _)) in enumerate(self.mean_data.items(), start=1):
            plots[k].add_data(
                dataset=self.to_sid(f"{fig_id}_{key}"),
                xid="time",
                yid="mean",
                yid_se="mean_se",
                count="count",
                label="4 EM, 1 IM",
                color="black",
                linestyle="",
            )
        return {
            "fig1": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Barnhart1980, output_dir="test", save_results=True)
