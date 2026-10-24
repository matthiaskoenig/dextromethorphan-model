"""Model of the CYP2D6 activity of a genotype, merged into the dextromethorphan liver.

The activity `cyp2d6_activity` of the diplotype is the sum of the activities of
its two alleles, the activity scores of PharmGKB. An allele is selected by its
index in the allele activities of `ALLELE_ACTIVITIES_PATH` (`cyp2d6_allele1`,
`cyp2d6_allele2`), the index -1 selects the custom activity `cyp2d6_ac` of the
diplotype, which is the activity score of a group whose diplotypes are not
reported.

The liver takes the activity relative to the score of two functional alleles
(`cyp2d6_activity_ref`, 2.0): the O-demethylation of dextromethorphan by CYP2D6
scales linearly with it.
"""

import json
import math

from pkpdsim.templates import terms_of_use
from sbmlutils.factory import AssignmentRule, Model, Parameter, create_model
from sbmlutils.metadata import SBO

from pkdb_models.models.dextromethorphan import ALLELE_ACTIVITIES_PATH
from pkdb_models.models.dextromethorphan.models import templates


class U(templates.U):
    """UnitsDefinitions."""


_m = Model(
    "cyp2d6",
    name="Model for CYP2D6 activity",
    notes="""
    # Model for CYP2D6 activity

    The activity of CYP2D6 of a diplotype is the sum of the activity scores
    of its two alleles (PharmGKB). The liver takes it relative to the score of
    two functional alleles.
    """
    + terms_of_use,
    units=U,
    model_units=templates.model_units,
    creators=templates.creators,
)


# allele activity information (*1 -> 1, *1x2 -> 2, ...), the parameters
# `cyp2d6_a<index>`
with ALLELE_ACTIVITIES_PATH.open() as read_file:
    allele_activities: dict[str, float] = json.load(read_file)

_m.parameters = [
    Parameter(
        f"cyp2d6_a{ka}",
        allele_activity,
        U.dimensionless,
        name=f"{allele} activity",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    )
    for ka, (allele, allele_activity) in enumerate(allele_activities.items())
]
_m.parameters.extend(
    [
        Parameter(
            "cyp2d6_ac",
            1.0,
            U.dimensionless,
            name="custom allele activity",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        # alleles in model (index in the allele activities)
        Parameter(
            "cyp2d6_allele1",
            0,
            unit=U.dimensionless,
            name="allele 1",
            constant=False,
            sboTerm=SBO.SWITCH_VALUE,
        ),
        Parameter(
            "cyp2d6_allele2",
            0,
            unit=U.dimensionless,
            name="allele 2",
            constant=False,
            sboTerm=SBO.SWITCH_VALUE,
        ),
        # activities of alleles in model
        Parameter(
            "cyp2d6_activity1",
            math.nan,
            unit=U.dimensionless,
            name="activity of allele 1",
            constant=False,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "cyp2d6_activity2",
            math.nan,
            unit=U.dimensionless,
            name="activity of allele 2",
            constant=False,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
    ]
)

_m.rules = []
for allele in [1, 2]:
    # piecewise function which selects the activity of the allele:
    # piecewise(x1, y1, [x2, y2,] [...] [z]): if (y1), x1, otherwise, if (y2), x2,
    # etc. Otherwise, z.
    rule_activity = f"piecewise(cyp2d6_ac/2 dimensionless, cyp2d6_allele{allele} == -1,"
    for ka in range(len(allele_activities)):
        rule_activity += f"cyp2d6_a{ka}, cyp2d6_allele{allele} == {ka},"
    rule_activity += "cyp2d6_ac/2 dimensionless)"

    _m.rules.append(
        AssignmentRule(
            f"cyp2d6_activity{allele}",
            rule_activity,
            unit=U.dimensionless,
            name=f"activity of allele {allele}",
        ),
    )

_m.rules.append(
    AssignmentRule(
        "cyp2d6_activity",
        "(cyp2d6_activity1 + cyp2d6_activity2)",
        unit=U.dimensionless,
        name="activity of CYP2D6 diplotype",
    )
)

model_cyp2d6 = _m

if __name__ == "__main__":
    from pkdb_models.models.dextromethorphan import MODEL_BASE_PATH

    create_model(
        model=model_cyp2d6,
        filepath=MODEL_BASE_PATH / f"{model_cyp2d6.sid}.xml",
    )
