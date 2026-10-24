"""Scan of the dissolution rate of dextromethorphan."""

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
    fig_dex_dose,
    fig_scan_array,
)
from pkdb_models.models.dextromethorphan.utils_plotting import CMAP


class DISRATEScan(DexSimulationExperiment):
    """Scan of the dissolution rate of dextromethorphan."""

    #: dissolution rates of the scan, set by `simulations`
    dex_dis_rates: Quantity
    #: the range of the scanned rates [1/hr], around the fitted rate of the
    #: model (about 0.4 1/hr, `Ka_dis_dxm` of the adopted fit)
    MIN_DISRATE = 0.05
    MAX_DISRATE = 2.0

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        changes = {
            **self.default_changes(),
            # set reference activity
            "PODOSE_dxm": Q(30, "mg"),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),  # custom allele
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),  # custom allele
            "LI__cyp2d6_ac": Q(2, "dimensionless"),  # custom allele
        }

        # a fast dissolution of 100 [1/hr] followed by the scanned rates
        self.dex_dis_rates = Q(
            np.insert(np.geomspace(self.MIN_DISRATE, self.MAX_DISRATE, num=20), 0, 100),
            "1/hr",
        )

        for k, dis_rate in enumerate(self.dex_dis_rates):
            tcsims[f"Ka_dis_dex_{k}"] = Simulation(
                time_unit="hr",
                end=15,
                preinit_changes={
                    **changes,
                    "Ka_dis_dxm": dis_rate,
                },
            )
        return tcsims

    @override
    def figures(self) -> dict[str, Figure]:
        rates = self.dex_dis_rates.magnitude
        fig, plots = fig_scan_array(
            experiment=self,
            fig_id="Fig_DEXDISRATE",
            array=rates,
            task_pattern="task_Ka_dis_dex_{}",
            scanning_template=fig_dex_dose,
            yid_scan="Ka_dis_dxm",
            # the colors span the scanned rates, the fast dissolution is black
            norm=LogNorm(vmin=rates[1:].min(), vmax=rates[1:].max()),
            cmap=CMAP.with_extremes(over="black"),
        )
        plots[0].set_yaxis(
            "DXM dissolution rate\n(Ka_dis_dxm)\n", unit="1/hr", scale="log"
        )
        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(DISRATEScan, output_dir="test")
