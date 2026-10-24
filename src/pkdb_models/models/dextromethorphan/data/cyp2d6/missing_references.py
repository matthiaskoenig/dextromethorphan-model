"""Print the references of the CYP2D6 phenotyping which are missing in PK-DB.

`missing_references.csv` lists the PubMed ids of the references (`new`) and of
the studies in PK-DB (`old`).
"""

from pathlib import Path

import pandas as pd


def read_missing_references_tsv(output_path: Path) -> None:
    """Print the PubMed ids which are references but not yet studies."""
    references = pd.read_csv(output_path, sep="\t")
    new_pmids = set(references["new"])
    old_pmids = set(references["old"])
    s = new_pmids.difference(old_pmids)
    print(s)
    print(len(s))


if __name__ == "__main__":
    output_path = Path(__file__).parent / "missing_references.csv"
    read_missing_references_tsv(output_path=output_path)
