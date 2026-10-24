"""Simulation experiment of the study Schadel1995."""

from typing import ClassVar, NamedTuple, override

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
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    hide_xaxis_label,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeStyle,
    MetabolicPhenotype,
)
from pkdb_models.models.dextromethorphan.experiments.table_datasets import from_csv
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Curve(NamedTuple):
    """A curve of the data: figure, substance, group or subject, quinidine."""

    fig_id: str
    substance: str
    group: str
    quinidine: bool

    @property
    def tissue(self) -> Tissue:
        """Get the tissue of the curve, the urine of the recoveries."""
        return Tissue.PLASMA if self.fig_id == "Fig2" else Tissue.URINE

    @property
    def single_subject(self) -> bool:
        """Check whether the curve is a single subject (Fig4: EM2, PM3)."""
        return self.fig_id == "Fig4"

    @property
    def phenotype(self) -> MetabolicPhenotype:
        """Get the metabolic phenotype of the group or subject."""
        if self.group.startswith("PM"):
            return MetabolicPhenotype.PM
        return MetabolicPhenotype.EM


class Schadel1995(DexSimulationExperiment):
    """Simulation experiment of Schadel1995.

    Five extensive (EM) and four poor metabolizers (PM) of CYP2D6, healthy,
    fasted overnight, received a single oral dose of 30 mg dextromethorphan
    hydrobromide (capsules), the 22 mg of the base which the publication uses.
    The extensive metabolizers took the same dose a second time about 12 hr
    after 100 mg of quinidine sulfate at bedtime, simulated with the constant
    CYP2D6 activity of quinidine of the base of the experiments (the waning
    of the inhibition of the single dose over the 72 hr of urine is not
    described). Plasma (Fig2, mean +- SD) and the urinary recoveries over
    72 hr (Tab3, mean +- SD; Fig4 cumulative of the subjects EM2 and PM3, who
    are part of the means of Tab3). The recoveries are molar percentages of
    the dose of the base. The N-demethylated morphinans of the model are the
    sum of 3-methoxymorphinan and 3-hydroxymorphinan (free and conjugated) of
    Tab3, and of the conjugated 3-hydroxymorphinan and 3-methoxymorphinan of
    the plasma (Fig2; 3-methoxymorphinan was not detected in the plasma of
    extensive metabolizers).
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]

    #: the observables of the substances in the plasma and the urine
    plasma_observables: ClassVar[dict[str, str]] = {
        "dex": "[Cve_dxm]",
        "dor": "[Cve_dxo]",
        "dor-glu": "[Cve_dxo_glu]",
        "mm": "[Cve_mm]",
    }
    urine_observables: ClassVar[dict[str, str]] = {
        "dex": "Aurine_dxm",
        "dor": "Aurine_dxo",
        "dor-glu": "Aurine_dxo_glu",
        "mm": "Aurine_mm",
    }
    #: the names of the substances in the keys of the mappings
    substance_names: ClassVar[dict[str, str]] = {
        "dex": "dxm",
        "dor": "dxo",
        "dor-glu": "dxoglu",
        "mm": "mm",
    }

    #: the curves of the data, every curve is mapped
    curves: ClassVar[list[Curve]] = [
        # urinary recoveries over 72 hr, means
        *(
            Curve("Tab3", substance, group, quinidine)
            for substance in ["dex", "dor", "dor-glu", "mm"]
            for group, quinidine in [("EM", False), ("EM", True), ("PM", False)]
        ),
        # plasma, means
        Curve("Fig2", "dor", "EM", False),
        Curve("Fig2", "dor-glu", "EM", False),
        Curve("Fig2", "mm", "EM", False),
        Curve("Fig2", "dex", "EM", True),
        Curve("Fig2", "dor-glu", "EM", True),
        Curve("Fig2", "mm", "EM", True),
        Curve("Fig2", "dex", "PM", False),
        Curve("Fig2", "dor-glu", "PM", False),
        Curve("Fig2", "mm", "PM", False),
        # cumulative urinary recoveries of single subjects
        Curve("Fig4", "dor-glu", "EM2", False),
        Curve("Fig4", "dex", "EM2", True),
        Curve("Fig4", "dor-glu", "EM2", True),
        Curve("Fig4", "dex", "PM3", False),
        Curve("Fig4", "dor-glu", "PM3", False),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        # Tab3 and Fig2 report all the N-demethylated morphinans which were
        # measured, Fig4 only the conjugated 3-hydroxymorphinan
        return {
            **from_csv(self, ["Tab3", "Fig2"], sum_mm=True),
            **from_csv(self, ["Fig4"]),
        }

    def dataset_id(self, curve: Curve) -> str:
        """Get the id of the dataset of a curve."""
        if curve.tissue == Tissue.PLASMA:
            measurement, tissue = "concentration", "plasma"
        else:
            measurement, tissue = "recovery", "urine"
        return self.to_sid(
            f"{curve.fig_id}_{curve.substance}_{curve.group}_{measurement}_{tissue}"
            f"_DEXHBr30mg{'Q' if curve.quinidine else ''}"
        )

    def mapping_id(self, curve: Curve) -> str:
        """Get the key of the fit mapping of a curve."""
        return self.to_sid(
            f"fm_schadel1995_{curve.fig_id.lower()}_"
            f"{self.substance_names[curve.substance]}_{curve.group.lower()}"
            f"{'_qui' if curve.quinidine else ''}"
        )

    def task_id(self, curve: Curve) -> str:
        """Get the task of a curve: activity score 0 (PM) or 2 (EM)."""
        activity_score = 0 if curve.phenotype == MetabolicPhenotype.PM else 2
        return self.to_sid(
            f"task_cyp2d6_activity_{activity_score}{'_qui' if curve.quinidine else ''}"
        )

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        # 30 mg of the hydrobromide monohydrate, 22 mg of the base
        PODOSE = Q(30, "mg") * self.f_dxmhbr_to_dxm()

        changes = {
            **self.default_changes(),
            "PODOSE_dxm": PODOSE,
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            changes_activity = {
                **changes,
                "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
            }
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=80,
                preinit_changes=changes_activity,
            )
            if activity_score == 2:
                tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}_qui")] = (
                    Simulation(
                        time_unit="hr",
                        end=80,
                        preinit_changes={
                            **changes_activity,
                            "LI__f_cyp2d6": Q(
                                self.cyp2d6_inhibition["quinidine"], "dimensionless"
                            ),
                        },
                    )
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for curve in self.curves:
            observables = (
                self.plasma_observables
                if curve.tissue == Tissue.PLASMA
                else self.urine_observables
            )
            if curve.single_subject:
                reference = FitData(
                    self,
                    dataset=self.dataset_id(curve),
                    xid="time",
                    yid="value",
                    count=1,
                )
            else:
                reference = FitData(
                    self,
                    dataset=self.dataset_id(curve),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                )
            mappings[self.mapping_id(curve)] = FitMapping(
                self,
                reference=reference,
                observable=FitData(
                    self,
                    task=self.task_id(curve),
                    xid="time",
                    yid=observables[curve.substance],
                ),
                metadata=DexMappingMetaData(
                    diplotype=None,
                    tissue=curve.tissue,
                    genetic_phenotype=None,
                    metabolic_phenotype=curve.phenotype,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=(
                        Coadministration.QUINIDINE
                        if curve.quinidine
                        else Coadministration.NONE
                    ),
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        scale = "linear"
        fig = Figure(
            experiment=self,
            sid="Tab3_Fig2_Fig4",
            name=f"{self.sid}_Tab3|Fig2|Fig4",
            num_rows=4,
            num_cols=2,
        )
        plots = fig.create_plots(xaxis=Axis("time", unit=self.unit_time), legend=True)
        # rows: the substances; columns: plasma, urine
        rows = ["dex", "dor", "dor-glu", "mm"]
        yaxes = {
            "dex": [
                (self.label_dxm, self.unit_dxm),
                (self.label_dxm_ur, self.unit_dxm_ur),
            ],
            "dor": [
                (self.label_dxo, self.unit_dxo),
                (self.label_dxo_ur, self.unit_dxo_ur),
            ],
            "dor-glu": [
                (self.label_dxoglu, self.unit_dxo),
                (self.label_dxoglu_ur, self.unit_dxo_ur),
            ],
            "mm": [
                (self.label_mm, self.unit_mm),
                (self.label_mm_ur, self.unit_mm_ur),
            ],
        }
        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        for k, substance in enumerate(rows):
            observables = [
                self.plasma_observables[substance],
                self.urine_observables[substance],
            ]
            for col, observable in enumerate(observables):
                plot = plots[2 * k + col]
                label, unit = yaxes[substance][col]
                # a long label in two lines, it fits the height of a row
                if len(label) > 30:
                    label = label.replace(" (", "\n(", 1)
                plot.set_yaxis(label, unit=unit, scale=scale)
                if k < len(rows) - 1:
                    hide_xaxis_label(plot)
                for activity_score in self.activity_scores:
                    task_id = f"task_cyp2d6_activity_{activity_score}"
                    plot.add_data(
                        task=self.to_sid(task_id),
                        xid="time",
                        yid=observable,
                        label=f"AS:{activity_score}",
                        color=gstyle.color(activity_score),
                    )
                    if activity_score == 2:
                        plot.add_data(
                            task=self.to_sid(f"{task_id}_qui"),
                            xid="time",
                            yid=observable,
                            label=f"AS:{activity_score} + QUI",
                            color="black",
                        )

        # data: the group means (squares) and the single subjects (circles)
        for curve in self.curves:
            k = rows.index(curve.substance)
            plot = plots[2 * k + (0 if curve.tissue == Tissue.PLASMA else 1)]
            if curve.quinidine:
                color = "black"
            elif curve.phenotype == MetabolicPhenotype.PM:
                color = gstyle.color(0)
            else:
                color = gstyle.color(2)
            label = f"subject {curve.group}" if curve.single_subject else curve.group
            if curve.quinidine:
                label += " + QUI"
            if curve.single_subject:
                plot.add_data(
                    dataset=self.dataset_id(curve),
                    xid="time",
                    yid="value",
                    count=1,
                    label=label,
                    color=color,
                    marker="o",
                )
            else:
                plot.add_data(
                    dataset=self.dataset_id(curve),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=label,
                    color=color,
                )

        return {
            "tab3fig2fig4": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Schadel1995, output_dir="test", save_results=True)
