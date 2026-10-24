"""Intestine model of the oral absorption of dextromethorphan.

An oral dose dissolves and passes the stomach with the rate `Ka_dis_dxm` into
the lumen of the small intestine, from which the fraction `F_dxm_abs` is
absorbed into the portal plasma with the rate `DXMABS_k`, the rest is excreted
in the feces. The oral bioavailability is the fraction absorbed times the
fraction which escapes the first pass through the liver; the first pass of
dextromethorphan is hepatic, the intestinal CYP3A4 is a few tenths of a percent
of a dose and is not part of the model.

Dextromethorphan is a weak base of high permeability which is well absorbed:
poor metabolizers recover 26 % of an oral dose unchanged and 25 % as the
N-demethylated morphinans in the urine (Capon1996), extensive metabolizers
55-97 % of a dose as the sum of the analytes (Schadel1995, Jones1996). The
fraction absorbed is fitted on these recoveries.
"""

from sbmlutils.factory import (
    AssignmentRule,
    Compartment,
    FactoryResult,
    Model,
    Parameter,
    RateRule,
    Reaction,
    Species,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import BQB, SBO

from pkdb_models.models.dextromethorphan.models import annotations, templates
from pkdb_models.models.dextromethorphan.models.fits import FITS


class U(templates.U):
    """Units of the intestine model."""

    mg_per_min = UnitDefinition("mg_per_min", "mg/min")


#: the substance given orally: id -> (name, molecular weight [g/mole], rate of
#: the absorption from the lumen [1/min]); the rate of the absorption is fixed
#: (it is in series with the dissolution and is not identified apart from it),
#: the fraction absorbed (`F_<sid>_abs`) and the rate of the dissolution and
#: gastric emptying (`Ka_dis_<sid>`) are the values of the adopted fit
#: (`models/fits.py`)
SUBSTANCES_INTESTINE: dict[str, tuple[str, float, float]] = {
    "dxm": ("dextromethorphan", 271.404, 0.08),
}

_m = Model(
    "dextromethorphan_intestine",
    name="Dextromethorphan (DXM) intestine model",
    notes="""
    # Intestine model of the oral absorption of dextromethorphan

    An oral dose dissolves and passes the stomach with the rate `Ka_dis_dxm`
    into the lumen of the small intestine, from which the fraction `F_dxm_abs`
    is absorbed into the portal plasma with the rate `DXMABS_k`, the rest is
    excreted in the feces. The oral bioavailability is the fraction absorbed
    times the fraction which escapes the first pass through the liver; the
    first pass of dextromethorphan is hepatic, the intestinal CYP3A4 is a few
    tenths of a percent of a dose and is not part of the model.
    """
    + templates.terms_of_use,
    units=U,
    model_units=templates.model_units,
    creators=templates.creators,
    annotations=[
        (BQB.OCCURS_IN, "bto/BTO:0000545"),  # gut
        (BQB.OCCURS_IN, "ncit/C12736"),  # intestine
        (BQB.OCCURS_IN, "fma/FMA:7199"),  # intestine
        (BQB.HAS_PROPERTY, "ncit/C79369"),  # Pharmacokinetics: Absorption
        (BQB.HAS_PROPERTY, "ncit/C79372"),  # Pharmacokinetics: Excretion
        *templates.model_annotations,
    ],
)

_m.compartments = [
    Compartment(
        "Vext",
        1.0,
        name="plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=True,
        port=True,
        annotations=annotations.compartments["plasma"],
    ),
    Compartment(
        "Vgu",
        1.2825,  # 0.0171 [l/kg] * 75 kg
        name="intestine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        port=True,
        annotations=annotations.compartments["gu"],
    ),
    Compartment(
        "Vlumen",
        1.2825 * 0.9,  # 0.0171 [l/kg] * 75 kg * 0.9
        name="intestinal lumen (inner part of intestine)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        port=True,
        annotations=annotations.compartments["gu_lumen"],
    ),
    Compartment(
        "Vfeces",
        metaId="meta_Vfeces",
        value=1,
        unit=U.liter,
        constant=True,
        name="feces",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        port=True,
        annotations=annotations.compartments["feces"],
    ),
    Compartment(
        "Vstomach",
        metaId="meta_Vstomach",
        value=1,
        unit=U.liter,
        constant=True,
        name="stomach",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        port=True,
        annotations=annotations.compartments["stomach"],
    ),
    Compartment(
        "Vapical",
        float("nan"),
        name="apical membrane (intestinal membrane enterocytes)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.m2,
        spatialDimensions=2,
        annotations=annotations.compartments["apical"],
    ),
]

_m.species = []
_m.parameters = []
_m.reactions = []
_m.rate_rules = []
for sid, (name, mr, k_abs) in SUBSTANCES_INTESTINE.items():
    rid = sid.upper()
    _m.species.extend(
        [
            Species(
                f"{sid}_stomach",
                initialConcentration=0.0,
                compartment="Vstomach",
                substanceUnit=U.mmole,
                name=f"{name} (stomach)",
                hasOnlySubstanceUnits=True,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
                boundaryCondition=True,
            ),
            Species(
                f"{sid}_lumen",
                initialConcentration=0.0,
                name=f"{name} (intestinal lumen)",
                compartment="Vlumen",
                substanceUnit=U.mmole,
                hasOnlySubstanceUnits=False,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
                port=True,
            ),
            Species(
                f"{sid}_ext",
                initialConcentration=0.0,
                name=f"{name} (plasma)",
                compartment="Vext",
                substanceUnit=U.mmole,
                hasOnlySubstanceUnits=False,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
                port=True,
            ),
            Species(
                f"{sid}_feces",
                initialConcentration=0.0,
                name=f"{name} (feces)",
                compartment="Vfeces",
                substanceUnit=U.mmole,
                hasOnlySubstanceUnits=True,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
                port=True,
            ),
        ]
    )
    _m.parameters.extend(
        [
            Parameter(
                f"F_{sid}_abs",
                **FITS.parameter(f"GU__F_{sid}_abs", unit=U.dimensionless),
                constant=True,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name=f"fraction absorbed {name}",
                notes=f"""
                The fraction of the {name} in the lumen which is absorbed,
                `(1 - F_{sid}_abs)` is excreted in the feces; fitted on the
                urinary recoveries.
                """,
            ),
            Parameter(
                f"{rid}ABS_k",
                k_abs,
                U.per_min,
                constant=True,
                name=f"rate of the absorption of {name}",
                sboTerm=SBO.KINETIC_CONSTANT,
                notes="Fixed: the step is in series with the dissolution and "
                "is not identified apart from it.",
            ),
            Parameter(
                f"PODOSE_{sid}",
                0,
                U.mg,
                constant=False,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name=f"oral dose {name} [mg]",
                port=True,
            ),
            Parameter(
                f"Ka_dis_{sid}",
                **FITS.parameter(f"Ka_dis_{sid}", unit=U.per_hr),
                constant=True,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name=f"Ka_dis [1/hr] dissolution {name}",
                port=True,
            ),
            Parameter(
                f"Mr_{sid}",
                mr,
                U.g_per_mole,
                constant=True,
                name=f"Molecular weight {name} [g/mole]",
                sboTerm=SBO.MOLECULAR_MASS,
                port=True,
            ),
        ]
    )
    _m.rules.append(
        AssignmentRule(
            f"absorption_{sid}",
            value=f"{rid}ABS_k * Vgu * {sid}_lumen",
            unit=U.mmole_per_min,
            name=f"absorption {name}",
        ),
    )
    _m.reactions.extend(
        [
            # dissolution of the dose in the stomach and gastric emptying
            Reaction(
                sid=f"dissolution_{sid}",
                name=f"dissolution {name}",
                formula=(
                    f"Ka_dis_{sid}/60 min_per_hr * PODOSE_{sid}/Mr_{sid}",
                    U.mmole_per_min,
                ),
                equation=f"{sid}_stomach -> {sid}_lumen",
                compartment="Vgu",
            ),
            Reaction(
                f"{rid}ABS",
                name=f"absorption {name}",
                equation=f"{sid}_lumen -> {sid}_ext",
                sboTerm=SBO.TRANSPORT_REACTION,
                compartment="Vapical",
                formula=(f"F_{sid}_abs * absorption_{sid}", U.mmole_per_min),
            ),
            Reaction(
                sid=f"{rid}EXC",
                name=f"excretion {name} (feces)",
                compartment="Vlumen",
                equation=f"{sid}_lumen -> {sid}_feces",
                sboTerm=SBO.TRANSPORT_REACTION,
                formula=(
                    f"(1 dimensionless - F_{sid}_abs) * absorption_{sid}",
                    U.mmole_per_min,
                ),
            ),
        ]
    )
    # d(PODOSE)/dt = -dissolution * Mr
    _m.rate_rules.append(
        RateRule(f"PODOSE_{sid}", f"-dissolution_{sid} * Mr_{sid}", U.mg_per_min)
    )

model_intestine = _m


if __name__ == "__main__":
    from pkdb_models.models.dextromethorphan import MODEL_BASE_PATH

    result: FactoryResult = create_model(
        filepath=MODEL_BASE_PATH / f"{model_intestine.sid}.xml",
        model=model_intestine,
    )
