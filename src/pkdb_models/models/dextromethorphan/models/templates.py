"""Templates of the dextromethorphan models: units, model units, creators and annotations."""

from pkpdsim.templates import creators as template_creators
from pkpdsim.templates import terms_of_use
from sbmlutils.factory import Creator, ModelUnits, UnitDefinition, Units
from sbmlutils.metadata import BQB

__all__ = ["U", "creators", "model_annotations", "model_units", "terms_of_use"]


class U(Units):
    """UnitDefinitions."""

    g_per_mole = UnitDefinition("g_per_mole", "g/mole")
    l_per_min = UnitDefinition("litre_per_min", "litre/min")
    l_per_ml = UnitDefinition("l_per_ml", "l/ml")
    m2 = UnitDefinition("m2", "meter^2")
    mg = UnitDefinition("mg")
    min = UnitDefinition("min")
    min_per_hr = UnitDefinition("min_per_hr", "min/hr")
    ml_per_min = UnitDefinition("ml_per_min", "ml/min")
    mM = UnitDefinition("mM", "mmole/liter")
    microM = UnitDefinition("microM", "micromole/liter")

    mmole = UnitDefinition("mmole")
    mmole_per_min = UnitDefinition("mmole_per_min", "mmole/min")
    mmole_per_min_l = UnitDefinition("mmole_per_min_l", "mmole/min/liter")
    per_min = UnitDefinition("per_min", "1/min")
    per_hr = UnitDefinition("per_hr", "1/hr")


model_units = ModelUnits(
    time=U.min,
    extent=U.mmole,
    substance=U.mmole,
    length=U.meter,
    area=U.m2,
    volume=U.liter,
)

model_annotations = [
    # taxonomy
    (BQB.HAS_TAXON, "taxonomy/9606"),  # human
    (BQB.HAS_TAXON, "snomedct/337915000"),  # human
    # modelling approach
    (BQB.HAS_PROPERTY, "mamo/MAMO_0000046"),  # ordinary differential equation model
    # biological process explained by model
    (BQB.HAS_PROPERTY, "ncit/C15299"),  # pharmacokinetics
]

creators = [
    Creator(
        familyName="Grzegorzewski",
        givenName="Jan",
        email="janekG89@hotmail.de",
        organization="Humboldt-Universität zu Berlin, Institute for Theoretical Biology",
    ),
    Creator(
        familyName="Brandhorst",
        givenName="Janosch",
        email="jbrandhorst1@googlemail.com",
        organization="Humboldt-Universität zu Berlin, Institute for Theoretical Biology",
    ),
    *template_creators,
]
