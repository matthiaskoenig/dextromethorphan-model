"""Simulation experiment of the study Pope2004."""

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


class Pope2004(DexSimulationExperiment):
    """Simulation experiment of Pope2004 (study 3).

    10 subjects (5 men, 5 women, mean age 53, body weight not reported),
    phenotyped by the 0-12 hr urinary DM/(DX + conjugates) after 30 mg
    dextromethorphan (cutoff 0.3), took one capsule of 30 mg dextromethorphan
    hydrobromide and quinidine every 12 hr, 15 doses, fasted 2 hr before and 4
    hr after every dose. The quinidine of the capsule is 25 mg in the methods
    of study 3 and 30 mg in the abstract, Fig3 and TabIV (AVP-923, 30 mg DM +
    30 mg Q); the curation takes 30 mg. The model describes quinidine by the
    constant activity factor of CYP2D6 of the base of the experiments
    (`cyp2d6_inhibition["quinidine"]`), so the waning of the inhibition after
    the last dose (the metabolic ratio of the extensive metabolizers returns to
    0.03 by day 14, Tab5) is not described.

    Fig3: plasma dextromethorphan and total dextrorphan over 72 hr after the
    last dose (day 8) of 7 extensive (the methods phenotype 8) and 2 poor
    metabolizers (mean).
    Tab5: urinary metabolic ratio DM/(DX + conjugates) of 12 hr collections.
    Only the collection after the first dose (0-12 hr) is used: it is the
    cumulative ratio of the model, the later collections (day 8 to 14) are
    ratios of a 12 hr window, which the model has no observable for.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]
    #: the phenotype groups: (group of the data, task of the simulation)
    groups: ClassVar[dict[MetabolicPhenotype, tuple[str, str]]] = {
        MetabolicPhenotype.PM: ("Study3_pm", "task_cyp2d6_activity_0_qui"),
        MetabolicPhenotype.EM: ("Study3_em", "task_cyp2d6_activity_2_qui"),
    }
    #: the series: (data, key, observable, tissue)
    series: ClassVar[list[tuple[str, str, str, Tissue]]] = [
        ("Fig3", "dxm", "[Cve_dxm]", Tissue.PLASMA),
        ("Fig3", "dxo_total", "dxo_total", Tissue.PLASMA),
        ("Tab5", "mr", "dxm_dxo_total_urine", Tissue.URINE),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3", "Tab5"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                if substance == "dextromethorphan":
                    key = "dxm"
                elif substance == "dtf+dtfglu":
                    key = "dxo_total"
                elif substance == "(dmt)/(dtf+dtfglu)":
                    key = "mr"
                    # the collection 0-12 hr after the first dose
                    df = df[df["intervention"].str.endswith("dose1")]
                else:
                    continue

                for phenotype, (group, _) in self.groups.items():
                    dset = DataSet.from_df(df[df.group == group], self.ureg)
                    if key == "dxm":
                        dset.unit_conversion("mean", 1 / self.Mr.dxm)
                    elif key == "dxo_total":
                        dset.unit_conversion("mean", 1 / self.Mr.dxo)
                    dsets[f"{fig_id}_{key}_{phenotype.name.lower()}"] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        PODOSE = Q(30, "mg") * self.f_dxmhbr_to_dxm()
        # the first dose at 0 hr, 14 doses every 12 hr, then 72 hr
        n_doses = 15
        dose_times = [12 * k for k in range(1, n_doses)]
        end = 12 * (n_doses - 1) + 84
        tcsims = {}
        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}_qui")] = Simulation(
                time_unit="hr",
                end=end,
                preinit_changes={
                    **self.default_changes(),
                    "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
                    "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                    "LI__f_cyp2d6": Q(
                        self.cyp2d6_inhibition["quinidine"], "dimensionless"
                    ),
                    "PODOSE_dxm": PODOSE,
                },
                changes=[self.add_doses(dose_times, {"PODOSE_dxm": PODOSE})],
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for fig_id, key, observable, tissue in self.series:
            for phenotype, (_, task) in self.groups.items():
                pid = phenotype.name.lower()
                mappings[f"fm_pope2004_{key}_{pid}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{fig_id}_{key}_{pid}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(self, task=task, xid="time", yid=observable),
                    metadata=DexMappingMetaData(
                        diplotype=None,
                        tissue=tissue,
                        genetic_phenotype=None,
                        metabolic_phenotype=phenotype,
                        route=Route.PO,
                        application_form=ApplicationForm.CAPSULE,
                        dosing=Dosing.MULTIPLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.QUINIDINE,
                        data=PKPDData.PK,
                        data_type=DataType.MEAN,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self, sid="Fig3_Tab5", name=f"{self.sid}_Fig3|Tab5", num_rows=3
        )
        plots = fig.create_plots(xaxis=Axis("time", unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_dxm, unit=self.unit_dxm, scale="linear")
        plots[1].set_yaxis(self.label_dxo_total, unit=self.unit_dxo, scale="linear")
        plots[2].set_yaxis(self.label_mrtot_urine, unit=self.unit_dimless, scale="log")
        hide_xaxis_label(plots[0])
        hide_xaxis_label(plots[1])

        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        for activity_score in self.activity_scores:
            task_id = f"task_cyp2d6_activity_{activity_score}_qui"
            for k, (_, _, observable, _) in enumerate(self.series):
                plots[k].add_data(
                    task=self.to_sid(task_id),
                    xid="time",
                    yid=observable,
                    label=f"AS:{activity_score} with QUI",
                    color=gstyle.color(activity_score),
                )

        # data
        for k, (fig_id, key, _, _) in enumerate(self.series):
            for phenotype, activity_score in [
                (MetabolicPhenotype.PM, 0),
                (MetabolicPhenotype.EM, 2),
            ]:
                plots[k].add_data(
                    dataset=f"{fig_id}_{key}_{phenotype.name.lower()}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{phenotype.name} with QUI",
                    color=gstyle.color(activity_score),
                )

        return {
            "fig1": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Pope2004, output_dir="test", save_results=True)
