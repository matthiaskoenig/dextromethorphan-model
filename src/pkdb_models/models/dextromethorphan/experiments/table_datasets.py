"""Datasets of the tables of a study, split into single curves (Schadel1995).

The tables of a study are split by group, individual, measurement, tissue and
intervention. The recoveries [% of dose] are molar percentages of the
dextromethorphan dose ("the molar amount excreted and expressed as a
percentage of the dextromethorphan dose", Schadel1995), so every substance is
converted to an amount with the dose of the base of the intervention in the
`study.json` of the study divided by the molecular weight of
dextromethorphan; the mass concentrations of dextromethorphan and dextrorphan
are converted to molar ones. The N-demethylated morphinans of the model (`mm`)
are the sum of the reported 3-methoxymorphinan and 3-hydroxymorphinan (free
and conjugated), see `sum_substances`.
"""

import json
import math
import warnings
from collections.abc import Collection, Mapping
from typing import Any

import pandas as pd
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.units import Quantity

from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)

intervention_mapping: dict[str, str] = {
    # interventions
    "dmthbr": "DEXHBr",
    "dmt": "DEX",
    "dextromethorphan": "DEX",
    "dextromethorphan hydrobromide": "DEXHBr",
    "quinidine": "Q",
    "quinidine sulphate": "Q",
    "qui-s": "Q",
}

key_mapping: dict[str, str] = {
    # substances
    "dextromethorphan": "dex",
    "dextrorphan": "dor",
    "3-methoxymorphinan": "mom3",
    "3-hydroxymorphinan": "hom3",
    "3-hydroxymorphinan-glucuronide": "hom3-glu",
    "dextrorphan-glucuronide": "dor-glu",
    "hm3+dtf+dex+mom3": "dex_total",
    "3-methoxymorphinan+3-hydroxymorphinan": "mm",
    # groups
    "all": "all",
    "um": "UM",
    "em": "EM",
    "im": "IM",
    "pm": "PM",
    "UM": "UM",
    "EM": "EM",
    "IM": "IM",
    "PM": "PM",
    # measurement
    "concentration": "concentration",
    "recovery": "recovery",
    # tissue
    "urine": "urine",
    "plasma": "plasma",
    "serum": "serum",
    # units
    "gram": "g",
    "milligram": "mg",
}

#: the N-demethylated morphinans of the model (`mm`): the sum of
#: 3-methoxymorphinan and 3-hydroxymorphinan, free and conjugated
MM_SUBSTANCE = "3-methoxymorphinan+3-hydroxymorphinan"
MM_PARTS: frozenset[str] = frozenset(
    {
        "3-methoxymorphinan",
        "3-hydroxymorphinan",
        "3-hydroxymorphinan-glucuronide",
    }
)

#: the substances which are not loaded as curves of their own: the parts of
#: the N-demethylated morphinans, which the model has only as their sum, and
#: the urinary total of dextromethorphan and all its metabolites (Schadel1995
#: Fig4), which the model has no observable of
NOT_LOADED: frozenset[str] = MM_PARTS | {"hm3+hm3glu+dtf+dtfglu+dex+mom3"}

#: the molecular weights of the mass concentrations which are converted
MASS_CONCENTRATIONS: dict[str, str] = {
    "dextromethorphan": "dxm",
    "dextrorphan": "dxo",
}


def sum_substances(
    frames: Mapping[str, pd.DataFrame], parts: Collection[str], name: str
) -> pd.DataFrame | None:
    """Get the sum of the substances of a table, per curve and time.

    A curve (group, individual, measurement, tissue, intervention) sums the
    parts it reports; a time point enters the sum when every part of the curve
    has a value at it. The standard deviations are added in quadrature (the
    parts are treated as independent).

    Args:
        frames: the data of a table by substance.
        parts: the substances which are summed.
        name: the substance of the sum.

    Returns:
        The rows of the sum, None if the table has none of the parts.

    Raises:
        ValueError: if the parts of a curve have different units.
    """
    dfs = [frames[part] for part in parts if part in frames]
    if not dfs:
        return None
    df = pd.concat(dfs, ignore_index=True)
    y = "mean" if "mean" in df.columns else "value"
    curve = [
        c
        for c in ["group", "id", "measurement", "tissue", "intervention"]
        if c in df.columns
    ]
    rows = []
    for _, df_curve in df.groupby(curve):
        if df_curve["unit"].nunique() != 1:
            raise ValueError(f"The parts of '{name}' have different units.")
        n_parts = df_curve["substance"].nunique()
        for _, df_time in df_curve.groupby("time"):
            if df_time["substance"].nunique() < n_parts or df_time[y].isna().any():
                continue
            row = df_time.iloc[0].copy()
            row["substance"] = name
            if "label" in row.index:
                row["label"] = name
            row[y] = df_time[y].sum()
            for err in ["sd", "se"]:
                if err in row.index:
                    row[err] = math.sqrt(float((df_time[err] ** 2).sum()))
            rows.append(row)
    return pd.DataFrame(rows).reset_index(drop=True)


def from_csv(
    experiment: DexSimulationExperiment,
    fig_ids: list[str],
    sum_mm: bool = False,
) -> dict[str, DataSet]:
    """Get the datasets of the tables of a study, one per curve.

    Args:
        experiment: the experiment of the study.
        fig_ids: ids of the figures and tables of the study, e.g. `Fig2`.
        sum_mm: whether the N-demethylated morphinans of the table are summed
            to a curve of `MM_SUBSTANCE` (only for tables which report all of
            them which were measured).

    Returns:
        The datasets by key, the SId (`experiment.to_sid`) of
        `<fig_id>_<substance>_<group>_<measurement>_<tissue>_<intervention>`
        (the parts which the table has).
    """
    dsets: dict[str, DataSet] = {}
    for sheet_id in fig_ids:
        # split by substance
        frames = experiment.load_dataframes_by_substance(sheet_id)
        if sum_mm:
            df_mm = sum_substances(frames, MM_PARTS, MM_SUBSTANCE)
            if df_mm is not None:
                frames[MM_SUBSTANCE] = df_mm
        for substance, df in frames.items():
            if substance in NOT_LOADED:
                continue
            if substance not in key_mapping:
                warnings.warn(f"{substance} not in mapping keys", stacklevel=2)
                continue
            d = {
                f"{sheet_id}_{key_mapping[substance]}": DataSet.from_df(
                    df, experiment.ureg
                )
            }
            # split each data frame in single time-courses
            for split_key in ["group", "id", "measurement", "tissue", "intervention"]:
                d = split_dataset(experiment, d, split_key)
            dsets.update({experiment.to_sid(key): dset for key, dset in d.items()})

    # convert units to molar
    for dset in dsets.values():
        convert_units(experiment, dset)
    return dsets


def split_dataset(
    experiment: DexSimulationExperiment, dsets: dict[str, DataSet], split_key: str
) -> dict[str, DataSet]:
    """Split the datasets by the values of a column, if they have the column."""
    dsets_split: dict[str, DataSet] = {}
    for key, dset in dsets.items():
        if split_key not in dset.columns.values:
            return dsets
        for splitter in getattr(dset, split_key).unique():
            name = dataset_name(experiment, splitter, split_key)
            dsets_split[f"{key}_{name}"] = DataSet.from_df(
                dset[getattr(dset, split_key) == splitter], experiment.ureg
            )
    return dsets_split


def dataset_name(
    experiment: DexSimulationExperiment, splitter: str, split_key: str
) -> str:
    """Get the part of the key of a dataset for a value of the split column."""
    name = ""
    if split_key == "intervention":
        doses = dose_from_json(experiment, splitter)
        for medication, dose in doses.items():
            if medication in ["quinidine", "quinidine sulphate"]:
                name += "Q"
            elif medication in ["dextromethorphan", "dextromethorphan hydrobromide"]:
                name += (
                    f"{intervention_mapping[medication]}{dose.magnitude}"
                    f"{key_mapping[str(dose.units)]}"
                )
            else:
                warnings.warn("Non standard intervention.", stacklevel=2)
                name += f"{medication}{dose.magnitude}{key_mapping[str(dose.units)]}"
    elif split_key == "id":
        # a single subject is named by its id (Schadel1995 Fig4: EM2, PM3); the
        # ids are not terms of the mapping
        name = splitter
    elif splitter in key_mapping:
        name += key_mapping[splitter]
    else:
        warnings.warn(f"{splitter} not in mapping keys", stacklevel=2)
        name = splitter
    return name


def convert_units(experiment: DexSimulationExperiment, dset: DataSet) -> None:
    """Convert a recovery to an amount and a concentration to a molar one.

    A recovery [% of dose] is a molar percentage of the dextromethorphan dose
    of the intervention of the dataset (the base, a dose of the hydrobromide
    is converted with `f_dxmhbr_to_dxm`), whatever the substance: the amount
    is `recovery * dose / Mr.dxm`. A mass concentration of dextromethorphan or
    dextrorphan is converted with its molecular weight; the metabolites with
    conjugates are reported as molar concentrations.

    Raises:
        ValueError: if the intervention has no dextromethorphan dose or a mass
            concentration has no molecular weight.
    """
    subject_type = "mean" if "mean" in dset.columns else "value"

    assert len(dset.measurement.unique()) == 1
    assert len(dset.substance.unique()) == 1
    assert len(dset.intervention.unique()) == 1
    assert len(dset[f"{subject_type}_unit"].unique()) == 1
    measurement = dset.measurement.unique()[0]
    substance = dset.substance.unique()[0]
    intervention = dset.intervention.unique()[0]

    # dextromethorphan dose of the intervention (the last one if several)
    dose: Quantity | None = None
    for intervention_dict in interventions_from_json(experiment, intervention).values():
        if intervention_dict["substance"] == "dextromethorphan hydrobromide":
            value = float(
                float(intervention_dict["dose"].magnitude)
                * experiment.f_dxmhbr_to_dxm()
            )
            dose = Q(value, intervention_dict["dose"].units)
        elif intervention_dict["substance"] == "dextromethorphan":
            dose = intervention_dict["dose"]
    if not dose:
        raise ValueError(f"No dextromethorphan dose in '{intervention}'.")

    # % of the dextromethorphan dose -> mmole
    if (
        measurement == "recovery"
        and Q(dset.uinfo[subject_type]).dimensionality != Q(1, "mole").dimensionality
    ):
        dset.unit_conversion(subject_type, dose / experiment.Mr.dxm / Q(100, "percent"))

    # mg/ml -> mmole/ml
    if (
        measurement == "concentration"
        and Q(dset.uinfo[subject_type]).dimensionality != Q(1, "mole/l").dimensionality
    ):
        if substance not in MASS_CONCENTRATIONS:
            raise ValueError(f"No molecular weight of '{substance}' in {dset.index}.")
        mr = getattr(experiment.Mr, MASS_CONCENTRATIONS[substance])
        dset.unit_conversion(subject_type, 1 / mr)


def _study(experiment: DexSimulationExperiment) -> dict[str, Any]:
    """Read the `study.json` of the study of an experiment.

    Raises:
        ValueError: if the experiment has no `data_path`.
    """
    if experiment.data_path is None:
        raise ValueError(f"No 'data_path' set on '{experiment.sid}'.")
    with (experiment.data_path[0] / experiment.sid / "study.json").open() as f:
        study: dict[str, Any] = json.load(f)
    return study


def dose_from_json(
    experiment: DexSimulationExperiment, interventions: str
) -> dict[str, Quantity]:
    """Get the doses of the interventions by substance from the `study.json`.

    Args:
        experiment: the experiment of the study.
        interventions: the interventions of a dataset, comma separated; an
            intervention is selected if its name is part of the string.
    """
    doses: dict[str, Quantity] = {}
    for element in _study(experiment)["interventionset"]["interventions"]:
        if element["name"] in interventions:
            # FIXME: this will fail if different doses of same substance are given
            doses[element["substance"]] = Q(element["value"], element["unit"])
    return doses


def interventions_from_json(
    experiment: DexSimulationExperiment, interventions: str
) -> dict[str, dict[str, Any]]:
    """Get the substance and the dose of the interventions from the `study.json`.

    Args:
        experiment: the experiment of the study.
        interventions: the interventions of a dataset, comma separated; an
            intervention is selected if its name is part of the string.
    """
    interventions_dict: dict[str, dict[str, Any]] = {}
    for element in _study(experiment)["interventionset"]["interventions"]:
        if element["name"] in interventions:
            interventions_dict[element["name"]] = {
                "substance": element["substance"],
                "dose": Q(element["value"], element["unit"]),
            }
    return interventions_dict
