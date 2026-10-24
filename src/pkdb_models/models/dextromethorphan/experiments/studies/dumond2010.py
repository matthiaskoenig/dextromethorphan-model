"""Simulation experiment of the study Dumond2010."""

from typing import ClassVar, NamedTuple, override

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
from pkdb_models.models.dextromethorphan.experiments.figure_templates import fig_dex
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeStyle,
)
from pkdb_models.models.dextromethorphan.fitting.mapping_collections import (
    DexMappingMetaData,
)

#: the cocktail of every phase, the key of the datasets
COCKTAIL = (
    "caffeine_200mg, warfarin_10mg,vitamin_k_10mg, omeprazole_40mg, "
    "dextromethorphan_30mg,midazolam_iv_2mg"
)


class Phase(NamedTuple):
    """A phase of the study: the activities of CYP2D6 and CYP3A4 under TPV/r."""

    intervention: str
    label: str
    coadministration: Coadministration
    #: the activity of CYP2D6, `LI__f_cyp2d6`
    f_cyp2d6: float
    #: the activity of hepatic CYP3A4, `LI__f_cyp3a4`
    f_cyp3a4: float


#: The phases of the study. Tipranavir/ritonavir (TPV/r, 500/200 mg) inhibits
#: CYP2D6 and CYP3A. The factors are the inverse geometric mean ratios of the
#: phenotyping metrics of the study (Tab 1, phase/baseline): CYP2D6 from the
#: urinary DM/DX ratio (first dose 3.12, steady state 6.26, the ratio is
#: inverse to the activity of CYP2D6), hepatic CYP3A from the AUC of iv
#: midazolam (first dose 5.13, steady state 2.92: the induction of CYP3A by
#: TPV lessens the net inhibition at steady state). The AUC of
#: dextromethorphan (x3.95 and x5.46) is not used for them and validates the
#: model.
PHASES: dict[str, Phase] = {
    "baseline": Phase(
        intervention=COCKTAIL,
        label="baseline",
        coadministration=Coadministration.COCKTAIL,
        f_cyp2d6=1.0,
        f_cyp3a4=1.0,
    ),
    "tpvr_first_dose": Phase(
        intervention=(f"{COCKTAIL}, tipranavir_first_dose, ritonavir_first_dose"),
        label="first dose TPV/r",
        coadministration=Coadministration.RITONAVIR,
        f_cyp2d6=1 / 3.12,
        f_cyp3a4=1 / 5.13,
    ),
    "tpvr_steady_state": Phase(
        intervention=(f"{COCKTAIL}, tipranavir_steady_state, ritonavir_steady_state"),
        label="steady state TPV/r",
        coadministration=Coadministration.RITONAVIR,
        f_cyp2d6=1 / 6.26,
        f_cyp3a4=1 / 2.92,
    ),
}


class Dumond2010(DexSimulationExperiment):
    """Simulation experiment of Dumond2010.

    23 healthy volunteers (16 men, 76.0 +- 14.4 kg) received a phenotyping
    cocktail of caffeine 200 mg, warfarin 10 mg with vitamin K 10 mg,
    omeprazole 40 mg, dextromethorphan 30 mg orally (the salt is not named,
    the strength of an oral product is the hydrobromide) and midazolam 2 mg iv
    at baseline, with the first dose of tipranavir/ritonavir (TPV/r) and at
    the steady state of TPV/r. Fasting is not reported. Fig 1d gives the mean
    +- SE of plasma dextromethorphan of all 23 subjects.

    The subjects are a mixed CYP2D6 population: one genetic and phenotypic
    poor metabolizer (*4/*4, urinary ratio > 0.3), six heterozygous
    intermediate metabolizers and wild type subjects with intermediate
    ratios. Their mean is simulated with the activity score 2 and is no
    curve of one phenotype.
    """

    activity_scores: ClassVar[list[float]] = [0, 0.5, 1.0, 1.5, 2, 3]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframes_by_substance("Fig1")["dextromethorphan"]
        for key, phase in PHASES.items():
            df_phase = df[df.intervention == phase.intervention]
            dset = DataSet.from_df(df_phase, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.dxm)
            dsets[self.to_sid(f"Fig1_dxm_{key}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        changes = {
            **self.default_changes(),
            # 30 mg dextromethorphan hydrobromide
            "PODOSE_dxm": Q(30, "mg") * self.f_dxmhbr_to_dxm(),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),
        }
        for key, phase in PHASES.items():
            # the phases with TPV/r are simulated for the activity score 2
            scores = self.activity_scores if key == "baseline" else [2]
            for activity_score in scores:
                tcsims[self.to_sid(f"{key}_cyp2d6_activity_{activity_score}")] = (
                    Simulation(
                        time_unit="hr",
                        end=28,
                        preinit_changes={
                            **changes,
                            "LI__cyp2d6_ac": Q(activity_score, "dimensionless"),
                            "LI__f_cyp2d6": Q(phase.f_cyp2d6, "dimensionless"),
                            "LI__f_cyp3a4": Q(phase.f_cyp3a4, "dimensionless"),
                        },
                    )
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for key, phase in PHASES.items():
            mappings[self.to_sid(f"fm_dumond2010_dxm_{key}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig1_dxm_{key}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_{key}_cyp2d6_activity_2"),
                    xid="time",
                    yid="[Cve_dxm]",
                ),
                metadata=DexMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    coadministration=phase.coadministration,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plot = fig_dex(experiment=self, fig_id="Fig1", scale="log")
        gstyle = GenotypeStyle(
            activities=np.array([self.activity_scores[0], self.activity_scores[-1]])
        )
        for activity_score in self.activity_scores:
            plot.add_data(
                task=self.to_sid(f"task_baseline_cyp2d6_activity_{activity_score}"),
                xid="time",
                yid="[Cve_dxm]",
                label=f"AS:{activity_score}",
                color=gstyle.color(activity_score),
            )
        colors = {
            "baseline": "black",
            "tpvr_first_dose": "dimgrey",
            "tpvr_steady_state": "silver",
        }
        for key, phase in PHASES.items():
            if key != "baseline":
                plot.add_data(
                    task=self.to_sid(f"task_{key}_cyp2d6_activity_2"),
                    xid="time",
                    yid="[Cve_dxm]",
                    label=f"AS:2 {phase.label}",
                    color=colors[key],
                    linestyle="--",
                )
            plot.add_data(
                dataset=self.to_sid(f"Fig1_dxm_{key}"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"DXM 30 mg {phase.label}",
                color=colors[key],
            )
        return {
            "fig1": fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Dumond2010, output_dir="test", save_results=True)
