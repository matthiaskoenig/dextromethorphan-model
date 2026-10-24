"""Simulation experiment of the study Tamminga2001b."""

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


class Tamminga2001b(DexSimulationExperiment):
    """Simulation experiment of Tamminga2001b.

    Healthy Dutch volunteers, genotyped for CYP2D6 and phenotyped with a
    cocktail of mephenytoin 100 mg, dextromethorphan 22 mg and caffeine
    100 mg; the urinary metabolic ratio DXM/(DXO + DXOGLU) over 8 hr by
    genotype (Fig1, single subjects; 191 of the 634 subjects of the figure
    are digitized). The 22 mg of the publication are the base, 30 mg of the
    hydrobromide monohydrate. Every point is one subject (count 1).
    """

    def genotype_mapping(self) -> dict[str, int]:
        """Get the index of the genotypes, sorted by decreasing activity score."""
        df = self.load_dataframe("Fig1")
        activities = {
            genotype: GenotypeScoring.activity_score_for_diplotype(genotype)
            for genotype in df["cyp2d6_genotype"].unique()
        }
        genotypes = sorted(activities, key=lambda g: (-activities[g], g))
        return {genotype: k for k, genotype in enumerate(genotypes)}

    @override
    def datasets(self) -> dict[str, DataSet]:
        df = self.load_dataframe("Fig1")
        genotype_mapping = self.genotype_mapping()
        dsets = {}
        for genotype, df_genotype in df.groupby("cyp2d6_genotype"):
            df_genotype = df_genotype.copy()
            df_genotype["time_jitter"] = jitter(df_genotype["time"], 0.1)
            df_genotype["time_jitter_unit"] = df_genotype["time_unit"]
            # single subjects
            df_genotype["count"] = 1
            dsets[f"Fig1_{genotype_mapping[str(genotype)]}"] = DataSet.from_df(
                df_genotype, self.ureg
            )
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}

        changes = {
            **self.default_changes(),
            # the base
            "PODOSE_dxm": Q(22, "mg"),
        }

        for genotype, index in self.genotype_mapping().items():
            genotype_indexes = GenotypeScoring.indices_for_diplotype(genotype)
            tcsims[f"cyp2d6_activity_{index}"] = Simulation(
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
        mappings = {}
        for genotype, index in self.genotype_mapping().items():
            # e.g. fm_tamminga2001b_1_4 of *1/*4
            key = genotype.replace("*", "").replace("/", "_")
            mappings[self.to_sid(f"fm_tamminga2001b_{key}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig1_{index}",
                    xid="time",
                    yid="value",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=f"task_cyp2d6_activity_{index}",
                    xid="time",
                    yid="dxm_dxo_total_urine",
                ),
                metadata=DexMappingMetaData(
                    diplotype=genotype,
                    tissue=Tissue.URINE,
                    genetic_phenotype=None,
                    metabolic_phenotype=None,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.COCKTAIL,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plots = fig_mrtot_urine(experiment=self, fig_id="Fig1")
        gstyle = GenotypeStyle(activities=np.array([0.0, 3]))
        # the number of subjects of a genotype
        n_subjects = self.load_dataframe("Fig1")["cyp2d6_genotype"].value_counts()
        for genotype, index in self.genotype_mapping().items():
            activity_score = GenotypeScoring.activity_score_for_diplotype(genotype)
            plots[0].add_data(
                dataset=f"Fig1_{index}",
                xid="time_jitter",
                yid="value",
                single_lines=True,
                label=f"{genotype} AS:{activity_score} (n={n_subjects[genotype]})",
                color=gstyle.color(activity_score),
                linestyle="",
                alpha=1,
            )

            task_id = f"task_cyp2d6_activity_{index}"
            plots[0].add_data(
                task=task_id,
                xid="time",
                yid="dxm_dxo_total_urine",
                label=None,
                color=gstyle.color(activity_score),
            )

        return {
            "fig1": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Tamminga2001b, output_dir="test", save_results=True)
