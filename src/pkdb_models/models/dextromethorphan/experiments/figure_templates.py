"""Templates for general plots."""

from collections.abc import Callable
from typing import TypedDict

import numpy as np
from matplotlib.colors import Colormap, Normalize, to_hex
from sbmlsim.plot import Axis, Figure, Plot

from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.utils_plotting import CMAP


class CurveStyle(TypedDict):
    """Style of the curves of a scan, keyword arguments of `Plot.add_data`."""

    color: str
    linewidth: float


def hide_xaxis_label(plot: Plot) -> None:
    """Hide the label of the x-axis of a plot, e.g. of the upper plots of a column."""
    if plot.xaxis is not None:
        plot.xaxis.label_visible = False


def fig_dex(
    experiment: DexSimulationExperiment, fig_id: str, scale: str = "linear"
) -> tuple[Figure, Plot]:
    """Template for a single plot."""
    return fig_single(
        experiment=experiment,
        fig_id=fig_id,
        name=experiment.label_dxm,
        unit=experiment.unit_dxm,
        scale=scale,
    )


def fig_dor(
    experiment: DexSimulationExperiment, fig_id: str, scale: str = "linear"
) -> tuple[Figure, Plot]:
    """Template for a single plot."""
    return fig_single(
        experiment=experiment,
        fig_id=fig_id,
        name=experiment.label_dxo,
        unit=experiment.unit_dxo,
        scale=scale,
    )


def fig_dor_total(
    experiment: DexSimulationExperiment, fig_id: str
) -> tuple[Figure, Plot]:
    """Template for a single plot."""
    return fig_single(
        experiment=experiment,
        fig_id=fig_id,
        name=experiment.label_dxo_total,
        unit=experiment.unit_dxo,
    )


def fig_single(
    experiment: DexSimulationExperiment,
    fig_id: str,
    name: str,
    unit: str,
    scale: str = "linear",
) -> tuple[Figure, Plot]:
    """Template for single-plot."""
    fig = Figure(
        experiment=experiment,
        sid=experiment.to_sid(fig_id),
        name=f"{experiment.sid}_{fig_id}",
    )
    plots = fig.create_plots(
        xaxis=Axis(experiment.label_time, unit=experiment.unit_time),
        yaxis=Axis(name, unit=unit, scale=scale),
        legend=True,
    )

    return fig, plots[0]


def fig_dex_dor(
    experiment: DexSimulationExperiment, fig_id: str, scale: str = "linear"
) -> tuple[Figure, list[Plot]]:
    """Template for dex-dor-plot."""
    fig = Figure(
        experiment=experiment,
        sid=experiment.to_sid(fig_id),
        name=f"{experiment.sid}_{fig_id}",
        num_rows=4,
    )
    plots = fig.create_plots(xaxis=Axis("time", unit=experiment.unit_time), legend=True)
    plots[0].set_yaxis(experiment.label_dxm, unit=experiment.unit_dxm, scale=scale)
    plots[1].set_yaxis(experiment.label_dxo, unit=experiment.unit_dxo, scale=scale)
    plots[2].set_yaxis(
        experiment.label_dxm_ur, unit=experiment.unit_dxm_ur, scale=scale
    )
    plots[3].set_yaxis(
        experiment.label_dxo_ur, unit=experiment.unit_dxo_ur, scale=scale
    )
    for plot in plots[:3]:
        hide_xaxis_label(plot)

    return fig, plots


def fig_dex_dor_dor_total(
    experiment: DexSimulationExperiment, fig_id: str, scale: str = "linear"
) -> tuple[Figure, list[Plot]]:
    """Template for dex-dor-plot."""
    fig = Figure(
        experiment=experiment,
        sid=experiment.to_sid(fig_id),
        name=f"{experiment.sid}_{fig_id}",
        num_rows=5,
    )
    plots = fig.create_plots(xaxis=Axis("time", unit=experiment.unit_time), legend=True)
    plots[0].set_yaxis(experiment.label_dxm, unit=experiment.unit_dxm, scale=scale)
    plots[1].set_yaxis(experiment.label_dxo, unit=experiment.unit_dxo, scale=scale)
    plots[2].set_yaxis(
        experiment.label_dxm_ur, unit=experiment.unit_dxm_ur, scale=scale
    )
    plots[3].set_yaxis(
        experiment.label_dxo_ur, unit=experiment.unit_dxo_ur, scale=scale
    )
    plots[4].set_yaxis(
        experiment.label_dxo_total_ur, unit=experiment.unit_dxo_total_ur, scale=scale
    )
    for plot in plots[:4]:
        hide_xaxis_label(plot)

    return fig, plots


def fig_dex_dor_plasma(
    experiment: DexSimulationExperiment, fig_id: str, scale: str = "linear"
) -> tuple[Figure, list[Plot]]:
    """Template for dex-dor plasma."""
    fig = Figure(
        experiment=experiment,
        sid=experiment.to_sid(fig_id),
        name=f"{experiment.sid}_{fig_id}",
        num_rows=2,
    )
    plots = fig.create_plots(xaxis=Axis("time", unit=experiment.unit_time), legend=True)
    plots[0].set_yaxis(experiment.label_dxm, unit=experiment.unit_dxm, scale=scale)
    plots[1].set_yaxis(
        experiment.label_dxo_total, unit=experiment.unit_dxo, scale=scale
    )
    hide_xaxis_label(plots[0])

    return fig, plots


def fig_dex_dor_urine(
    experiment: DexSimulationExperiment, fig_id: str, scale: str = "linear"
) -> tuple[Figure, list[Plot]]:
    """Template for dex-dor urine."""
    fig = Figure(
        experiment=experiment,
        sid=experiment.to_sid(fig_id),
        name=f"{experiment.sid}_{fig_id}",
        num_rows=2,
    )
    plots = fig.create_plots(xaxis=Axis("time", unit=experiment.unit_time), legend=True)
    plots[0].set_yaxis(
        experiment.label_dxm_ur, unit=experiment.unit_dxm_ur, scale=scale
    )
    plots[1].set_yaxis(
        experiment.label_dxo_ur, unit=experiment.unit_dxo_ur, scale=scale
    )
    hide_xaxis_label(plots[0])

    return fig, plots


def fig_mr_urine(
    experiment: DexSimulationExperiment, fig_id: str
) -> tuple[Figure, list[Plot]]:
    """Template for the CYP2D6 phenotype-genotype matching.

    The phenotyping is performed with dextromethorphan and urinary metabolic ratios.
    """
    fig = Figure(
        experiment=experiment,
        sid=experiment.to_sid(fig_id),
        name=f"{experiment.sid}_{fig_id}",
        num_rows=1,
    )
    plots = fig.create_plots(xaxis=Axis("time", unit=experiment.unit_time), legend=True)
    plots[0].set_yaxis(
        experiment.label_mr_urine, unit=experiment.unit_dimless, scale="log"
    )
    return fig, plots


def fig_mrtot_urine(
    experiment: DexSimulationExperiment, fig_id: str
) -> tuple[Figure, list[Plot]]:
    """Template for the CYP2D6 phenotype-genotype matching.

    The phenotyping is performed with dextromethorphan and urinary metabolic ratios.
    """
    fig = Figure(
        experiment=experiment,
        sid=experiment.to_sid(fig_id),
        name=f"{experiment.sid}_{fig_id}",
        num_rows=1,
    )
    plots = fig.create_plots(xaxis=Axis("time", unit=experiment.unit_time), legend=True)
    plots[0].set_yaxis(
        experiment.label_mrtot_urine, unit=experiment.unit_dimless, scale="log"
    )
    return fig, plots


def fig_mr_urine_plasma(
    experiment: DexSimulationExperiment, fig_id: str
) -> tuple[Figure, list[Plot]]:
    """Template for the CYP2D6 phenotype-genotype matching.

    The phenotyping is performed with dextromethorphan and urinary metabolic ratios.
    """
    fig = Figure(
        experiment=experiment,
        sid=experiment.to_sid(fig_id),
        name=f"{experiment.sid}_{fig_id}",
        num_rows=2,
    )
    plots = fig.create_plots(xaxis=Axis("time", unit=experiment.unit_time), legend=True)
    plots[0].set_yaxis(
        experiment.label_mr_urine, unit=experiment.unit_dimless, scale="log"
    )
    plots[1].set_yaxis(
        experiment.label_mr_plasma, unit=experiment.unit_dimless, scale="log"
    )
    hide_xaxis_label(plots[0])

    return fig, plots


def fig_mr_urine_serum(
    experiment: DexSimulationExperiment, fig_id: str
) -> tuple[Figure, list[Plot]]:
    """Template for the CYP2D6 phenotype-genotype matching.

    The phenotyping is performed with dextromethorphan and urinary metabolic ratios.
    """
    fig = Figure(
        experiment=experiment,
        sid=experiment.to_sid(fig_id),
        name=f"{experiment.sid}_{fig_id}",
        num_rows=2,
    )
    plots = fig.create_plots(xaxis=Axis("time", unit=experiment.unit_time), legend=True)
    plots[0].set_yaxis(
        experiment.label_mr_urine, unit=experiment.unit_dimless, scale="log"
    )
    plots[1].set_yaxis(
        experiment.label_mr_serum, unit=experiment.unit_dimless, scale="log"
    )
    hide_xaxis_label(plots[0])

    return fig, plots


def fig_cyp2d6_interaction(
    experiment: DexSimulationExperiment,
    fig_id: str,
) -> tuple[Figure, list[Plot]]:
    """Template for drug-drug (quinidine) or drug-gene (CYP2D6 genotype) interactions."""
    fig = Figure(
        experiment=experiment,
        sid=experiment.to_sid(fig_id),
        name=f"{experiment.sid}_{fig_id}",
        num_cols=3,
        num_rows=3,
    )

    plots = fig.create_plots(xaxis=Axis("time", unit=experiment.unit_time), legend=True)
    plots[0].set_yaxis(
        experiment.label_cyp2d6_activity, unit="dimensionless", scale="linear"
    )

    # metabolic ratios (plasma & urine)
    plots[1].set_yaxis(
        experiment.label_mr_plasma, unit=experiment.unit_dimless, scale="log"
    )
    plots[2].set_yaxis(
        experiment.label_mrtot_urine, unit=experiment.unit_dimless, scale="log"
    )

    # metabolites
    plots[4].set_yaxis(experiment.label_dxm, unit=experiment.unit_dxm)
    plots[7].set_yaxis(experiment.label_dxo, unit=experiment.unit_dxo)

    plots[5].set_yaxis(experiment.label_dxm_ur, unit=experiment.unit_dxm_ur)
    plots[8].set_yaxis(experiment.label_dxo_ur, unit=experiment.unit_dxo_ur)

    # rates
    # N-demethylation in the liver
    plots[3].set_yaxis("Liver metabolism\n(CYP3A4)\n", unit="µmole/min")
    # liver CYP2D6 (DXM -> DXO)
    plots[6].set_yaxis("Liver metabolism\n(CYP2D6)\n", unit="µmole/min")

    return fig, plots


def fig_dex_dose(
    experiment: DexSimulationExperiment, fig_id: str
) -> tuple[Figure, list[Plot]]:
    """Template for the scan of the dextromethorphan dose."""
    fig, plots = fig_cyp2d6_interaction(experiment, fig_id)
    plots[0].set_yaxis("DXM oral dose\n", unit="mg", scale="linear")

    return fig, plots


def fig_f_cyp2d6(
    experiment: DexSimulationExperiment, fig_id: str
) -> tuple[Figure, list[Plot]]:
    """Template for the inhibition of CYP2D6 (quinidine, paroxetine)."""
    fig, plots = fig_cyp2d6_interaction(experiment, fig_id)
    plots[0].set_yaxis(
        "CYP2D6 activity\n(f_cyp2d6)\n", unit="dimensionless", scale="log"
    )

    return fig, plots


def fig_f_cyp3a4(
    experiment: DexSimulationExperiment, fig_id: str
) -> tuple[Figure, list[Plot]]:
    """Template for the inhibition or induction of CYP3A4."""
    fig, plots = fig_cyp2d6_interaction(experiment, fig_id)
    plots[0].set_yaxis(
        "CYP3A4 activity\n(f_cyp3a4)\n", unit="dimensionless", scale="log"
    )

    return fig, plots


def fig_scan_array(
    experiment: DexSimulationExperiment,
    fig_id: str,
    array: np.ndarray,
    task_pattern: str,
    scanning_template: Callable[
        ..., tuple[Figure, list[Plot]]
    ] = fig_cyp2d6_interaction,
    yid_scan: str | None = None,
    norm: Normalize | None = None,
    cmap: Colormap = CMAP,
) -> tuple[Figure, list[Plot]]:
    """Template for the scan of a parameter.

    Args:
        experiment: the experiment of the figure.
        fig_id: id of the figure.
        array: the values of the scanned parameter, which color the curves.
        task_pattern: the task of the k-th value, `task_pattern.format(k)`.
        scanning_template: template of the figure.
        yid_scan: the scanned parameter, which the first plot shows.
        norm: the normalization of the values to the colormap, linear from 0 to
            the largest value by default; a scan over orders of magnitude needs
            a `LogNorm` of its range.
        cmap: the colormap of the values.
    """
    if norm is None:
        norm = Normalize(vmin=0, vmax=float(array.max()))
    fig, plots = scanning_template(experiment=experiment, fig_id=fig_id)
    for k, value in enumerate(array):
        task_id = task_pattern.format(k)
        color = to_hex(cmap(norm(value)))

        kwargs: CurveStyle = {"color": color, "linewidth": 2.0}

        # scanned parameter
        if yid_scan is not None:
            plots[0].add_data(
                task=experiment.to_sid(task_id), xid="time", yid=yid_scan, **kwargs
            )

        # plasma ratio
        plots[1].add_data(
            task=experiment.to_sid(task_id), xid="time", yid="dxm_dxo", **kwargs
        )
        # urinary ratio
        plots[2].add_data(
            task=experiment.to_sid(task_id),
            xid="time",
            yid="dxm_dxo_total_urine",
            **kwargs,
        )

        # plasma
        plots[4].add_data(
            task=experiment.to_sid(task_id), xid="time", yid="[Cve_dxm]", **kwargs
        )
        plots[7].add_data(
            task=experiment.to_sid(task_id), xid="time", yid="[Cve_dxo]", **kwargs
        )

        # urinary excretion
        plots[5].add_data(
            task=experiment.to_sid(task_id), xid="time", yid="Aurine_dxm", **kwargs
        )
        plots[8].add_data(
            task=experiment.to_sid(task_id), xid="time", yid="Aurine_dxo", **kwargs
        )

        # the CYP2D6-independent metabolism in the liver
        plots[3].add_data(
            task=experiment.to_sid(task_id),
            xid="time",
            yid="LI__DXMNDM",
            label="N-demethylation" if k == 0 else None,
            linestyle=":",
            **kwargs,
        )
        plots[3].add_data(
            task=experiment.to_sid(task_id),
            xid="time",
            yid="LI__DXMCYPX",
            label="O-demethylation (CYPX)" if k == 0 else None,
            linestyle="-",
            **kwargs,
        )

        # liver CYP2D6 (DXM -> DXO)
        plots[6].add_data(
            task=experiment.to_sid(task_id),
            xid="time",
            yid="LI__DXMCYP2D6",
            label="CYP2D6" if k == 0 else None,
            **kwargs,
        )

    return fig, plots
