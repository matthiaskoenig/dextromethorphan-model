"""Simulation experiment of the study Zawertailo2010."""

from typing import ClassVar, override

import numpy as np
import pandas as pd
from pkpdsim.metadata import Coadministration, Dosing, Fasting, Health, Route, Tissue
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    hide_xaxis_label,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeStyle,
    MetabolicPhenotype,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Zawertailo2010(DexSimulationExperiment):
    """Simulation experiment of Zawertailo2010.

    Eight healthy volunteers, genotyped (wt/wt or wt/inactive) and phenotyped
    extensive metabolizers of CYP2D6, fasted overnight; seven sessions of
    escalating oral doses of dextromethorphan hydrobromide (Hoffmann-LaRoche,
    1.3 to 6.0 mg/kg), after placebo (days 1 to 4) or 100 mg quinidine (days
    5 to 7) the evening before (about 10 hr before the dose, simulated with
    the constant CYP2D6 activity of quinidine of the base of the
    experiments). Fig1 is the 3 mg/kg day, plasma of a forearm vein over 6 hr
    (means of 8, no errors): total dextromethorphan (TDEX, after hydrolysis,
    mapped to the free dextromethorphan of the model, its conjugates are a
    small part), free (FDOR) and total dextrorphan (TDOR) and the total
    3-hydroxymorphinan (T3HM) and 3-methoxymorphinan (T3MM, only after
    quinidine), whose sum are the N-demethylated morphinans of the model. The
    body weights are not reported, the dose is for the 75 kg of the model.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1, 1.5, 2, 3]

    #: the substances of the data: key, observable
    substances: ClassVar[dict[str, tuple[str, str]]] = {
        "dextromethorphan": ("dxm", "[Cve_dxm]"),
        "dextrorphan": ("dxo", "[Cve_dxo]"),
        "dtf+dtfglu": ("dxo_total", "dxo_total"),
        "mm": ("mm", "[Cve_mm]"),
    }
    mm_parts: ClassVar[set[str]] = {"3-hydroxymorphinan", "3-methoxymorphinan"}
    #: the arms by intervention: key
    arms: ClassVar[dict[str, str]] = {"dex": "", "dex,Q100mg": "_qui"}

    @override
    def datasets(self) -> dict[str, DataSet]:
        df = self.load_dataframe("Fig1")
        df = pd.concat(
            [df[~df.substance.isin(self.mm_parts)], self.sum_mm(df)],
            ignore_index=True,
        )
        dsets = {}
        for (substance, intervention), df_arm in df.groupby(
            ["substance", "intervention"]
        ):
            sid, _ = self.substances[str(substance)]
            arm = self.arms[str(intervention)]
            dsets[self.to_sid(f"Fig1_{sid}{arm}")] = DataSet.from_df(df_arm, self.ureg)
        return dsets

    def sum_mm(self, df: pd.DataFrame) -> pd.DataFrame:
        """Get the N-demethylated morphinans, the sum of the parts per arm and time.

        Without quinidine only 3-hydroxymorphinan is reported.
        """
        rows = []
        df_mm = df[df.substance.isin(self.mm_parts)]
        for (_, _), df_time in df_mm.groupby(["intervention", "time"]):
            row = df_time.iloc[0].copy()
            row["substance"] = "mm"
            row["label"] = "mm"
            row["mean"] = df_time["mean"].sum()
            rows.append(row)
        return pd.DataFrame(rows)

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        # 3 mg/kg of the hydrobromide monohydrate for the body weight of the
        # model (75 kg), the weights are not reported
        PODOSE = Q(3, "mg/kg") * Q(75, "kg") * self.f_dxmhbr_to_dxm()
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": PODOSE,
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            changes_as = {
                **changes,
                "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
            }
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=7,
                preinit_changes=changes_as,
            )
            if activity_score == 2:
                tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}_qui")] = (
                    Simulation(
                        time_unit="hr",
                        end=7,
                        preinit_changes={
                            **changes_as,
                            "LI__f_cyp2d6": Q(
                                self.cyp2d6_inhibition["quinidine"], "dimensionless"
                            ),
                        },
                    )
                )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for sid, observable in self.substances.values():
            for arm in self.arms.values():
                mappings[self.to_sid(f"fm_zawertailo2010_{sid}{arm}")] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig1_{sid}{arm}"),
                        xid="time",
                        yid="mean",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(f"task_cyp2d6_activity_2{arm}"),
                        xid="time",
                        yid=observable,
                    ),
                    metadata=DexMappingMetaData(
                        diplotype=None,
                        tissue=Tissue.PLASMA,
                        genetic_phenotype=None,
                        metabolic_phenotype=MetabolicPhenotype.EM,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=(
                            Coadministration.QUINIDINE if arm else Coadministration.NONE
                        ),
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        scale = "linear"
        fig = Figure(experiment=self, sid="Fig1", name=f"{self.sid}_Fig1", num_rows=4)
        plots = fig.create_plots(xaxis=Axis("time", unit=self.unit_time), legend=True)
        labels = [
            (f"total {self.label_dxm}", self.unit_dxm),
            (self.label_dxo, self.unit_dxo),
            (self.label_dxo_total, self.unit_dxo),
            (self.label_mm, self.unit_mm),
        ]
        for k, (label, unit) in enumerate(labels):
            if len(label) > 30:
                label = label.replace(" (", "\n(", 1)
            plots[k].set_yaxis(label, unit=unit, scale=scale)
            if k < len(labels) - 1:
                hide_xaxis_label(plots[k])

        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        for activity_score in self.activity_scores:
            task_id = f"task_cyp2d6_activity_{activity_score}"
            for k, (_, observable) in enumerate(self.substances.values()):
                plots[k].add_data(
                    task=self.to_sid(task_id),
                    xid="time",
                    yid=observable,
                    label=f"AS:{activity_score}",
                    color=gstyle.color(activity_score),
                )
                if activity_score == 2:
                    plots[k].add_data(
                        task=self.to_sid(f"{task_id}_qui"),
                        xid="time",
                        yid=observable,
                        label=f"AS:{activity_score} + QUI",
                        color="black",
                    )

        # data
        for k, (sid, _) in enumerate(self.substances.values()):
            for arm in self.arms.values():
                plots[k].add_data(
                    dataset=self.to_sid(f"Fig1_{sid}{arm}"),
                    xid="time",
                    yid="mean",
                    count="count",
                    label="EM + QUI" if arm else "EM",
                    color="black" if arm else gstyle.color(2),
                )

        return {
            "fig1": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Zawertailo2010, output_dir="test", save_results=True)
