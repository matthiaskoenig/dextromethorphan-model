"""Simulation experiment of the study Eichhold1997."""

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


class Eichhold1997(DexSimulationExperiment):
    """Simulation experiment of Eichhold1997.

    One healthy male volunteer (39 years), overnight fasted, a single oral dose
    of 15 ml of a cough syrup (Vicks 44) with 30 mg dextromethorphan
    hydrobromide. Plasma of dextromethorphan and free dextrorphan over 24 hr
    (Fig6). The subject was an extensive metabolizer ("with the peak DEX plasma
    level being < 500 pg/ml", p. 1210); neither the genotype nor the body weight
    are reported.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]

    #: the series of Fig6 by substance: (key of the data, observable); the
    #: plasma metabolic ratio is the phenotype of the subject
    series: ClassVar[dict[str, tuple[str, str]]] = {
        "dextromethorphan": ("dex", "[Cve_dxm]"),
        "dextrorphan": ("dor", "[Cve_dxo]"),
        "dmt/dtf": ("mr", "dxm_dxo"),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig6"]:
            for substance, df in self.load_dataframes_by_substance(fig_id).items():
                if substance not in self.series:
                    continue
                dset = DataSet.from_df(df, self.ureg)
                if substance == "dextromethorphan":
                    dset.unit_conversion("value", 1 / self.Mr.dxm)
                elif substance == "dextrorphan":
                    dset.unit_conversion("value", 1 / self.Mr.dxo)
                sid = self.series[substance][0]
                dsets[self.to_sid(f"{fig_id}_{sid}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": Q(30, "mg") * self.f_dxmhbr_to_dxm(),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }

        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=28,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for sid, observable in self.series.values():
            mappings[f"fm_eichhold1997_{sid}_em"] = FitMapping(
                self,
                reference=FitData(
                    self, dataset=f"Fig6_{sid}", xid="time", yid="value", count=1
                ),
                observable=FitData(
                    self, task="task_cyp2d6_activity_2", xid="time", yid=observable
                ),
                metadata=DexMappingMetaData(
                    diplotype=None,
                    tissue=Tissue.PLASMA,
                    genetic_phenotype=None,
                    metabolic_phenotype=MetabolicPhenotype.EM,
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
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig6",
            name=f"{self.sid}_Fig6",
            num_rows=3,
        )
        plots = fig.create_plots(xaxis=Axis("time", unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_dxm, unit=self.unit_dxm, scale="log")
        plots[1].set_yaxis(self.label_dxo, unit=self.unit_dxo)
        plots[2].set_yaxis(self.label_mr_plasma, unit=self.unit_dimless, scale="log")
        for plot in plots[:2]:
            hide_xaxis_label(plot)

        gstyle = GenotypeStyle(
            activities=np.array([self.activity_scores[0], self.activity_scores[-1]])
        )
        for activity_score in self.activity_scores:
            task_id = f"task_cyp2d6_activity_{activity_score}"
            for k, (_, observable) in enumerate(self.series.values()):
                # simulations
                plots[k].add_data(
                    task=self.to_sid(task_id),
                    xid="time",
                    yid=observable,
                    label=f"AS:{activity_score}",
                    color=gstyle.color(activity_score),
                )

        # data
        for k, (sid, _) in enumerate(self.series.values()):
            plots[k].add_data(
                dataset=f"Fig6_{sid}",
                xid="time",
                yid="value",
                count=1,
                label="EM",
                color=gstyle.color(2),
            )

        return {"fig6": fig}


if __name__ == "__main__":
    MODEL.run_experiments(Eichhold1997, output_dir="test", save_results=True)
