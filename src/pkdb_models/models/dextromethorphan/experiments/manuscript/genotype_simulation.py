"""Simulations of a subset of CYP2D6 diplotypes."""

from typing import ClassVar, override

from sbmlsim import Q
from sbmlsim.simulation import Simulation

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.experiments.genotype_phenotype import (
    GenotypeScoring,
)


class GenotypeExperiment(DexSimulationExperiment):
    """Simulation of subset of genotypes."""

    # subset of diplotypes corresponding to data
    diplotypes: ClassVar[list[str]] = [
        "*4/*5",
        "*1/*6",
        "*17/*17",
        "*17/*29",
        "*2/*6",
        "*29/*41",
        "*6/*35",
        "*1/*29",
        "*1x2/*4",
        "*35/*35",
        "*2/*2x2",
        "*1/*1",
        "*1/*2",
        "*2/*2",
        "*1/*4",
        "*2/*4",
        "*4/*4",
        "*1x2/*1",
        "*2x2/*1",
        "*1x2/*10",
        "*2x2/*4",
        "*1/*10",
        "*2/*10",
        "*2/*17",
        "*4/*10",
        "*3/*4",
        "*1/*1x2",
        "*1x2/*2",
        "*1/*2x2",
        "*1x2/*41",
        "*1/*9",
        "*1/*41",
        "*2/*41",
        "*10/*41x2",
        "*1/*3",
        "*1/*5",
        "*1/*42",
        "*2/*5",
        "*10/*10",
        "*10/*41",
        "*4/*41",
        "*5/*10",
        "*5/*29",
        "*1x2/*17",
        "*2x2/*17",
        "*2x2/*5",
        "*1/*17",
        "*2/*29",
        "*1/*4x2",
        "*1/*36",
        "*10/*17",
        "*17/*41",
        "*29/*29",
        "*4/*17",
        "*4x2/*17",
        "*5/*17",
        "*17/*42",
        "*5/*5",
        "*1x2/*5",
        "*1/*10x2",
        "*2/*4x2",
        "*10/*10x2",
        "*1/*21",
        "*10/*36",
        "*2/*3",
        "*2/*14",
        "*2/*21",
        "*4/*36",
        "*5/*14",
        "*10/*14",
        "*1/*7",
        "*3/*3",
        "*6/*6",
        "*4/*6",
    ]

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        for n, diplotype in enumerate(self.diplotypes):
            diplotype_indexes = GenotypeScoring.indices_for_diplotype(diplotype)
            tcsims[f"dex20_{n}"] = Simulation(
                time_unit="hr",
                end=24,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_dxm": Q(30, "mg"),
                    "LI__cyp2d6_allele1": Q(diplotype_indexes[0], "dimensionless"),
                    "LI__cyp2d6_allele2": Q(diplotype_indexes[1], "dimensionless"),
                },
            )
        return tcsims


if __name__ == "__main__":
    MODEL.run_experiments(GenotypeExperiment, output_dir="genotype", save_results=True)
