"""Annotations of the dextromethorphan models: the species and the shared compartments.

The compartments are the shared ones of `pkpdsim.annotations`. The lumped
N-demethylated morphinans (`mm`: 3-methoxymorphinan, 3-hydroxymorphinan and
its glucuronide) are one species of several substances and carry no identifier
of a single compound.
"""

from pkpdsim.annotations import compartments
from sbmlutils.metadata import BQB

__all__ = ["compartments", "species"]

species: dict[str, list[tuple[BQB, str]]] = {
    "dxm": [  # dextromethorphan
        (BQB.IS, "chebi/CHEBI:4470"),
        (BQB.IS, "ncit/C62022"),
        (BQB.IS, "inchikey/MKXZASYAUGDDCJ-NJAFHUGGSA-N"),
    ],
    "dxo": [  # dextrorphan
        (BQB.IS, "chebi/CHEBI:29133"),
        (BQB.IS, "ncit/C171857"),
        (BQB.IS, "inchikey/JAQUASYNZVUNQP-PVAVHDDUSA-N"),
    ],
    "dxo_glu": [  # dextrorphan glucuronide
        (BQB.IS, "chebi/CHEBI:32645"),
        (BQB.IS, "pubchem.compound/24883428"),
        (BQB.IS, "inchikey/YQAUTKINOXBFCA-DCWOAAMISA-N"),
    ],
    # 3-methoxymorphinan and 3-hydroxymorphinan (free and conjugated), lumped
    "mm": [],
}
