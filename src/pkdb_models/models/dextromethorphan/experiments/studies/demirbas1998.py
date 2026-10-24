"""Simulation experiment of the study Demirbas1998."""

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
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    fig_dor_total,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Demirbas1998(DexSimulationExperiment):
    """Simulation experiment of Demirbas1998.

    Six healthy men (66-84 kg, not phenotyped), fasted overnight, three way
    crossover. Treatment A: two sustained release tablets of 30 mg
    dextromethorphan hydrobromide and 600 mg guaifenesin (60 mg DXM-HBr and
    1200 mg guaifenesin); treatment B: 10 ml of the sustained release
    suspension Delsym (30 mg/5 ml, 60 mg DXM-HBr). One dose on day 1, then the
    same dose every 12 hr on days 2 to 6 (9 doses, the last at 120 hr). The
    total dextrorphan (free and conjugated, "conjugated dextrorphan was
    prevailing") was measured in plasma on day 1 (0-24 hr) and day 6
    (120-144 hr); the curation labels the day 6 profile `day5`.

    Both products release dextromethorphan slowly (tmax 3.7-5.2 hr, MRT
    6.3 hr), which the immediate release of the model does not describe: the
    data validate a limitation of the model. Guaifenesin does not change the
    pharmacokinetics (relative bioavailability 110-113 %, p > 0.05), so A and
    B are the same simulation.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]
    #: the curves of the data by their label in the curation, which labels the
    #: profile of day 6 `day5`
    curves: ClassVar[dict[str, str]] = {
        "A_day1": "A_day1",
        "A_day5": "A_day6",
        "B_day1": "B_day1",
        "B_day5": "B_day6",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig2")
        for label, df_label in df.groupby("label"):
            dset = DataSet.from_df(df_label, self.ureg)
            # total dextrorphan in dextrorphan equivalents
            dset.unit_conversion("mean", 1 / self.Mr.dxo)
            dsets[self.to_sid(f"Fig2_{self.curves[str(label)]}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        # 60 mg dextromethorphan hydrobromide per administration
        dose = Q(60, "mg") * self.f_dxmhbr_to_dxm()
        # day 1 one dose, days 2 to 6 every 12 hr (9 doses, the last at 120 hr)
        dose_times = [24 + 12 * k for k in range(9)]
        tcsims = {}
        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=dose_times[-1] + 27,
                preinit_changes={
                    **self.default_changes(),
                    "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
                    "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                    "PODOSE_dxm": dose,
                },
                changes=[self.add_doses(dose_times, {"PODOSE_dxm": dose})],
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        coadministrations = {
            "A": Coadministration.GUAIFENESIN,
            "B": Coadministration.NONE,
        }
        for curve in self.curves.values():
            treatment, day = curve.split("_")
            mappings[self.to_sid(f"fm_demirbas1998_dxo_total_{curve}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig2_{curve}"),
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_cyp2d6_activity_2",
                    xid="time",
                    yid="dxo_total",
                ),
                metadata=DexMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    # the profile of day 1 follows the first dose
                    dosing=Dosing.SINGLE if day == "day1" else Dosing.MULTIPLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=coadministrations[treatment],
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plot = fig_dor_total(experiment=self, fig_id="Fig2")
        gstyle = GenotypeStyle(
            activities=np.array([self.activity_scores[0], self.activity_scores[-1]])
        )
        for activity_score in self.activity_scores:
            plot.add_data(
                task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                xid="time",
                yid="dxo_total",
                label=f"AS:{activity_score}",
                color=gstyle.color(activity_score),
            )
        styles = {
            "A": ("A: tablet, DXM and guaifenesin", "^"),
            "B": ("B: suspension, DXM", "s"),
        }
        for curve in self.curves.values():
            treatment, day = curve.split("_")
            label, marker = styles[treatment]
            plot.add_data(
                dataset=self.to_sid(f"Fig2_{curve}"),
                xid="time",
                yid="mean",
                count="count",
                label=label if day == "day1" else None,
                marker=marker,
                color="black",
            )
        return {
            "fig2": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Demirbas1998, output_dir="test", save_results=True)
