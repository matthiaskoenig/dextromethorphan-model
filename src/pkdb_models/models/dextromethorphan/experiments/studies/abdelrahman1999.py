"""Simulation experiment of the study Abdelrahman1999."""

from typing import ClassVar, override

import numpy as np
import pandas as pd
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
    jitter,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    hide_xaxis_label,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeScoring,
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)

#: the activity of CYP2D6 under terbinafine (250 mg once daily for 14 days):
#: the urinary metabolic ratio of the six extensive metabolizers rises 97 fold
#: on average (20 to 265 fold, Table I), which the model reaches with 1 % of
#: the activity of CYP2D6 (its ratio rises 98 fold at the activity score 2).
#: Terbinafine is a potent competitive inhibitor of CYP2D6 with a half-life of
#: weeks, so the inhibition is constant over the 24 hr of a phenotyping
F_CYP2D6_TERBINAFINE = 0.01


class Abdelrahman1999(DexSimulationExperiment):
    """Simulation experiment of Abdelrahman1999.

    Nine healthy white adults (6 male, 3 female, 22 to 44 yr), CYP2D6 genotyped
    (six extensive and three poor metabolizers by the genotype). On each study
    day 0.3 mg/kg dextromethorphan as a cough syrup (Tussin, 15 mg/5 ml of the
    hydrobromide) by mouth and the urine of 0-24 hr; the urine was hydrolysed
    (beta-glucuronidase/arylsulfatase), so the metabolic ratio is
    DXM/(DXO+DXOGLU). The baseline ratio is the mean of three phenotypings, then
    terbinafine 250 mg once daily for 14 days and the ratio on the last day.
    Body weight and food are not reported: the dose is given for the body
    weight of the model (75 kg).

    The genotype `*5/*16` of subject P2 (Table I) is simulated as `*5/*13`:
    `*16` is a CYP2D7/2D6 hybrid without function, which PharmVar merged into
    `*13` (the allele table of the model has no `*16`).
    """

    #: the reference body weight of the model, the weight is not reported
    bodyweight: ClassVar[float] = 75.0
    #: the alleles of the publication which the allele table names otherwise
    allele_synonyms: ClassVar[dict[str, str]] = {"*16": "*13"}
    #: the arms of the study by their intervention: baseline and terbinafine
    arms: ClassVar[dict[str, str]] = {"DEX": "dex", "DEX, TER": "ter"}

    #: index of the CYP2D6 diplotypes (sorted by activity score), set by `datasets`
    diplotype_mapping: dict[str, int]

    def diplotype(self, genotype: str) -> str:
        """Get the diplotype of the allele table for a published genotype."""
        return "/".join(
            self.allele_synonyms.get(allele, allele)
            for allele in GenotypeScoring.alleles_from_diplotype(genotype)
        )

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframes_by_substance("Tab1")["(dmt)/(dtf+dtfglu)"]
        df["diplotype"] = df["cyp2d6_genotype"].apply(self.diplotype)
        # the SD of the three baseline phenotypings of a subject
        df["value_sd"] = pd.to_numeric(df["sd_intra"], errors="coerce")

        # the diplotypes sorted by their activity score
        diplotypes = sorted(
            df["diplotype"].unique(),
            key=GenotypeScoring.activity_score_for_diplotype,
            reverse=True,
        )
        self.diplotype_mapping = {v: k for k, v in enumerate(diplotypes)}

        for intervention, df_arm in df.groupby("intervention"):
            arm = self.arms[str(intervention)]
            for diplotype, dset_group in df_arm.groupby("diplotype"):
                # the subjects of a diplotype side by side in the figure, the
                # fits use the time
                dset_group["time_jitter"] = jitter(dset_group["time"], 0.1)
                dset_group["time_jitter_unit"] = dset_group["time_unit"]
                index = self.diplotype_mapping[str(diplotype)]
                dsets[self.to_sid(f"Tab1_{arm}_{index}")] = DataSet.from_df(
                    dset_group, self.ureg
                )
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        bodyweight = Q(self.bodyweight, "kg")
        changes = {
            **self.default_changes(),
            "BW": bodyweight,
            # 0.3 mg/kg of the hydrobromide of the syrup
            "PODOSE_dxm": Q(0.3, "mg/kg") * bodyweight * self.f_dxmhbr_to_dxm(),
        }
        for diplotype, index in self.diplotype_mapping.items():
            alleles = GenotypeScoring.indices_for_diplotype(diplotype)
            changes_diplotype = {
                **changes,
                "LI__cyp2d6_allele1": Q(alleles[0], "dimensionless"),
                "LI__cyp2d6_allele2": Q(alleles[1], "dimensionless"),
            }
            for arm, f_cyp2d6 in {"dex": 1.0, "ter": F_CYP2D6_TERBINAFINE}.items():
                tcsims[self.to_sid(f"cyp2d6_{arm}_{index}")] = Simulation(
                    time_unit="hr",
                    end=28,
                    preinit_changes={
                        **changes_diplotype,
                        "LI__f_cyp2d6": Q(f_cyp2d6, "dimensionless"),
                    },
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        coadministrations = {
            "dex": Coadministration.NONE,
            # terbinafine, which has no member in `Coadministration`
            "ter": Coadministration.COMEDICATION,
        }
        for diplotype, index in self.diplotype_mapping.items():
            for arm, coadministration in coadministrations.items():
                suffix = "" if arm == "dex" else "_ter"
                key = self.to_sid(
                    "fm_abdelrahman1999_mr_urine_"
                    f"{GenotypeScoring.diplotype_to_string(diplotype)}{suffix}"
                )
                mappings[key] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Tab1_{arm}_{index}"),
                        xid="time",
                        yid="value",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(f"task_cyp2d6_{arm}_{index}"),
                        xid="time",
                        yid="dxm_dxo_total_urine",
                    ),
                    metadata=DexMappingMetaData(
                        diplotype=diplotype,
                        tissue=Tissue.URINE,
                        route=Route.PO,
                        application_form=ApplicationForm.SYRUP,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.NR,
                        coadministration=coadministration,
                        data=PKPDData.PK,
                        data_type=DataType.INDIVIDUAL,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(experiment=self, sid="Tab1", name=f"{self.sid}_Tab1", num_rows=2)
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        for plot, arm in zip(plots, ["baseline", "terbinafine"], strict=True):
            plot.set_yaxis(
                f"{self.label_mrtot_urine}{arm}", unit=self.unit_dimless, scale="log"
            )
        hide_xaxis_label(plots[0])

        gstyle = GenotypeStyle(activities=np.array([0, 3]))
        for diplotype, index in self.diplotype_mapping.items():
            activity_score = GenotypeScoring.activity_score_for_diplotype(diplotype)
            color = gstyle.color(activity_score)
            for k, arm in enumerate(["dex", "ter"]):
                plots[k].add_data(
                    dataset=self.to_sid(f"Tab1_{arm}_{index}"),
                    xid="time_jitter",
                    yid="value",
                    yid_sd="value_sd" if arm == "dex" else None,
                    count="count",
                    label=f"{diplotype} AS:{activity_score}",
                    color=color,
                    linestyle="",
                )
                plots[k].add_data(
                    task=self.to_sid(f"task_cyp2d6_{arm}_{index}"),
                    xid="time",
                    yid="dxm_dxo_total_urine",
                    label=None,
                    color=color,
                )
        return {"fig1": fig}


if __name__ == "__main__":
    MODEL.run_experiments(Abdelrahman1999, output_dir="test", save_results=True)
