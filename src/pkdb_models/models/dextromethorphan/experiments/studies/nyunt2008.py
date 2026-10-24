"""Simulation experiment of the study Nyunt2008."""

from typing import ClassVar, override

import numpy as np
from pkpdsim.metadata import (
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
from sbmlsim.plot import Figure
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


class Nyunt2008(DexSimulationExperiment):
    """Simulation experiment of Nyunt2008.

    Open-label sequential study of 12 healthy subjects (9 African American, 3
    Caucasian, 3 women, 22-53 years, body weight not reported): after an
    overnight fast a single oral dose of 5 mg midazolam and 30 mg
    dextromethorphan (breakfast 2 hr after the dose), on day 1 alone and on day
    9 after AMD070 200 mg twice daily. The product is not named; 30 mg is the
    usual unit of the hydrobromide and the salt factor is applied (the curation
    gives the base). Subjects with a poor or ultrarapid CYP2D6 genotype
    (AmpliChip) were excluded, the 12 are extensive or intermediate
    metabolizers by genotype; the genotypes are not reported.

    Fig1: plasma dextromethorphan without AMD070 (mean, n=12). The AMD070 arm
    (AUC x2.86, attributed to the bioavailability) is not digitized.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dframes = self.load_dataframes_by_substance("Fig1")
        dset = DataSet.from_df(dframes["dextromethorphan"], self.ureg)
        dset.unit_conversion("mean", 1 / self.Mr.dxm)
        return {"Fig1_dxm": dset}

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        # 30 mg of the hydrobromide (the salt is not named)
        PODOSE = Q(30, "mg") * self.f_dxmhbr_to_dxm()

        changes = {
            **self.default_changes(),
            "PODOSE_dxm": PODOSE,
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=30,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        return {
            "fm_nyunt2008_dxm": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_dxm",
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
                    tissue=Tissue.PLASMA,
                    # extensive or intermediate metabolizers by genotype
                    # (poor and ultrarapid excluded), not reported per subject
                    genetic_phenotype=None,
                    metabolic_phenotype=None,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    # midazolam 5 mg, which does not change CYP2D6
                    coadministration=Coadministration.COCKTAIL,
                    data=PKPDData.PK,
                    data_type=DataType.MEAN,
                ),
            )
        }

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plot = fig_dex(experiment=self, fig_id="Fig1", scale="log")
        # the data end at 24 hr, the axis at the lowest data
        plot.set_yaxis(self.label_dxm, unit=self.unit_dxm, scale="log", min=1e-4)
        # simulations
        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        for activity_score in self.activity_scores:
            task_id = f"task_cyp2d6_activity_{activity_score}"
            plot.add_data(
                task=self.to_sid(task_id),
                xid="time",
                yid="[Cve_dxm]",
                label=f"AS:{activity_score}",
                color=gstyle.color(activity_score),
            )

        # data
        plot.add_data(
            dataset="Fig1_dxm",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="gEM/gIM",
            color=gstyle.color(2),
        )

        return {
            "fig1": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Nyunt2008, output_dir="test", save_results=True)
