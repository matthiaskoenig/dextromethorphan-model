# Dextromethorphan

Physiologically based pharmacokinetic (PBPK) model of dextromethorphan and its metabolites: the oral and intravenous administration of dextromethorphan, its distribution in the tissues, the hepatic O-demethylation to dextrorphan by CYP2D6 (with the activity score of the CYP2D6 diplotype) and by the CYP2D6-independent pathway (CYP3A4, CYP2C9), the N-demethylation of dextromethorphan and of dextrorphan to the lumped N-demethylated morphinans (3-methoxymorphinan and 3-hydroxymorphinan, which the studies report together), the glucuronidation of dextrorphan (UGT2B15) and the renal excretion of dextromethorphan and its metabolites relative to the glomerular filtration rate. The model describes the CYP2D6 phenotype over the activity score of the diplotype (poor, intermediate, extensive and ultrarapid metabolizers), the urinary and plasma metabolic ratios which phenotype the subjects, the inhibition of CYP2D6 (quinidine, paroxetine, terbinafine, cinacalcet and others) and of CYP3A4 (tipranavir/ritonavir, isavuconazole) by documented factors of the activities of the enzymes, and the renal function.

The repository of the published model is [dextromethorphan-model](https://github.com/matthiaskoenig/dextromethorphan-model), the model is described in [Grzegorzewski et al. (2022)](https://doi.org/10.3389/fphar.2022.1029073).

## Structure

- `__init__.py`: the paths of the model, of the CYP2D6 allele activities and its model object `MODEL` with its release metadata and its adopted fit, which the commands below run (pkpdsim).
- `models/`: the CYP2D6 activity model (`model_cyp2d6.py`, merged into the liver), the tissue models (`model_intestine.py`, `model_liver.py`, `model_kidney.py`) and the whole-body model (`model_body.py`). `models/factory.py` creates the SBML models, the flattened whole-body model which is simulated, the ODEs and the COMBINE archive in `models/output/`; the fitted values come from the adopted fit (`models/fits.py`, `models/output/fits/`).
- `experiments/`: the simulation experiments of the clinical studies (`studies/`, 37 publications), the parameter scans of the dose, the dissolution, the absorption, the CYP2D6 activity score and the activities of CYP2D6 and CYP3A4 (`scans/`) and the simulations of the manuscript (`manuscript/`). The fit mappings are described with the vocabulary of `pkpdsim.metadata`, extended by the CYP2D6 diplotype, the genetic and the metabolic phenotype and the activity score (`fitting/mapping_collections.py`).
- `fitting/`: the fit problem of the pharmacokinetics (`PK`), its parameters and the selection of the training, the named validation (interactions, doses, populations, limitations) and the outlier data.
- `sensitivity/`: the sensitivity analysis of the pharmacokinetics of dextromethorphan and dextrorphan and of the urinary metabolic ratio.
- `dextromethorphan_pk.py`: the pharmacokinetic parameters of the scans, the non-compartmental analysis of `pkpdutils`.
- `tolerances.py`: the absolute tolerances of the integrator per state.
- `simulations.py`: the simulation experiments and their groups, `MODEL` runs them.
- `data/`: the data of the studies, a subset of the PK-DB studies (`data/collect_data.py`), and the CYP2D6 allele activities of PharmGKB (`data/cyp2d6/`).
- `TODO.md`: the open issues of the model.

## Commands

```bash
# models, simulations
run_simulation pkdb_models.models.dextromethorphan --action factory
run_simulation pkdb_models.models.dextromethorphan --action list_experiments
run_simulation pkdb_models.models.dextromethorphan --action simulate --experiments all
run_simulation pkdb_models.models.dextromethorphan --action simulate --experiments all --uncertainty

# fits, adoption of a fit, reports of stored parameters, identifiability
run_fit pkdb_models.models.dextromethorphan --subset=PK --runs=3 --cores=3 --method=DE
run_fit pkdb_models.models.dextromethorphan --adopt PK_<fit id>
run_report pkdb_models.models.dextromethorphan --subset=PK results/fit/PK_<fit id>/parameters.json
run_identifiability pkdb_models.models.dextromethorphan --subset=PK results/fit/PK_<fit id>/parameters.json

# sensitivity analysis (local by default)
python -m pkdb_models.models.dextromethorphan.sensitivity.sensitivity_analysis
```

The results are written into `results/` of the model.

## Adopted fits and uncertainty

The values of the fitted parameters come from the adopted fit of the model
(`PK_20261020_094137__4239e`), not from numbers in the code.
`run_fit pkdb_models.models.dextromethorphan --adopt <fit id>` copies the record
of a finished fit (its parameters, problem, profile likelihood and Fisher
information) into `models/output/fits/<fit id>/`, which is tracked; the ids of
the adopted fits are listed in `fits` of the model object (`__init__.py`). The
factory takes the fitted values and their uncertainty from the records
(`models/fits.py`) and writes the uncertainty into the SBML
(`distrib:uncertainty`). `run_simulation ... --uncertainty` runs the experiments
over draws of these distributions and draws the simulations as the median with
a band of quantiles into `results/simulation_uncertainty`. A refit is: fit,
adopt, replace the id in `fits`, rebuild the model.
