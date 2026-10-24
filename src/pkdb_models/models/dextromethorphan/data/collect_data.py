"""Collect the data of the dextromethorphan studies from the PK-DB study folders.

The studies are copied from a `pkdb_data` checkout (`PKDB_DATA`, else
`../pkdb_data`, see `pkpdsim.data.studies_dir`) into the data folder of the
model, see `pkpdsim.data.collect_tsv_files`.
Besides the dextromethorphan studies, four cocktail studies of caffeine have
dextromethorphan groups: Armani2017, Doroshyenko2013, Oh2012 and Yamazaki2016.
Schadel1995 reads the doses of its interventions from its `study.json`, which is
copied as well.
"""

import shutil
from pathlib import Path

from pkpdsim.data import collect_tsv_files
from pkpdsim.data import studies_dir as pkdb_studies_dir

from pkdb_models.models.dextromethorphan import (
    DATA_PATH_CAFFEINE,
    DATA_PATH_DEXTROMETHORPHAN,
)

#: the studies of other substances which the dextromethorphan experiments use
CAFFEINE_STUDIES = {"Armani2017", "Doroshyenko2013", "Oh2012", "Yamazaki2016"}

#: the studies whose experiments read the `study.json`
STUDY_JSON_STUDIES = {"Schadel1995"}


def collect_data(studies_dir: Path | None = None) -> None:
    """Copy the data of the dextromethorphan studies into the data folder of the model.

    Args:
        studies_dir: the `studies` folder of pkdb_data, by default the one of
            the checkout `pkpdsim.data.studies_dir` finds.
    """
    if studies_dir is None:
        studies_dir = pkdb_studies_dir()
    DATA_PATH_DEXTROMETHORPHAN.parent.mkdir(exist_ok=True)
    collect_tsv_files(
        source_dir=studies_dir / "dextromethorphan",
        target_dir=DATA_PATH_DEXTROMETHORPHAN,
    )
    collect_tsv_files(
        source_dir=studies_dir / "caffeine",
        target_dir=DATA_PATH_CAFFEINE,
        filter_study=lambda study: study in CAFFEINE_STUDIES,
    )
    for study in sorted(STUDY_JSON_STUDIES):
        shutil.copy2(
            studies_dir / "dextromethorphan" / study / "study.json",
            DATA_PATH_DEXTROMETHORPHAN / study / "study.json",
        )


if __name__ == "__main__":
    collect_data()
