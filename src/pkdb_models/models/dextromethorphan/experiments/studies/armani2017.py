"""Simulation experiment of the study Armani2017."""

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
from pkdb_models.models.dextromethorphan.experiments.figure_templates import fig_dex
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)

#: the activity of CYP2D6 under osilodrostat: a single dose of 50 mg 30 min
#: before the cocktail raises the AUC of dextromethorphan 1.48 fold (90 % CI
#: 1.34 to 1.63, geometric mean ratio, Fig1), a moderate inhibition; in
#: extensive metabolizers the AUC of an oral dose is inversely proportional to
#: the activity of CYP2D6, so the factor is 1/1.48 (the model gives 1.44 at the
#: activity score 2). The waning of the inhibition (half-life of osilodrostat
#: 4.7 hr) is not described
F_CYP2D6_OSILODROSTAT = 1 / 1.48


class Armani2017(DexSimulationExperiment):
    """Simulation experiment of Armani2017.

    Open label interaction study of osilodrostat in 19 healthy adults (27 to
    55 yr, 73.0 +- 12.9 kg). Period 1: the modified Cooperstown cocktail orally
    (caffeine 100 mg, omeprazole 20 mg, dextromethorphan 30 mg, midazolam 2
    mg); period 2 (day 8): osilodrostat 50 mg and the cocktail 30 min later.
    Plasma to 48 hr (Fig2: mean +- SD to 24 hr). The salt is not named, the
    dextromethorphan of a Cooperstown cocktail is the hydrobromide (30 mg are
    22 mg of the base).

    The CYP2D6 genotype was not determined and the poor metabolizers were not
    excluded: the publication attributes the large variability (gCV of Cmax
    331 %) to two subjects with extreme values, consistent with poor
    metabolizers. The arithmetic mean of Fig2 mixes the phenotypes (its tail at
    24 hr is the poor metabolizers), so the mean is compared to the extensive
    metabolizers (activity score 2) for validation only.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]
    #: the mean body weight of the subjects
    bodyweight: ClassVar[float] = 73.0
    #: the arms of Fig2: the cocktail without and with osilodrostat
    arms: ClassVar[dict[str, str]] = {
        "ctl": "Fig2_caf_ome_dex_mid_dextromethorphan",
        "osi": "Fig2_caf_ome_dex_mid_osi_dextromethorphan",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for label, dset_group in dframes["dextromethorphan"].groupby("label"):
                dset = DataSet.from_df(dset_group, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.dxm)
                dsets[self.to_sid(f"{fig_id}_{label}")] = dset
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
            changes_as = {
                **changes,
                "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
            }
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr", end=30, preinit_changes=changes_as
            )
            if activity_score == 2:
                tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}_osi")] = (
                    Simulation(
                        time_unit="hr",
                        end=30,
                        preinit_changes={
                            **changes_as,
                            "LI__f_cyp2d6": Q(F_CYP2D6_OSILODROSTAT, "dimensionless"),
                        },
                    )
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        tasks = {"ctl": "task_cyp2d6_activity_2", "osi": "task_cyp2d6_activity_2_osi"}
        for arm, dataset in self.arms.items():
            suffix = "" if arm == "ctl" else "_osi"
            mappings[f"fm_armani2017_dxm_plasma{suffix}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=dataset,
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(self, task=tasks[arm], xid="time", yid="[Cve_dxm]"),
                metadata=DexMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.NR,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    # osilodrostat has no member in `Coadministration`
                    coadministration=Coadministration.COCKTAIL
                    if arm == "ctl"
                    else Coadministration.COMEDICATION,
                    data=PKPDData.PK,
                    data_type=DataType.MEAN,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plot = fig_dex(experiment=self, fig_id="Fig2", scale="log")
        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        for activity_score in self.activity_scores:
            plot.add_data(
                task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                xid="time",
                yid="[Cve_dxm]",
                label=f"AS:{activity_score}",
                color=gstyle.color(activity_score),
            )
        plot.add_data(
            task="task_cyp2d6_activity_2_osi",
            xid="time",
            yid="[Cve_dxm]",
            label="AS:2 osilodrostat",
            color="black",
            linestyle="--",
        )
        # the SD exceeds the mean at every time (two poor metabolizers), the
        # bars would reach the bottom of the logarithmic axis
        for arm, label, color in [
            ("ctl", "cocktail, mean", gstyle.color(2)),
            ("osi", "cocktail + osilodrostat, mean", "black"),
        ]:
            plot.add_data(
                dataset=self.arms[arm],
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
    MODEL.run_experiments(Armani2017, output_dir="test", save_results=True)
