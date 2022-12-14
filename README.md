[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6976102.svg)](https://doi.org/10.5281/zenodo.6976102)

# Dextromethorphan model
This repository provides the dextromethorphan physiologically based pharmacokinetics (PBPK) model described in

> Grzegorzewski J, Brandhorst J, König M. Physiologically based pharmacokinetic (PBPK) modeling of the role of CYP2D6 polymorphism for metabolic phenotyping with dextromethorphan. Front Pharmacol. 2022 Oct 24;13:1029073. doi: https://doi.org/10.3389/fphar.2022.1029073. PMID: 36353484; PMCID: PMC9637881.

The model is distributed as [SBML](http://sbml.org) available from [`dextromethorphan_body_flat.xml`](./models/dextromethorphan_body_flat.xml) with 
corresponding SBML4humans model report at [https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/dextromethorphan-model/main/models/dextromethorphan_body_flat.xml](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/dextromethorphan-model/main/models/dextromethorphan_body_flat.xml)

### Comp submodels
The CYP2D6 submodel is available from [`cyp2d6.xml`](./models/cyp2d6.xml) with corresponding SBML4humans report at
[https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/dextromethorphan-model/main/models/cyp2d6.xml](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/dextromethorphan-model/main/models/cyp2d6.xml)

The liver submodel is available from [`dextromethorphan_liver.xml`](./models/dextromethorphan_liver.xml) with corresponding SBML4humans report at
[https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/dextromethorphan-model/main/models/dextromethorphan_liver.xml](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/dextromethorphan-model/main/models/dextromethorphan_liver.xml)

The kidney submodel is available from [`dextromethorphan_kidney.xml`](./models/dextromethorphan_kidney.xml) with corresponding SBML4humans report at
[https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/dextromethorphan-model/main/models/dextromethorphan_kidney.xml](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/dextromethorphan-model/main/models/dextromethorphan_kidney.xml)

The intestine submodel is available from [`dextromethorphan_intestine.xml`](./models/dextromethorphan_intestine.xml) with corresponding SBML4humans report at
[https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/dextromethorphan-model/main/models/dextromethorphan_intestine.xml](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/dextromethorphan-model/main/models/dextromethorphan_intestine.xml)

The whole-body submodel is available from [`dextromethorphan_body.xml`](./models/dextromethorphan_body.xml) with corresponding SBML4humans report at
[https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/dextromethorphan-model/main/models/dextromethorphan_body.xml](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/dextromethorphan-model/main/models/dextromethorphan_body.xml)

## How to cite
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7025683.svg)](https://doi.org/10.5281/zenodo.7025683)

> Grzegorzewski, Jan, & König, Matthias. (2022). 
> *Physiologically based pharmacokinetic (PBPK) model of dextromethorphan (v0.9.5).*   
> Zenodo. [https://doi.org/10.5281/zenodo.7025683](https://doi.org/10.5281/zenodo.7025683)

## License

* Source Code: [LGPLv3](http://opensource.org/licenses/LGPL-3.0)
* Documentation: [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/)

The dextromethorphan-model source is released under both the GPL and LGPL licenses version 2 or
later. You may choose which license you choose to use the software under.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License or the GNU Lesser General Public
License as published by the Free Software Foundation, either version 2 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

Funding
=======
Jan Grzegorzewski and Matthias König were supported by the Federal Ministry of Education and Research (BMBF, Germany)
within the research network Systems Medicine of the Liver (LiSyM, grant number 031L0054)
and by the German Research Foundation (DFG) within the Research Unit Programme FOR 5151
[QuaLiPerF](https://qualiperf.de) (Quantifying Liver Perfusion-Function Relationship in Complex Resection -
A Systems Medicine Approach) by grant number 436883643.

© 2021-2022 Jan Grzegorzewski & Matthias König, [Systems Medicine of the Liver](https://livermetabolism.com)
