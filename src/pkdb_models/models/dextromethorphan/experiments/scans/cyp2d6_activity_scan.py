"""Scan of the CYP2D6 activity."""

from typing import override

import numpy as np
from sbmlsim import Q
from sbmlsim.plot import Figure
from sbmlsim.simulation import Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    fig_scan_array,
)


class CYP2D6ActivityScan(DexSimulationExperiment):
    """Scan of the CYP2D6 activity."""

    #: CYP2D6 activities of the scan, set by `simulations`
    cyp2d6_activities: Quantity

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": Q(30, "mg"),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),  # custom allele
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),  # custom allele
        }
        # the activity scores of the diplotypes, from poor (0) to ultrarapid (3)
        self.cyp2d6_activities = Q(np.linspace(0.0, 3.0, num=13), "dimensionless")
        for k, cyp2d6_activity in enumerate(self.cyp2d6_activities):
            tcsims[f"cyp2d6_activity_{k}"] = Simulation(
                time_unit="hr",
                end=15,
                preinit_changes={
                    **changes,
                    "LI__cyp2d6_ac": cyp2d6_activity,
                },
            )

        return tcsims

    @override
    def figures(self) -> dict[str, Figure]:
        activities = self.cyp2d6_activities.magnitude
        fig, plots = fig_scan_array(
            experiment=self,
            fig_id="Fig_CYP2D6Activity",
            array=activities,
            task_pattern="task_cyp2d6_activity_{}",
            yid_scan="LI__cyp2d6_ac",
        )
        plots[0].set_yaxis(
            self.label_cyp2d6_activity, unit=self.unit_dimless, scale="linear"
        )
        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(CYP2D6ActivityScan, output_dir="test")
