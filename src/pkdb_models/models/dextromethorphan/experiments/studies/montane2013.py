"""Simulation experiment of the study Montane2013."""

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


class Montane2013(DexSimulationExperiment):
    """Simulation experiment of Montane2013.

    A single oral dose of 30 mg dextromethorphan hydrobromide (11.56 g of
    Benylin cough suppressant, adult formula, Parke Davis) with a glass of
    water after voiding to 270 healthy Trinidadians (103 Afro-, 167
    Indo-Trinidadians), fasted at the dose (breakfast 30 min after it), urine
    over 5 hr. Dextromethorphan and dextrorphan by HPLC with a hydrolysis by
    beta-glucuronidase, i.e. the metabolic ratio DXM/(DXO+DXOGLU) of every
    subject by CYP2D6 diplotype (Fig3). The syrup is simulated with the
    dissolution of the model (a fit parameter, which a study does not change);
    the ratio hardly depends on it.

    One simulation per diplotype. The tandem alleles have the activity scores
    of Tab3 of the publication (*13+*1 1, *36+*10x2 1) and are simulated with
    the activity score of the diplotype. The diplotypes with *45 or *46 (n=6)
    are not simulated: the publication gives the allele the activity score 1
    (Tab3) and 0.5 (text, Tab5). The data are 228 of the 270 subjects (dense
    rows of the figure not digitized). A cross-sectional genotype-phenotype
    cohort: validation of a population.
    """

    #: genotypes of Fig3 which are not simulated, the activity score of the
    #: *45/*46 allele is not defined by the publication
    exclude_genotypes: ClassVar[set[str]] = {
        "*1/*45 or 46",
        "*29/*45 or 46",
    }
    #: activity scores of the diplotypes with tandem alleles (Tab3 of the
    #: publication: *13+*1 1, *36+*10x2 1, *2 1, *4 0), which the scores of
    #: the alleles of the model do not have
    custom_activity_scores: ClassVar[dict[str, float]] = {
        "*13+*1/*4": 1.0,
        "*2/*36+*10x2": 2.0,
    }
    #: diplotype by diplotype key, sorted by decreasing activity score; set by
    #: `datasets`
    genotype_mapping: dict[str, str]

    def activity_score(self, genotype: str) -> float:
        """Get the activity score of a diplotype."""
        if genotype in self.custom_activity_scores:
            return self.custom_activity_scores[genotype]
        return GenotypeScoring.activity_score_for_diplotype(genotype)

    @override
    def datasets(self) -> dict[str, DataSet]:
        df = self.load_dataframes_by_substance("Fig3")["(dmt)/(dtf+dtfglu)"]
        df = df[~df["cyp2d6_genotype"].isin(self.exclude_genotypes)].copy()
        # the order of the simulations and of the plot
        df["activities"] = df["cyp2d6_genotype"].apply(self.activity_score)
        df.sort_values(by=["activities"], ascending=False, inplace=True)
        self.genotype_mapping = {
            GenotypeScoring.diplotype_to_string(genotype): genotype
            for genotype in df["cyp2d6_genotype"].unique()
        }
        dsets = {}
        for genotype, dset_group in df.groupby("cyp2d6_genotype"):
            dset_group["time_jitter"] = jitter(dset_group["time"], 0.1)
            dset_group["time_jitter_unit"] = dset_group["time_unit"]
            key = GenotypeScoring.diplotype_to_string(str(genotype))
            dsets[self.to_sid(f"Fig3_{key}")] = DataSet.from_df(dset_group, self.ureg)
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": Q(30, "mg") * self.f_dxmhbr_to_dxm(),
        }
        tcsims: dict[str, Simulation] = {}
        for genotype_key, genotype in self.genotype_mapping.items():
            if genotype in self.custom_activity_scores:
                genotype_changes = {
                    "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
                    "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
                    "LI__cyp2d6_ac": Q(
                        self.custom_activity_scores[genotype], "dimensionless"
                    ),
                }
            else:
                indexes = GenotypeScoring.indices_for_diplotype(genotype)
                genotype_changes = {
                    "LI__cyp2d6_allele1": Q(indexes[0], "dimensionless"),
                    "LI__cyp2d6_allele2": Q(indexes[1], "dimensionless"),
                }
            tcsims[self.to_sid(f"cyp2d6_activity_{genotype_key}")] = Simulation(
                time_unit="hr",
                end=6.5,
                preinit_changes={**changes, **genotype_changes},
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        for genotype_key, genotype in self.genotype_mapping.items():
            activity_score = self.activity_score(genotype)
            mappings[self.to_sid(f"fm_montane2013_{genotype_key}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig3_{genotype_key}"),
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
                    genetic_phenotype=GenotypeScoring.genetic_phenotype_for_activity_score(
                        activity_score
                    ),
                    activity_score=activity_score,
                    tissue=Tissue.URINE,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.NONE,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plots = fig_mrtot_urine(experiment=self, fig_id="Fig3")
        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        # one legend entry per activity score
        labeled: set[float] = set()
        for genotype_key, genotype in self.genotype_mapping.items():
            activity_score = self.activity_score(genotype)
            plots[0].add_data(
                dataset=self.to_sid(f"Fig3_{genotype_key}"),
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
            "fig3": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Montane2013, output_dir="test", save_results=True)
