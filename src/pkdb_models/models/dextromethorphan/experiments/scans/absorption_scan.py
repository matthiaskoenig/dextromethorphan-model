"""Scan of the absorption rate of dextromethorphan."""

from typing import override

import numpy as np
from matplotlib.colors import Normalize
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


class ABSORBRATEScan(DexSimulationExperiment):
    """Scan of the absorption rate of dextromethorphan."""

    #: absorption rates of the scan, set by `simulations`
    dex_dis_rates: Quantity
    MAX_DISRATE = 0.16

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        changes = {
            **self.default_changes(),
            # the dissolution is the fitted one of the model
            "PODOSE_dxm": Q(30, "mg"),
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),  # custom allele
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),  # custom allele
            "LI__cyp2d6_ac": Q(2, "dimensionless"),  # custom allele
        }

        # a fast absorption of 1 [1/min] followed by the scanned rates
        self.dex_dis_rates = Q(
            np.insert(np.linspace(0.002, self.MAX_DISRATE, num=20), 0, 1.0), "1/min"
        )

        for k, dis_rate in enumerate(self.dex_dis_rates):
            tcsims[f"Ka_abs_dex{k}"] = Simulation(
                time_unit="hr",
                end=15,
                preinit_changes={
                    **changes,
                    "GU__DXMABS_k": dis_rate,
                },
            )
        return tcsims

    @override
    def figures(self) -> dict[str, Figure]:
        rates = self.dex_dis_rates.magnitude
        fig, plots = fig_scan_array(
            experiment=self,
            fig_id="Fig_DEX_ABSOPTION",
            array=rates,
            task_pattern="task_Ka_abs_dex{}",
            scanning_template=fig_dex_dose,
            yid_scan="GU__DXMABS_k",
            # the colors span the scanned rates, the fast absorption is black
            norm=Normalize(vmin=rates[1:].min(), vmax=rates[1:].max()),
            cmap=CMAP.with_extremes(over="black"),
        )
        plots[0].set_yaxis(
            "DXM absorption rate\n(GU__DXMABS_k)\n", unit="1/min", scale="log"
        )
        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(ABSORBRATEScan, output_dir="test")
