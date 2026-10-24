"""Base class of the dextromethorphan simulation experiments."""

from collections.abc import Iterable
from typing import ClassVar, NamedTuple

import numpy as np
import pandas as pd
from pkpdsim.experiment import PKPDSimulationExperiment
from pkpdsim.impairment import RENAL_COLORS_END_STAGE, RENAL_FUNCTION_GFR
from sbmlsim import Q
from sbmlsim.units import Quantity

from pkdb_models.models.dextromethorphan import MODEL
from pkdb_models.models.dextromethorphan.dextromethorphan_pk import (
    calculate_dextromethorphan_pk,
)


class MolecularWeights(NamedTuple):
    """Molecular weights for the conversion of the data and the doses."""

    dxm: Quantity
    dxo: Quantity
    dxoglu: Quantity
    mm: Quantity
    dxmhbr: Quantity


def jitter(values: pd.Series, sd: float) -> pd.Series:
    """Values with a normal jitter of standard deviation `sd` (for plotting).

    The jitter is the same in every run (seeded), so the datasets are reproducible.
    """
    rng = np.random.default_rng(seed=1234)
    return values + rng.normal(0.0, sd, size=len(values))


class DexSimulationExperiment(PKPDSimulationExperiment):
    """Base class of the dextromethorphan simulation experiments.

    The observables of the model, their labels and units, the molecular
    weights for the conversion of the data and of the doses, and the maps of
    the CYP2D6 phenotype, of the interactions and of the renal function.
    """

    pkpd_model = MODEL
    selections = (
        "time",
        # dosing
        "PODOSE_dxm",
        "IVDOSE_dxm",
        "Ri_dxm",
        "Ka_dis_dxm",
        "BW",
        # venous plasma
        "[Cve_dxm]",
        "[Cve_dxo]",
        "[Cve_dxo_glu]",
        "[Cve_mm]",
        "dxo_total",
        # other compartments (first pass, arterial blood)
        "[Car_dxm]",
        "[Chv_dxm]",
        "[Cli_plasma_dxm]",
        "[Cli_dxm]",
        "[Cgulumen_dxm]",
        # metabolic ratios
        "dxm_dxo",
        "dxm_dxo_total",
        "dxm_dxo_urine",
        "dxm_dxo_total_urine",
        # urine and feces
        "Aurine_dxm",
        "Aurine_dxo",
        "Aurine_dxo_glu",
        "Aurine_dxo_total",
        "Aurine_mm",
        "Afeces_dxm",
        # the CYP2D6 genotype and the metabolism
        "LI__cyp2d6_allele1",
        "LI__cyp2d6_allele2",
        "LI__cyp2d6_ac",
        "LI__cyp2d6_activity",
        "LI__DXMCYP2D6",
        "LI__DXMCYPX",
        "LI__DXMNDM",
        "LI__DXONDM",
        "LI__DXOUGT",
        # cases: the interactions and the renal function
        "LI__f_cyp2d6",
        "LI__f_cyp3a4",
        "LI__f_ugt2b15",
        "KI__f_renal_function",
        "KI__GFR",
        # distribution and absorption
        "Kp_dxm",
        "Kp_dxo",
        "Kp_dxo_glu",
        "Kp_mm",
        "ftissue_dxm",
        "GU__F_dxm_abs",
    )

    # labels
    label_time = "time"
    label_dxm = "dextromethorphan (DXM)\n"
    label_dxo = "dextrorphan (DXO)\n"
    label_dxoglu = "dextrorphan glucuronide (DXOGLU)\n"
    label_dxo_total = "dextrorphan total (DXO + DXOGLU)\n"
    label_mm = "N-demethylated morphinans (3MM + 3HM)\n"

    label_dxm_ur = "dextromethorphan (DXM) urine\n"
    label_dxo_ur = "dextrorphan (DXO) urine\n"
    label_dxoglu_ur = "dextrorphan glucuronide (DXOGLU) urine\n"
    label_dxo_total_ur = "dextrorphan total (DXO+DXOGLU) urine\n"
    label_mm_ur = "N-demethylated morphinans (3MM + 3HM) urine\n"

    label_mr_urine = "DXM/DXO urine\n"
    label_mr_plasma = "DXM/DXO plasma\n"
    label_mr_serum = "DXM/DXO serum\n"

    label_mrtot_urine = "DXM/(DXO+DXOGLU) urine\n"
    label_mrtot_plasma = "DXM/(DXO+DXOGLU) plasma\n"
    label_mrtot_serum = "DXM/(DXO+DXOGLU) serum\n"

    label_cyp2d6_activity = "CYP2D6 activity\n"

    # units
    unit_time = "hr"
    unit_dxm = "µM"
    unit_dxo = "µM"
    unit_mm = "µM"
    unit_dxm_ur = "µmole"
    unit_dxo_ur = "µmole"
    unit_dxo_total_ur = "µmole"
    unit_mm_ur = "µmole"

    unit_dimless = "dimensionless"

    # ----------- CYP2D6 interactions --------------
    #: the activity of CYP2D6 (`LI__f_cyp2d6`) under an inhibitor, the factor
    #: of the model which an experiment of an interaction sets; the CYP2D6
    #: activity of the diplotype (`LI__cyp2d6_activity`) is multiplied by it.
    #: The factors are documented values of the study which measures the
    #: interaction, they are never fitted
    #: quinidine is a strong inhibitor: a single 50 mg dose of the sulfate 1 hr
    #: before raises the AUC of dextromethorphan of extensive metabolizers 42
    #: fold (383 against 9 µg*h/l, Capon1996), and 100 mg the evening before
    #: lowers their clearance to 516 ml/min, close to the 275 ml/min of poor
    #: metabolizers (Schadel1995); both give about 2 % of the activity of
    #: CYP2D6. The factor is constant over a simulation, the waning of the
    #: inhibition of a single dose of quinidine is not described (TODO.md)
    cyp2d6_inhibition: ClassVar[dict[str, float]] = {
        "quinidine": 0.02,
    }
    #: the activity of CYP3A4 (`LI__f_cyp3a4`) and of UGT2B15
    #: (`LI__f_ugt2b15`) under a coadministered drug, documented factors,
    #: never fitted
    cyp3a4_inhibition: ClassVar[dict[str, float]] = {}
    ugt2b15_inhibition: ClassVar[dict[str, float]] = {}

    # ----------- Renal map --------------
    #: a measured creatinine clearance of X ml/min is the renal function X/101
    renal_map = RENAL_FUNCTION_GFR
    renal_colors = RENAL_COLORS_END_STAGE

    #: molecular weights of dextromethorphan, its metabolites and of the salt;
    #: the lumped N-demethylated morphinans are measured as dextrorphan
    #: equivalents. The hydrobromide of the products is the monohydrate
    #: (370.3 g/mole), which the publications confirm: 30 mg of the salt are
    #: 22 mg of the base (Schadel1995, Barnhart1980) and 81.0 µmole
    #: (Nagai1996)
    Mr: ClassVar[MolecularWeights] = MolecularWeights(
        dxm=Q(271.404, "g/mole"),
        dxo=Q(257.37066, "g/mole"),
        dxoglu=Q(433.49478, "g/mole"),
        mm=Q(257.37066, "g/mole"),
        dxmhbr=Q(370.3, "g/mole"),
    )

    def f_dxmhbr_to_dxm(self) -> Quantity:
        """Get the factor which converts a dose of dextromethorphan hydrobromide.

        dose_dxm = f * dose_dxmhbr, the monohydrate of the hydrobromide
        (0.733, i.e. 30 mg of the salt are 22 mg of the base).
        """
        return self.Mr.dxm / self.Mr.dxmhbr

    def f_dxo_free_to_dxo_conjugated(self) -> Quantity:
        """Get the factor which converts free dextrorphan to dextrorphan with conjugates.

        dxo + dxo_conj = f * dxo, the mean 1/(1 - 0.957) of Nagai1996 Tab2.
        """
        return Q(1 / (1 - 0.957), "dimensionless")

    # --- Pharmacokinetic parameters ---
    def calculate_dextromethorphan_pk(
        self,
        scans: Iterable[str] | None = None,
        substances: Iterable[str] | None = None,
    ) -> dict[str, pd.DataFrame]:
        """Calculate the pharmacokinetic parameters of the scans.

        Args:
            scans: keys of the simulations, all simulations by default.
            substances: the analytes (`dextromethorphan_pk.ANALYTES`), all by
                default.

        Returns:
            The parameters of every scan by simulation key, per draw of the
            fitted parameters in a run over them (`uncertainty`).
        """
        keys = self._simulations if scans is None else scans
        across = None if self.uncertainty is None else self.uncertainty.id
        return {
            key: calculate_dextromethorphan_pk(
                experiment=self,
                res=self.results[f"task_{key}"],
                across=across,
                substances=substances,
            )
            for key in keys
        }
