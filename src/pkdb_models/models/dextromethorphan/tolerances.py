"""The tolerances of the integrator for the dextromethorphan model."""

from sbmlsim.model.tolerances import AbsoluteTolerance


def absolute_tolerance(value: float, species: float) -> AbsoluteTolerance:
    """Get the absolute tolerance of the integrator for the dextromethorphan model.

    The species of dextromethorphan and its metabolites are small: the plasma
    concentrations of dextromethorphan in extensive metabolizers are about
    1e-9 mM and those of its metabolites 1e-6 to 1e-3 mM, the amounts in the
    urine are 1e-6 to 1e-1 mmole. The other states are the doses in mg (the
    targets of the rate rules).

    Args:
        value: tolerance of the other states [mg].
        species: tolerance of the species, of their concentrations [mM] and
            amounts [mmole].

    Returns:
        The absolute tolerance per kind of state.
    """
    return AbsoluteTolerance(amount=species, concentration=species, other=value)


#: the absolute tolerance of the simulation experiments
ABSOLUTE_TOLERANCE = absolute_tolerance(1e-10, species=1e-14)
