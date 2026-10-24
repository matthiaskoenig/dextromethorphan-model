"""CYP2D6 genotypes and phenotypes: activity scores of the alleles and diplotypes.

The activity scores of the CYP2D6 alleles are the functionality of the
PharmGKB CYP2D6 allele functionality table
(`data/cyp2d6/CYP2D6_allele_functionality_reference.xlsx`). The CYP2D6 model
reads them from `data/cyp2d6/allele_activities.json`, which this module writes
(`python genotype_phenotype.py`); an allele is selected in the model by its
index in the sorted scores.
"""

import json
from enum import StrEnum, unique
from typing import ClassVar

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import to_hex

from pkdb_models.models.dextromethorphan import (
    ALLELE_ACTIVITIES_PATH,
    DEXTROMETHORPHAN_PATH,
)

colors_phenotype: dict[str, str] = {
    "um": "tab:green",
    "em": "tab:orange",
    "im": "tab:blue",
    "pm": "tab:red",
}


def read_allele_scores() -> dict[str, float]:
    """Read the activity scores of the CYP2D6 alleles, sorted by allele.

    The alleles with several copies (`*1x3`, ...) are added, alleles without a
    score are left out.
    """
    path_allele_score = (
        DEXTROMETHORPHAN_PATH
        / "data"
        / "cyp2d6"
        / "CYP2D6_allele_functionality_reference.xlsx"
    )
    df_allele_score: pd.DataFrame = pd.read_excel(path_allele_score, skiprows=1)
    df_allele_score = df_allele_score.iloc[:, 0:3]
    df_allele_score.columns = ["allele", "activity", "status"]

    activities: dict[str, float | str] = dict(
        zip(df_allele_score["allele"], df_allele_score["activity"], strict=True)
    )
    # the alleles with three or more copies are given as ranges
    del activities["*1≥3"]
    del activities["*2≥3"]
    del activities["*4≥2"]
    for k in [3, 4, 5, 6]:
        activities[f"*1x{k}"] = float(k)
        activities[f"*2x{k}"] = float(k)
        activities[f"*4x{k - 1}"] = 0.0

    scores: dict[str, float] = {}
    for allele, activity in activities.items():
        if "≥" in allele:
            raise ValueError(f"Handle special alleles manually: {allele, activity}")
        scores[allele] = float(activity)

    return {k: scores[k] for k in sorted(scores) if not np.isnan(scores[k])}


allele_scores = read_allele_scores()


@unique
class GeneticPhenotype(StrEnum):
    """Phenotype of a CYP2D6 diplotype from its activity score."""

    gPM = "gPM"
    gIM = "gIM"
    gEM = "gEM"
    gUM = "gUM"


@unique
class MetabolicPhenotype(StrEnum):
    """Phenotype from phenotyping, e.g. the urinary metabolic ratio DXM/DXO."""

    PM = "PM"
    IM = "IM"
    EM = "EM"
    UM = "UM"


class GenotypeScoring:
    """Activity scores based on genetic information."""

    allele_scores: ClassVar[dict[str, float]] = allele_scores
    allele_indices: ClassVar[dict[str, int]] = {
        k: i for i, k in enumerate(allele_scores)
    }

    @staticmethod
    def diplotype_to_string(diplotype: str) -> str:
        """String representation due to special characters."""
        return diplotype.replace("*", "").replace("/", "-")

    @staticmethod
    def alleles_from_diplotype(diplotype: str) -> list[str]:
        """Get alleles from diplotype (genotype).

        Returns multiple alleles.
        """
        return diplotype.split("/")

    @classmethod
    def index_for_allele(cls, allele: str) -> int:
        """Return the index of an allele, its parameter in the CYP2D6 model.

        Raises an error for special alleles such as '*9x2'.
        """
        return int(cls.allele_indices[allele])

    @classmethod
    def indices_for_diplotype(cls, diplotype: str) -> tuple[int, ...]:
        """Return the allele indices of a diplotype (genotype), e.g. '*1/*1'."""
        alleles: list[str] = GenotypeScoring.alleles_from_diplotype(diplotype)
        return tuple(cls.index_for_allele(a) for a in alleles)

    @classmethod
    def activity_score_for_diplotype(cls, diplotype: str) -> float:
        """Returns score for diplotype (genotype).

        Example given '*1/*1'.

        return: sum of activity scores for alleles.
        """
        alleles: list[str] = GenotypeScoring.alleles_from_diplotype(diplotype)
        score = 0.0
        for allele in alleles:
            score += cls.activity_score_allele(allele)
        return score

    @classmethod
    def activity_score_allele(cls, allele: str) -> float:
        """Returns allele score.

        Raises Error for special alleles such as '*9x2'
        """
        return float(cls.allele_scores[allele])

    @classmethod
    def genetic_phenotype_for_diplotype(cls, diplotype: str) -> GeneticPhenotype:
        """Mapping of diplotype to phenotype based on activity score.

        Multiple mapping systems exist, such as
        - CPIC
        - DPWG
        Here the system from the PharmGKB CYP2D6 Diplotype-Phenotype Table
        is used.
        - PM: 0 (poor)
        - IM: 0.25 <= x <= 1.0 (intermediate)
        - NM/EM: 1.25 <= x <= 2.25 (normal)
        - UM: x >= 2.5 (ultrarapid)
        """
        activity_score = cls.activity_score_for_diplotype(diplotype)
        return cls.genetic_phenotype_for_activity_score(activity_score)

    @classmethod
    def genetic_phenotype_for_activity_score(
        cls, activity_score: float
    ) -> GeneticPhenotype:
        """Mapping to phenotype based on activity score.

        Multiple mapping systems exist, such as
        - CPIC
        - DPWG
        Here the system from the PharmGKB CYP2D6 Diplotype-Phenotype Table
        is used.
        - PM: 0 (poor)
        - IM: 0.25 <= x <= 1.0 (intermediate)
        - NM/EM: 1.25 <= x <= 2.25 (normal)
        - UM: x >= 2.5 (ultrarapid)
        """
        if activity_score == 0:
            return GeneticPhenotype.gPM
        if 0.25 <= activity_score <= 1.0:
            return GeneticPhenotype.gIM
        if 1.25 <= activity_score <= 2.25:
            return GeneticPhenotype.gEM
        if activity_score >= 2.5:
            return GeneticPhenotype.gUM
        raise ValueError(f"No genetic phenotype for activity score {activity_score}")

    @classmethod
    def metabolic_phenotype_for_urinary_ratio(cls, ratio: float) -> MetabolicPhenotype:
        """Phenotype based on urinary ratio of DEX/DOR.

        Valid for >= 4 hr; for small times different cutoffs are necessary.

        Classification based on urinary metabolic ratios (Gaedigk2013) with cutoffs as
        [0.0003|0.03|0.3].

        - PM: x => 0.3 (poor)
        - IM: 0.03 <= x < 0.3 (intermediate)
        - NM|EM: 0.0003 <= x < 0.03 (normal)
        - UM: x < 0.0003 (ultrarapid)
        """
        if ratio >= 0.3:
            return MetabolicPhenotype.PM
        if 0.03 <= ratio < 0.3:
            return MetabolicPhenotype.IM
        if 0.0003 <= ratio < 0.03:
            return MetabolicPhenotype.EM
        if ratio < 0.0003:
            return MetabolicPhenotype.UM
        raise ValueError(f"No metabolic phenotype for urinary ratio {ratio}")


class GenotypeStyle:
    """Colors of the curves of genotypes by their activity score."""

    colormap = sns.color_palette("Spectral", as_cmap=True)
    max_activity_score = 3

    def __init__(self, activities: np.ndarray) -> None:
        """Style for activity scores from 0 to the largest of `activities`."""
        self.activities = activities

    def color(self, activity_score: float) -> str:
        """Get the color of an activity score."""
        color_value = activity_score / self.activities.max()
        return to_hex(self.colormap(color_value))


if __name__ == "__main__":
    # the activity scores of the alleles for the CYP2D6 model
    with ALLELE_ACTIVITIES_PATH.open("w") as f_json:
        json.dump(allele_scores, f_json, indent=2)
