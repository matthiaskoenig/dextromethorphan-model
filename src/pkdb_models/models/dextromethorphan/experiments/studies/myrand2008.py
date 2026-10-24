"""Simulation experiment of the study Myrand2008."""

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


class Myrand2008(DexSimulationExperiment):
    """Simulation experiment of Myrand2008.

    A multi-drug cocktail to healthy non-smoking men of six populations (native,
    first- and third-generation Japanese, Koreans, Chinese, Caucasians): on
    day 2 dextromethorphan 30 mg orally with caffeine, omeprazole and
    chlorzoxazone (none of them inhibits CYP2D6), urine over 12 hr. The
    publication writes "dextromethorphan 30 mg" without the salt; 30 mg of the
    hydrobromide is the phenotyping dose of the other studies (Jones1996,
    Lopez2005, Montane2013), so the dose is the hydrobromide (the curation has
    the base). The formulation and fasting are not reported, the dose is
    simulated with the dissolution of the model. The metabolic ratio is
    curated as DXM/(DXO+DXOGLU); the main text does not describe a
    hydrolysis of the conjugates (supplementary material).

    One simulation per CYP2D6 diplotype (Fig5). The data are 413 of about 630
    subjects of four populations (Caucasians, Chinese, Koreans, native
    Japanese), the dense rows of the figure are incomplete and the subjects
    below the axis limit of the figure (MR 3.2e-4) are censored. A
    cross-sectional genotype-phenotype cohort: validation of a population.
    """

    #: diplotype by diplotype key, sorted by decreasing activity score; set by
    #: `datasets`
    genotype_mapping: dict[str, str]

    @override
    def datasets(self) -> dict[str, DataSet]:
        df = self.load_dataframes_by_substance("Fig5")["(dmt)/(dtf+dtfglu)"].copy()
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
            dsets[self.to_sid(f"Fig5_{key}")] = DataSet.from_df(dset_group, self.ureg)
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
                end=14.5,
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
            mappings[self.to_sid(f"fm_myrand2008_{genotype_key}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig5_{genotype_key}"),
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
                    coadministration=Coadministration.COCKTAIL,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plots = fig_mrtot_urine(experiment=self, fig_id="Fig5")
        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        # one legend entry per activity score
        labeled: set[float] = set()
        for genotype_key, genotype in self.genotype_mapping.items():
            activity_score = GenotypeScoring.activity_score_for_diplotype(genotype)
            plots[0].add_data(
                dataset=self.to_sid(f"Fig5_{genotype_key}"),
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
            "fig5": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Myrand2008, output_dir="test", save_results=True)
