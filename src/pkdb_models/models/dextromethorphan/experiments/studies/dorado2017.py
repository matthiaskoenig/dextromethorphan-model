"""Simulation experiment of the study Dorado2017."""

from typing import override

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
    jitter,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeScoring,
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


def diplotype_of_genotype(genotype: str) -> str:
    """Get the diplotype of the model for a CYP2D6 genotype of the study.

    The study did not determine the copy number of a duplicated allele
    (`*1xN`, `*2xN`) and scores a duplication of a functional allele as 2
    (Gaedigk2008), the score of two copies (`*1x2`, `*2x2`).
    """
    return genotype.replace("xN", "x2")


class Dorado2017(DexSimulationExperiment):
    """Simulation experiment of Dorado2017.

    174 unrelated healthy Cuban volunteers (60.1 +- 11.2 kg), fasted for at
    least 8 hr, a single oral dose of 15 mg dextromethorphan (Romilar, Bayer
    Hispania, a dextromethorphan hydrobromide product), urine collected 0-8 hr.
    The urine was hydrolyzed with beta-glucuronidase, so the metabolic ratio
    DM/DX of every subject (Fig 3, one point per subject, 161 of the 174 are
    digitized) is the ratio of the total (free and conjugated) analytes. The
    subjects are grouped by their CYP2D6 genotype; the urinary concentrations
    of Tab 2 are not used, the urine volumes are not reported.
    """

    #: key of the CYP2D6 diplotypes (sorted by activity score), set by `datasets`
    gmap: dict[str, str]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig3")
        df["cyp2d6_genotype"] = df["cyp2d6_genotype"].apply(diplotype_of_genotype)
        df["time_jitter"] = jitter(df["time"], 0.1)
        df["time_jitter_unit"] = df["time_unit"]
        genotypes = sorted(
            df["cyp2d6_genotype"].unique(),
            key=GenotypeScoring.activity_score_for_diplotype,
        )
        self.gmap = {
            genotype: GenotypeScoring.diplotype_to_string(genotype)
            for genotype in genotypes
        }
        for genotype, df_genotype in df.groupby("cyp2d6_genotype"):
            dset = DataSet.from_df(df_genotype, self.ureg)
            dsets[self.to_sid(f"Fig3_{self.gmap[str(genotype)]}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        changes = {
            **self.default_changes(),
            # 15 mg dextromethorphan hydrobromide
            "PODOSE_dxm": Q(15, "mg") * self.f_dxmhbr_to_dxm(),
        }
        for genotype, genotype_key in self.gmap.items():
            indices = GenotypeScoring.indices_for_diplotype(genotype)
            tcsims[self.to_sid(f"cyp2d6_activity_{genotype_key}")] = Simulation(
                time_unit="hr",
                end=10,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_allele1": Q(indices[0], "dimensionless"),
                    "LI__cyp2d6_allele2": Q(indices[1], "dimensionless"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        for diplotype, diplotype_key in self.gmap.items():
            mappings[self.to_sid(f"fm_dorado2017_mr_total_urine_{diplotype_key}")] = (
                FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig3_{diplotype_key}"),
                        xid="time",
                        yid="value",
                        count=1,
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(f"task_cyp2d6_activity_{diplotype_key}"),
                        xid="time",
                        yid="dxm_dxo_total_urine",
                    ),
                    metadata=DexMappingMetaData(
                        diplotype=diplotype,
                        tissue=Tissue.URINE,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                    ),
                )
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(experiment=self, sid="Fig3", name=f"{self.sid}_Fig3", num_rows=1)
        plots = fig.create_plots(xaxis=Axis("time", unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_mrtot_urine, unit=self.unit_dimless, scale="log")
        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        # one legend entry per activity score, the diplotypes of a score give
        # the same simulation
        labeled: set[float] = set()
        for genotype, genotype_key in self.gmap.items():
            activity_score = GenotypeScoring.activity_score_for_diplotype(genotype)
            plots[0].add_data(
                task=self.to_sid(f"task_cyp2d6_activity_{genotype_key}"),
                xid="time",
                yid="dxm_dxo_total_urine",
                label=None if activity_score in labeled else f"AS:{activity_score}",
                color=gstyle.color(activity_score),
            )
            labeled.add(activity_score)
        # the subjects of a diplotype
        for genotype, genotype_key in self.gmap.items():
            activity_score = GenotypeScoring.activity_score_for_diplotype(genotype)
            plots[0].add_data(
                dataset=self.to_sid(f"Fig3_{genotype_key}"),
                xid="time_jitter",
                yid="value",
                single_lines=True,
                color=gstyle.color(activity_score),
                linestyle="",
                alpha=1,
            )
        return {
            "fig3": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Dorado2017, output_dir="test", save_results=True)
