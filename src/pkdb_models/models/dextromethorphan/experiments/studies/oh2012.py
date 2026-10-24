"""Simulation experiment of the study Oh2012."""

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
from sbmlsim.plot import Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    fig_dex_dor_plasma,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Oh2012(DexSimulationExperiment):
    """Simulation experiment of Oh2012.

    Application of an LC-MS/MS assay: 13 healthy Korean volunteers (sex, body
    weight and CYP2D6 genotype not reported), caffeine-free for 72 hr, took one
    capsule at 09:00 with a microdose cocktail of caffeine (10 mg), losartan
    (2 mg), omeprazole (200 µg), dextromethorphan (2 mg) and midazolam
    (100 µg). The capsule was compounded for the study and the dose is given as
    "dextromethorphan 2 mg" (the hydrobromide monohydrate appears only as the
    analytical standard), so the dose is the base without a salt factor. The
    assay has no hydrolysis step, the dextrorphan is the free dextrorphan.

    Fig3D: plasma dextromethorphan and dextrorphan (mean, n=13). The dose is
    15 fold below the usual 30 mg and the cohort is not phenotyped, the curves
    are validation data of the dose.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]

    @override
    def datasets(self) -> dict[str, DataSet]:
        # the panels of Fig3 are curated in one table, D is dextromethorphan
        dframes = self.load_dataframes_by_substance("Fig3")
        dsets = {}
        for substance, key, mr in [
            ("dextromethorphan", "dxm", self.Mr.dxm),
            ("dextrorphan", "dxo", self.Mr.dxo),
        ]:
            dset = DataSet.from_df(dframes[substance], self.ureg)
            dset.unit_conversion("mean", 1 / mr)
            dsets[f"Fig3D_{key}"] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        # the base, the publication names no salt
        PODOSE = Q(2, "mg")

        changes = {
            **self.default_changes(),
            "PODOSE_dxm": PODOSE,
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=15,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        sids = ["dxm", "dxo"]
        for sid in sids:
            mappings[f"fm_oh2012_{sid}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig3D_{sid}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_cyp2d6_activity_2",
                    xid="time",
                    yid=f"[Cve_{sid}]",
                ),
                metadata=DexMappingMetaData(
                    diplotype=None,
                    tissue=Tissue.PLASMA,
                    genetic_phenotype=None,
                    metabolic_phenotype=None,
                    route=Route.PO,
                    application_form=ApplicationForm.CAPSULE,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.COCKTAIL,
                    data=PKPDData.PK,
                    data_type=DataType.MEAN,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plots = fig_dex_dor_plasma(experiment=self, fig_id="Fig3D", scale="log")
        # the axes at the lowest data, the poor metabolizer is 40 fold above
        plots[0].set_yaxis(self.label_dxm, unit=self.unit_dxm, scale="log", min=1e-5)
        plots[1].set_yaxis(self.label_dxo, unit=self.unit_dxo, scale="log", min=1e-5)
        # data
        sids = ["dxm", "dxo"]
        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        for activity_score in self.activity_scores:
            task_id = f"task_cyp2d6_activity_{activity_score}"
            for i, sid in enumerate(sids):
                plots[i].add_data(
                    task=self.to_sid(task_id),
                    xid="time",
                    yid=f"[Cve_{sid}]",
                    label=f"AS:{activity_score}",
                    color=gstyle.color(activity_score),
                )
        for i, sid in enumerate(sids):
            plots[i].add_data(
                dataset=f"Fig3D_{sid}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="all (not phenotyped)",
                color="black",
                alpha=1,
            )

        return {
            "fig3d": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Oh2012, output_dir="test", save_results=True)
