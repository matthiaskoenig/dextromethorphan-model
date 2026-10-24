"""Scan of the activity of CYP3A4, which carries the CYP2D6-independent metabolism."""

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
    fig_f_cyp3a4,
    fig_scan_array,
)


class CYP3A4ActivityScan(DexSimulationExperiment):
    """Scan of the activity of CYP3A4 (inhibition, induction by a coadministered drug)."""

    #: activities of CYP3A4 of the scan, set by `simulations`
    f_cyp3a4: Quantity

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        changes = {
            **self.default_changes(),
            "PODOSE_dxm": Q(30, "mg"),
        }
        self.f_cyp3a4 = Q(np.logspace(-2, 1, num=7), "dimensionless")
        for k, f_cyp3a4 in enumerate(self.f_cyp3a4):
            tcsims[f"f_cyp3a4_{k}"] = Simulation(
                time_unit="hr",
                end=15,
                preinit_changes={
                    **changes,
                    "LI__f_cyp3a4": f_cyp3a4,
                },
            )
        return tcsims

    @override
    def figures(self) -> dict[str, Figure]:
        values = self.f_cyp3a4.magnitude
        fig, _ = fig_scan_array(
            experiment=self,
            fig_id="Fig_f_cyp3a4",
            array=values,
            task_pattern="task_f_cyp3a4_{}",
            scanning_template=fig_f_cyp3a4,
            yid_scan="LI__f_cyp3a4",
            norm=LogNorm(vmin=values.min(), vmax=values.max()),
        )
        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(CYP3A4ActivityScan, output_dir="test")
