"""Simulations of the metabolic ratios over the CYP2D6 activity score."""

from typing import override

import numpy as np
from sbmlsim import Q
from sbmlsim.simulation import Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)


class ActivityScoreExperiment(DexSimulationExperiment):
    """Plasma and urinary metabolic ratios."""

    #: CYP2D6 activity scores of the simulations; set by `simulations`
    cyp2d6_scores: Quantity

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": Q(30, "mg"),
            # custom/custom
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),  # custom allele
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),  # custom allele
        }
        # scan CYP2D6 score from 0 to 3
        # FIXME: use a real scan for accessing data
        self.cyp2d6_scores = Q(np.linspace(0, 3, num=10), "dimensionless")
        for k, cyp2d6_score in enumerate(self.cyp2d6_scores):
            tcsims[f"cyp2d6_score_{k}"] = Simulation(
                time_unit="hr",
                end=24,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": cyp2d6_score,
                },
            )

        return tcsims


if __name__ == "__main__":
    MODEL.run_experiments(
        ActivityScoreExperiment, output_dir="activity_score", save_results=True
    )
