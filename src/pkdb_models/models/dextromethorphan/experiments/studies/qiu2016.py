"""Simulation experiment of the study Qiu2016."""

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
from sbmlsim.units import Quantity

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    fig_dex_dor_plasma,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeScoring,
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Qiu2016(DexSimulationExperiment):
    """Simulation experiment of Qiu2016.

    18 healthy Chinese volunteers (24.4 years, 60.6 kg), selected for the
    CYP2D6*10 allele, six (3 men, 3 women) of each genotype *1/*1, *1/*10 and
    *10/*10. Day 1: after an overnight fast a single oral 15 mg
    dextromethorphan hydrobromide tablet (light meals 4 and 10 hr after the
    dose), plasma from a forearm vein over 24 hr. Days 2 to 8: Zuojin pill (ZJP)
    3 g twice daily, on day 8 again 15 mg dextromethorphan hydrobromide.

    ZJP (Rhizoma Coptidis and Fructus Evodiae, 6:1) contains berberine
    (49.6 mg/g) and coptisine, which inhibit CYP2D6. It raises the AUC0-24 of
    dextromethorphan 3.00 fold in *1/*1, 1.71 fold in *1/*10 and not
    significantly in *10/*10 (Tab1). The inhibition is the constant activity
    factor `cyp2d6_inhibition["zuojin"]` after 7 days of dosing; the ZJP arms
    are validation data of the interaction.

    Fig1: plasma dextromethorphan of the three genotypes, control (day 1) and
    after ZJP (day 8) (mean, n=6).
    """

    #: the diplotypes of the genotype groups
    genotypes: ClassVar[dict[str, str]] = {
        "group1": "*1/*1",
        "group2": "*1/*10",
        "group3": "*10/*10",
    }
    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.25, 1.5, 2, 3]
    #: the body weight of the subjects (mean)
    bodyweight: ClassVar[Quantity] = Q(60.6, "kg")
    #: the Zuojin pill (3 g twice daily for 7 days) lowers the activity of
    #: CYP2D6 to 32 %: the factor at which the *1/*1 subjects of the model have
    #: the 3.00 fold AUC0-24 of dextromethorphan of this study (Tab1); berberine
    #: inhibits CYP2D6 (IC50 of berberine and coptisine 4.4 to 14.5 µM in
    #: vitro, Qiu2016)
    cyp2d6_inhibition: ClassVar[dict[str, float]] = {
        **DexSimulationExperiment.cyp2d6_inhibition,
        "zuojin": 0.32,
    }

    def task_id(self, activity_score: float, zjp: bool = False) -> str:
        """Get the id of the task of an activity score, with or without ZJP."""
        return self.to_sid(
            f"task_cyp2d6_activity_{activity_score:g}{'_zjp' if zjp else ''}"
        )

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        for label, df_label in df.groupby("label"):
            dset = DataSet.from_df(df_label, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.dxm)
            dsets[f"Fig1_{label}"] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        changes = {
            **self.default_changes(),
            "BW": self.bodyweight,
            "PODOSE_dxm": Q(15, "mg") * self.f_dxmhbr_to_dxm(),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            tcsims[self.task_id(activity_score).removeprefix("task_")] = Simulation(
                time_unit="hr",
                end=28,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )
        # the genotypes after ZJP
        for genotype in self.genotypes.values():
            activity_score = GenotypeScoring.activity_score_for_diplotype(genotype)
            tcsims[self.task_id(activity_score, zjp=True).removeprefix("task_")] = (
                Simulation(
                    time_unit="hr",
                    end=28,
                    preinit_changes={
                        **changes,
                        "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                        "LI__f_cyp2d6": Q(
                            self.cyp2d6_inhibition["zuojin"], "dimensionless"
                        ),
                    },
                )
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for group, genotype in self.genotypes.items():
            activity_score = GenotypeScoring.activity_score_for_diplotype(genotype)
            for arm, coadministration in [
                ("control", Coadministration.NONE),
                ("zuojin", Coadministration.COMEDICATION),
            ]:
                mappings[f"fm_qiu2016_dxm_{group}_{arm}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"Fig1_{group}_{arm}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=self.task_id(activity_score, zjp=arm == "zuojin"),
                        xid="time",
                        yid="[Cve_dxm]",
                    ),
                    metadata=DexMappingMetaData(
                        diplotype=genotype,
                        tissue=Tissue.PLASMA,
                        genetic_phenotype=None,
                        metabolic_phenotype=None,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=coadministration,
                        data=PKPDData.PK,
                        data_type=DataType.MEAN,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        scale = "log"
        fig, plots = fig_dex_dor_plasma(experiment=self, fig_id="Fig1", scale=scale)
        # the data end at 24 hr, the axes at the lowest data
        plots[0].set_yaxis(self.label_dxm, unit=self.unit_dxm, scale=scale, min=1e-5)
        plots[1].set_yaxis(
            f"{self.label_dxm.strip()} after ZJP\n",
            unit=self.unit_dxm,
            scale=scale,
            min=1e-5,
        )
        gstyle = GenotypeStyle(
            activities=np.array([self.activity_scores[0], self.activity_scores[-1]])
        )
        # simulations
        for activity_score in self.activity_scores:
            plots[0].add_data(
                task=self.task_id(activity_score),
                xid="time",
                yid="[Cve_dxm]",
                label=f"AS:{activity_score}",
                color=gstyle.color(activity_score),
            )
        for genotype in self.genotypes.values():
            activity_score = GenotypeScoring.activity_score_for_diplotype(genotype)
            plots[1].add_data(
                task=self.task_id(activity_score, zjp=True),
                xid="time",
                yid="[Cve_dxm]",
                label=f"AS:{activity_score} ZJP",
                color=gstyle.color(activity_score),
            )

        # data
        for group, genotype in self.genotypes.items():
            activity_score = GenotypeScoring.activity_score_for_diplotype(genotype)
            for k, arm in enumerate(["control", "zuojin"]):
                plots[k].add_data(
                    dataset=f"Fig1_{group}_{arm}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{genotype} (AS:{activity_score})",
                    color=gstyle.color(activity_score),
                )

        return {
            "fig1": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Qiu2016, output_dir="test", save_results=True)
