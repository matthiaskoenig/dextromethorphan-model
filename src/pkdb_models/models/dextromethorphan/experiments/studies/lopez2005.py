"""Simulation experiment of the study Lopez2005."""

from typing import override

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
    jitter,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    fig_mrtot_urine,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeScoring,
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Lopez2005(DexSimulationExperiment):
    """Simulation experiment of Lopez2005.

    A single oral dose of 30 mg dextromethorphan hydrobromide as syrup
    (300 mg/100 ml, Laboratorios Euromex) to 100 healthy Mexican Mestizos
    (of 243 genotyped), urine over 8 hr. Dextromethorphan and dextrorphan by
    HPLC with a hydrolysis by beta-glucuronidase (Ducharme1996), i.e. the
    metabolic ratio DXM/(DXO+DXOGLU) of every subject by CYP2D6 diplotype
    (Fig2). Fasting is not reported. The syrup is simulated with the
    dissolution of the model (a fit parameter, which a study does not
    change); the ratio hardly depends on it.

    One simulation per diplotype. The data are 88 of the 100 subjects, 7 of
    *1/*1 and 5 of *1/*2 overlap in the figure and were not digitized. A
    cross-sectional genotype-phenotype cohort: validation of a population.
    """

    #: diplotype by diplotype key, sorted by decreasing activity score; set by
    #: `datasets`
    genotype_mapping: dict[str, str]

    @override
    def datasets(self) -> dict[str, DataSet]:
        df = self.load_dataframes_by_substance("Fig2")["(dmt)/(dtf+dtfglu)"].copy()
        # the order of the simulations and of the plot
        df["activities"] = df["cyp2d6_genotype"].apply(
            GenotypeScoring.activity_score_for_diplotype
        )
        df.sort_values(by=["activities"], inplace=True, ascending=False)
        self.genotype_mapping = {
            GenotypeScoring.diplotype_to_string(genotype): genotype
            for genotype in df["cyp2d6_genotype"].unique()
        }
        dsets = {}
        for genotype, dset_group in df.groupby("cyp2d6_genotype"):
            dset_group["time_jitter"] = jitter(dset_group["time"], 0.1)
            dset_group["time_jitter_unit"] = dset_group["time_unit"]
            key = GenotypeScoring.diplotype_to_string(str(genotype))
            dsets[self.to_sid(f"Fig2_{key}")] = DataSet.from_df(dset_group, self.ureg)
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": Q(30, "mg") * self.f_dxmhbr_to_dxm(),
        }
        tcsims: dict[str, Simulation] = {}
        for genotype_key, genotype in self.genotype_mapping.items():
            genotype_indexes = GenotypeScoring.indices_for_diplotype(genotype)
            tcsims[self.to_sid(f"cyp2d6_activity_{genotype_key}")] = Simulation(
                time_unit="hr",
                end=10,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_allele1": Q(genotype_indexes[0], "dimensionless"),
                    "LI__cyp2d6_allele2": Q(genotype_indexes[1], "dimensionless"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        for genotype_key, genotype in self.genotype_mapping.items():
            mappings[self.to_sid(f"fm_lopez2005_{genotype_key}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig2_{genotype_key}"),
                    xid="time",
                    yid="value",
                    count=1,
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_cyp2d6_activity_{genotype_key}"),
                    xid="time",
                    yid="dxm_dxo_total_urine",
                ),
                metadata=DexMappingMetaData(
                    diplotype=genotype,
                    tissue=Tissue.URINE,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.NONE,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plots = fig_mrtot_urine(experiment=self, fig_id="Fig2")
        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        # one legend entry per activity score
        labeled: set[float] = set()
        for genotype_key, genotype in self.genotype_mapping.items():
            activity_score = GenotypeScoring.activity_score_for_diplotype(genotype)
            plots[0].add_data(
                dataset=self.to_sid(f"Fig2_{genotype_key}"),
                xid="time_jitter",
                yid="value",
                single_lines=True,
                label=f"AS {activity_score}" if activity_score not in labeled else None,
                color=gstyle.color(activity_score),
                linestyle="",
                alpha=1,
            )
            labeled.add(activity_score)
            plots[0].add_data(
                task=self.to_sid(f"task_cyp2d6_activity_{genotype_key}"),
                xid="time",
                yid="dxm_dxo_total_urine",
                label=None,
                color=gstyle.color(activity_score),
            )

        return {
            "fig2": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Lopez2005, output_dir="test", save_results=True)
