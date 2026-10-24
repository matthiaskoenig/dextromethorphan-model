"""Simulation experiment of the study Chen2017."""

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
    jitter,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    fig_mr_urine_plasma,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeScoring,
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Chen2017(DexSimulationExperiment):
    """Simulation experiment of Chen2017.

    Healthy Chinese volunteers genotyped for CYP2D6, 235 of them phenotyped in
    four genotype groups (Table 1: *1/*1 n=22, 68.2 kg; *1/*10 n=93, 65.0 kg;
    *10/*10 n=85, 63.6 kg; *5/*10 n=35, 64.2 kg): 15 mg dextromethorphan as a
    Tylenol Cold tablet with 300 ml water, urine of 0-3 hr and plasma at 3 hr.
    Only unconjugated dextrorphan was measured (HPLC-MS/MS), so both metabolic
    ratios are DXM/DXO (free); the antimode 0.3 of DXM/total DXO does not
    apply. Fasting is not reported.

    The dose is the hydrobromide: the dextromethorphan of the combination
    tablet (with paracetamol, pseudoephedrine and chlorphenamine) is the
    hydrobromide monohydrate of the pharmacopoeias, 15 mg are 11.0 mg of the
    base. The other ingredients do not inhibit CYP2D6 at their doses, the arm
    has no coadministration.

    The activity scores of the model are the CPIC scores of the allele table
    (`*10` 0.25): *1/*10 1.25, *10/*10 0.5, *5/*10 0.25; the publication
    uses 1.5, 1.0 and 0.5 (`*10` 0.5). Fig2A has 21, 89, 76 and 35 of the 22,
    93, 85 and 35 subjects, overlapping points of the dense centre of the
    clouds are lost.
    """

    #: the groups of the data by their CYP2D6 diplotype
    diplotype_mapping: ClassVar[dict[str, str]] = {
        "1_1": "*1/*1",
        "1_10": "*1/*10",
        "10_10": "*10/*10",
        "5_10": "*5/*10",
    }
    #: the mean body weight of the groups (Table 1)
    bodyweights: ClassVar[dict[str, float]] = {
        "1_1": 68.2,
        "1_10": 65.0,
        "10_10": 63.6,
        "5_10": 64.2,
    }
    #: the metabolic ratios (DXM/free DXO) by tissue
    observables_mr: ClassVar[dict[str, str]] = {
        "urine": "dxm_dxo_urine",
        "plasma": "dxm_dxo",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2A"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for group, df_group in dframes["dmt/dtf"].groupby("group"):
                for tissue, dset_group in df_group.groupby("tissue"):
                    # the subjects side by side in the figure, the fits use
                    # the time
                    dset_group["time_jitter"] = jitter(dset_group["time"], 0.1)
                    dset_group["time_jitter_unit"] = dset_group["time_unit"]
                    # every row is one subject
                    dset_group["count"] = 1
                    dsets[self.to_sid(f"{fig_id}_{group}_{tissue}")] = DataSet.from_df(
                        dset_group, self.ureg
                    )
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": Q(15, "mg") * self.f_dxmhbr_to_dxm(),
        }
        for group, diplotype in self.diplotype_mapping.items():
            alleles = GenotypeScoring.indices_for_diplotype(diplotype)
            # urine of 0-3 hr and plasma at 3 hr
            tcsims[self.to_sid(f"cyp2d6_activity_{group}")] = Simulation(
                time_unit="hr",
                end=6,
                preinit_changes={
                    **changes,
                    "BW": Q(self.bodyweights[group], "kg"),
                    "LI__cyp2d6_allele1": Q(alleles[0], "dimensionless"),
                    "LI__cyp2d6_allele2": Q(alleles[1], "dimensionless"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        for group, diplotype in self.diplotype_mapping.items():
            for tissue, observable in self.observables_mr.items():
                key = self.to_sid(
                    f"fm_chen2017_mr_{tissue}_"
                    f"{GenotypeScoring.diplotype_to_string(diplotype)}"
                )
                mappings[key] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig2A_{group}_{tissue}"),
                        xid="time",
                        yid="value",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(f"task_cyp2d6_activity_{group}"),
                        xid="time",
                        yid=observable,
                    ),
                    metadata=DexMappingMetaData(
                        diplotype=diplotype,
                        tissue=Tissue(tissue),
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.NR,
                        coadministration=Coadministration.NONE,
                        data=PKPDData.PK,
                        data_type=DataType.INDIVIDUAL,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plots = fig_mr_urine_plasma(experiment=self, fig_id="Fig2A")

        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        for group, diplotype in self.diplotype_mapping.items():
            activity_score = GenotypeScoring.activity_score_for_diplotype(diplotype)
            g_phenotype = GenotypeScoring.genetic_phenotype_for_diplotype(diplotype)
            color = gstyle.color(activity_score)
            for k, (tissue, observable) in enumerate(self.observables_mr.items()):
                plots[k].add_data(
                    dataset=self.to_sid(f"Fig2A_{group}_{tissue}"),
                    xid="time_jitter",
                    yid="value",
                    label=f"{diplotype} AS:{activity_score} {g_phenotype}",
                    color=color,
                    linestyle="",
                    markersize=4,
                )
                plots[k].add_data(
                    task=self.to_sid(f"task_cyp2d6_activity_{group}"),
                    xid="time",
                    yid=observable,
                    label=None,
                    color=color,
                )

        return {
            "fig2A": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Chen2017, output_dir="test", save_results=True)
