# dextromethorphan model
This repository provides the dextromethorphan physiologically based pharmacokinetic (PBPK) model:
the oral and intravenous administration of dextromethorphan, its O-demethylation to dextrorphan by
CYP2D6 (with the activity score of the CYP2D6 diplotype) and by the CYP2D6-independent pathway
(CYP3A4, CYP2C9), the N-demethylation of dextromethorphan and of dextrorphan to the lumped
N-demethylated morphinans (3-methoxymorphinan, 3-hydroxymorphinan), the glucuronidation of
dextrorphan (UGT2B15), the distribution in the tissues and the renal excretion of dextromethorphan
and its metabolites.
The CYP2D6 activity of a diplotype is the sum of the activity scores of its two alleles
(`LI__cyp2d6_activity`, the CYP2D6 submodel); an inhibitor of CYP2D6 or CYP3A4 is a factor of the
activity of the enzyme (`LI__f_cyp2d6`, `LI__f_cyp3a4`, `LI__f_ugt2b15`).
The parameters of the absorption, the metabolism, the distribution and the renal excretion are fitted
to the data of the clinical studies; the SBML carries the uncertainty of every fitted parameter
(`distrib:uncertainty`).

The model is distributed as [SBML](http://sbml.org) format available from [`dextromethorphan_body_flat.xml`](./models/dextromethorphan_body_flat.xml) with
corresponding [SBML4humans model report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fdextromethorphan-model%2Fmain%2Fmodels%2Fdextromethorphan_body_flat.xml) and [model equations](./models/dextromethorphan_body_flat.md).

The COMBINE archive is available from [`dextromethorphan_model.omex`](./dextromethorphan_model.omex).

### Comp submodels
* **CYP2D6** submodel [`cyp2d6.xml`](./models/cyp2d6.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fdextromethorphan-model%2Fmain%2Fmodels%2Fcyp2d6.xml) and [equations](./models/cyp2d6.md).
* **liver** submodel [`dextromethorphan_liver.xml`](./models/dextromethorphan_liver.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fdextromethorphan-model%2Fmain%2Fmodels%2Fdextromethorphan_liver.xml) and [equations](./models/dextromethorphan_liver.md).
* **kidney** submodel [`dextromethorphan_kidney.xml`](./models/dextromethorphan_kidney.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fdextromethorphan-model%2Fmain%2Fmodels%2Fdextromethorphan_kidney.xml) and [equations](./models/dextromethorphan_kidney.md).
* **intestine** submodel [`dextromethorphan_intestine.xml`](./models/dextromethorphan_intestine.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fdextromethorphan-model%2Fmain%2Fmodels%2Fdextromethorphan_intestine.xml) and [equations](./models/dextromethorphan_intestine.md).
* **whole-body** submodel [`dextromethorphan_body.xml`](./models/dextromethorphan_body.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fdextromethorphan-model%2Fmain%2Fmodels%2Fdextromethorphan_body.xml) and [equations](./models/dextromethorphan_body.md).

## How to cite

> Grzegorzewski, J., Brandhorst, J., König, M. (2026).
> *Physiologically based pharmacokinetic (PBPK) model of dextromethorphan.*
> [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6976102.svg)](https://doi.org/10.5281/zenodo.6976102)

> Grzegorzewski J, Brandhorst J, König M. Physiologically based pharmacokinetic (PBPK) modeling of
> the role of CYP2D6 polymorphism for metabolic phenotyping with dextromethorphan.
> Front Pharmacol. 2022 Oct 24;13:1029073. doi: https://doi.org/10.3389/fphar.2022.1029073

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.


## Run simulations
### python
Clone the repository
```bash
git clone https://github.com/matthiaskoenig/dextromethorphan-model.git
cd dextromethorphan-model
```

#### uv
Run the complete analysis with uv (https://docs.astral.sh/uv/getting-started/installation/):
```bash
uv run run_simulation pkdb_models.models.dextromethorphan -a all -r results
```

#### pip
If you use pip install the package via
```bash
pip install -e .
```
Run the complete analysis in the environment via:
```bash
run_simulation pkdb_models.models.dextromethorphan -a all -r results
```

### docker
Simulations can also be run within a docker container:

```bash
docker run -v "${PWD}/results:/results" -it matthiaskoenig/dextromethorphan:latest /bin/bash
```

Run the complete analysis:
```bash
uv run run_simulation pkdb_models.models.dextromethorphan -a all -r /results
```
The results are written into the mounted `/results` folder on the host.

In case of permission issues with the mounted folder, adjust ownership and access rights with:
```bash
sudo chown $(id -u):$(id -g) -R "${PWD}/results"
sudo chmod 775 "${PWD}/results"
```

## Funding
Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B).

© 2021-2026 Matthias König, [Systems Medicine of the Liver](https://livermetabolism.com)
