"""Simulation experiment of the study Capon1996."""

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

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    fig_dex_dor_plasma,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeStyle,
    MetabolicPhenotype,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Capon1996(DexSimulationExperiment):
    """Simulation experiment of Capon1996.

    Twelve healthy non-smoking subjects (8 male, 4 female, 20 to 26 yr), six
    extensive (EM, urinary metabolic ratio total DXO/DXM 59 to 3402, 70 kg) and
    six poor metabolizers (PM, ratio 0.06 to 0.93, 71 kg) matched for age,
    weight and sex: a single oral dose of 30 mg dextromethorphan hydrobromide
    (capsule, 22 mg of the base). The extensive metabolizers took the dose
    again with 50 mg quinidine sulfate 1 hr before. Plasma to 168 hr, urine to
    168 hr; dextromethorphan and the total (conjugated and unconjugated)
    dextrorphan of Fig2 and Fig3 are means.

    The total dextrorphan of Fig3 is 5 to 6 fold the maximum of Tab1 in every
    group (EM 2300 against 396 µg/l), while the AUC and the half-life of Tab1
    agree with its maximum: a scale error of the figure, whose data are not
    used for fits.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]
    #: the mean body weight of the two groups (70 and 71 kg)
    bodyweight: ClassVar[float] = 70.5
    #: the arms of the figures: group, intervention and the task of the model
    arms: ClassVar[dict[str, tuple[str, str, str]]] = {
        "em": ("EM", "dextromethorphan_30mg", "task_cyp2d6_activity_2"),
        "pm": ("PM", "dextromethorphan_30mg", "task_cyp2d6_activity_0"),
        "em_qui": (
            "EM",
            "dextromethorphan_30mg, quinidine_50mg",
            "task_cyp2d6_activity_2_qui",
        ),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        sids = {"dextromethorphan": "dxm", "dtf+dtfglu": "dxo_total"}
        # the total dextrorphan in µg/l of dextrorphan
        mrs = {"dxm": self.Mr.dxm, "dxo_total": self.Mr.dxo}
        for fig_id in ["Fig2", "Fig3"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                sid = sids[substance]
                for arm, (group, intervention, _) in self.arms.items():
                    df_arm = df[(df.group == group) & (df.intervention == intervention)]
                    dset = DataSet.from_df(df_arm, self.ureg)
                    dset.unit_conversion("mean", 1 / mrs[sid])
                    dsets[self.to_sid(f"{fig_id}_{sid}_{arm}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        changes = {
            **self.default_changes(),
            "BW": Q(self.bodyweight, "kg"),
            "PODOSE_dxm": Q(30, "mg") * self.f_dxmhbr_to_dxm(),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            changes_ac = {
                **changes,
                "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
            }
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=175,
                preinit_changes=changes_ac,
            )
            if activity_score == 2:
                tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}_qui")] = (
                    Simulation(
                        time_unit="hr",
                        end=175,
                        preinit_changes={
                            **changes_ac,
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
        observables = {"dxm": "[Cve_dxm]", "dxo_total": "dxo_total"}
        for fig_id, sid in [("Fig2", "dxm"), ("Fig3", "dxo_total")]:
            for arm, (group, _, task) in self.arms.items():
                qui = arm == "em_qui"
                mappings[f"fm_capon1996_{sid}_plasma_{arm}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"{fig_id}_{sid}_{arm}"),
                        xid="time",
                        yid="mean",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=task, xid="time", yid=observables[sid]
                    ),
                    metadata=DexMappingMetaData(
                        tissue=Tissue.PLASMA,
                        # the phenotype of the subjects, quinidine turns the
                        # extensive metabolizers into poor ones
                        metabolic_phenotype=MetabolicPhenotype(group),
                        route=Route.PO,
                        application_form=ApplicationForm.CAPSULE,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.NR,
                        coadministration=Coadministration.QUINIDINE
                        if qui
                        else Coadministration.NONE,
                        data=PKPDData.PK,
                        data_type=DataType.MEAN,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        fig, plots = fig_dex_dor_plasma(
            experiment=self, fig_id="Fig2_Fig3", scale="log"
        )
        # the range of the data, not the noise of the integrator after 5 days
        plots[0].set_yaxis(self.label_dxm, unit=self.unit_dxm, scale="log", min=1e-4)
        plots[1].set_yaxis(
            self.label_dxo_total, unit=self.unit_dxo, scale="log", min=1e-3
        )
        tasks = {
            self.to_sid(f"task_cyp2d6_activity_{activity_score}"): (
                f"AS:{activity_score}",
                gstyle.color(activity_score),
            )
            for activity_score in self.activity_scores
        }
        tasks["task_cyp2d6_activity_2_qui"] = ("AS:2 quinidine", "black")
        for task, (label, color) in tasks.items():
            for k, yid in enumerate(["[Cve_dxm]", "dxo_total"]):
                plots[k].add_data(
                    task=task,
                    xid="time",
                    yid=yid,
                    label=label,
                    color=color,
                    linestyle="--" if task.endswith("_qui") else "-",
                )

        styles = {
            "pm": ("PM", gstyle.color(0)),
            "em": ("EM", gstyle.color(2)),
            "em_qui": ("EM + quinidine", "black"),
        }
        for k, sid in enumerate(["dxm", "dxo_total"]):
            fig_id = "Fig2" if sid == "dxm" else "Fig3"
            for arm, (label, color) in styles.items():
                plots[k].add_data(
                    dataset=self.to_sid(f"{fig_id}_{sid}_{arm}"),
                    xid="time",
                    yid="mean",
                    count="count",
                    label=label,
                    color=color,
                    linestyle="",
                )

        return {
            "fig1": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Capon1996, output_dir="test", save_results=True)
