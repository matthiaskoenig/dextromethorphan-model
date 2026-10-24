"""Simulation experiment of the study Hu2011."""

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
    fig_dor_total,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Hu2011(DexSimulationExperiment):
    """Simulation experiment of Hu2011.

    Randomized two-period cross-over of 6 healthy Chinese males (22 to 26 yr,
    59 to 72 kg, mean 65.8 kg), fasted overnight for 10 hr: a single oral dose
    of 30 mg dextromethorphan hydrobromide as a floating sustained release
    tablet (DMB-SR floating) and as a conventional sustained release tablet
    (DMB-SR), with 250 ml water. Plasma dextrorphan over 24 hr (Fig6).

    The assay reports dextrorphan without a deconjugation step, but 230 ng/ml
    after 30 mg is the total dextrorphan (free and conjugated), the free
    dextrorphan is about 100 fold lower (every other study); the curation maps
    the data to the total dextrorphan. The subjects were neither phenotyped nor
    genotyped; they are simulated as extensive metabolizers (activity score
    2), the poor metabolizers are about 1 % of Chinese subjects.

    Both products release dextromethorphan over hours (tmax 3.2 and 4.7 hr
    against 1.5 hr of the immediate release of the model), which the model
    does not describe: the arms are the validation of a limitation.
    """

    #: the arms: (key of the data, marker)
    arms: ClassVar[dict[str, tuple[str, str]]] = {
        "floating": ("Fig6_dex30mg_floating", "^"),
        "conventional": ("Fig6_dex30mg_conventional", "s"),
    }

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig6"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.dxo)
                dsets[self.to_sid(str(label))] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        PODOSE = Q(30, "mg") * self.f_dxmhbr_to_dxm()  # DEX-HBr

        changes = {
            **self.default_changes(),
            "PODOSE_dxm": PODOSE,
            # mean body weight of the subjects
            "BW": Q(65.8, "kg"),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=24,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for arm, (dataset, _) in self.arms.items():
            mappings[f"fm_hu2011_dxo_total_{arm}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=dataset,
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_cyp2d6_activity_2",
                    xid="time",
                    yid="dxo_total",
                ),
                metadata=DexMappingMetaData(
                    diplotype=None,
                    tissue=Tissue.PLASMA,
                    genetic_phenotype=None,
                    metabolic_phenotype=None,
                    route=Route.PO,
                    application_form=ApplicationForm.SUSTAINED_RELEASE_TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.NONE,
                    data=PKPDData.PK,
                    data_type=DataType.MEAN,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:

        fig, plot = fig_dor_total(experiment=self, fig_id="Fig6")
        gstyle = GenotypeStyle(
            activities=np.array([self.activity_scores[0], self.activity_scores[-1]])
        )

        for activity_score in self.activity_scores:
            task_id = f"task_cyp2d6_activity_{activity_score}"
            # simulations
            plot.add_data(
                task=self.to_sid(task_id),
                yid="dxo_total",
                xid="time",
                color=gstyle.color(activity_score),
                label=f"AS:{activity_score}",
            )

        # data
        for arm, (dataset, marker) in self.arms.items():
            plot.add_data(
                dataset=dataset,
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=arm,
                marker=marker,
                color=gstyle.color(2),
            )

        return {
            "fig6": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Hu2011, output_dir="test", save_results=True)
