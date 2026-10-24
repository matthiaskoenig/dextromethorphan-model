"""Simulation experiment of the study Koehler1997."""

from typing import ClassVar, override

import numpy as np
from pkpdsim.metadata import Coadministration, Dosing, Fasting, Health, Route, Tissue
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
    GeneticPhenotype,
    GenotypeScoring,
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)


class Koehler1997(DexSimulationExperiment):
    """Simulation experiment of Koehler1997.

    10 ml of a liquid containing 20 mg dextromethorphan orally (the salt is
    not named, the dose is simulated as the base) to 14 drug-free healthy
    controls (Tab1) and 22 psychiatric patients under psychotropic medication
    (Tab2), genotyped for CYP2D6 (*3, *4, *5, *6). Two sessions: the dose
    before sleep with the urine over 8 hr, and the serum 1 hr after a dose.
    Both are simulated by one simulation per diplotype; fasting is not
    reported. Dextromethorphan and dextrorphan by HPLC after a hydrolysis of
    the conjugates (the serum dextrorphan of 40 to 510 ng/ml 1 hr after 20 mg
    is the total dextrorphan), so the metabolic ratios are DXM/(DXO+DXOGLU).
    The liquid is simulated with the dissolution of the model (a fit
    parameter, which a study does not change).

    The serum concentrations of Fig2 were substituted by the limit of
    quantification (5 ng/ml) below it: the dextromethorphan of the extensive
    metabolizers sits at 5 ng/ml (0.018 µM) in the figure, which is no
    measurement; these groups are plotted, not mapped. The poor metabolizers
    of Fig2 are 3 healthy controls and 2 patients under medication in one
    group (validation of a population, not training data). The patients of
    Tab2 are plotted, not mapped.
    """

    fig_ids: ClassVar[list[str]] = ["Tab1_metabolic_ratio", "Tab2_metabolic_ratio"]
    #: observable of the metabolic ratio by tissue
    mr_observables: ClassVar[dict[str, str]] = {
        "urine": "dxm_dxo_total_urine",
        "serum": "dxm_dxo_total",
    }
    #: substance of the data and key of the dataset by observable of Fig2
    observable_substances: ClassVar[dict[str, tuple[str, str]]] = {
        "[Cve_dxm]": ("dextromethorphan", "dxm"),
        "dxo_total": ("dtf+dtfglu", "dxo_total"),
    }
    #: diplotype of the poor metabolizers of Fig2 (*4/*4, one patient *4/*6)
    diplotype_pm: ClassVar[str] = "*4/*4"

    #: diplotype by diplotype key of the subjects of the tables, sorted by
    #: decreasing activity score; set by `datasets`
    genotype_mapping: dict[str, str]
    #: diplotype by diplotype key of the subjects of Tab1, set by `datasets`
    genotype_mapping_tab1: dict[str, str]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        self.genotype_mapping = {}
        for fig_id in self.fig_ids:
            df = self.load_dataframes_by_substance(fig_id)["(dmt)/(dtf+dtfglu)"].copy()
            df["activities"] = df["cyp2d6_genotype"].apply(
                GenotypeScoring.activity_score_for_diplotype
            )
            df.sort_values(by=["activities"], ascending=False, inplace=True)
            this_genotype_mapping = {
                GenotypeScoring.diplotype_to_string(genotype): genotype
                for genotype in df["cyp2d6_genotype"].unique()
            }
            self.genotype_mapping = {**this_genotype_mapping, **self.genotype_mapping}
            if fig_id == "Tab1_metabolic_ratio":
                self.genotype_mapping_tab1 = this_genotype_mapping
            for group_key, dset_group in df.groupby(["cyp2d6_genotype", "tissue"]):
                # the keys of a groupby by several columns are tuples
                assert isinstance(group_key, tuple)
                genotype, tissue = group_key
                dset_group["time_jitter"] = jitter(dset_group["time"], 0.1)
                dset_group["time_jitter_unit"] = dset_group["time_unit"]
                key = GenotypeScoring.diplotype_to_string(str(genotype))
                dsets[self.to_sid(f"{fig_id}_{tissue}_{key}")] = DataSet.from_df(
                    dset_group, self.ureg
                )

        dframes = self.load_dataframes_by_substance("Fig2")
        for substance, key in self.observable_substances.values():
            for parent_group, df_group in dframes[substance].groupby("parent_group"):
                df_group["time_jitter"] = jitter(df_group["time"], 0.1)
                df_group["time_jitter_unit"] = df_group["time_unit"]
                dset = DataSet.from_df(df_group, self.ureg)
                mr = self.Mr.dxm if key == "dxm" else self.Mr.dxo
                dset.unit_conversion("value", 1 / mr)
                dsets[self.to_sid(f"Fig2_{key}_{parent_group}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": Q(20, "mg"),
        }
        tcsims: dict[str, Simulation] = {}
        for diplotype_key, genotype in self.genotype_mapping.items():
            genotype_indexes = GenotypeScoring.indices_for_diplotype(genotype)
            tcsims[self.to_sid(f"cyp2d6_activity_{diplotype_key}")] = Simulation(
                time_unit="hr",
                end=20,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_allele1": Q(genotype_indexes[0], "dimensionless"),
                    "LI__cyp2d6_allele2": Q(genotype_indexes[1], "dimensionless"),
                },
            )
        return tcsims

    def task_id(self, diplotype: str) -> str:
        """Get the task of a diplotype."""
        key = GenotypeScoring.diplotype_to_string(diplotype)
        return self.to_sid(f"task_cyp2d6_activity_{key}")

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        # the healthy controls of Tab1, the patients of Tab2 are not mapped
        for tissue, yid in self.mr_observables.items():
            for diplotype_key, diplotype in self.genotype_mapping_tab1.items():
                key = f"fm_koehler1997_tab1_mr_{tissue}_{diplotype_key}"
                mappings[self.to_sid(key)] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(
                            f"Tab1_metabolic_ratio_{tissue}_{diplotype_key}"
                        ),
                        xid="time",
                        yid="value",
                        count=1,
                    ),
                    observable=FitData(
                        self, task=self.task_id(diplotype), xid="time", yid=yid
                    ),
                    metadata=DexMappingMetaData(
                        diplotype=diplotype,
                        tissue=Tissue(tissue),
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.NR,
                        coadministration=Coadministration.NONE,
                    ),
                )

        # the poor metabolizers of Fig2: 3 healthy controls and 2 patients
        # under psychotropic medication in one group
        for observable, (_, key) in self.observable_substances.items():
            mappings[self.to_sid(f"fm_koehler1997_fig2_{key}_pm")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig2_{key}_all"),
                    xid="time",
                    yid="value",
                    count=1,
                ),
                observable=FitData(
                    self,
                    task=self.task_id(self.diplotype_pm),
                    xid="time",
                    yid=observable,
                ),
                metadata=DexMappingMetaData(
                    tissue=Tissue.SERUM,
                    genetic_phenotype=GeneticPhenotype.gPM,
                    activity_score=0,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.NR,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.COMEDICATION,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Tab1Tab2Fig2",
            name=f"{self.sid}_Tab1Tab2Fig2",
            num_rows=2,
            num_cols=2,
        )
        plots = fig.create_plots(xaxis=Axis("time", unit=self.unit_time), legend=True)

        plots[0].set_yaxis(self.label_mrtot_urine, unit=self.unit_dimless, scale="log")
        plots[1].set_yaxis(self.label_mrtot_serum, unit=self.unit_dimless, scale="log")
        plots[2].set_yaxis(self.label_dxm, unit=self.unit_dxm)
        plots[3].set_yaxis(self.label_dxo_total, unit=self.unit_dxo)
        hide_xaxis_label(plots[0])
        hide_xaxis_label(plots[1])
        gstyle = GenotypeStyle(activities=np.array([0, 3]))

        # label and marker of the subjects of a table
        table_styles = {
            "Tab1_metabolic_ratio": ("controls", "s"),
            "Tab2_metabolic_ratio": ("patients", "^"),
        }
        # diplotypes with data by plot of the metabolic ratio; their
        # simulations are drawn once per plot
        genotype_keys: list[list[str]] = [[] for _ in self.mr_observables]
        for fig_id in self.fig_ids:
            label, marker = table_styles[fig_id]
            for n, tissue in enumerate(self.mr_observables):
                # one legend entry per table and activity score
                labeled: set[float] = set()
                for genotype_key, genotype in self.genotype_mapping.items():
                    activity_score = GenotypeScoring.activity_score_for_diplotype(
                        genotype
                    )
                    dataset = self.to_sid(f"{fig_id}_{tissue}_{genotype_key}")
                    # the tables do not have every diplotype
                    if dataset not in self._datasets:
                        continue
                    plots[n].add_data(
                        dataset=dataset,
                        xid="time_jitter",
                        yid="value",
                        single_lines=True,
                        label=(
                            f"{label} AS {activity_score}"
                            if n == 0 and activity_score not in labeled
                            else None
                        ),
                        color=gstyle.color(activity_score),
                        marker=marker,
                        linestyle="",
                        alpha=1,
                    )
                    labeled.add(activity_score)
                    if genotype_key not in genotype_keys[n]:
                        genotype_keys[n].append(genotype_key)

        # simulations of the diplotypes
        for n, yid in enumerate(self.mr_observables.values()):
            for genotype_key in genotype_keys[n]:
                genotype = self.genotype_mapping[genotype_key]
                activity_score = GenotypeScoring.activity_score_for_diplotype(genotype)
                plots[n].add_data(
                    task=self.task_id(genotype),
                    xid="time",
                    yid=yid,
                    label=None,
                    color=gstyle.color(activity_score),
                )
        # one legend entry per activity score
        labeled = set()
        for genotype_key in dict.fromkeys(genotype_keys[0] + genotype_keys[1]):
            genotype = self.genotype_mapping[genotype_key]
            activity_score = GenotypeScoring.activity_score_for_diplotype(genotype)
            for n, observable in enumerate(self.observable_substances, start=2):
                plots[n].add_data(
                    task=self.task_id(genotype),
                    xid="time",
                    yid=observable,
                    label=(
                        f"AS {activity_score}"
                        if n == 3 and activity_score not in labeled
                        else None
                    ),
                    color=gstyle.color(activity_score),
                )
            labeled.add(activity_score)

        # Fig2: the groups of the serum at 1 hr
        fig2_styles = {
            "all": ("PM: 3 controls, 2 patients", 0, "o"),
            "control": ("EM controls", 2, "s"),
            "patients": ("EM patients", 2, "^"),
        }
        for n, (_, key) in enumerate(self.observable_substances.values(), start=2):
            for group, (label, activity_score, marker) in fig2_styles.items():
                plots[n].add_data(
                    dataset=self.to_sid(f"Fig2_{key}_{group}"),
                    xid="time_jitter",
                    yid="value",
                    single_lines=True,
                    label=label if n == 2 else None,
                    color=gstyle.color(activity_score),
                    marker=marker,
                    linestyle="",
                    alpha=1,
                )

        return {
            "tab1tab2fig2": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Koehler1997, output_dir="test", save_results=True)
