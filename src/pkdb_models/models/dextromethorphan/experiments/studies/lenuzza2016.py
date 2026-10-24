"""Simulation experiment of the study Lenuzza2016."""

import math
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
    fig_dex_dor_plasma,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeScoring,
    GenotypeStyle,
    MetabolicPhenotype,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Lenuzza2016(DexSimulationExperiment):
    """Simulation experiment of Lenuzza2016.

    The CIME cocktail (acetaminophen, repaglinide, dextromethorphan 18 mg,
    digoxin, memantine, midazolam, omeprazole, rosuvastatin, tolbutamide,
    caffeine) as a single oral dose with 200 ml water after an overnight fast
    (fasted for 2 hr after the dose) to 10 healthy Caucasians. The publication
    writes "dextromethorphan 18 mg" and names no salt, the dose is simulated
    as the base. Plasma dextromethorphan and free dextrorphan by LC-MS/MS
    without a hydrolysis (Fig1, individual curves).

    CYP2D6 genotypes: *1/*1 n=5, *1/*3, *1/*4 n=2, *1/*6, *4/*5. The poor
    metabolizer (*4/*5, the open circles of Fig1, the curve 1 of the data,
    "subject 4" of the text) is simulated with its diplotype. The curves of
    the 9 extensive metabolizers are not assigned to their genotypes (5 with
    the activity score 2, 4 heterozygous with 1, one wild type behaves like an
    intermediate metabolizer, MR 1.49), so they are simulated with the mean
    activity score of their genotypes (14/9) and are validation data of a
    population. The authors set the last value below the limit of
    quantification of the ascending and the first of the descending phase to
    half of it, which is why several curves end flat at 0.2 to 0.3 ng/ml.
    """

    #: the diplotype of the poor metabolizer
    diplotype_pm: ClassVar[str] = "*4/*5"
    #: the mean activity score of the genotypes of the 9 extensive
    #: metabolizers: 5 *1/*1 (2) and *1/*3, *1/*4 (2), *1/*6 (1)
    activity_score_em: ClassVar[float] = (5 * 2 + 4 * 1) / 9
    #: the activity scores of the genotypes of the extensive metabolizers
    #: (figure)
    activity_scores_em: ClassVar[list[float]] = [1.0, 2.0]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        dframes = self.load_dataframes_by_substance("Fig1")
        for substance, mr in [
            ("dextromethorphan", self.Mr.dxm),
            ("dextrorphan", self.Mr.dxo),
        ]:
            for label, df_label in dframes[substance].groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("value", 1 / mr)
                dsets[self.to_sid(str(label))] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": Q(18, "mg"),
        }
        custom = {
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        indexes = GenotypeScoring.indices_for_diplotype(self.diplotype_pm)
        activity_scores = {
            "em": self.activity_score_em,
            **{f"as{a}": a for a in self.activity_scores_em},
        }
        tcsims: dict[str, Simulation] = {
            "pm": Simulation(
                time_unit="hr",
                end=30,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_allele1": Q(indexes[0], "dimensionless"),
                    "LI__cyp2d6_allele2": Q(indexes[1], "dimensionless"),
                },
            )
        }
        for key, activity_score in activity_scores.items():
            tcsims[self.to_sid(key)] = Simulation(
                time_unit="hr",
                end=30,
                preinit_changes={
                    **changes,
                    **custom,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )
        return tcsims

    @staticmethod
    def phenotype(subject_index: int) -> MetabolicPhenotype:
        """Get the phenotype of a curve of Fig1, the first is the poor metabolizer."""
        return MetabolicPhenotype.PM if subject_index == 1 else MetabolicPhenotype.EM

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        for subject_index in range(1, 11):
            phenotype = self.phenotype(subject_index)
            is_pm = phenotype == MetabolicPhenotype.PM
            task = "task_pm" if is_pm else "task_em"
            # the dataset labels of the data use dex/dor, the model dxm/dxo
            for substance_key, sid in [("dex", "dxm"), ("dor", "dxo")]:
                dataset = f"Fig1_{substance_key}_{subject_index}"
                key = f"fm_lenuzza2016_{sid}_{subject_index}"
                mappings[self.to_sid(key)] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(dataset),
                        xid="time",
                        yid="value",
                        count=1,
                    ),
                    observable=FitData(self, task=task, xid="time", yid=f"[Cve_{sid}]"),
                    metadata=DexMappingMetaData(
                        diplotype=self.diplotype_pm if is_pm else None,
                        activity_score=(math.nan if is_pm else self.activity_score_em),
                        tissue=Tissue.PLASMA,
                        metabolic_phenotype=phenotype,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.COCKTAIL,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plots = fig_dex_dor_plasma(experiment=self, fig_id="Fig1", scale="log")
        plots[1].set_yaxis(self.label_dxo, unit=self.unit_dxo, scale="log")
        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        # the extensive metabolizers in the color of the activity score 2, the
        # color of their mean (1.56) is too light
        color_em = gstyle.color(2.0)
        observables = ["[Cve_dxm]", "[Cve_dxo]"]

        # simulations: the poor metabolizer, the mean of the extensive
        # metabolizers and the activity scores of their genotypes
        curves = [
            ("task_pm", 0.0, f"PM {self.diplotype_pm}", "-"),
            ("task_em", None, "EM mean AS 1.56", "-"),
            *[
                (self.to_sid(f"task_as{a}"), a, f"AS {a}", ":")
                for a in self.activity_scores_em
            ],
        ]
        for task, activity_score, label, linestyle in curves:
            color = color_em if activity_score is None else gstyle.color(activity_score)
            for n, observable in enumerate(observables):
                plots[n].add_data(
                    task=task,
                    xid="time",
                    yid=observable,
                    label=label if n == 0 else None,
                    color=color,
                    linestyle=linestyle,
                )

        # data
        for subject_index in range(1, 11):
            phenotype = self.phenotype(subject_index)
            color = (
                gstyle.color(0.0) if phenotype == MetabolicPhenotype.PM else color_em
            )
            for n, substance_key in enumerate(["dex", "dor"]):
                plots[n].add_data(
                    dataset=self.to_sid(f"Fig1_{substance_key}_{subject_index}"),
                    xid="time",
                    yid="value",
                    single_lines=True,
                    # one legend entry per phenotype
                    label=(
                        f"{phenotype} (Fig1)"
                        if n == 0 and subject_index in (1, 2)
                        else None
                    ),
                    color=color,
                    alpha=1,
                )

        return {
            "fig1": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Lenuzza2016, output_dir="test", save_results=True)
