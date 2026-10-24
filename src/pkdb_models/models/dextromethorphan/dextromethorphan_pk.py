"""Pharmacokinetic parameters of the dextromethorphan scans.

The parameters are the non-compartmental analysis of `pkpdutils`, named like
the variables of its `NCAResult` (e.g. `auc_inf_obs`, `cmax`, `thalf`,
`lambda_z`, `cl_f`, `vz_f`), with the unit of every parameter in
`<name>_unit`. Dextromethorphan and its metabolites are analysed in the venous
plasma; only dextromethorphan has a dose of its own (oral `PODOSE_dxm` or
intravenous `IVDOSE_dxm`), a metabolite has no clearance and no volume. The
concentrations below `LLOQ_FRACTION` of the maximum are below the limit of
quantification, so that the noise of the integrator is not the terminal phase.

A scan has one dimension, the scanned parameter; a run over the draws of the
fitted parameters (`run_simulation pkdb_models.models.dextromethorphan
--uncertainty`) adds the dimension of the draws. The parameters are calculated
for every point of every dimension, a row per point with its position along
each dimension (the columns `point` and, with draws, `draw`), see `summarize`.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pkpdsim.pk import nca_frame, scan_nca
from pkpdsim.scan import scan_dimensions, start_values
from pkpdutils import Route
from sbmlsim import Q
from sbmlsim.result import ScanResult

if TYPE_CHECKING:
    from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
        DexSimulationExperiment,
    )

#: the analytes -> their concentration in the venous plasma; the total
#: dextrorphan (free and conjugated) is what most studies measure
ANALYTES: dict[str, str] = {
    "dxm": "[Cve_dxm]",
    "dxo": "[Cve_dxo]",
    "dxo_glu": "[Cve_dxo_glu]",
    "dxo_total": "dxo_total",
    "mm": "[Cve_mm]",
}
#: the molecular weight of an analyte, the sums in equivalents of the parent
MR_ANALYTE: dict[str, str] = {
    "dxm": "dxm",
    "dxo": "dxo",
    "dxo_glu": "dxoglu",
    "dxo_total": "dxo",
    "mm": "dxo",
}
#: the doses of an analyte by route
DOSES: dict[Route, str] = {
    Route.IV_BOLUS: "IVDOSE_{sid}",
    Route.ORAL: "PODOSE_{sid}",
}
#: the limit of quantification relative to the maximal concentration
LLOQ_FRACTION = 1e-4


def _point_dimension(res: ScanResult, across: str | None) -> str:
    """Get the dimension of the scan besides the draws `across`.

    Raises:
        ValueError: if the scan has not one dimension besides the draws.
    """
    dims = scan_dimensions(res, across)
    if len(dims) != 1:
        raise ValueError(
            f"A scan of one dimension is required, not of {dims} (draws: {across})."
        )
    return dims[0]


def _nca(
    res: ScanResult, key: str, substance: str, doses: Mapping[Route, np.ndarray]
) -> pd.DataFrame:
    """Get the analysis of a timecourse at every point of a scan with its dose.

    A point is analysed with the dose of the last route of `doses` which is
    positive at it, without a dose if none is; every route is one analysis of
    all points, of which the rows of its points are taken.

    Args:
        res: result of the scan.
        key: the concentration.
        substance: the analyte.
        doses: the amount of every route [mmol], an array over the dimensions
            of the scan.

    Returns:
        A row per point, see `pkpdsim.pk.nca_frame`.
    """
    shape = tuple(res.ds.sizes[dim] for dim in res.dims)
    rest = np.ones(shape, dtype=bool)
    parts: list[tuple[np.ndarray, pd.DataFrame]] = []
    for route, amount in reversed(list(doses.items())):
        dosed = rest & (amount > 0)
        if dosed.any():
            result = scan_nca(
                res,
                key,
                dose=Q(np.where(dosed, amount, np.nan), "mmole"),
                route=route,
                substance=substance,
                lloq_fraction=LLOQ_FRACTION,
            )
            parts.append((dosed, nca_frame(result)))
        rest &= ~dosed
    if rest.any():
        result = scan_nca(
            res,
            key,
            dose=None,
            route=None,
            substance=substance,
            lloq_fraction=LLOQ_FRACTION,
        )
        parts.append((rest, nca_frame(result)))
    if len(parts) == 1:
        return parts[0][1]
    # the rows of a point from the analysis of its dose (C order of both), the
    # columns in the order of the first point of every analysis
    parts.sort(key=lambda part: int(np.argmax(part[0])))
    return pd.concat([df[mask.ravel()] for mask, df in parts]).sort_index()


def calculate_dextromethorphan_pk(
    experiment: DexSimulationExperiment,
    res: ScanResult,
    across: str | None = None,
    substances: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Calculate the pharmacokinetic parameters of every simulation of a scan.

    The non-compartmental analysis of all simulations at once per analyte
    (`pkpdsim.pk.scan_nca`); dextromethorphan with its dose, in the substance
    unit of the concentration which `cl_f` and `vz_f` require, a metabolite
    without a dose.

    Args:
        experiment: experiment of the scan, for the molecular weight.
        res: result of the scan, with the dose of dextromethorphan.
        across: the dimension of the draws of the fitted parameters, `None`
            for a scan without draws.
        substances: the analytes, keys of `ANALYTES`, all by default.

    Returns:
        One row per simulation of the scan and analyte, with its position
        (`point`, and `draw` with draws), the parameters and their units
        (`<name>_unit`).
    """
    point = _point_dimension(res, across)
    units = res.units
    frames = []
    for substance in ANALYTES if substances is None else substances:
        mr = getattr(experiment.Mr, MR_ANALYTE[substance])
        doses = {
            route: (Q(start_values(res, key).values, units[key]) / mr)
            .to("mmole")
            .magnitude
            for route, template in DOSES.items()
            if (key := template.format(sid=substance)) in res.ds
        }
        df = _nca(res, ANALYTES[substance], substance, doses).drop(columns="nca_flags")
        df.insert(len(res.dims), "substance", substance)
        frames.append(df)
    names = {point: "point", **({across: "draw"} if across is not None else {})}
    return pd.concat(frames, ignore_index=True).rename(columns=names)


def summarize(
    df: pd.DataFrame, key: str, quantiles: tuple[float, float]
) -> pd.DataFrame:
    """Get the median and the quantiles of a parameter over the draws of every point.

    Args:
        df: the parameters with the columns `point` and `draw`.
        key: the parameter.
        quantiles: the lower and the upper quantile.

    Returns:
        One row per point (the index), the columns `lower`, `median`, `upper`.
    """
    low, high = quantiles
    grouped = df.groupby("point")[key]
    return pd.DataFrame(
        {
            "lower": grouped.quantile(low),
            "median": grouped.median(),
            "upper": grouped.quantile(high),
        }
    ).astype(np.float64)
