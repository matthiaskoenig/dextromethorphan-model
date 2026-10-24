"""Simulation experiment of the study Yamazaki2016."""

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
    GeneticPhenotype,
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Yamazaki2016(DexSimulationExperiment):
    """Simulation experiment of Yamazaki2016.

    The dextromethorphan group (n = 24, healthy adults) of a study of the
    interactions of isavuconazole: a single oral dose of dextromethorphan
    hydrobromide 30 mg (ROBITUSSIN capsules) alone on day 1 and with
    isavuconazole (200 mg three times daily on days 6 and 7, then 200 mg once
    daily) on day 10, fasted 10 hr before and 4 hr after the dose. Plasma
    dextromethorphan of the intermediate (n = 12) and extensive metabolizers
    (n = 11) and total dextrorphan of all subjects (Fig3, mean +- SD).

    The groups are classified by genotype in the publication, not by the
    activity score: the extensive metabolizers are *10/WT, *17/GD, *17/WT,
    *2/*10, *2/*17, *2/*2, *2/*29, *2/*41, *2/*45, *2/*9, *2/WT, *29/WT,
    *4/GD, *41/WT, *46/GD, *5/GD, *6/GD, *9/WT or WT/WT (activity scores 1.25
    to 2), the intermediate metabolizers carry one mutant allele (*3, *4, *5,
    *6, *7) and one reduced-activity (*9, *10, *17, *29, *41, *45, *46) or
    functional allele (WT, *2), or two reduced-activity alleles (activity
    scores 0.25 to 1). The groups are simulated with the activity scores 1
    (IM) and 2 (EM) and are a validation of the populations, the mean of a
    group mixes activity scores.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1, 1.5, 2, 3]

    #: the CYP3A4 activity of the study: isavuconazole 200 mg once daily is a
    #: moderate inhibitor of CYP3A4, it raises the AUC of midazolam 2.03 fold
    #: (Townsend2017), i.e. 1/(0.07 + 0.93 f) = 2.03 with a fraction of
    #: midazolam metabolized by CYP3A4 of 0.93, about 46 % of the activity.
    #: Observed in this study: the AUCinf of dextromethorphan rises 1.19 fold
    #: (45.7 to 54.4 ng*h/ml, Tab1), the validation of the factor
    cyp3a4_inhibition: ClassVar[dict[str, float]] = {
        **DexSimulationExperiment.cyp3a4_inhibition,
        "isavuconazole": 0.46,
    }

    #: the groups of the data: dataset group, activity score of the simulation
    groups: ClassVar[dict[str, tuple[str, float]]] = {
        "all": ("dex_group", 2),
        "IM": ("dex_group_im", 1),
        "EM": ("dex_group_em", 2),
    }
    #: the arms of the data: intervention, key
    arms: ClassVar[dict[str, str]] = {
        "dextromethorphan": "",
        "dextromethorphan, isavuconazole": "_isa",
    }
    #: the curves which are mapped: substance, group, observable
    curves: ClassVar[list[tuple[str, str, str]]] = [
        ("dxm", "IM", "[Cve_dxm]"),
        ("dxm", "EM", "[Cve_dxm]"),
        ("dxo_total", "all", "dxo_total"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, self.ureg)
                if substance == "dextromethorphan":
                    sid = "dxm"
                    dset.unit_conversion("mean", 1 / self.Mr.dxm)
                elif substance == "dtf+dtfglu":
                    # dextrorphan equivalents
                    sid = "dxo_total"
                    dset.unit_conversion("mean", 1 / self.Mr.dxo)
                else:
                    raise ValueError(f"Unknown substance '{substance}'.")

                for group, (dset_group, _) in self.groups.items():
                    for intervention, arm in self.arms.items():
                        d = dset[
                            (dset.group == dset_group)
                            & (dset.intervention == intervention)
                        ]
                        if len(d) > 0:
                            dsets[self.to_sid(f"{fig_id}_{sid}_{group}{arm}")] = d
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        # 30 mg of the hydrobromide monohydrate, 22 mg of the base
        PODOSE = Q(30, "mg") * self.f_dxmhbr_to_dxm()

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
                end=75,
                preinit_changes=changes_as,
            )
            if activity_score in {1, 2}:
                tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}_isa")] = (
                    Simulation(
                        time_unit="hr",
                        end=75,
                        preinit_changes={
                            **changes_as,
                            "LI__f_cyp3a4": Q(
                                self.cyp3a4_inhibition["isavuconazole"],
                                "dimensionless",
                            ),
                        },
                    )
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        genetic_phenotypes = {
            "IM": GeneticPhenotype.gIM,
            "EM": GeneticPhenotype.gEM,
            "all": None,
        }
        mappings = {}
        for sid, group, observable in self.curves:
            _, activity_score = self.groups[group]
            for arm in self.arms.values():
                key = f"fm_yamazaki2016_{sid}_{group.lower()}{arm}"
                mappings[self.to_sid(key)] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig3_{sid}_{group}{arm}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(f"task_cyp2d6_activity_{activity_score}{arm}"),
                        xid="time",
                        yid=observable,
                    ),
                    metadata=DexMappingMetaData(
                        diplotype=None,
                        tissue=Tissue.PLASMA,
                        genetic_phenotype=genetic_phenotypes[group],
                        metabolic_phenotype=None,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        # pkpdsim has no term of isavuconazole
                        coadministration=(
                            Coadministration.COMEDICATION
                            if arm
                            else Coadministration.NONE
                        ),
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        scale = "log"
        fig, plots = fig_dex_dor_plasma(experiment=self, fig_id="Fig3", scale=scale)
        plots[0].set_yaxis(self.label_dxm, unit=self.unit_dxm, scale=scale, min=1e-4)
        plots[1].set_yaxis(
            self.label_dxo_total, unit=self.unit_dxo, scale=scale, min=1e-3
        )
        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        for activity_score in self.activity_scores:
            task_id = f"task_cyp2d6_activity_{activity_score}"
            for k, observable in enumerate(["[Cve_dxm]", "dxo_total"]):
                plots[k].add_data(
                    task=self.to_sid(task_id),
                    xid="time",
                    yid=observable,
                    label=f"AS:{activity_score}",
                    color=gstyle.color(activity_score),
                )
                if activity_score in {1, 2}:
                    plots[k].add_data(
                        task=self.to_sid(f"{task_id}_isa"),
                        xid="time",
                        yid=observable,
                        label=f"AS:{activity_score} + isavuconazole",
                        color=gstyle.color(activity_score),
                        linestyle="--",
                    )

        # data
        for sid, group, _ in self.curves:
            k = 0 if sid == "dxm" else 1
            _, activity_score = self.groups[group]
            color = "black" if group == "all" else gstyle.color(activity_score)
            for arm in self.arms.values():
                plots[k].add_data(
                    dataset=self.to_sid(f"Fig3_{sid}_{group}{arm}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{group} + isavuconazole" if arm else group,
                    color=color,
                    marker="^" if arm else "s",
                )

        return {
            "fig1": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Yamazaki2016, output_dir="test", save_results=True)
