"""Simulation experiment of the study Eichhold2007."""

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


class Eichhold2007(DexSimulationExperiment):
    """Simulation experiment of Eichhold2007.

    Randomized cross-over study of 20 extensive and 8 poor metabolizers: a
    single oral dose of 20 mg dextromethorphan hydrobromide with 200 mg
    guaifenesin, as 10 ml of the conventional syrup (Robitussin DM) and as an
    optimized formulation with an equivalent amount of both (not described).
    Plasma of dextromethorphan and free dextrorphan over 24 hr (EM, Fig4) and
    168 hr (PM, Fig5). Health, fasting, age and body weight are not reported.

    Guaifenesin does not change the pharmacokinetics of dextromethorphan
    (Demirbas1998). The optimized formulation releases dextromethorphan faster
    (120 fold the plasma level at 5 min, twice the Cmax and the AUC in the
    extensive metabolizers), which the one absorption of the model cannot
    describe: both arms are simulated with the absorption of the model, the
    conventional syrup is the training data, the optimized formulation the
    validation of a limitation (the same subjects).
    """

    groups: ClassVar[list[str]] = ["em", "pm"]
    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]
    #: the formulations by the key of their data
    formulations: ClassVar[dict[str, ApplicationForm]] = {
        "conventional": ApplicationForm.SYRUP,
        "optimized": ApplicationForm.NR,
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig4", "Fig5"]:
            for substance, df in self.load_dataframes_by_substance(fig_id).items():
                dset = DataSet.from_df(df, self.ureg)
                if substance == "dextromethorphan":
                    sid = "dex"
                    dset.unit_conversion("mean", 1 / self.Mr.dxm)
                elif substance == "dextrorphan":
                    sid = "dor"
                    dset.unit_conversion("mean", 1 / self.Mr.dxo)
                else:
                    continue

                for k, group in enumerate(
                    ["extensive metabolizer", "poor metabolizer"]
                ):
                    dset_group = dset[dset.group == group]

                    for intervention in dset_group.intervention.unique():
                        if intervention == "RobitussinDM_20mg_DEX,RobitussinDM_20mg_GG":
                            iid = "conventional"
                        elif intervention == "Optimized_20mg_DEX,Optimized_20mg_GG":
                            iid = "optimized"
                        else:
                            iid = intervention
                        d = dset_group[dset_group.intervention == intervention]
                        if len(d) > 0:
                            dsets[
                                self.to_sid(f"{fig_id}_{sid}_{self.groups[k]}_{iid}")
                            ] = d

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": Q(20, "mg") * self.f_dxmhbr_to_dxm(),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=175,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for group, activity_score, phenotype, fig_id in [
            ("em", 2, MetabolicPhenotype.EM, "Fig4"),
            ("pm", 0, MetabolicPhenotype.PM, "Fig5"),
        ]:
            for iid, application_form in self.formulations.items():
                for sid, observable in [("dex", "[Cve_dxm]"), ("dor", "[Cve_dxo]")]:
                    key = f"fm_eichhold2007_{sid}_{group}_{iid}"
                    mappings[key] = FitMapping(
                        self,
                        reference=FitData(
                            self,
                            dataset=f"{fig_id}_{sid}_{group}_{iid}",
                            xid="time",
                            yid="mean",
                            count="count",
                        ),
                        observable=FitData(
                            self,
                            task=f"task_cyp2d6_activity_{activity_score}",
                            xid="time",
                            yid=observable,
                        ),
                        metadata=DexMappingMetaData(
                            diplotype=None,
                            tissue=Tissue.PLASMA,
                            genetic_phenotype=None,
                            metabolic_phenotype=phenotype,
                            route=Route.PO,
                            application_form=application_form,
                            dosing=Dosing.SINGLE,
                            health=Health.NR,
                            fasting=Fasting.NR,
                            coadministration=Coadministration.GUAIFENESIN,
                            data=PKPDData.PK,
                            data_type=DataType.MEAN,
                        ),
                    )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        scale = "log"

        fig, plots = fig_dex_dor_plasma(
            experiment=self, fig_id="Fig4 | Fig5", scale=scale
        )
        plots[1].set_yaxis(self.label_dxo, unit=self.unit_dxo, scale=scale)
        # the data span 1e-5 to 1e-1 µM; the curves of the extensive
        # metabolizers fall far below them to the numerical noise of the
        # solver within the 175 hr of the poor metabolizers
        for plot in plots:
            if plot.yaxis is not None:
                plot.yaxis.min = 1e-6
        gstyle = GenotypeStyle(
            activities=np.array([self.activity_scores[0], self.activity_scores[-1]])
        )
        for activity_score in self.activity_scores:
            task_id = f"task_cyp2d6_activity_{activity_score}"
            for k, observable in enumerate(["[Cve_dxm]", "[Cve_dxo]"]):
                # simulations
                plots[k].add_data(
                    task=self.to_sid(task_id),
                    xid="time",
                    yid=observable,
                    label=f"AS:{activity_score}",
                    color=gstyle.color(activity_score),
                )

        # data
        plots[0].add_data(
            dataset="Fig4_dex_em_conventional",
            xid="time",
            yid="mean",
            count="count",
            label="EM conv",
            color=gstyle.color(2),
        )
        plots[0].add_data(
            dataset="Fig4_dex_em_optimized",
            xid="time",
            yid="mean",
            count="count",
            label="EM opt",
            marker="^",
            color=gstyle.color(2),
        )
        plots[0].add_data(
            dataset="Fig5_dex_pm_conventional",
            xid="time",
            yid="mean",
            count="count",
            label="PM conv",
            color=gstyle.color(0),
        )
        plots[0].add_data(
            dataset="Fig5_dex_pm_optimized",
            xid="time",
            yid="mean",
            count="count",
            label="PM opt",
            marker="^",
            color=gstyle.color(0),
        )
        plots[1].add_data(
            dataset="Fig4_dor_em_conventional",
            xid="time",
            yid="mean",
            count="count",
            label="EM conv",
            color=gstyle.color(2),
        )
        plots[1].add_data(
            dataset="Fig4_dor_em_optimized",
            xid="time",
            yid="mean",
            count="count",
            label="EM opt",
            marker="^",
            color=gstyle.color(2),
        )
        plots[1].add_data(
            dataset="Fig5_dor_pm_conventional",
            xid="time",
            yid="mean",
            count="count",
            label="PM conv",
            color=gstyle.color(0),
        )
        plots[1].add_data(
            dataset="Fig5_dor_pm_optimized",
            xid="time",
            yid="mean",
            count="count",
            label="PM opt",
            marker="^",
            color=gstyle.color(0),
        )

        return {
            "fig4___fig5": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Eichhold2007, output_dir="test", save_results=True)
