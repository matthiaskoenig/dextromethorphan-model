"""Kidney model of the renal excretion of dextromethorphan and its metabolites.

The renal clearance of a substance is `GFR * fu_<sid> * <X>EX_f`, the
filtration of its unbound fraction times a factor: 1 is filtration alone, above
1 a net tubular secretion, below 1 a net reabsorption. The glomerular
filtration rate is `GFR = f_renal_function * GFR_base`, `GFR_base` is 101
ml/min at 75 kg and scales with the renal blood flow; a measured creatinine
clearance of X ml/min is the renal function X/101.

The start values of the factors are the renal clearances and the urinary
recoveries of the literature: the renal clearance of dextromethorphan in poor
metabolizers is 41 +- 23 ml/min (Schadel1995) and about 78 ml/min (Capon1996),
with 11-26 % of an oral dose excreted unchanged; extensive metabolizers excrete
0.2 % of a dose unchanged and 27-39 % as total dextrorphan, of which about 4 %
is unconjugated (Nagai1996, Schadel1995, Capon1996). The N-demethylated
morphinans (3-methoxymorphinan, 3-hydroxymorphinan and its glucuronide, lumped
as `mm`) are 16 % of a dose in extensive and 9-25 % in poor metabolizers.

The fractions unbound are those of the literature (Bolger2019, Lutz2012,
Taylor2016): dextromethorphan 0.35-0.72 (0.5 is used), dextrorphan 0.55 and its
glucuronide 0.44; the lumped morphinans are taken as dextrorphan.
"""

from sbmlutils.factory import (
    AssignmentRule,
    Compartment,
    FactoryResult,
    Model,
    Parameter,
    Reaction,
    Species,
    create_model,
)
from sbmlutils.metadata import BQB, SBO

from pkdb_models.models.dextromethorphan.models import annotations, templates
from pkdb_models.models.dextromethorphan.models.fits import FITS


class U(templates.U):
    """Units of the kidney model."""


#: the substances excreted in the urine: id -> (name, fraction unbound in the
#: plasma); the factor of the renal clearance relative to the filtration of
#: the unbound fraction (`<SID>EX_f`) is the value of the adopted fit
#: (`models/fits.py`)
SUBSTANCES_KIDNEY: dict[str, tuple[str, float]] = {
    "dxm": ("dextromethorphan", 0.5),
    "dxo": ("dextrorphan", 0.55),
    "dxo_glu": ("dextrorphan glucuronide", 0.44),
    "mm": ("N-demethylated morphinans", 0.5),
}

_m = Model(
    "dextromethorphan_kidney",
    name="Dextromethorphan (DXM) kidney model",
    notes="""
    # Kidney model of the renal excretion of dextromethorphan

    The renal clearance of a substance is `GFR * fu_<sid> * <X>EX_f`, the
    filtration of its unbound fraction times a factor: 1 is filtration alone,
    above 1 a net tubular secretion, below 1 a net reabsorption. The glomerular
    filtration rate is `GFR = f_renal_function * GFR_base`, `GFR_base` is 101
    ml/min at 75 kg and scales with the renal blood flow; a measured creatinine
    clearance of X ml/min is the renal function X/101.

    The factors are of the renal clearances and the urinary recoveries of the
    literature: the renal clearance of dextromethorphan in poor metabolizers is
    41-78 ml/min (Schadel1995, Capon1996) with 11-26 % of an oral dose excreted
    unchanged, extensive metabolizers excrete 0.2 % unchanged and 27-39 % as
    total dextrorphan.
    """
    + templates.terms_of_use,
    units=U,
    model_units=templates.model_units,
    creators=templates.creators,
    annotations=[
        (BQB.OCCURS_IN, "fma/FMA:7203"),  # kidney
        (BQB.OCCURS_IN, "bto/BTO:0000671"),
        (BQB.OCCURS_IN, "ncit/C12415"),
        (BQB.HAS_PROPERTY, "ncit/C79372"),  # Pharmacokinetics: Excretion
        *templates.model_annotations,
    ],
)

_m.compartments = [
    Compartment(
        "Vext",
        value=1.0,
        unit=U.liter,
        name="plasma",
        constant=True,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["plasma"],
        port=True,
    ),
    Compartment(
        "Vurine",
        1.0,
        name="urine",
        unit=U.liter,
        constant=True,
        port=True,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["urine"],
    ),
]

_m.species = []
for sid, (name, _) in SUBSTANCES_KIDNEY.items():
    _m.species.extend(
        [
            Species(
                f"{sid}_ext",
                name=f"{name} (plasma)",
                initialConcentration=0.0,
                compartment="Vext",
                substanceUnit=U.mmole,
                hasOnlySubstanceUnits=False,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
                port=True,
            ),
            Species(
                f"{sid}_urine",
                name=f"{name} (urine)",
                initialConcentration=0.0,
                compartment="Vurine",
                substanceUnit=U.mmole,
                hasOnlySubstanceUnits=True,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
                port=True,
            ),
        ]
    )

_m.parameters = [
    Parameter(
        "f_renal_function",
        name="renal function",
        value=1.0,
        unit=U.dimensionless,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        >1.0: increased kidney function
        1.0: normal kidney function (healthy control)
        <1.0: decreased kidney function

        Renal function relative to the healthy glomerular filtration rate
        `GFR_base`, which is 101 ml/min at 75 kg; a measured creatinine
        clearance of X ml/min is the renal function X/101.
        """,
    ),
    Parameter(
        "GFR_base",
        101,
        U.ml_per_min,
        constant=False,
        name="glomerular filtration rate (healthy)",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        port=True,
        notes="""Overwritten by the whole-body model, which scales it with
        the renal blood flow and so with the body weight.""",
    ),
    Parameter(
        "GFR",
        101,
        U.ml_per_min,
        constant=False,
        name="glomerular filtration rate",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
]
for sid, (name, fu) in SUBSTANCES_KIDNEY.items():
    _m.parameters.extend(
        [
            Parameter(
                f"fu_{sid}",
                fu,
                U.dimensionless,
                constant=True,
                name=f"fraction unbound in plasma {name}",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                port=True,
            ),
            Parameter(
                f"{sid.upper().replace('_', '')}EX_f",
                **FITS.parameter(
                    f"KI__{sid.upper().replace('_', '')}EX_f", unit=U.dimensionless
                ),
                constant=True,
                name=f"renal clearance of unbound {name} relative to the GFR",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
        ]
    )

_m.rules = [
    AssignmentRule(
        "GFR",
        "f_renal_function * GFR_base",
        unit=U.ml_per_min,
        name="glomerular filtration rate",
    ),
]

_m.reactions = [
    Reaction(
        sid=f"{sid.upper().replace('_', '')}EX",
        name=f"{name} renal excretion",
        equation=f"{sid}_ext -> {sid}_urine",
        sboTerm=SBO.TRANSPORT_REACTION,
        # [ml/min] * [l/ml] * [-] * [-] * [mmole/l]
        formula=(
            f"GFR * 0.001 l_per_ml * fu_{sid} * "
            f"{sid.upper().replace('_', '')}EX_f * {sid}_ext",
            U.mmole_per_min,
        ),
    )
    for sid, (name, _) in SUBSTANCES_KIDNEY.items()
]

model_kidney = _m


if __name__ == "__main__":
    from pkdb_models.models.dextromethorphan import MODEL_BASE_PATH

    results: FactoryResult = create_model(
        model=model_kidney,
        filepath=MODEL_BASE_PATH / f"{model_kidney.sid}.xml",
    )
