"""Simulation experiment of the study Nakashima2007."""

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
from sbmlsim.units import Quantity

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


class Nakashima2007(DexSimulationExperiment):
    """Simulation experiment of Nakashima2007.

    Randomized, double-blind crossover of 24 healthy Japanese men (24.7 years,
    64.2 kg): 50 mg cinacalcet (two film tablets of 25 mg) or placebo once
    daily for 8 days, on day 8 a single oral dose of 30 mg dextromethorphan
    hydrobromide monohydrate (2 film tablets of 15 mg, Medicon) with
    standardized meals (no fast stated). Fig2 shows the plasma
    dextromethorphan and free dextrorphan of the 23 extensive metabolizers
    (urinary metabolic ratio below 2.0 in the placebo period; the one poor
    metabolizer is not in the figure).

    Cinacalcet inhibits CYP2D6 (Ki 0.087 µM in vitro, quinidine 0.064 µM in the
    same assay) and raises the AUC of dextromethorphan 11.5 fold (Tab1,
    AUCinf 265.3 against 53.8 ng*h/ml). The pre-treatment of 8 days is at
    steady state, so the inhibition is a constant activity factor of CYP2D6
    (`cyp2d6_inhibition["cinacalcet"]`), the arm is validation data of the
    interaction.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]
    #: the body weight of the subjects (mean)
    bodyweight: ClassVar[Quantity] = Q(64.2, "kg")
    #: cinacalcet (50 mg once daily for 8 days) lowers the activity of CYP2D6
    #: to 8 %: the factor at which the extensive metabolizers of the model
    #: have the 11.5 fold AUC of dextromethorphan of this study (Tab1); a Ki
    #: of 0.087 µM and the total plasma cinacalcet of 0.05 µM would give a
    #: factor of 0.6, the inhibition in the liver is stronger (mechanism-based
    #: inhibition, accumulation of the lipophilic cinacalcet)
    cyp2d6_inhibition: ClassVar[dict[str, float]] = {
        **DexSimulationExperiment.cyp2d6_inhibition,
        "cinacalcet": 0.08,
    }
    #: the arms of Fig2: (intervention of the data, key, coadministration)
    interventions: ClassVar[dict[str, tuple[str, Coadministration]]] = {
        "dextromethorphan_30mg": ("placebo", Coadministration.NONE),
        # the curation names the 50 mg of cinacalcet (2 x 25 mg) `25mg`
        "dextromethorphan_30mg, cinacalcet25mg_pre-treatment": (
            "cinacalcet",
            Coadministration.COMEDICATION,
        ),
    }
    #: the analytes of Fig2: (key, observable)
    substances: ClassVar[dict[str, tuple[str, str]]] = {
        "dextromethorphan": ("dxm", "[Cve_dxm]"),
        "dextrorphan": ("dxo", "[Cve_dxo]"),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for substance, df in self.load_dataframes_by_substance("Fig2").items():
            key, _ = self.substances[substance]
            mr = self.Mr.dxm if key == "dxm" else self.Mr.dxo
            for intervention, df_intervention in df.groupby("intervention"):
                arm, _ = self.interventions[str(intervention)]
                dset = DataSet.from_df(df_intervention, self.ureg)
                dset.unit_conversion("mean", 1 / mr)
                dsets[f"Fig2_{key}_{arm}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        changes = {
            **self.default_changes(),
            "BW": self.bodyweight,
            "PODOSE_dxm": Q(30, "mg") * self.f_dxmhbr_to_dxm(),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for activity_score in self.activity_scores:
            tcsims[self.to_sid(f"cyp2d6_activity_{activity_score}")] = Simulation(
                time_unit="hr",
                end=50,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                },
            )
        # the extensive metabolizers with cinacalcet
        tcsims["cyp2d6_activity_2_cinacalcet"] = Simulation(
            time_unit="hr",
            end=50,
            preinit_changes={
                **changes,
                "LI__cyp2d6_ac": Q(2, "dimensionless"),
                "LI__f_cyp2d6": Q(
                    self.cyp2d6_inhibition["cinacalcet"], "dimensionless"
                ),
            },
        )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for key, observable in self.substances.values():
            for arm, coadministration in self.interventions.values():
                task = (
                    "task_cyp2d6_activity_2"
                    if arm == "placebo"
                    else "task_cyp2d6_activity_2_cinacalcet"
                )
                mappings[f"fm_nakashima2007_{key}_{arm}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"Fig2_{key}_{arm}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(self, task=task, xid="time", yid=observable),
                    metadata=DexMappingMetaData(
                        diplotype=None,
                        tissue=Tissue.PLASMA,
                        genetic_phenotype=None,
                        metabolic_phenotype=MetabolicPhenotype.EM,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.NR,
                        coadministration=coadministration,
                        data=PKPDData.PK,
                        data_type=DataType.MEAN,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        scale = "log"
        fig, plots = fig_dex_dor_plasma(experiment=self, fig_id="Fig2", scale=scale)
        # the data end at 48 hr, the axes at the lowest data
        plots[0].set_yaxis(self.label_dxm, unit=self.unit_dxm, scale=scale, min=1e-4)
        plots[1].set_yaxis(self.label_dxo, unit=self.unit_dxo, scale=scale, min=1e-4)
        gstyle = GenotypeStyle(
            activities=np.array([self.activity_scores[0], self.activity_scores[-1]])
        )
        for k, (key, observable) in enumerate(self.substances.values()):
            # simulations
            for activity_score in self.activity_scores:
                plots[k].add_data(
                    task=self.to_sid(f"task_cyp2d6_activity_{activity_score}"),
                    xid="time",
                    yid=observable,
                    label=f"AS:{activity_score}",
                    color=gstyle.color(activity_score),
                )
            plots[k].add_data(
                task="task_cyp2d6_activity_2_cinacalcet",
                xid="time",
                yid=observable,
                label="AS:2 cinacalcet",
                color="black",
            )
            # data
            plots[k].add_data(
                dataset=f"Fig2_{key}_placebo",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="EM",
                color=gstyle.color(2),
            )
            plots[k].add_data(
                dataset=f"Fig2_{key}_cinacalcet",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="EM cinacalcet",
                marker="^",
                color="black",
            )

        return {
            "fig2": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Nakashima2007, output_dir="test", save_results=True)
