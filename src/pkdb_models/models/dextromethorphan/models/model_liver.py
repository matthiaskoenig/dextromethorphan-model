"""Liver model of the metabolism of dextromethorphan.

Dextromethorphan (DXM) is O-demethylated to dextrorphan (DXO) by CYP2D6, the
pathway which the metabolizer phenotype changes, and by a CYP2D6-independent
pathway (`DXMCYPX`, mainly CYP3A4 and CYP2C9), which carries the
O-demethylation of poor metabolizers. Dextromethorphan and dextrorphan are
N-demethylated by CYP3A4 to 3-methoxymorphinan and 3-hydroxymorphinan, which
the model keeps as one lumped species (`mm`, free and conjugated): the studies
report them together as the N-demethylated morphinans, 9-25 % of a dose in poor
and about 16 % in extensive metabolizers (Capon1996, Schadel1995,
Barnhart1980). Dextrorphan is glucuronidated (UGT2B15, `DXOUGT`); about 96 % of
the dextrorphan of the plasma is conjugated (Nagai1996).

The rates are Michaelis-Menten kinetics with Michaelis constants of the order
of the values of human liver microsomes. The hepatic concentrations after a
therapeutic dose are nanomolar to micromolar, far below every Km, so the
kinetics are linear and the data identify the intrinsic clearance
`Vmax/Km * Vli` of a pathway, not Vmax and Km apart: the Km are fixed, the Vmax
are the parameters of the fits.

The activity of CYP2D6 is the activity score of the diplotype
(`cyp2d6_activity` of the CYP2D6 submodel) relative to the score of two
functional alleles (`cyp2d6_activity_ref`, 2.0), times the factor `f_cyp2d6` of
an inhibitor (quinidine, paroxetine, cinacalcet); the activity of CYP3A4 is
`f_cyp3a4` (ritonavir, terbinafine). Both factors are set by the experiments
from the observed interaction, they are never fitted.

Michaelis constants of the literature:

    DXM O-demethylation (CYP2D6): 3.9 +- 0.6 uM (Kronbach1987), 4.6 +- 1.8 uM
      (Broly1989), 2.2-9.4 uM (Kerry1994), 3.7 +- 1.2 uM (Yu2001)
    DXM O-demethylation (CYP3A4, low affinity site): 143-289 uM
      (Schmider1997), 55-307 uM (Kerry1994), 157 +- 26 uM (Yu2001)
    DXM N-demethylation (CYP3A4): 632-977 uM (Kerry1994), 232 +- 38 uM (Yu2001)
    DXO N-demethylation (CYP3A4): 1571-4286 uM (Kerry1994),
      724 +- 213 uM (Yu2001)
    DXO glucuronidation (UGT2B15): 690 uM (Lutz2012)
"""

import math
from typing import NamedTuple

from sbmlutils.factory import (
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
    """Units of the liver model."""


#: the substances of the liver: id -> name
SUBSTANCES_LIVER: dict[str, str] = {
    "dxm": "dextromethorphan",
    "dxo": "dextrorphan",
    "dxo_glu": "dextrorphan glucuronide",
    "mm": "N-demethylated morphinans",
}

#: the activity score of a diplotype of two fully functional alleles, the
#: reference of the CYP2D6 activity of the model
CYP2D6_ACTIVITY_REF = 2.0


class Pathway(NamedTuple):
    """A metabolic pathway of the liver."""

    substrate: str
    product: str
    #: the activity factor of the enzyme (`f_<enzyme>`)
    enzyme: str
    #: Michaelis constant [mM], fixed
    km: float
    notes: str


#: the metabolic pathways with their fixed Michaelis constants; the maximal
#: rates are the values of the adopted fit (`models/fits.py`). The start values
#: of the fit (`fitting/parameters.py`) were chosen by hand for the clearances
#: of the literature (the liver tissue is 1.54 l at 75 kg, the
#: hepatic blood flow 1.5 l/min and the intrinsic clearance of a pathway
#: `Vmax/Km * Vli_tissue * Kp`): the O-demethylation by CYP2D6 of extensive
#: metabolizers gives a hepatic extraction of about 0.96, an oral
#: bioavailability of 2-4 % and an AUC of 9 ug*h/l after 22 mg (Capon1996); the
#: CYP2D6-independent pathways give the clearance of the poor metabolizers
#: (CL/F 275 ml/min, Schadel1995) with the N-demethylation about three times
#: the residual O-demethylation (the urinary 3MM + 3HM against the total
#: dextrorphan of poor metabolizers); the glucuronidation leaves about 4 % of
#: the dextrorphan of the plasma unconjugated (Nagai1996) and the
#: N-demethylation of dextrorphan is about 30 % of the hepatic turnover of
#: dextrorphan (the urinary 3HM against the total dextrorphan of extensive
#: metabolizers)
PATHWAYS: dict[str, Pathway] = {
    "DXMCYP2D6": Pathway(
        "dxm",
        "dxo",
        "cyp2d6",
        km=0.004,
        notes="O-demethylation of dextromethorphan to dextrorphan (CYP2D6), "
        "the pathway of the metabolizer phenotype: it is most of the "
        "clearance of extensive metabolizers and absent in poor metabolizers.",
    ),
    "DXMCYPX": Pathway(
        "dxm",
        "dxo",
        "cyp3a4",
        km=0.157,
        notes="CYP2D6-independent O-demethylation of dextromethorphan to "
        "dextrorphan (CYP3A4, CYP2C9), the low affinity site of the "
        "microsomes; it forms the dextrorphan of poor metabolizers.",
    ),
    "DXMNDM": Pathway(
        "dxm",
        "mm",
        "cyp3a4",
        km=0.7,
        notes="N-demethylation of dextromethorphan to 3-methoxymorphinan "
        "(CYP3A4), the main CYP2D6-independent clearance of dextromethorphan.",
    ),
    "DXONDM": Pathway(
        "dxo",
        "mm",
        "cyp3a4",
        km=0.72,
        notes="N-demethylation of dextrorphan to 3-hydroxymorphinan (CYP3A4); "
        "3-hydroxymorphinan is about 16 % of an oral dose in the urine of "
        "extensive metabolizers (Capon1996, Schadel1995).",
    ),
    "DXOUGT": Pathway(
        "dxo",
        "dxo_glu",
        "ugt2b15",
        km=0.69,
        notes="Glucuronidation of dextrorphan (UGT2B15), the main route of "
        "the dextrorphan which is formed: about 96 % of the dextrorphan of "
        "the plasma is conjugated (Nagai1996).",
    ),
}

#: the enzymes and their names
ENZYMES: dict[str, str] = {
    "cyp2d6": "CYP2D6",
    "cyp3a4": "CYP3A4",
    "ugt2b15": "UGT2B15",
}

_m = Model(
    "dextromethorphan_liver",
    name="Dextromethorphan (DXM) liver model",
    notes="""
    # Liver model of the metabolism of dextromethorphan

    Dextromethorphan (DXM) is O-demethylated to dextrorphan (DXO) by CYP2D6,
    the pathway of the metabolizer phenotype, and by a CYP2D6-independent
    pathway (`DXMCYPX`, mainly CYP3A4 and CYP2C9), which carries the
    O-demethylation of poor metabolizers. Dextromethorphan and dextrorphan are
    N-demethylated by CYP3A4 to 3-methoxymorphinan and 3-hydroxymorphinan,
    which the model keeps as one lumped species (`mm`, free and conjugated), as
    the studies report them. Dextrorphan is glucuronidated (UGT2B15).

    The rates are Michaelis-Menten kinetics; the hepatic concentrations are far
    below every Km, so the kinetics are linear and the data identify the
    intrinsic clearance `Vmax/Km * Vli` of a pathway: the Km are fixed at the
    values of human liver microsomes, the Vmax are the parameters of the fits.

    The activity of CYP2D6 is the activity score of the diplotype
    (`cyp2d6_activity`) relative to two functional alleles
    (`cyp2d6_activity_ref`), times the factor `f_cyp2d6` of an inhibitor; the
    activity of CYP3A4 is `f_cyp3a4`. The factors are set by the experiments
    from the observed interaction and are never fitted.
    """
    + templates.terms_of_use,
    units=U,
    model_units=templates.model_units,
    creators=templates.creators,
    annotations=[
        (BQB.OCCURS_IN, "fma/FMA:7197"),  # liver
        (BQB.OCCURS_IN, "bto/BTO:0000759"),
        (BQB.OCCURS_IN, "ncit/C12392"),
        (BQB.HAS_PROPERTY, "ncit/C79371"),  # Pharmacokinetics: Metabolism
        *templates.model_annotations,
    ],
)

_m.compartments = [
    Compartment(
        "Vli",
        0.0210 * 75,
        unit=U.liter,
        name="liver",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["li"],
        port=True,
        notes="""Overwritten by the whole-body model.""",
    ),
    Compartment(
        "Vmem",
        math.nan,
        unit=U.m2,
        spatialDimensions=2,
        name="plasma membrane",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["plasma membrane"],
    ),
]

_m.species = [
    Species(
        sid,
        initialConcentration=0.0,
        name=f"{name} (liver)",
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species[sid],
        port=True,
    )
    for sid, name in SUBSTANCES_LIVER.items()
]

_m.parameters = [
    Parameter(
        f"f_{enzyme}",
        1.0,
        U.dimensionless,
        constant=True,
        name=f"activity of {ename}",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes=f"""
        Activity of {ename} relative to the reference (1.0, no interacting
        drug), set by the experiments for an interaction, never fitted. The
        activity of CYP2D6 of a diplotype is the activity score
        `cyp2d6_activity` of the CYP2D6 submodel, which this factor multiplies.
        """,
    )
    for enzyme, ename in ENZYMES.items()
]
_m.parameters.append(
    Parameter(
        "cyp2d6_activity_ref",
        CYP2D6_ACTIVITY_REF,
        U.dimensionless,
        constant=True,
        name="reference CYP2D6 activity score",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        The activity score of a diplotype of two fully functional alleles
        (*1/*1), at which the maximal rate `DXMCYP2D6_Vmax` is given: the rate
        of the O-demethylation by CYP2D6 scales linearly with
        `cyp2d6_activity/cyp2d6_activity_ref`.
        """,
    )
)

_m.reactions = []
for rid, pathway in PATHWAYS.items():
    substrate = pathway.substrate
    activity = (
        "f_cyp2d6 * cyp2d6_activity/cyp2d6_activity_ref"
        if pathway.enzyme == "cyp2d6"
        else f"f_{pathway.enzyme}"
    )
    _m.reactions.append(
        Reaction(
            sid=rid,
            name=(
                f"{SUBSTANCES_LIVER[substrate]} -> "
                f"{SUBSTANCES_LIVER[pathway.product]} ({ENZYMES[pathway.enzyme]})"
            ),
            equation=f"{substrate} -> {pathway.product}",
            compartment="Vli",
            sboTerm=SBO.BIOCHEMICAL_REACTION,
            pars=[
                Parameter(
                    f"{rid}_Vmax",
                    **FITS.parameter(f"LI__{rid}_Vmax", unit=U.mmole_per_min_l),
                    name=f"Vmax {rid}",
                    sboTerm=SBO.MAXIMAL_VELOCITY,
                    notes="Maximal rate per liver volume.",
                ),
                Parameter(
                    f"{rid}_Km_{substrate}",
                    pathway.km,
                    U.mM,
                    name=f"Km {rid}",
                    sboTerm=SBO.MICHAELIS_CONSTANT,
                    notes="Of the order of the values of human liver "
                    "microsomes, fixed: the hepatic concentrations are far "
                    "below it, the kinetics are linear.",
                ),
            ],
            formula=(
                f"{activity} * {rid}_Vmax * Vli * {substrate}"
                f"/({rid}_Km_{substrate} + {substrate})",
                U.mmole_per_min,
            ),
            notes=pathway.notes,
        )
    )

model_liver = _m


if __name__ == "__main__":
    from pkdb_models.models.dextromethorphan import MODEL_BASE_PATH
    from pkdb_models.models.dextromethorphan.models.model_cyp2d6 import model_cyp2d6

    results: FactoryResult = create_model(
        model=[model_cyp2d6, model_liver],
        filepath=MODEL_BASE_PATH / f"{model_liver.sid}.xml",
    )
