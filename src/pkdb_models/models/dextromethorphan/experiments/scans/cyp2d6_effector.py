"""Scan of the activity of CYP2D6 under an inhibitor (quinidine, paroxetine)."""

from typing import override

import numpy as np
from matplotlib.colors import LogNorm
from sbmlsim import Q
from sbmlsim.plot import Figure
from sbmlsim.simulation import Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    fig_f_cyp2d6,
    fig_scan_array,
)


class CYP2D6InhibitionScan(DexSimulationExperiment):
    """Scan of the activity of CYP2D6, the inhibition by quinidine or paroxetine."""

    #: activities of CYP2D6 of the scan, set by `simulations`
    f_cyp2d6: Quantity

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": Q(30, "mg"),
        }
        self.f_cyp2d6 = Q(np.logspace(-3, 0, num=7), "dimensionless")
        for k, f_cyp2d6 in enumerate(self.f_cyp2d6):
            tcsims[f"f_cyp2d6_{k}"] = Simulation(
                time_unit="hr",
                end=15,
                preinit_changes={
                    **changes,
                    "LI__f_cyp2d6": f_cyp2d6,
                },
            )
        return tcsims

    @override
    def figures(self) -> dict[str, Figure]:
        values = self.f_cyp2d6.magnitude
        fig, _ = fig_scan_array(
            experiment=self,
            fig_id="Fig_f_cyp2d6",
            array=values,
            task_pattern="task_f_cyp2d6_{}",
            scanning_template=fig_f_cyp2d6,
            yid_scan="LI__f_cyp2d6",
            norm=LogNorm(vmin=values.min(), vmax=values.max()),
        )
        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(CYP2D6InhibitionScan, output_dir="test")
