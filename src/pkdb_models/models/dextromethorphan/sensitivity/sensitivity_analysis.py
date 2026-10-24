"""Sensitivity analysis of the dextromethorphan model.

The outputs are the pharmacokinetic parameters of dextromethorphan and of the
total dextrorphan (free and conjugated), its CYP2D6 metabolite, in the venous
plasma after a single oral dose (the non-compartmental analysis of
`pkpdutils`), and the urinary metabolic ratio DXM/(DXO+DXOGLU) of the 0-8 hr
collection, the phenotyping metric of CYP2D6. The parameters are the
parameters of the model with bounds of +-15 % around their value. The analyses
are run as a script, the local analysis by default:

    python -m pkdb_models.models.dextromethorphan.sensitivity.sensitivity_analysis
    python -m pkdb_models.models.dextromethorphan.sensitivity.sensitivity_analysis local sampling

The analyses run on `pkpdsim.sensitivity.SensitivityRunner`, which writes the
table of the parameters into `results/sensitivity` of the model and the tables
and figures of an analysis into `results/sensitivity/<analysis>`.
An analysis does not vary a parameter which one of its groups sets
(`pkpdsim.sensitivity.free_parameters`): `sampling`, over the groups, leaves
out `KI__f_renal_function`. The environment variable `PKPDSIM_SENSITIVITY_N`
replaces the numbers of samples of the global analyses for a quick run, see
`pkpdsim.sensitivity.sample_size`.

The model without dextromethorphan is stationary, so the simulation of a group
starts with the dose. The dose is followed for `END_HR` hours, long enough for
the terminal phase of the poor metabolizers (a half-life of about 80 hr).
"""

from collections.abc import Mapping

import numpy as np
from pkpdsim.sensitivity import (
    FastAnalysis,
    LocalAnalysis,
    ParameterType,
    SamplingAnalysis,
    SensitivityGroup,
    SensitivityOutput,
    SensitivityParameter,
    SensitivityRunner,
    SobolAnalysis,
    parameters_from_sbml,
    set_bounds,
    set_relative_bounds,
)
from pkpdutils import NCAOptions
from sbmlsim import Q
from sbmlsim.simulation import PK, Formula, Simulation

from pkdb_models.models.dextromethorphan import MODEL, MODEL_PATH
from pkdb_models.models.dextromethorphan.experiments.base_experiment import (
    DexSimulationExperiment,
)
from pkdb_models.models.dextromethorphan.fitting.parameters import (
    parameters_pk as fit_parameters,
)

#: oral dose of dextromethorphan (base) of the analysis [mg], the 30 mg of the
#: hydrobromide monohydrate of the phenotyping studies
DOSE_DXM = 22
#: the hours after the dose
END_HR = 336
#: the time of the urinary metabolic ratio [min], the end of the 0-8 hr
#: collection of the phenotyping
MR_URINE_TIME_MIN = 480
#: the limits of quantification of the non-compartmental analysis [mM], about
#: 1e-4 of the maximal plasma concentrations of the extensive metabolizers
#: after 22 mg (dextromethorphan 3e-6 mM, total dextrorphan 1e-3 mM), so that
#: the noise of the integrator is not the terminal phase
LLOQ: dict[str, float] = {"dxm": 3e-10, "dxo_total": 1e-8}
#: fraction of the bounds of a parameter relative to its value
BOUNDS_FRACTION = 0.15

#: outputs of the non-compartmental analysis of dextromethorphan -> unit of
#: the output
PK_OUTPUTS_DXM: dict[str, str] = {
    "auc_inf_obs": "mM*min",
    "cmax": "mM",
    "tmax": "min",
    "thalf": "min",
    "vz_f": "l",
    "cl_f": "ml/min",
}
#: outputs of the non-compartmental analysis of the total dextrorphan, the
#: metabolite of the dose: no clearance or volume -> unit of the output
PK_OUTPUTS_DXO_TOTAL: dict[str, str] = {
    "auc_inf_obs": "mM*min",
    "cmax": "mM",
    "tmax": "min",
    "thalf": "min",
}
#: the outputs whose unit has the amount of the dose: the dose is a mass
#: (`PODOSE_dxm` in mg), so they are divided by the molecular weight (its value
#: at the start, a value per simulation like the parameter of the analysis)
PK_PER_DOSE_MASS: frozenset[str] = frozenset({"vz_f", "cl_f"})
#: the concentrations of the analytes in the venous plasma
CONCENTRATIONS: dict[str, str] = {"dxm": "[Cve_dxm]", "dxo_total": "dxo_total"}

#: the outputs with their ids and names
OUTPUTS: list[SensitivityOutput] = [
    SensitivityOutput("dxm_auc_inf_obs", "dextromethorphan AUC∞"),
    SensitivityOutput("dxm_cmax", "dextromethorphan Cmax"),
    SensitivityOutput("dxm_tmax", "dextromethorphan tmax"),
    SensitivityOutput("dxm_thalf", "dextromethorphan Half-life"),
    SensitivityOutput("dxm_vz_f", "dextromethorphan Vz/F"),
    SensitivityOutput("dxm_cl_f", "dextromethorphan CL/F"),
    SensitivityOutput("dxo_total_auc_inf_obs", "dextrorphan total AUC∞"),
    SensitivityOutput("dxo_total_cmax", "dextrorphan total Cmax"),
    SensitivityOutput("dxo_total_tmax", "dextrorphan total tmax"),
    SensitivityOutput("dxo_total_thalf", "dextrorphan total Half-life"),
    SensitivityOutput("mr_urine_8hr", "DXM/(DXO+DXOGLU) urine 0-8 hr"),
]


def _pk_observables(sid: str, outputs: Mapping[str, str]) -> list:
    """Get the non-compartmental analysis of an analyte in plasma and its outputs."""
    pk_id = f"pk_{sid}"
    return [
        PK(
            pk_id,
            CONCENTRATIONS[sid],
            dose="PODOSE_dxm",
            route="oral",
            options=NCAOptions(lloq=LLOQ[sid]),
            parameters=list(outputs),
        ),
        *(
            Formula(
                f"{sid}_{key}",
                f"{pk_id}.{key} / at(Mr_dxm, 0)"
                if key in PK_PER_DOSE_MASS
                else f"{pk_id}.{key}",
                unit=unit,
            )
            for key, unit in outputs.items()
        ),
    ]


#: the observables of a simulation, the outputs with their units; the ids of
#: the analyses (`pk_dxm`, `pk_dxo_total`) are no species of the model
OBSERVABLES = [
    *_pk_observables("dxm", PK_OUTPUTS_DXM),
    *_pk_observables("dxo_total", PK_OUTPUTS_DXO_TOTAL),
    Formula(
        "mr_urine_8hr",
        f"at(dxm_dxo_total_urine, {MR_URINE_TIME_MIN})",
        unit="dimensionless",
    ),
]

#: the output times [hr]: every 0.01 hr in the first 12 hr after the dose
#: (absorption and maximum, tmax about 1-2.5 hr), every 0.5 hr after it; 8 hr
#: (the urinary metabolic ratio) is a time of the grid. tmax is a time of the
#: grid and its local sensitivities are steps of the grid (the warnings of
#: large delta differences of the local analysis); the maximum is flat and
#: tmax moves along it
TIMES_HR: tuple[float, ...] = tuple(
    np.unique(
        np.concatenate(
            [
                np.linspace(0, 12, 1201),
                np.linspace(12, END_HR, 2 * (END_HR - 12) + 1),
            ]
        )
    ).tolist()
)


def sensitivity_simulation(changes: Mapping[str, float]) -> Simulation:
    """Get the simulation of a group: a single oral dose of dextromethorphan at time 0."""
    return Simulation(
        start=0,
        end=END_HR,
        times=TIMES_HR,
        time_unit="hr",
        preinit_changes={**changes, "PODOSE_dxm": Q(DOSE_DXM, "mg")},
    )


#: the CYP2D6 poor metabolizer: the custom activity score 0 for both alleles
#: (`LI__cyp2d6_allele1`/`2` -1 select the custom activity `LI__cyp2d6_ac`)
POOR_METABOLIZER: dict[str, float] = {
    "LI__cyp2d6_allele1": -1,
    "LI__cyp2d6_allele2": -1,
    "LI__cyp2d6_ac": 0.0,
}

#: the groups the analyses are run for: the control (an extensive metabolizer,
#: *1/*1, activity score 2), the poor metabolizer (activity score 0), whose
#: elimination is not by CYP2D6, and the stages of renal impairment, which
#: the conjugated dextrorphan accumulates in
SENSITIVITY_GROUPS: list[SensitivityGroup] = [
    SensitivityGroup("control", "Control", sensitivity_simulation({}), "dimgrey"),
    SensitivityGroup(
        "poorMetabolizer",
        "Poor metabolizer",
        sensitivity_simulation(POOR_METABOLIZER),
        "tab:purple",
    ),
    *(
        SensitivityGroup(
            uid,
            name,
            sensitivity_simulation(
                {"KI__f_renal_function": DexSimulationExperiment.renal_map[name]}
            ),
            DexSimulationExperiment.renal_colors[name],
        )
        for uid, name in [
            ("mildRI", "Mild renal impairment"),
            ("modRI", "Moderate renal impairment"),
            ("sevRI", "Severe renal impairment"),
        ]
    ),
]


def sensitivity_parameters() -> list[SensitivityParameter]:
    """Get the parameters of the analyses with their bounds and references."""
    parameters = parameters_from_sbml(
        MODEL_PATH,
        exclude_ids={
            # molecular weights
            "Mr_dxm",
            "Mr_dxo",
            "Mr_dxo_glu",
            "Mr_mm",
            # reference values
            "BW_ref",
            "LI__cyp2d6_activity_ref",
            # unchangeable values
            "FQlu",
            "FVhv",
            "FVpo",
            # dosing parameters: the infusion of dextromethorphan, which the
            # oral dose does not use
            "ti_dxm",
            # the CYP2D6 genotype: the activities of the alleles of the table
            # (only *1 of the control is used) and the custom activity score,
            # which the groups set
            *(
                p.uid
                for p in parameters_from_sbml(MODEL_PATH, exclude_zero=False)
                if p.uid.startswith("LI__cyp2d6_a")
            ),
            # unused volumes
            "Vurine",
            "Vfeces",
            "Vstomach",
        },
        exclude_na=True,
        exclude_zero=True,
    )

    # the fitted parameters, their bounds are set relative to the value below
    set_bounds(
        parameters,
        [(fp.pid, np.nan, np.nan, ParameterType.FIT) for fp in fit_parameters],
    )
    # the scaling factors of the organ functions and of the enzyme activities
    set_bounds(
        parameters,
        [
            (uid, 1 - BOUNDS_FRACTION, 1 + BOUNDS_FRACTION, ParameterType.SCALING)
            for uid in [
                "KI__f_renal_function",
                "LI__f_cyp2d6",
                "LI__f_cyp3a4",
                "LI__f_ugt2b15",
            ]
        ],
    )

    # the references of the values from the literature
    references = {
        "BW": r"\cite{Ogden2004, Jones2013, Thompson2009, Brown1997}",
        "FQgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FQh": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FQki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVar": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVli": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FVlu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVve": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "COBW": r"\cite{Cattermole2017, Patel2021, Collis2001}",
        "KI__f_renal_function": r"\cite{Stevens2024}",
    }
    by_uid = {p.uid: p for p in parameters}
    for uid, reference in references.items():
        p = by_uid[uid]
        p.reference = reference
        if p.type == ParameterType.NA:
            p.type = ParameterType.DATA

    # every parameter without bounds varies around its value
    set_relative_bounds(parameters, BOUNDS_FRACTION)
    return parameters


#: the analyses of the script, with their groups and numbers of samples
SENSITIVITY = SensitivityRunner(
    model=MODEL,
    parameters=sensitivity_parameters,
    outputs=OUTPUTS,
    observables=OBSERVABLES,
    analyses={
        "local": LocalAnalysis(groups=SENSITIVITY_GROUPS[:2], delta=0.01),
        "sampling": SamplingAnalysis(groups=SENSITIVITY_GROUPS, n=1000),
        "fast": FastAnalysis(groups=SENSITIVITY_GROUPS[:1], n=1000),
        "sobol": SobolAnalysis(groups=SENSITIVITY_GROUPS[:1], n=4096),
    },
    default=("local",),
)


if __name__ == "__main__":
    SENSITIVITY.main()
