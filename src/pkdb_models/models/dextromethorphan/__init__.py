"""Dextromethorphan: PBPK model of dextromethorphan and its CYP2D6 metabolism.

The paths of the model and of the CYP2D6 genotype information, and its model
object `MODEL`, which the commands `run_simulation`, `run_fit`, `run_report`
and `run_identifiability` of pkpdsim run by its package
`pkdb_models.models.dextromethorphan`.
"""

from pathlib import Path

from pkpdsim.model import FigureSettings, PKPDModel, SimulatorSettings
from pkpdsim.release.settings import Author, ReleaseSettings

from pkdb_models.models.dextromethorphan.tolerances import ABSOLUTE_TOLERANCE

DEXTROMETHORPHAN_PATH = Path(__file__).parent

MODEL_BASE_PATH = DEXTROMETHORPHAN_PATH / "models" / "output" / "models"
MODEL_PATH = MODEL_BASE_PATH / "dextromethorphan_body_flat.xml"

# the subset of the PK-DB studies the model uses, see `data/collect_data.py`
DATA_PATH_BASE = DEXTROMETHORPHAN_PATH / "data"
DATA_PATH_DEXTROMETHORPHAN = DATA_PATH_BASE / "dextromethorphan"
DATA_PATH_CAFFEINE = DATA_PATH_BASE / "caffeine"
DATA_PATHS = [
    DATA_PATH_DEXTROMETHORPHAN,
    DATA_PATH_CAFFEINE,
]

# genotype/phenotype information
ALLELE_ACTIVITIES_PATH = (
    DEXTROMETHORPHAN_PATH / "data" / "cyp2d6" / "allele_activities.json"
)

MODEL = PKPDModel(
    name="dextromethorphan",
    package=__name__,
    title="Dextromethorphan PBPK model",
    path=DEXTROMETHORPHAN_PATH,
    model_path=MODEL_PATH,
    data_paths=tuple(DATA_PATHS),
    archive_path=MODEL_BASE_PATH.parent / "dextromethorphan_model.omex",
    factory=".models.factory:create_dextromethorphan_models",
    experiments=".simulations:EXPERIMENTS",
    fit_definitions=".fitting.fitting:FIT_DEFINITIONS",
    # the adopted fits, whose values the factory takes (`models/fits.py`)
    fits=("PK_20261020_094137__4239e",),
    simulator=SimulatorSettings(
        absolute_tolerance=ABSOLUTE_TOLERANCE, relative_tolerance=1e-10
    ),
    figures=FigureSettings(
        formats=("svg",),
        fig_dpi=150,
        legend_position="outside",
        axes_labelsize=13,
        xtick_labelsize=11,
        ytick_labelsize=11,
    ),
    fit_identifiability=True,
    release=ReleaseSettings(
        title=(
            "Physiologically based pharmacokinetic (PBPK) model of dextromethorphan"
        ),
        repository="matthiaskoenig/dextromethorphan-model",
        doi="10.5281/zenodo.6976102",
        authors=(
            Author(
                "Grzegorzewski, Jan",
                "0000-0002-4588-4925",
                "Humboldt-Universität zu Berlin, Institute for Theoretical Biology, Berlin",
            ),
            Author(
                "Brandhorst, Janosch",
                affiliation="Humboldt-Universität zu Berlin, Institute for Theoretical Biology, Berlin",
            ),
            Author(
                "König, Matthias",
                "0000-0003-1725-179X",
                (
                    "Humboldt-Universität zu Berlin, Faculty of Life Sciences, Department of Biology, Institute of Theoretical Biology, Systems Medicine of the Liver; University of Stuttgart, Institute of Structural Mechanics and Dynamics in Aerospace Engineering; University of Southern Denmark, Clinical Pharmacology, Pharmacy and Environmental Medicine, Department of Public Health; University Hospital Schleswig-Holstein, Campus Lübeck, First Department of Medicine, Lübeck, Germany"
                ),
            ),
        ),
        keywords=(
            "model",
            "dextromethorphan",
            "dextrorphan",
            "CYP2D6",
            "pharmacogenetics",
            "metabolic phenotyping",
            "pharmacokinetics",
            "PBPK",
            "physiologically based pharmacokinetic model",
            "SBML",
        ),
        docker_image="matthiaskoenig/dextromethorphan",
        funding=(
            "Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B)."
        ),
        description=(
            "This repository provides the dextromethorphan physiologically"
            " based pharmacokinetic (PBPK) model: the oral and intravenous"
            " administration of dextromethorphan, its O-demethylation to"
            " dextrorphan by CYP2D6 (with the activity score of the CYP2D6"
            " diplotype) and by the CYP2D6-independent pathway, the"
            " N-demethylation of dextromethorphan and dextrorphan, the"
            " glucuronidation of dextrorphan, the distribution in the tissues"
            " and the renal excretion of dextromethorphan and its metabolites."
        ),
        first_year=2021,
    ),
)
"""The dextromethorphan model: its commands, see `pkpdsim.model`."""
