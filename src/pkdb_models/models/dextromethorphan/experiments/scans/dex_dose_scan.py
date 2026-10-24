"""Scan of the dextromethorphan dose."""

from collections.abc import Callable
from typing import override

import numpy as np
import seaborn as sns
from matplotlib.colors import to_hex
from sbmlsim import Q
from sbmlsim.plot import Figure, Plot
from sbmlsim.simulation import Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.experiments.figure_templates import (
    CurveStyle,
    fig_cyp2d6_interaction,
    fig_dex_dose,
)

CMAP = sns.color_palette("flare", as_cmap=True)


class DEXDoseScan(DexSimulationExperiment):
    """Scan of the dextromethorphan dose."""

    #: doses of the scan, set by `simulations`
    dxm_doses: Quantity
    MAX_DOSE = 100

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}
        changes = {
            **self.default_changes(),
            # set reference activity
            "LI__cyp2d6_allele1": Q(-1, "dimensionless"),  # custom allele
            "LI__cyp2d6_allele2": Q(-1, "dimensionless"),  # custom allele
            "LI__cyp2d6_ac": Q(2, "dimensionless"),  # custom allele
        }

        self.dxm_doses = Q(np.linspace(0.1, self.MAX_DOSE, num=10), "mg")

        for k, dxm_dose in enumerate(self.dxm_doses):
            tcsims[f"dxm_dose_{k}"] = Simulation(
                time_unit="hr",
                end=15,
                preinit_changes={
                    **changes,
                    "PODOSE_dxm": dxm_dose,
                },
            )

        return tcsims

    @override
    def figures(self) -> dict[str, Figure]:
        fig, plots = self.fig_scan_array(
            fig_id="Fig_DEXDose",
            array=self.dxm_doses.magnitude,
            task_pattern="task_dxm_dose_{}",
            scanning_template=fig_dex_dose,
        )
        for k, dxm_dose in enumerate(self.dxm_doses):
            task_id = f"task_dxm_dose_{k}"
            color = to_hex(CMAP(dxm_dose.magnitude / self.MAX_DOSE))
            plots[0].add_data(
                task=task_id,
                xid="time",
                yid="PODOSE_dxm",
                color=color,
                linewidth=2.0,
            )
        return self.figures_by_sid(fig)

    def fig_scan_array(
        self,
        fig_id: str,
        array: np.ndarray,
        task_pattern: str,
        scanning_template: Callable[
            ..., tuple[Figure, list[Plot]]
        ] = fig_cyp2d6_interaction,
    ) -> tuple[Figure, list[Plot]]:
        """Template for the scan of the dose, with the gut lumen in the first pass panel.

        The panel of the urinary excretion of dextromethorphan has the feces as well.

        Args:
            fig_id: id of the figure.
            array: the values of the scanned dose, which color the curves.
            task_pattern: the task of the k-th value, `task_pattern.format(k)`.
            scanning_template: template of the figure.
        """
        fig, plots = scanning_template(experiment=self, fig_id=fig_id)
        plots[3].set_yaxis("DXM gut lumen\n", unit=self.unit_dxm)
        plots[5].set_yaxis(
            "dextromethorphan (DXM)\nurine, feces\n", unit=self.unit_dxm_ur
        )
        for k, value in enumerate(array):
            task_id = task_pattern.format(k)
            color = to_hex(CMAP(value / array.max()))

            kwargs: CurveStyle = {"color": color, "linewidth": 2.0}

            # plasma ratio
            plots[1].add_data(task=task_id, xid="time", yid="dxm_dxo", **kwargs)
            # urinary ratio
            plots[2].add_data(
                task=task_id, xid="time", yid="dxm_dxo_total_urine", **kwargs
            )

            # plasma
            plots[4].add_data(task=task_id, xid="time", yid="[Cve_dxm]", **kwargs)
            plots[7].add_data(task=task_id, xid="time", yid="[Cve_dxo]", **kwargs)

            # urinary excretion
            plots[5].add_data(
                task=task_id,
                xid="time",
                yid="Aurine_dxm",
                label="urine" if k == 0 else None,
                **kwargs,
            )
            plots[8].add_data(task=task_id, xid="time", yid="Aurine_dxo", **kwargs)

            # gut lumen and feces
            plots[3].add_data(
                task=task_id,
                xid="time",
                yid="[Cgulumen_dxm]",
                linestyle=":",
                **kwargs,
            )
            plots[5].add_data(
                task=task_id,
                xid="time",
                yid="Afeces_dxm",
                label="feces" if k == 0 else None,
                linestyle=":",
                **kwargs,
            )

            # liver CYP2D6 (DXM -> DXO)
            plots[6].add_data(
                task=task_id,
                xid="time",
                yid="LI__DXMCYP2D6",
                **kwargs,
            )

        return fig, plots


if __name__ == "__main__":
    MODEL.run_experiments(DEXDoseScan, output_dir="test", save_results=True)
