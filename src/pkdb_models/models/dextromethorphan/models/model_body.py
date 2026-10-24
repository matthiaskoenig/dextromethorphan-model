"""Whole-body model of dextromethorphan and its metabolites.

The circulation of the plasma through the organs, the distribution into the
tissues, the oral absorption (intestine submodel), the hepatic metabolism
(liver submodel with the CYP2D6 activity of the diplotype) and the renal
excretion (kidney submodel). Dextromethorphan is given orally (`PODOSE_dxm`)
or intravenously (bolus `IVDOSE_dxm`, infusion `Ri_dxm`).

The substances are dextromethorphan (`dxm`), dextrorphan (`dxo`), dextrorphan
glucuronide (`dxo_glu`) and the lumped N-demethylated morphinans (`mm`:
3-methoxymorphinan, 3-hydroxymorphinan and its glucuronide, which the studies
report together). The concentrations of the blood compartments are plasma
concentrations, the blood to plasma ratio is 1 for every substance.

The distribution into a tissue is the perfusion limited exchange
`ftissue_<sid> * BW/BW_ref * (C_plasma * Kp_<sid> - C_tissue)`: the exchange is
fast against the blood flows, the partition coefficients set the volumes of
distribution (dextromethorphan 5-6.7 l/kg, Bolger2019, Capon1996).

The venous plasma `Cve_<sid>` is what the studies sample; the model has no
sampling site of its own, the arteriovenous difference during an intravenous
infusion (Duedahl2005) is not described.
"""

from typing import NamedTuple

import numpy as np
from sbmlutils.factory import (
    PORT_SUFFIX,
    AssignmentRule,
    Compartment,
    ExternalModelDefinition,
    FactoryResult,
    Model,
    Parameter,
    RateRule,
    Reaction,
    ReplacedElement,
    Species,
    Submodel,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import BQB, SBO

from pkdb_models.models.dextromethorphan.models import annotations, templates
from pkdb_models.models.dextromethorphan.models.fits import FITS
from pkdb_models.models.dextromethorphan.models.model_intestine import (
    SUBSTANCES_INTESTINE,
)
from pkdb_models.models.dextromethorphan.models.model_kidney import SUBSTANCES_KIDNEY


class U(templates.U):
    """Units of the whole-body model."""

    hr = UnitDefinition("hr")
    kg = UnitDefinition("kg")

    l_per_kg = UnitDefinition("l_per_kg", "l/kg")
    mg_per_l = UnitDefinition("mg_per_l", "mg/l")
    mg_per_min = UnitDefinition("mg_per_min", "mg/min")
    ml = UnitDefinition("ml")
    ml_per_l = UnitDefinition("ml_per_l", "ml/l")
    ml_per_s = UnitDefinition("ml_per_s", "ml/s")
    ml_per_s_kg = UnitDefinition("ml_per_s_kg", "ml/s/kg")
    mmole_per_l = UnitDefinition("mmole_per_l", "mmole/l")
    s_per_min = UnitDefinition("s_per_min", "s/min")


class SubstanceBody(NamedTuple):
    """A substance of the whole-body model."""

    name: str
    #: molecular weight [g/mole]
    Mr: float
    #: tissue/plasma partition coefficient, None: the value of the adopted
    #: fit (`models/fits.py`)
    Kp: float | None
    #: exchange flow with the tissues at the reference body weight [l/min]
    ftissue: float
    #: the substance is dosed (oral, intravenous)
    dosed: bool = False


#: the substances of the body. The partition coefficients of dextromethorphan
#: and of the N-demethylated morphinans are the values of the adopted fit
#: (`models/fits.py`), the others are fixed: free dextrorphan 4.0 (its
#: concentration is formation limited, no observable depends on it); the
#: glucuronide of dextrorphan stays in the plasma (0.01, not fitted: the first
#: fit of the model took it to the lower bound 0.01 of the fit, below which
#: the cost does not change; the total dextrorphan of the plasma of
#: Nagai1996, Schadel1995 and Tenneze1999 needs it). The exchange with the
#: tissues (`ftissue`) is fast against the perfusion, the distribution is
#: perfusion limited (the first fit took `ftissue_dxm` to its upper bound)
SUBSTANCES_BODY: dict[str, SubstanceBody] = {
    "dxm": SubstanceBody(
        "dextromethorphan", 271.404, Kp=None, ftissue=100.0, dosed=True
    ),
    "dxo": SubstanceBody("dextrorphan", 257.37066, Kp=4.0, ftissue=100.0),
    "dxo_glu": SubstanceBody(
        "dextrorphan glucuronide", 433.49478, Kp=0.01, ftissue=3.0
    ),
    "mm": SubstanceBody("N-demethylated morphinans", 257.37066, Kp=None, ftissue=10.0),
}
for _sid, (_name, _mr, *_rest) in SUBSTANCES_INTESTINE.items():
    if _mr != SUBSTANCES_BODY[_sid].Mr:
        raise ValueError(f"The molecular weights of '{_sid}' differ.")

# -----------------------------------------------------------------------------
# Submodels
# -----------------------------------------------------------------------------
COMPARTMENTS_BODY = {
    "ki": "kidney",
    "li": "liver",
    "lu": "lung",
    "gu": "gut",
    "re": "rest",
    "ar": "arterial blood",
    "ve": "venous blood",
    "po": "portal vein",
    "hv": "hepatic vein",
}
#: the blood compartments without tissue
BLOOD = ("ar", "ve", "po", "hv")
#: the organs which eliminate dextromethorphan or its metabolites: their
#: tissue exchanges fast with their plasma
ELIMINATING = ("li", "ki", "gu")

SUBMODEL_SID_DICT = {  # tissue to submodel mapping
    "ki": "KI",  # kidney
    "li": "LI",  # liver
    "gu": "GU",  # gut
}

kidney_id = "dextromethorphan_kidney"
liver_id = "dextromethorphan_liver"
gut_id = "dextromethorphan_intestine"

_m = Model(
    "dextromethorphan_body",
    name="Dextromethorphan (DXM) body model",
    notes="""
    # Whole-body model of dextromethorphan and its metabolites

    The circulation of the plasma through the organs, the distribution into
    the tissues, the oral absorption (intestine submodel), the hepatic
    metabolism (liver submodel with the CYP2D6 activity of the diplotype) and
    the renal excretion (kidney submodel). Dextromethorphan is given orally
    (`PODOSE_dxm`) or intravenously (bolus `IVDOSE_dxm`, infusion `Ri_dxm`).

    The substances are dextromethorphan (`dxm`), dextrorphan (`dxo`),
    dextrorphan glucuronide (`dxo_glu`) and the lumped N-demethylated
    morphinans (`mm`: 3-methoxymorphinan, 3-hydroxymorphinan and its
    glucuronide, which the studies report together). The concentrations of the
    blood compartments are plasma concentrations, the blood to plasma ratio is
    1 for every substance; the venous plasma `Cve_<sid>` is what the studies
    sample.
    """
    + templates.terms_of_use,
    units=U,
    model_units=templates.model_units,
    creators=templates.creators,
    annotations=[
        (BQB.OCCURS_IN, "bto/BTO:0001489"),  # whole body
        (BQB.OCCURS_IN, "fma/FMA:256135"),  # body
        (BQB.HAS_PROPERTY, "ncit/C79369"),  # Pharmacokinetics: Absorption
        (BQB.HAS_PROPERTY, "ncit/C79370"),  # Pharmacokinetics: Distribution
        (BQB.HAS_PROPERTY, "ncit/C79371"),  # Pharmacokinetics: Metabolism
        (BQB.HAS_PROPERTY, "ncit/C79372"),  # Pharmacokinetics: Excretion
        *templates.model_annotations,
    ],
)

_m.ports = []
_m.deletions = []
_m.replaced_elements = []

_m.external_model_definitions = [
    ExternalModelDefinition(
        sid="kidney",
        name="kidney model definition",
        source=f"{kidney_id}.xml",
        modelRef=kidney_id,
    ),
    ExternalModelDefinition(
        sid="liver",
        name="liver model definition",
        source=f"{liver_id}.xml",
        modelRef=liver_id,
    ),
    ExternalModelDefinition(
        sid="gut", name="gut model definition", source=f"{gut_id}.xml", modelRef=gut_id
    ),
]

_m.submodels = [
    Submodel(sid=SUBMODEL_SID_DICT["ki"], modelRef="kidney", name="kidney submodel"),
    Submodel(sid=SUBMODEL_SID_DICT["li"], modelRef="liver", name="liver submodel"),
    Submodel(sid=SUBMODEL_SID_DICT["gu"], modelRef="gut", name="gut submodel"),
]

# -----------------------------------------------------------------------------
# Compartments
# -----------------------------------------------------------------------------
_m.compartments = [
    Compartment(
        f"V{cid}",
        metaId=f"meta_V{cid}",
        value=1,
        unit=U.liter,
        constant=False,
        name=cname,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments[cid],
    )
    for cid, cname in COMPARTMENTS_BODY.items()
]
_m.compartments.extend(
    [
        Compartment(
            f"V{cid}",
            metaId=f"meta_V{cid}",
            value=1,
            unit=U.liter,
            constant=True,
            name=cid,
            sboTerm=SBO.PHYSICAL_COMPARTMENT,
            annotations=annotations.compartments[cid],
        )
        for cid in ("urine", "feces", "stomach")
    ]
)
_m.compartments.append(
    Compartment(
        "Vgulumen",
        metaId="meta_Vgulumen",
        value=1,
        unit=U.liter,
        constant=False,
        name="gut lumen",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["gu_lumen"],
    )
)
_m.parameters = [
    Parameter("f_lumen", 0.9, name="fraction lumen of intestine", unit=U.dimensionless)
]
_m.rules = [
    AssignmentRule("Vgulumen", "f_lumen * Vgu", unit=U.liter),
]

# plasma and tissue compartments of the organs
for cid in COMPARTMENTS_BODY:
    if cid in BLOOD:
        continue
    _m.compartments.extend(
        [
            Compartment(
                f"V{cid}_tissue",
                value=1,
                unit=U.liter,
                constant=False,
                name=f"{cid} tissue",
                metaId=f"meta_V{cid}_tissue",
                port=True,
                annotations=[
                    *annotations.compartments["parenchyma"],
                    *(
                        (BQB.IS_PART_OF, aid[1])
                        for aid in annotations.compartments[cid]
                    ),
                ],
                sboTerm=SBO.PHYSICAL_COMPARTMENT,
            ),
            Compartment(
                f"V{cid}_plasma",
                value=1,
                unit=U.liter,
                constant=False,
                name=f"{cid} plasma",
                metaId=f"meta_V{cid}_plasma",
                port=True,
                annotations=[
                    *annotations.compartments["plasma"],
                    *(
                        (BQB.IS_PART_OF, aid[1])
                        for aid in annotations.compartments[cid]
                    ),
                ],
                sboTerm=SBO.PHYSICAL_COMPARTMENT,
            ),
        ]
    )

# the volumes of the submodels
for element, submodel, port in [
    ("Vki_plasma", "ki", "Vext"),
    ("Vurine", "ki", "Vurine"),
    ("Vli_tissue", "li", "Vli"),
    ("Vgu_plasma", "gu", "Vext"),
    ("Vgu", "gu", "Vgu"),
    ("Vgulumen", "gu", "Vlumen"),
    ("Vfeces", "gu", "Vfeces"),
    ("Vstomach", "gu", "Vstomach"),
]:
    _m.replaced_elements.append(
        ReplacedElement(
            sid=f"{element}_{submodel}_RE",
            metaId=f"{element}_{submodel}_RE",
            elementRef=element,
            submodelRef=SUBMODEL_SID_DICT[submodel],
            portRef=f"{port}{PORT_SUFFIX}",
        )
    )

# -----------------------------------------------------------------------------
# Species
# -----------------------------------------------------------------------------
_m.species = []
for sid, substance in SUBSTANCES_BODY.items():
    # plasma
    for cid, cname in COMPARTMENTS_BODY.items():
        if cid in BLOOD:
            sid_ex = f"C{cid}_{sid}"
            cid_ex = f"V{cid}"
        else:
            sid_ex = f"C{cid}_plasma_{sid}"
            cid_ex = f"V{cid}_plasma"
        _m.species.append(
            Species(
                sid_ex,
                metaId=f"meta_{sid_ex}",
                initialConcentration=0.0,
                compartment=cid_ex,
                substanceUnit=U.mmole,
                name=f"{substance.name} ({cname} plasma)",
                hasOnlySubstanceUnits=False,
                port=True,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
            )
        )
    # tissue
    for cid, cname in COMPARTMENTS_BODY.items():
        if cid in BLOOD:
            continue
        sid_ex = f"C{cid}_{sid}"
        _m.species.append(
            Species(
                sid_ex,
                metaId=f"meta_{sid_ex}",
                initialConcentration=0.0,
                compartment=f"V{cid}_tissue",
                substanceUnit=U.mmole,
                name=f"{substance.name} ({cname})",
                hasOnlySubstanceUnits=False,
                port=True,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
            )
        )
    # urine
    _m.species.append(
        Species(
            f"Aurine_{sid}",
            metaId=f"meta_Aurine_{sid}",
            initialConcentration=0,
            compartment="Vurine",
            substanceUnit=U.mmole,
            name=f"{substance.name} (urine)",
            hasOnlySubstanceUnits=True,
            sboTerm=SBO.SIMPLE_CHEMICAL,
            annotations=annotations.species[sid],
        )
    )
# the lumen, the stomach and the feces of the oral substance
for sid in SUBSTANCES_INTESTINE:
    substance = SUBSTANCES_BODY[sid]
    _m.species.extend(
        [
            Species(
                f"Cgulumen_{sid}",
                metaId=f"meta_Cgulumen_{sid}",
                initialConcentration=0,
                compartment="Vgulumen",
                substanceUnit=U.mmole,
                name=f"{substance.name} (gut lumen)",
                hasOnlySubstanceUnits=False,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
            ),
            Species(
                f"Afeces_{sid}",
                metaId=f"meta_Afeces_{sid}",
                initialConcentration=0,
                compartment="Vfeces",
                substanceUnit=U.mmole,
                name=f"{substance.name} (feces)",
                hasOnlySubstanceUnits=True,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
            ),
        ]
    )

# the liver tissue is the compartment of the liver submodel, the plasma of the
# kidney and of the gut the external compartment of their submodels
for skey in SUBSTANCES_BODY:
    _m.replaced_elements.append(
        ReplacedElement(
            sid=f"Cli_{skey}_RE",
            metaId=f"Cli_{skey}_RE",
            elementRef=f"Cli_{skey}",
            submodelRef=SUBMODEL_SID_DICT["li"],
            portRef=f"{skey}{PORT_SUFFIX}",
        )
    )
for skey in SUBSTANCES_KIDNEY:
    _m.replaced_elements.extend(
        [
            ReplacedElement(
                sid=f"Cki_plasma_{skey}_RE",
                metaId=f"Cki_plasma_{skey}_RE",
                elementRef=f"Cki_plasma_{skey}",
                submodelRef=SUBMODEL_SID_DICT["ki"],
                portRef=f"{skey}_ext{PORT_SUFFIX}",
            ),
            ReplacedElement(
                sid=f"Aurine_{skey}_RE",
                metaId=f"Aurine_{skey}_RE",
                elementRef=f"Aurine_{skey}",
                submodelRef=SUBMODEL_SID_DICT["ki"],
                portRef=f"{skey}_urine{PORT_SUFFIX}",
            ),
        ]
    )
for skey in SUBSTANCES_INTESTINE:
    _m.replaced_elements.extend(
        [
            ReplacedElement(
                sid=f"Cgu_plasma_{skey}_RE",
                metaId=f"Cgu_plasma_{skey}_RE",
                elementRef=f"Cgu_plasma_{skey}",
                submodelRef=SUBMODEL_SID_DICT["gu"],
                portRef=f"{skey}_ext{PORT_SUFFIX}",
            ),
            ReplacedElement(
                sid=f"Cgulumen_{skey}_RE",
                metaId=f"Cgulumen_{skey}_RE",
                elementRef=f"Cgulumen_{skey}",
                submodelRef=SUBMODEL_SID_DICT["gu"],
                portRef=f"{skey}_lumen{PORT_SUFFIX}",
            ),
            ReplacedElement(
                sid=f"Afeces_{skey}_RE",
                metaId=f"Afeces_{skey}_RE",
                elementRef=f"Afeces_{skey}",
                submodelRef=SUBMODEL_SID_DICT["gu"],
                portRef=f"{skey}_feces{PORT_SUFFIX}",
            ),
        ]
    )

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
_m.parameters.extend(
    [
        Parameter(
            "BW",
            75,
            U.kg,
            constant=True,
            name="body weight [kg]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "BW_ref",
            75,
            U.kg,
            constant=True,
            name="reference body weight [kg]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes=(
                "Body weight at which the exchange flows of the tissue "
                "distribution (`ftissue_<sid>`) are given; they scale with the "
                "body weight as the volumes, the blood flows and the renal "
                "clearance do."
            ),
        ),
        Parameter(
            "COBW",
            1.548,
            U.ml_per_s_kg,
            constant=True,
            name="cardiac output per bodyweight [ml/s/kg]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "CO",
            np.nan,
            U.ml_per_s,
            constant=False,
            name="cardiac output [ml/s]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "QC",
            np.nan,
            U.l_per_min,
            constant=False,
            name="cardiac output [l/min]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "Fblood",
            0.02,
            U.dimensionless,
            constant=True,
            name="blood fraction of organ volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "HCT",
            0.51,
            U.dimensionless,
            constant=True,
            metaId="meta_HCT",
            name="hematocrit",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        # fractional tissue volumes
        Parameter(
            "FVgu",
            0.0171,
            U.l_per_kg,
            constant=True,
            name="gut fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVki",
            0.0044,
            U.l_per_kg,
            constant=True,
            name="kidney fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVli",
            0.0210,
            U.l_per_kg,
            constant=True,
            name="liver fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVlu",
            0.0076,
            U.l_per_kg,
            constant=True,
            name="lung fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVre",
            np.nan,
            U.l_per_kg,
            constant=False,
            name="rest of body fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVve",
            0.0514,
            U.l_per_kg,
            constant=True,
            name="venous fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVar",
            0.0257,
            U.l_per_kg,
            constant=True,
            name="arterial fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVpo",
            0.001,
            U.l_per_kg,
            constant=True,
            name="portal fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVhv",
            0.001,
            U.l_per_kg,
            constant=True,
            name="hepatic venous fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        # fractional tissue blood flows
        Parameter(
            "FQgu",
            0.18,
            U.dimensionless,
            constant=True,
            name="gut fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
            FQgu is the sum of FQgu + FQsp + FQpa for the correct portal blood
            flow, with FQgu=0.146, FQsp=0.017, FQpa=0.017.
            """,
        ),
        Parameter(
            "FQki",
            0.190,
            U.dimensionless,
            constant=True,
            name="kidney fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FQh",
            0.215,
            U.dimensionless,
            constant=True,
            name="hepatic (venous side) fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FQlu",
            1,
            U.dimensionless,
            constant=True,
            name="lung fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FQre",
            np.nan,
            U.dimensionless,
            constant=False,
            name="rest of body fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        # renal function
        Parameter(
            "ftissue_fast",
            100.0,
            U.l_per_min,
            constant=True,
            name="tissue distribution of the eliminating organs",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
            The exchange flow between the plasma and the tissue of the liver,
            the kidney and the gut at the reference body weight `BW_ref`:
            fast against their perfusion, so the exchange does not limit the
            hepatic metabolism, the renal excretion or the absorption. Fixed.
            """,
        ),
        Parameter(
            "f_GFR_Qki",
            101 / 1.32354,
            U.ml_per_l,
            constant=True,
            name="relationship GFR and Qki",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
            GFR per renal blood flow (76.3 ml/l). Calibrated so that the
            healthy GFR is 101 ml/min at the renal blood flow of 1.32354 l/min
            of 75 kg, the normal GFR of the classes of renal impairment
            (`pkpdsim.impairment`).
            """,
        ),
        Parameter(
            "GFR_base",
            np.nan,
            U.ml_per_min,
            constant=False,
            name="glomerular filtration rate (healthy)",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
            The GFR of healthy kidneys, which scales with the renal blood flow
            and so with the body weight; the GFR is `KI__f_renal_function`
            times this rate.
            """,
        ),
    ]
)

for sid, substance in SUBSTANCES_BODY.items():
    _m.parameters.extend(
        [
            Parameter(
                f"Mr_{sid}",
                substance.Mr,
                U.g_per_mole,
                constant=True,
                name=f"Molecular weight {sid} [g/mole]",
                sboTerm=SBO.MOLECULAR_MASS,
            ),
            Parameter(
                f"ftissue_{sid}",
                substance.ftissue,
                U.l_per_min,
                constant=True,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name=f"tissue distribution {sid}",
                notes="Exchange flow between the plasma and the tissue of the "
                "peripheral organs (the rest of the body, the lung) at the "
                "reference body weight `BW_ref`; it sets how fast the "
                "distribution phase is.",
            ),
            Parameter(
                f"Kp_{sid}",
                **(
                    FITS.parameter(f"Kp_{sid}", unit=U.dimensionless)
                    if substance.Kp is None
                    else {"value": substance.Kp, "unit": U.dimensionless}
                ),
                constant=True,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name=f"tissue/plasma partition coefficient {sid}",
            ),
        ]
    )
    if not substance.dosed:
        continue
    _m.parameters.extend(
        [
            # intravenous
            Parameter(
                f"IVDOSE_{sid}",
                0,
                U.mg,
                constant=False,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name=f"IV bolus dose {sid} [mg]",
            ),
            Parameter(
                f"ti_{sid}",
                10,
                U.second,
                constant=True,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name=f"injection time {sid} [s]",
            ),
            Parameter(
                f"Ki_{sid}",
                np.nan,
                U.per_min,
                constant=False,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name=f"Ki [1/min] injection {sid}",
            ),
            Parameter(
                f"Ri_{sid}",
                0,
                U.mg_per_min,
                constant=True,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name=f"Ri [mg/min] rate of infusion {sid}",
            ),
            Parameter(
                f"cum_dose_{sid}",
                0,
                U.mg,
                constant=False,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name=f"cumulative dose of the infusion {sid} [mg]",
            ),
            # oral
            Parameter(
                f"PODOSE_{sid}",
                0,
                U.mg,
                constant=False,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name=f"oral dose {sid} [mg]",
                annotations=[(BQB.IS, "ncit/C38288")],
            ),
            Parameter(
                f"Ka_dis_{sid}",
                **FITS.parameter(f"Ka_dis_{sid}", unit=U.per_hr),
                constant=True,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name=f"Ka_dis [1/hr] dissolution {substance.name}",
            ),
        ]
    )
    for pid in (f"PODOSE_{sid}", f"Ka_dis_{sid}", f"Mr_{sid}"):
        _m.replaced_elements.append(
            ReplacedElement(
                sid=f"{pid}_gu_RE",
                metaId=f"{pid}_gu_RE",
                elementRef=pid,
                submodelRef=SUBMODEL_SID_DICT["gu"],
                portRef=f"{pid}{PORT_SUFFIX}",
            )
        )

# the fractions unbound of the kidney and the glomerular filtration rate
for skey in SUBSTANCES_KIDNEY:
    _m.parameters.append(
        Parameter(
            f"fu_{skey}",
            SUBSTANCES_KIDNEY[skey][1],
            U.dimensionless,
            constant=True,
            name=f"fraction unbound in plasma {skey}",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        )
    )
    _m.replaced_elements.append(
        ReplacedElement(
            sid=f"fu_{skey}_RE",
            metaId=f"fu_{skey}_RE",
            elementRef=f"fu_{skey}",
            submodelRef=SUBMODEL_SID_DICT["ki"],
            portRef=f"fu_{skey}{PORT_SUFFIX}",
        )
    )
_m.replaced_elements.append(
    ReplacedElement(
        sid="GFR_base_ki_RE",
        metaId="GFR_base_ki_RE",
        elementRef="GFR_base",
        submodelRef=SUBMODEL_SID_DICT["ki"],
        portRef=f"GFR_base{PORT_SUFFIX}",
    )
)

# -----------------------------------------------------------------------------
# AssignmentRules
# -----------------------------------------------------------------------------
_m.rules.extend(
    [
        # rest of body volume and perfusion
        AssignmentRule(
            "FVre",
            "1.0 l_per_kg - (FVgu + FVki + FVli + FVlu + FVve + FVar)",
            U.l_per_kg,
        ),
        AssignmentRule("FQre", "1.0 dimensionless - (FQki + FQh)", U.dimensionless),
        # cardiac output (depending on the bodyweight)
        AssignmentRule("CO", "BW*COBW", U.ml_per_s),
        AssignmentRule("QC", "CO/1000 ml_per_l * 60 s_per_min", U.l_per_min),
        # volumes
        AssignmentRule("Vgu", "BW*FVgu", U.liter),
        AssignmentRule("Vki", "BW*FVki", U.liter),
        AssignmentRule("Vli", "BW*FVli", U.liter),
        AssignmentRule("Vlu", "BW*FVlu", U.liter),
        AssignmentRule("Vre", "BW*FVre", U.liter),
        # venous and arterial blood volume (corrected for tissue blood volumes)
        AssignmentRule(
            "Vve",
            "BW*FVve - FVve/(FVar+FVve) * BW * Fblood * (1 l_per_kg - FVve - FVar)",
            U.liter,
        ),
        AssignmentRule(
            "Var",
            "BW*FVar - FVar/(FVar+FVve) * BW * Fblood * (1 l_per_kg - FVve - FVar)",
            U.liter,
        ),
        AssignmentRule(
            "Vpo",
            "(1 dimensionless - HCT) * (BW*FVpo - FVpo/(FVar+FVve+FVpo+FVhv) "
            "* BW * Fblood * (1 l_per_kg - (FVar+FVve+FVpo+FVhv)))",
            U.liter,
        ),
        AssignmentRule(
            "Vhv",
            "(1 dimensionless - HCT) * (BW*FVhv - FVhv/(FVar+FVve+FVpo+FVhv) "
            "* BW * Fblood * (1 l_per_kg - (FVar+FVve+FVpo+FVhv)))",
            U.liter,
        ),
        # blood flows
        AssignmentRule("Qgu", "QC*FQgu", U.l_per_min, name="gut blood flow"),
        AssignmentRule("Qki", "QC*FQki", U.l_per_min, name="kidney blood flow"),
        AssignmentRule(
            "Qh", "QC*FQh", U.l_per_min, name="hepatic (venous side) blood flow"
        ),
        AssignmentRule(
            "Qha", "Qh - Qgu", U.l_per_min, name="hepatic artery blood flow"
        ),
        AssignmentRule("Qlu", "QC*FQlu", U.l_per_min, name="lung blood flow"),
        AssignmentRule("Qre", "QC*FQre", U.l_per_min, name="rest of body blood flow"),
        AssignmentRule("Qpo", "Qgu", U.l_per_min, name="portal blood flow"),
        # glomerular filtration rate of healthy kidneys
        AssignmentRule(
            "GFR_base",
            "f_GFR_Qki * Qki",
            U.ml_per_min,
            name="glomerular filtration rate (healthy)",
        ),
    ]
)

for cid, cname in COMPARTMENTS_BODY.items():
    if cid in BLOOD:
        continue
    _m.rules.extend(
        [
            AssignmentRule(
                f"V{cid}_plasma",
                value=f"V{cid} * Fblood * (1 dimensionless - HCT)",
                unit=U.liter,
                name=f"plasma volume of {cname}",
            ),
            AssignmentRule(
                f"V{cid}_tissue",
                value=f"V{cid} * (1 dimensionless - Fblood)",
                unit=U.liter,
                name=f"tissue volume of {cname}",
            ),
        ]
    )

for sid, substance in SUBSTANCES_BODY.items():
    sname = substance.name
    if substance.dosed:
        _m.rules.append(
            AssignmentRule(
                f"Ki_{sid}",
                f"0.693 dimensionless/ti_{sid} * 60 s_per_min",
                U.per_min,
                name="injection rate IV",
                notes="""
                log(2) ~ 0.693 used for conversion of the half-life of the
                injection time to the injection rate.
                """,
            )
        )
    # amounts and mass concentrations of the venous plasma and of the urine
    _m.rules.extend(
        [
            AssignmentRule(
                f"Ave_{sid}",
                f"Cve_{sid}*Vve",
                U.mmole,
                name=f"{sname} amount (venous blood) [mmole]",
            ),
            AssignmentRule(
                f"Mve_{sid}",
                f"Cve_{sid}*Mr_{sid}",
                U.mg_per_l,
                name=f"{sname} concentration (venous plasma) [mg/l]",
            ),
            AssignmentRule(
                f"Xurine_{sid}",
                f"Aurine_{sid}*Mr_{sid}",
                U.mg,
                name=f"{sname} amount (urine) [mg]",
            ),
        ]
    )
_m.rules.append(
    AssignmentRule(
        "Xfeces_dxm",
        "Afeces_dxm*Mr_dxm",
        U.mg,
        name="dextromethorphan amount (feces) [mg]",
    )
)

# the observables of the studies: the total dextrorphan (free and conjugated)
# and the metabolic ratios of the plasma and of the urine
_m.rules.extend(
    [
        AssignmentRule(
            "dxo_total",
            "Cve_dxo + Cve_dxo_glu",
            U.mmole_per_l,
            name="total dextrorphan (plasma)",
        ),
        AssignmentRule(
            "dxm_dxo",
            "Cve_dxm/Cve_dxo",
            U.dimensionless,
            name="DXM/DXO ratio (plasma)",
        ),
        AssignmentRule(
            "dxm_dxo_total",
            "Cve_dxm/(Cve_dxo + Cve_dxo_glu)",
            U.dimensionless,
            name="DXM/total DXO ratio (plasma)",
        ),
        AssignmentRule(
            "Aurine_dxo_total",
            "Aurine_dxo + Aurine_dxo_glu",
            U.mmole,
            name="cumulative urinary total dextrorphan",
        ),
        AssignmentRule(
            "dxm_dxo_urine",
            "Aurine_dxm/Aurine_dxo",
            U.dimensionless,
            name="cumulative urinary DXM/DXO ratio",
        ),
        AssignmentRule(
            "dxm_dxo_total_urine",
            "Aurine_dxm/(Aurine_dxo + Aurine_dxo_glu)",
            U.dimensionless,
            name="cumulative urinary DXM/total DXO ratio",
        ),
    ]
)

# -----------------------------------------------------------------------------
# Reactions
# -----------------------------------------------------------------------------
_m.reactions = []

for sid, substance in SUBSTANCES_BODY.items():
    sname = substance.name

    # tissue distribution: the eliminating organs exchange fast with their
    # plasma (`ftissue_fast`, the exchange does not limit the metabolism and
    # the excretion), the peripheral tissues with `ftissue_<sid>`
    for cid in COMPARTMENTS_BODY:
        if cid in BLOOD:
            continue
        ftissue = "ftissue_fast" if cid in ELIMINATING else f"ftissue_{sid}"
        _m.reactions.append(
            Reaction(
                sid=f"transport_{cid}_{sid}",
                name=f"transport {sname}",
                formula=(
                    f"{ftissue} * BW/BW_ref * "
                    f"(C{cid}_plasma_{sid} * Kp_{sid} - C{cid}_{sid})",
                    U.mmole_per_min,
                ),
                equation=f"C{cid}_plasma_{sid} <-> C{cid}_{sid}",
                compartment=f"V{cid}_tissue",
                sboTerm=SBO.TRANSPORT_REACTION,
            ),
        )

    if substance.dosed:
        _m.reactions.append(
            Reaction(
                sid=f"iv_{sid}",
                name=f"iv {sname}",
                formula=(f"Ki_{sid}*IVDOSE_{sid}/Mr_{sid}", U.mmole_per_min),
                equation=f"-> Cve_{sid}",
                sboTerm=SBO.TRANSPORT_REACTION,
                annotations=[(BQB.IS, "ncit/C38276")],
                compartment="Vve",
            ),
        )

    # ve -> lung -> ar
    _m.reactions.extend(
        [
            Reaction(
                sid=f"Flow_ve_lu_{sid}",
                name=f"inflow lung {sname}",
                formula=(f"Qlu*Cve_{sid}", U.mmole_per_min),
                equation=f"Cve_{sid} -> Clu_plasma_{sid}",
                sboTerm=SBO.TRANSPORT_REACTION,
            ),
            Reaction(
                sid=f"Flow_lu_ar_{sid}",
                name=f"outflow lung {sname}",
                formula=(f"Qlu*Clu_plasma_{sid}", U.mmole_per_min),
                equation=f"Clu_plasma_{sid} -> Car_{sid}",
                sboTerm=SBO.TRANSPORT_REACTION,
            ),
        ]
    )
    # ar -> organ -> ve (kidney, rest), ar -> gut -> po
    for cid, target in [("ki", "ve"), ("re", "ve"), ("gu", "po")]:
        cname = COMPARTMENTS_BODY[cid]
        _m.reactions.extend(
            [
                Reaction(
                    sid=f"Flow_ar_{cid}_{sid}",
                    name=f"inflow {cname} {sname}",
                    formula=(f"Q{cid}*Car_{sid}", U.mmole_per_min),
                    equation=f"Car_{sid} -> C{cid}_plasma_{sid}",
                    sboTerm=SBO.TRANSPORT_REACTION,
                ),
                Reaction(
                    sid=f"Flow_{cid}_{target}_{sid}",
                    name=f"outflow {cname} {sname}",
                    formula=(f"Q{cid}*C{cid}_plasma_{sid}", U.mmole_per_min),
                    equation=f"C{cid}_plasma_{sid} -> C{target}_{sid}",
                    sboTerm=SBO.TRANSPORT_REACTION,
                ),
            ]
        )
    # ar -> li, po -> li, li -> hv -> ve
    _m.reactions.extend(
        [
            Reaction(
                sid=f"Flow_ar_li_{sid}",
                name=f"arterial inflow liver {sname}",
                formula=(f"Qha*Car_{sid}", U.mmole_per_min),
                equation=f"Car_{sid} -> Cli_plasma_{sid}",
                sboTerm=SBO.TRANSPORT_REACTION,
            ),
            Reaction(
                sid=f"Flow_po_li_{sid}",
                name=f"outflow po {sname}",
                formula=(f"Qpo*Cpo_{sid}", U.mmole_per_min),
                equation=f"Cpo_{sid} -> Cli_plasma_{sid}",
                sboTerm=SBO.TRANSPORT_REACTION,
            ),
            Reaction(
                sid=f"Flow_li_hv_{sid}",
                name=f"outflow liver {sname}",
                formula=(f"Qh*Cli_plasma_{sid}", U.mmole_per_min),
                equation=f"Cli_plasma_{sid} -> Chv_{sid}",
                sboTerm=SBO.TRANSPORT_REACTION,
            ),
            Reaction(
                sid=f"Flow_hv_ve_{sid}",
                name=f"outflow hepatic vein {sname}",
                formula=(f"Qh*Chv_{sid}", U.mmole_per_min),
                equation=f"Chv_{sid} -> Cve_{sid}",
                sboTerm=SBO.TRANSPORT_REACTION,
            ),
        ]
    )

# -----------------------------------------------------------------------------
# RateRules
# -----------------------------------------------------------------------------
_m.rate_rules = []
for sid, substance in SUBSTANCES_BODY.items():
    if not substance.dosed:
        continue
    _m.rate_rules.extend(
        [
            # injection of the dose and infusion
            RateRule(f"IVDOSE_{sid}", f"-iv_{sid}*Mr_{sid} + Ri_{sid}", U.mg_per_min),
            # cumulative infusion dose
            RateRule(f"cum_dose_{sid}", f"Ri_{sid}", U.mg_per_min),
        ]
    )

model_body: Model = _m


if __name__ == "__main__":
    from pkdb_models.models.dextromethorphan import MODEL_BASE_PATH

    results: FactoryResult = create_model(
        model=model_body,
        filepath=MODEL_BASE_PATH / f"{model_body.sid}.xml",
    )
