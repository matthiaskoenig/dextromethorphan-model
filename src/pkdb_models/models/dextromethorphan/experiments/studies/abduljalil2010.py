"""Simulation experiment of the study Abduljalil2010."""

from typing import ClassVar, override

import numpy as np
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.plot import Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    fig_dex_dor_dor_total,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeScoring,
    GenotypeStyle,
)


class Abduljalil2010(DexSimulationExperiment):
    """Simulation experiment of Abduljalil2010.

    Population pharmacokinetics of the reference periods of three cocktail
    studies: 36 healthy Caucasian men (29.4 +- 6.9 yr, 76.5 +- 9.0 kg), a
    single oral dose of 30 mg dextromethorphan hydrobromide (one capsule
    Hustenstiller-ratiopharm, the monohydrate, 22 mg of the base). Plasma to 24
    hr (study C to 12 hr), urine in intervals to 24 hr, hydrolysed with
    beta-glucuronidase, so the urinary dextrorphan is the total dextrorphan.

    The data of Fig3 are the single samples of all subjects (a visual
    predictive check), which the figure does not assign to a subject or a
    genotype, so they are plotted against the activity scores of the
    diplotypes of Table 2 and not fitted. The cumulative urinary dextrorphan
    (median 0.7 mg at 24 hr, 3.4 % of the dose) is a tenth of the total
    dextrorphan of the other studies (27 to 46 %, Capon1996, Barnhart1980) and
    close to their free dextrorphan, although the methods name a hydrolysis.
    """

    #: the CYP2D6 diplotypes of the 36 subjects (Table 2)
    diplotypes: ClassVar[dict[str, int]] = {
        "*4/*4": 1,  # AS: 0
        "*4/*41": 1,  # AS: 0.5
        "*1/*4": 7,  # AS: 1
        "*2/*4": 4,  # AS: 1
        "*2/*4x2": 1,  # AS: 1
        "*1/*41": 5,  # AS: 1.5
        "*2/*41": 1,  # AS: 1.5
        "*1/*1": 6,  # AS: 2
        "*1/*2": 4,  # AS: 2
        "*2/*2": 2,  # AS: 2
        "*2x2/*3": 1,  # AS: 2
        "*1x2/*2": 1,  # AS: 3
        "*1/*1x2": 1,  # AS: 3
        "*2/*2x2": 1,  # AS: 3
    }
    #: the mean body weight of the subjects
    bodyweight: ClassVar[float] = 76.5

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        sids = {
            "dextromethorphan": "dxm",
            "dextrorphan": "dxo",
            "dtf+dtfglu": "dxo_total",
        }
        mrs = {"dxm": self.Mr.dxm, "dxo": self.Mr.dxo, "dxo_total": self.Mr.dxo}
        for fig_id in ["Fig3"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                sid = sids[substance]
                for tissue, df_tissue in df.groupby("tissue"):
                    # every row is a single sample of one subject
                    df_tissue["count"] = 1
                    dset = DataSet.from_df(df_tissue, self.ureg)
                    dset.unit_conversion("value", 1 / mrs[sid])
                    dsets[self.to_sid(f"{fig_id}_{tissue}_{sid}")] = dset

        return dsets

    def activity_scores(self) -> dict[float, list[str]]:
        """Get the diplotypes of the subjects by their activity score."""
        scores: dict[float, list[str]] = {}
        for diplotype in self.diplotypes:
            score = GenotypeScoring.activity_score_for_diplotype(diplotype)
            scores.setdefault(score, []).append(diplotype)
        return dict(sorted(scores.items()))

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        changes = {
            **self.default_changes(),
            "BW": Q(self.bodyweight, "kg"),
            "PODOSE_dxm": Q(30, "mg") * self.f_dxmhbr_to_dxm(),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores():
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
    def figures(self) -> dict[str, Figure]:
        fig, plots = fig_dex_dor_dor_total(experiment=self, fig_id="Fig3", scale="log")

        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        # the urine was hydrolysed: the urinary dextrorphan is the total of
        # plots[4], plots[3] (free dextrorphan in the urine) has no data
        for k, dset in [
            (0, "Fig3_plasma_dxm"),
            (1, "Fig3_plasma_dxo"),
            (2, "Fig3_urine_dxm"),
            (4, "Fig3_urine_dxo_total"),
        ]:
            plots[k].add_data(
                dataset=dset,
                xid="time",
                yid="value",
                label="samples of 36 subjects",
                linestyle="",
                color="black",
                markersize=4,
            )

        for activity_score, diplotypes in self.activity_scores().items():
            task_id = self.to_sid(f"task_cyp2d6_activity_{activity_score}")
            count = sum(self.diplotypes[diplotype] for diplotype in diplotypes)
            label = f"AS:{activity_score} {', '.join(diplotypes)} (n={count})"
            color = gstyle.color(activity_score)
            for k, yid in enumerate(
                [
                    "[Cve_dxm]",
                    "[Cve_dxo]",
                    "Aurine_dxm",
                    "Aurine_dxo",
                    "Aurine_dxo_total",
                ]
            ):
                plots[k].add_data(
                    task=task_id, xid="time", yid=yid, label=label, color=color
                )
        return {
            "fig1": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Abduljalil2010, output_dir="test", save_results=True)
