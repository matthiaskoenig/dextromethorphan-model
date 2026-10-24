# Dextromethorphan (DXM) body model

Model `dextromethorphan_body`, SBML Level 3 Version 2, read from dextromethorphan\_body\_flat.xml, written by sbmlode 0.3.0.

Whole-body model of dextromethorphan and its metabolites

The circulation of the plasma through the organs, the distribution into the tissues, the oral absorption (intestine submodel), the hepatic metabolism (liver submodel with the CYP2D6 activity of the diplotype) and the renal excretion (kidney submodel). Dextromethorphan is given orally (PODOSE\_dxm) or intravenously (bolus IVDOSE\_dxm, infusion Ri\_dxm).

The substances are dextromethorphan (dxm), dextrorphan (dxo), dextrorphan glucuronide (dxo\_glu) and the lumped N-demethylated morphinans (mm: 3-methoxymorphinan, 3-hydroxymorphinan and its glucuronide, which the studies report together). The concentrations of the blood compartments are plasma concentrations, the blood to plasma ratio is 1 for every substance; the venous plasma Cve\_&lt;sid&gt; is what the studies sample.

The content of this model has been carefully created in a manual research effort.

Terms of use

Copyright © 2026 Matthias König.

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

Redistribution and use of any part of this model, with or without modification, are permitted provided that the following conditions are met:

Redistributions of this SBML file must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in a different form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

This model is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

## Units

| Time | Substance | Extent | Volume | Area | Length |
| --- | --- | --- | --- | --- | --- |
| min | mmol | mmol | l | m<sup>2</sup> | m |

## Compartments

| Symbol | Id | Name | Size | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{Vki}$ | `Vki` | kidney |  | l |  |
| $\mathrm{Vli}$ | `Vli` | liver |  | l |  |
| $\mathrm{Vlu}$ | `Vlu` | lung |  | l |  |
| $\mathrm{Vgu}$ | `Vgu` | gut |  | l |  |
| $\mathrm{Vre}$ | `Vre` | rest |  | l |  |
| $\mathrm{Var}$ | `Var` | arterial blood |  | l |  |
| $\mathrm{Vve}$ | `Vve` | venous blood |  | l |  |
| $\mathrm{Vpo}$ | `Vpo` | portal vein |  | l |  |
| $\mathrm{Vhv}$ | `Vhv` | hepatic vein |  | l |  |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vstomach}$ | `Vstomach` | stomach | $1$ | l | ✓ |
| $\mathrm{Vgulumen}$ | `Vgulumen` | gut lumen |  | l |  |
| $\mathrm{Vki}_{\mathrm{tissue}}$ | `Vki_tissue` | ki tissue |  | l |  |
| $\mathrm{Vki}_{\mathrm{plasma}}$ | `Vki_plasma` | ki plasma |  | l |  |
| $\mathrm{Vli}_{\mathrm{tissue}}$ | `Vli_tissue` | li tissue |  | l |  |
| $\mathrm{Vli}_{\mathrm{plasma}}$ | `Vli_plasma` | li plasma |  | l |  |
| $\mathrm{Vlu}_{\mathrm{tissue}}$ | `Vlu_tissue` | lu tissue |  | l |  |
| $\mathrm{Vlu}_{\mathrm{plasma}}$ | `Vlu_plasma` | lu plasma |  | l |  |
| $\mathrm{Vgu}_{\mathrm{tissue}}$ | `Vgu_tissue` | gu tissue |  | l |  |
| $\mathrm{Vgu}_{\mathrm{plasma}}$ | `Vgu_plasma` | gu plasma |  | l |  |
| $\mathrm{Vre}_{\mathrm{tissue}}$ | `Vre_tissue` | re tissue |  | l |  |
| $\mathrm{Vre}_{\mathrm{plasma}}$ | `Vre_plasma` | re plasma |  | l |  |
| $\mathrm{LI}_{\mathrm{\_Vmem}}$ | `LI__Vmem` | plasma membrane | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vapical}}$ | `GU__Vapical` | apical membrane (intestinal membrane enterocytes) | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{Cki}_{\mathrm{plasma\_dxm}}$ | `Cki_plasma_dxm` | dextromethorphan (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_dxm}}$ | `Cli_plasma_dxm` | dextromethorphan (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_dxm}}$ | `Clu_plasma_dxm` | dextromethorphan (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_dxm}}$ | `Cgu_plasma_dxm` | dextromethorphan (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_dxm}}$ | `Cre_plasma_dxm` | dextromethorphan (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{dxm}}$ | `Car_dxm` | dextromethorphan (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{dxm}}$ | `Cve_dxm` | dextromethorphan (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{dxm}}$ | `Cpo_dxm` | dextromethorphan (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{dxm}}$ | `Chv_dxm` | dextromethorphan (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{dxm}}$ | `Cki_dxm` | dextromethorphan (kidney) | $\mathrm{Vki}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{dxm}}$ | `Cli_dxm` | dextromethorphan (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{dxm}}$ | `Clu_dxm` | dextromethorphan (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{dxm}}$ | `Cgu_dxm` | dextromethorphan (gut) | $\mathrm{Vgu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{dxm}}$ | `Cre_dxm` | dextromethorphan (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{dxm}}$ | `Aurine_dxm` | dextromethorphan (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Cki}_{\mathrm{plasma\_dxo}}$ | `Cki_plasma_dxo` | dextrorphan (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_dxo}}$ | `Cli_plasma_dxo` | dextrorphan (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_dxo}}$ | `Clu_plasma_dxo` | dextrorphan (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_dxo}}$ | `Cgu_plasma_dxo` | dextrorphan (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_dxo}}$ | `Cre_plasma_dxo` | dextrorphan (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{dxo}}$ | `Car_dxo` | dextrorphan (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{dxo}}$ | `Cve_dxo` | dextrorphan (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{dxo}}$ | `Cpo_dxo` | dextrorphan (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{dxo}}$ | `Chv_dxo` | dextrorphan (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{dxo}}$ | `Cki_dxo` | dextrorphan (kidney) | $\mathrm{Vki}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{dxo}}$ | `Cli_dxo` | dextrorphan (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{dxo}}$ | `Clu_dxo` | dextrorphan (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{dxo}}$ | `Cgu_dxo` | dextrorphan (gut) | $\mathrm{Vgu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{dxo}}$ | `Cre_dxo` | dextrorphan (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{dxo}}$ | `Aurine_dxo` | dextrorphan (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Cki}_{\mathrm{plasma\_dxo\_glu}}$ | `Cki_plasma_dxo_glu` | dextrorphan glucuronide (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_dxo\_glu}}$ | `Cli_plasma_dxo_glu` | dextrorphan glucuronide (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_dxo\_glu}}$ | `Clu_plasma_dxo_glu` | dextrorphan glucuronide (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_dxo\_glu}}$ | `Cgu_plasma_dxo_glu` | dextrorphan glucuronide (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_dxo\_glu}}$ | `Cre_plasma_dxo_glu` | dextrorphan glucuronide (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{dxo\_glu}}$ | `Car_dxo_glu` | dextrorphan glucuronide (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{dxo\_glu}}$ | `Cve_dxo_glu` | dextrorphan glucuronide (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{dxo\_glu}}$ | `Cpo_dxo_glu` | dextrorphan glucuronide (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{dxo\_glu}}$ | `Chv_dxo_glu` | dextrorphan glucuronide (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{dxo\_glu}}$ | `Cki_dxo_glu` | dextrorphan glucuronide (kidney) | $\mathrm{Vki}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{dxo\_glu}}$ | `Cli_dxo_glu` | dextrorphan glucuronide (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{dxo\_glu}}$ | `Clu_dxo_glu` | dextrorphan glucuronide (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{dxo\_glu}}$ | `Cgu_dxo_glu` | dextrorphan glucuronide (gut) | $\mathrm{Vgu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{dxo\_glu}}$ | `Cre_dxo_glu` | dextrorphan glucuronide (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{dxo\_glu}}$ | `Aurine_dxo_glu` | dextrorphan glucuronide (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Cki}_{\mathrm{plasma\_mm}}$ | `Cki_plasma_mm` | N-demethylated morphinans (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_mm}}$ | `Cli_plasma_mm` | N-demethylated morphinans (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_mm}}$ | `Clu_plasma_mm` | N-demethylated morphinans (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_mm}}$ | `Cgu_plasma_mm` | N-demethylated morphinans (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_mm}}$ | `Cre_plasma_mm` | N-demethylated morphinans (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{mm}}$ | `Car_mm` | N-demethylated morphinans (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{mm}}$ | `Cve_mm` | N-demethylated morphinans (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{mm}}$ | `Cpo_mm` | N-demethylated morphinans (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{mm}}$ | `Chv_mm` | N-demethylated morphinans (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{mm}}$ | `Cki_mm` | N-demethylated morphinans (kidney) | $\mathrm{Vki}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{mm}}$ | `Cli_mm` | N-demethylated morphinans (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{mm}}$ | `Clu_mm` | N-demethylated morphinans (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{mm}}$ | `Cgu_mm` | N-demethylated morphinans (gut) | $\mathrm{Vgu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{mm}}$ | `Cre_mm` | N-demethylated morphinans (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{mm}}$ | `Aurine_mm` | N-demethylated morphinans (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Cgulumen}_{\mathrm{dxm}}$ | `Cgulumen_dxm` | dextromethorphan (gut lumen) | $\mathrm{Vgulumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{Afeces}_{\mathrm{dxm}}$ | `Afeces_dxm` | dextromethorphan (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{GU}_{\mathrm{\_dxm\_stomach}}$ | `GU__dxm_stomach` | dextromethorphan (stomach) | $\mathrm{Vstomach}$ |  | mmol | amount, boundary |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $f_{\mathrm{lumen}}$ | `f_lumen` | fraction lumen of intestine | $0.9$ | \- | ✓ |
| $\mathrm{BW}$ | `BW` | body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{BW}_{\mathrm{ref}}$ | `BW_ref` | reference body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{COBW}$ | `COBW` | cardiac output per bodyweight \[ml/s/kg\] | $1.548$ | ml/s/kg | ✓ |
| $\mathrm{CO}$ | `CO` | cardiac output \[ml/s\] |  | ml/s |  |
| $\mathrm{QC}$ | `QC` | cardiac output \[l/min\] |  | l/min |  |
| $\mathrm{Fblood}$ | `Fblood` | blood fraction of organ volume | $0.02$ | \- | ✓ |
| $\mathrm{HCT}$ | `HCT` | hematocrit | $0.51$ | \- | ✓ |
| $\mathrm{FVgu}$ | `FVgu` | gut fractional tissue volume | $0.0171$ | l/kg | ✓ |
| $\mathrm{FVki}$ | `FVki` | kidney fractional tissue volume | $0.0044$ | l/kg | ✓ |
| $\mathrm{FVli}$ | `FVli` | liver fractional tissue volume | $0.021$ | l/kg | ✓ |
| $\mathrm{FVlu}$ | `FVlu` | lung fractional tissue volume | $0.0076$ | l/kg | ✓ |
| $\mathrm{FVre}$ | `FVre` | rest of body fractional tissue volume |  | l/kg |  |
| $\mathrm{FVve}$ | `FVve` | venous fractional tissue volume | $0.0514$ | l/kg | ✓ |
| $\mathrm{FVar}$ | `FVar` | arterial fractional tissue volume | $0.0257$ | l/kg | ✓ |
| $\mathrm{FVpo}$ | `FVpo` | portal fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FVhv}$ | `FVhv` | hepatic venous fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FQgu}$ | `FQgu` | gut fractional tissue blood flow | $0.18$ | \- | ✓ |
| $\mathrm{FQki}$ | `FQki` | kidney fractional tissue blood flow | $0.19$ | \- | ✓ |
| $\mathrm{FQh}$ | `FQh` | hepatic (venous side) fractional tissue blood flow | $0.215$ | \- | ✓ |
| $\mathrm{FQlu}$ | `FQlu` | lung fractional tissue blood flow | $1$ | \- | ✓ |
| $\mathrm{FQre}$ | `FQre` | rest of body fractional tissue blood flow |  | \- |  |
| $\mathrm{ftissue}_{\mathrm{fast}}$ | `ftissue_fast` | tissue distribution of the eliminating organs | $100$ | l/min | ✓ |
| $f_{\mathrm{GFR\_Qki}}$ | `f_GFR_Qki` | relationship GFR and Qki | $76.3105006271061$ | ml/l | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate (healthy) |  | ml/min |  |
| $\mathrm{Mr}_{\mathrm{dxm}}$ | `Mr_dxm` | Molecular weight dxm \[g/mole\] | $271.404$ | g/mol | ✓ |
| $\mathrm{ftissue}_{\mathrm{dxm}}$ | `ftissue_dxm` | tissue distribution dxm | $100$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{dxm}}$ | `Kp_dxm` | tissue/plasma partition coefficient dxm | $9.48805754878147$ | \- | ✓ |
| $\mathrm{IVDOSE}_{\mathrm{dxm}}$ | `IVDOSE_dxm` | IV bolus dose dxm \[mg\] | $0$ | mg |  |
| $\mathrm{ti}_{\mathrm{dxm}}$ | `ti_dxm` | injection time dxm \[s\] | $10$ | s | ✓ |
| $\mathrm{Ki}_{\mathrm{dxm}}$ | `Ki_dxm` | Ki \[1/min\] injection dxm |  | 1/min |  |
| $\mathrm{Ri}_{\mathrm{dxm}}$ | `Ri_dxm` | Ri \[mg/min\] rate of infusion dxm | $0$ | mg/min | ✓ |
| $\mathrm{cum}_{\mathrm{dose\_dxm}}$ | `cum_dose_dxm` | cumulative dose of the infusion dxm \[mg\] | $0$ | mg |  |
| $\mathrm{PODOSE}_{\mathrm{dxm}}$ | `PODOSE_dxm` | oral dose dxm \[mg\] | $0$ | mg |  |
| $\mathrm{Ka}_{\mathrm{dis\_dxm}}$ | `Ka_dis_dxm` | Ka\_dis \[1/hr\] dissolution dextromethorphan | $0.401682131288553$ | 1/hr | ✓ |
| $\mathrm{Mr}_{\mathrm{dxo}}$ | `Mr_dxo` | Molecular weight dxo \[g/mole\] | $257.37066$ | g/mol | ✓ |
| $\mathrm{ftissue}_{\mathrm{dxo}}$ | `ftissue_dxo` | tissue distribution dxo | $100$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{dxo}}$ | `Kp_dxo` | tissue/plasma partition coefficient dxo | $4$ | \- | ✓ |
| $\mathrm{Mr}_{\mathrm{dxo\_glu}}$ | `Mr_dxo_glu` | Molecular weight dxo\_glu \[g/mole\] | $433.49478$ | g/mol | ✓ |
| $\mathrm{ftissue}_{\mathrm{dxo\_glu}}$ | `ftissue_dxo_glu` | tissue distribution dxo\_glu | $3$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{dxo\_glu}}$ | `Kp_dxo_glu` | tissue/plasma partition coefficient dxo\_glu | $0.01$ | \- | ✓ |
| $\mathrm{Mr}_{\mathrm{mm}}$ | `Mr_mm` | Molecular weight mm \[g/mole\] | $257.37066$ | g/mol | ✓ |
| $\mathrm{ftissue}_{\mathrm{mm}}$ | `ftissue_mm` | tissue distribution mm | $10$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{mm}}$ | `Kp_mm` | tissue/plasma partition coefficient mm | $0.0932977851429064$ | \- | ✓ |
| $\mathrm{fu}_{\mathrm{dxm}}$ | `fu_dxm` | fraction unbound in plasma dxm | $0.5$ | \- | ✓ |
| $\mathrm{fu}_{\mathrm{dxo}}$ | `fu_dxo` | fraction unbound in plasma dxo | $0.55$ | \- | ✓ |
| $\mathrm{fu}_{\mathrm{dxo\_glu}}$ | `fu_dxo_glu` | fraction unbound in plasma dxo\_glu | $0.44$ | \- | ✓ |
| $\mathrm{fu}_{\mathrm{mm}}$ | `fu_mm` | fraction unbound in plasma mm | $0.5$ | \- | ✓ |
| $\mathrm{Qgu}$ | `Qgu` | gut blood flow |  | l/min |  |
| $\mathrm{Qki}$ | `Qki` | kidney blood flow |  | l/min |  |
| $\mathrm{Qh}$ | `Qh` | hepatic (venous side) blood flow |  | l/min |  |
| $\mathrm{Qha}$ | `Qha` | hepatic artery blood flow |  | l/min |  |
| $\mathrm{Qlu}$ | `Qlu` | lung blood flow |  | l/min |  |
| $\mathrm{Qre}$ | `Qre` | rest of body blood flow |  | l/min |  |
| $\mathrm{Qpo}$ | `Qpo` | portal blood flow |  | l/min |  |
| $\mathrm{Ave}_{\mathrm{dxm}}$ | `Ave_dxm` | dextromethorphan amount (venous blood) \[mmole\] |  | mmol |  |
| $\mathrm{Mve}_{\mathrm{dxm}}$ | `Mve_dxm` | dextromethorphan concentration (venous plasma) \[mg/l\] |  | mg/l |  |
| $\mathrm{Xurine}_{\mathrm{dxm}}$ | `Xurine_dxm` | dextromethorphan amount (urine) \[mg\] |  | mg |  |
| $\mathrm{Ave}_{\mathrm{dxo}}$ | `Ave_dxo` | dextrorphan amount (venous blood) \[mmole\] |  | mmol |  |
| $\mathrm{Mve}_{\mathrm{dxo}}$ | `Mve_dxo` | dextrorphan concentration (venous plasma) \[mg/l\] |  | mg/l |  |
| $\mathrm{Xurine}_{\mathrm{dxo}}$ | `Xurine_dxo` | dextrorphan amount (urine) \[mg\] |  | mg |  |
| $\mathrm{Ave}_{\mathrm{dxo\_glu}}$ | `Ave_dxo_glu` | dextrorphan glucuronide amount (venous blood) \[mmole\] |  | mmol |  |
| $\mathrm{Mve}_{\mathrm{dxo\_glu}}$ | `Mve_dxo_glu` | dextrorphan glucuronide concentration (venous plasma) \[mg/l\] |  | mg/l |  |
| $\mathrm{Xurine}_{\mathrm{dxo\_glu}}$ | `Xurine_dxo_glu` | dextrorphan glucuronide amount (urine) \[mg\] |  | mg |  |
| $\mathrm{Ave}_{\mathrm{mm}}$ | `Ave_mm` | N-demethylated morphinans amount (venous blood) \[mmole\] |  | mmol |  |
| $\mathrm{Mve}_{\mathrm{mm}}$ | `Mve_mm` | N-demethylated morphinans concentration (venous plasma) \[mg/l\] |  | mg/l |  |
| $\mathrm{Xurine}_{\mathrm{mm}}$ | `Xurine_mm` | N-demethylated morphinans amount (urine) \[mg\] |  | mg |  |
| $\mathrm{Xfeces}_{\mathrm{dxm}}$ | `Xfeces_dxm` | dextromethorphan amount (feces) \[mg\] |  | mg |  |
| $\mathrm{dxo}_{\mathrm{total}}$ | `dxo_total` | total dextrorphan (plasma) |  | mmol/l |  |
| $\mathrm{dxm}_{\mathrm{dxo}}$ | `dxm_dxo` | DXM/DXO ratio (plasma) |  | \- |  |
| $\mathrm{dxm}_{\mathrm{dxo\_total}}$ | `dxm_dxo_total` | DXM/total DXO ratio (plasma) |  | \- |  |
| $\mathrm{Aurine}_{\mathrm{dxo\_total}}$ | `Aurine_dxo_total` | cumulative urinary total dextrorphan |  | mmol |  |
| $\mathrm{dxm}_{\mathrm{dxo\_urine}}$ | `dxm_dxo_urine` | cumulative urinary DXM/DXO ratio |  | \- |  |
| $\mathrm{dxm}_{\mathrm{dxo\_total\_urine}}$ | `dxm_dxo_total_urine` | cumulative urinary DXM/total DXO ratio |  | \- |  |
| $\mathrm{KI}_{\mathrm{\_f\_renal\_function}}$ | `KI__f_renal_function` | renal function | $1$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_GFR}}$ | `KI__GFR` | glomerular filtration rate |  | ml/min |  |
| $\mathrm{KI}_{\mathrm{\_DXMEX\_f}}$ | `KI__DXMEX_f` | renal clearance of unbound dextromethorphan relative to the GFR | $0.656113552124429$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_DXOEX\_f}}$ | `KI__DXOEX_f` | renal clearance of unbound dextrorphan relative to the GFR | $1.86913741202018$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_DXOGLUEX\_f}}$ | `KI__DXOGLUEX_f` | renal clearance of unbound dextrorphan glucuronide relative to the GFR | $2.2657913496198$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_MMEX\_f}}$ | `KI__MMEX_f` | renal clearance of unbound N-demethylated morphinans relative to the GFR | $1.66127389767754$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a0}}$ | `LI__cyp2d6_a0` | \*1 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a1}}$ | `LI__cyp2d6_a1` | \*10 activity | $0.25$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a2}}$ | `LI__cyp2d6_a2` | \*100 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a3}}$ | `LI__cyp2d6_a3` | \*101 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a4}}$ | `LI__cyp2d6_a4` | \*10x2 activity | $0.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a5}}$ | `LI__cyp2d6_a5` | \*11 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a6}}$ | `LI__cyp2d6_a6` | \*114 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a7}}$ | `LI__cyp2d6_a7` | \*12 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a8}}$ | `LI__cyp2d6_a8` | \*120 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a9}}$ | `LI__cyp2d6_a9` | \*124 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a10}}$ | `LI__cyp2d6_a10` | \*129 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a11}}$ | `LI__cyp2d6_a11` | \*13 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a12}}$ | `LI__cyp2d6_a12` | \*14 activity | $0.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a13}}$ | `LI__cyp2d6_a13` | \*15 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a14}}$ | `LI__cyp2d6_a14` | \*17 activity | $0.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a15}}$ | `LI__cyp2d6_a15` | \*17x2 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a16}}$ | `LI__cyp2d6_a16` | \*18 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a17}}$ | `LI__cyp2d6_a17` | \*19 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a18}}$ | `LI__cyp2d6_a18` | \*1x2 activity | $2$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a19}}$ | `LI__cyp2d6_a19` | \*1x3 activity | $3$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a20}}$ | `LI__cyp2d6_a20` | \*1x4 activity | $4$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a21}}$ | `LI__cyp2d6_a21` | \*1x5 activity | $5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a22}}$ | `LI__cyp2d6_a22` | \*1x6 activity | $6$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a23}}$ | `LI__cyp2d6_a23` | \*2 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a24}}$ | `LI__cyp2d6_a24` | \*20 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a25}}$ | `LI__cyp2d6_a25` | \*21 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a26}}$ | `LI__cyp2d6_a26` | \*27 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a27}}$ | `LI__cyp2d6_a27` | \*29 activity | $0.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a28}}$ | `LI__cyp2d6_a28` | \*29x2 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a29}}$ | `LI__cyp2d6_a29` | \*2x2 activity | $2$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a30}}$ | `LI__cyp2d6_a30` | \*2x3 activity | $3$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a31}}$ | `LI__cyp2d6_a31` | \*2x4 activity | $4$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a32}}$ | `LI__cyp2d6_a32` | \*2x5 activity | $5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a33}}$ | `LI__cyp2d6_a33` | \*2x6 activity | $6$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a34}}$ | `LI__cyp2d6_a34` | \*3 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a35}}$ | `LI__cyp2d6_a35` | \*31 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a36}}$ | `LI__cyp2d6_a36` | \*33 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a37}}$ | `LI__cyp2d6_a37` | \*34 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a38}}$ | `LI__cyp2d6_a38` | \*35 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a39}}$ | `LI__cyp2d6_a39` | \*35x2 activity | $2$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a40}}$ | `LI__cyp2d6_a40` | \*36 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a41}}$ | `LI__cyp2d6_a41` | \*36x2 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a42}}$ | `LI__cyp2d6_a42` | \*38 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a43}}$ | `LI__cyp2d6_a43` | \*39 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a44}}$ | `LI__cyp2d6_a44` | \*3x2 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a45}}$ | `LI__cyp2d6_a45` | \*4 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a46}}$ | `LI__cyp2d6_a46` | \*40 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a47}}$ | `LI__cyp2d6_a47` | \*41 activity | $0.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a48}}$ | `LI__cyp2d6_a48` | \*41x2 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a49}}$ | `LI__cyp2d6_a49` | \*41x3 activity | $1.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a50}}$ | `LI__cyp2d6_a50` | \*42 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a51}}$ | `LI__cyp2d6_a51` | \*44 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a52}}$ | `LI__cyp2d6_a52` | \*45 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a53}}$ | `LI__cyp2d6_a53` | \*45x2 activity | $2$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a54}}$ | `LI__cyp2d6_a54` | \*46 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a55}}$ | `LI__cyp2d6_a55` | \*47 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a56}}$ | `LI__cyp2d6_a56` | \*48 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a57}}$ | `LI__cyp2d6_a57` | \*49 activity | $0.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a58}}$ | `LI__cyp2d6_a58` | \*4x2 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a59}}$ | `LI__cyp2d6_a59` | \*4x3 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a60}}$ | `LI__cyp2d6_a60` | \*4x4 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a61}}$ | `LI__cyp2d6_a61` | \*4x5 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a62}}$ | `LI__cyp2d6_a62` | \*5 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a63}}$ | `LI__cyp2d6_a63` | \*50 activity | $0.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a64}}$ | `LI__cyp2d6_a64` | \*51 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a65}}$ | `LI__cyp2d6_a65` | \*53 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a66}}$ | `LI__cyp2d6_a66` | \*54 activity | $0.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a67}}$ | `LI__cyp2d6_a67` | \*55 activity | $0.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a68}}$ | `LI__cyp2d6_a68` | \*56 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a69}}$ | `LI__cyp2d6_a69` | \*57 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a70}}$ | `LI__cyp2d6_a70` | \*59 activity | $0.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a71}}$ | `LI__cyp2d6_a71` | \*6 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a72}}$ | `LI__cyp2d6_a72` | \*60 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a73}}$ | `LI__cyp2d6_a73` | \*62 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a74}}$ | `LI__cyp2d6_a74` | \*68 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a75}}$ | `LI__cyp2d6_a75` | \*69 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a76}}$ | `LI__cyp2d6_a76` | \*6x2 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a77}}$ | `LI__cyp2d6_a77` | \*7 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a78}}$ | `LI__cyp2d6_a78` | \*8 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a79}}$ | `LI__cyp2d6_a79` | \*81 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a80}}$ | `LI__cyp2d6_a80` | \*9 activity | $0.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a81}}$ | `LI__cyp2d6_a81` | \*92 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a82}}$ | `LI__cyp2d6_a82` | \*96 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a83}}$ | `LI__cyp2d6_a83` | \*99 activity | $0$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_a84}}$ | `LI__cyp2d6_a84` | \*9x2 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_ac}}$ | `LI__cyp2d6_ac` | custom allele activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}}$ | `LI__cyp2d6_allele1` | allele 1 | $0$ | \- |  |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}}$ | `LI__cyp2d6_allele2` | allele 2 | $0$ | \- |  |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_activity1}}$ | `LI__cyp2d6_activity1` | activity of allele 1 |  | \- |  |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_activity2}}$ | `LI__cyp2d6_activity2` | activity of allele 2 |  | \- |  |
| $\mathrm{LI}_{\mathrm{\_f\_cyp2d6}}$ | `LI__f_cyp2d6` | activity of CYP2D6 | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_cyp3a4}}$ | `LI__f_cyp3a4` | activity of CYP3A4 | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_ugt2b15}}$ | `LI__f_ugt2b15` | activity of UGT2B15 | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_activity\_ref}}$ | `LI__cyp2d6_activity_ref` | reference CYP2D6 activity score | $2$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_DXMCYP2D6\_Vmax}}$ | `LI__DXMCYP2D6_Vmax` | Vmax DXMCYP2D6 | $0.00590550755641818$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_DXMCYP2D6\_Km\_dxm}}$ | `LI__DXMCYP2D6_Km_dxm` | Km DXMCYP2D6 | $0.004$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_DXMCYPX\_Vmax}}$ | `LI__DXMCYPX_Vmax` | Vmax DXMCYPX | $0.000454889875045166$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_DXMCYPX\_Km\_dxm}}$ | `LI__DXMCYPX_Km_dxm` | Km DXMCYPX | $0.157$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_DXMNDM\_Vmax}}$ | `LI__DXMNDM_Vmax` | Vmax DXMNDM | $0.00117141808294257$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_DXMNDM\_Km\_dxm}}$ | `LI__DXMNDM_Km_dxm` | Km DXMNDM | $0.7$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_DXONDM\_Vmax}}$ | `LI__DXONDM_Vmax` | Vmax DXONDM | $0.322454464355667$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_DXONDM\_Km\_dxo}}$ | `LI__DXONDM_Km_dxo` | Km DXONDM | $0.72$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_DXOUGT\_Vmax}}$ | `LI__DXOUGT_Vmax` | Vmax DXOUGT | $0.636675714500387$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_DXOUGT\_Km\_dxo}}$ | `LI__DXOUGT_Km_dxo` | Km DXOUGT | $0.69$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2d6\_activity}}$ | `LI__cyp2d6_activity` | activity of CYP2D6 diplotype |  | \- |  |
| $\mathrm{GU}_{\mathrm{\_F\_dxm\_abs}}$ | `GU__F_dxm_abs` | fraction absorbed dextromethorphan | $0.523770919743564$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_DXMABS\_k}}$ | `GU__DXMABS_k` | rate of the absorption of dextromethorphan | $0.08$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_absorption\_dxm}}$ | `GU__absorption_dxm` | absorption dextromethorphan |  | mmol/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{Aurine}_{\mathrm{dxm}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{Aurine}_{\mathrm{dxo}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{Aurine}_{\mathrm{dxo\_glu}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{Aurine}_{\mathrm{mm}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{Afeces}_{\mathrm{dxm}} &= 0 \cdot \mathrm{Vfeces} \\[1ex]
\mathrm{GU}_{\mathrm{\_dxm\_stomach}} &= 0 \cdot \mathrm{Vstomach}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{FVre} &= 1 - \mathrm{FVgu} - \mathrm{FVki} - \mathrm{FVli} \\
&\quad {} - \mathrm{FVlu} - \mathrm{FVve} - \mathrm{FVar} \\[1ex]
\mathrm{FQre} &= 1 - \mathrm{FQki} - \mathrm{FQh} \\[1ex]
\mathrm{CO} &= \mathrm{BW} \cdot \mathrm{COBW} \\[1ex]
\mathrm{QC} &= \frac{\mathrm{CO}}{1000} \cdot 60 \\[1ex]
\mathrm{Vgu} &= \mathrm{BW} \cdot \mathrm{FVgu} \\[1ex]
\mathrm{Vgulumen} &= f_{\mathrm{lumen}} \cdot \mathrm{Vgu} \\[1ex]
\mathrm{Vki} &= \mathrm{BW} \cdot \mathrm{FVki} \\[1ex]
\mathrm{Vli} &= \mathrm{BW} \cdot \mathrm{FVli} \\[1ex]
\mathrm{Vlu} &= \mathrm{BW} \cdot \mathrm{FVlu} \\[1ex]
\mathrm{Vre} &= \mathrm{BW} \cdot \mathrm{FVre} \\[1ex]
\mathrm{Vve} &= \mathrm{BW} \cdot \mathrm{FVve} - \frac{\mathrm{FVve}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Var} &= \mathrm{BW} \cdot \mathrm{FVar} - \frac{\mathrm{FVar}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Vpo} &= \mathopen{}\left(1 - \mathrm{HCT}\right) \cdot \mathopen{}\left(\mathrm{BW} \cdot \mathrm{FVpo} - \frac{\mathrm{FVpo}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right)\right) \\[1ex]
\mathrm{Vhv} &= \mathopen{}\left(1 - \mathrm{HCT}\right) \cdot \mathopen{}\left(\mathrm{BW} \cdot \mathrm{FVhv} - \frac{\mathrm{FVhv}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right)\right) \\[1ex]
\mathrm{Qgu} &= \mathrm{QC} \cdot \mathrm{FQgu} \\[1ex]
\mathrm{Qki} &= \mathrm{QC} \cdot \mathrm{FQki} \\[1ex]
\mathrm{Qh} &= \mathrm{QC} \cdot \mathrm{FQh} \\[1ex]
\mathrm{Qha} &= \mathrm{Qh} - \mathrm{Qgu} \\[1ex]
\mathrm{Qlu} &= \mathrm{QC} \cdot \mathrm{FQlu} \\[1ex]
\mathrm{Qre} &= \mathrm{QC} \cdot \mathrm{FQre} \\[1ex]
\mathrm{Qpo} &= \mathrm{Qgu} \\[1ex]
\mathrm{GFR}_{\mathrm{base}} &= f_{\mathrm{GFR\_Qki}} \cdot \mathrm{Qki} \\[1ex]
\mathrm{Vki}_{\mathrm{plasma}} &= \mathrm{Vki} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vki}_{\mathrm{tissue}} &= \mathrm{Vki} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{plasma}} &= \mathrm{Vli} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{tissue}} &= \mathrm{Vli} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{plasma}} &= \mathrm{Vlu} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{tissue}} &= \mathrm{Vlu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vgu}_{\mathrm{plasma}} &= \mathrm{Vgu} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vgu}_{\mathrm{tissue}} &= \mathrm{Vgu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{plasma}} &= \mathrm{Vre} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{tissue}} &= \mathrm{Vre} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Ki}_{\mathrm{dxm}} &= \frac{0.693}{\mathrm{ti}_{\mathrm{dxm}}} \cdot 60 \\[1ex]
\mathrm{Ave}_{\mathrm{dxm}} &= \mathrm{Cve}_{\mathrm{dxm}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Mve}_{\mathrm{dxm}} &= \mathrm{Cve}_{\mathrm{dxm}} \cdot \mathrm{Mr}_{\mathrm{dxm}} \\[1ex]
\mathrm{Xurine}_{\mathrm{dxm}} &= \mathrm{Aurine}_{\mathrm{dxm}} \cdot \mathrm{Mr}_{\mathrm{dxm}} \\[1ex]
\mathrm{Ave}_{\mathrm{dxo}} &= \mathrm{Cve}_{\mathrm{dxo}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Mve}_{\mathrm{dxo}} &= \mathrm{Cve}_{\mathrm{dxo}} \cdot \mathrm{Mr}_{\mathrm{dxo}} \\[1ex]
\mathrm{Xurine}_{\mathrm{dxo}} &= \mathrm{Aurine}_{\mathrm{dxo}} \cdot \mathrm{Mr}_{\mathrm{dxo}} \\[1ex]
\mathrm{Ave}_{\mathrm{dxo\_glu}} &= \mathrm{Cve}_{\mathrm{dxo\_glu}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Mve}_{\mathrm{dxo\_glu}} &= \mathrm{Cve}_{\mathrm{dxo\_glu}} \cdot \mathrm{Mr}_{\mathrm{dxo\_glu}} \\[1ex]
\mathrm{Xurine}_{\mathrm{dxo\_glu}} &= \mathrm{Aurine}_{\mathrm{dxo\_glu}} \cdot \mathrm{Mr}_{\mathrm{dxo\_glu}} \\[1ex]
\mathrm{Ave}_{\mathrm{mm}} &= \mathrm{Cve}_{\mathrm{mm}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Mve}_{\mathrm{mm}} &= \mathrm{Cve}_{\mathrm{mm}} \cdot \mathrm{Mr}_{\mathrm{mm}} \\[1ex]
\mathrm{Xurine}_{\mathrm{mm}} &= \mathrm{Aurine}_{\mathrm{mm}} \cdot \mathrm{Mr}_{\mathrm{mm}} \\[1ex]
\mathrm{Xfeces}_{\mathrm{dxm}} &= \mathrm{Afeces}_{\mathrm{dxm}} \cdot \mathrm{Mr}_{\mathrm{dxm}} \\[1ex]
\mathrm{dxo}_{\mathrm{total}} &= \mathrm{Cve}_{\mathrm{dxo}} + \mathrm{Cve}_{\mathrm{dxo\_glu}} \\[1ex]
\mathrm{dxm}_{\mathrm{dxo}} &= \frac{\mathrm{Cve}_{\mathrm{dxm}}}{\mathrm{Cve}_{\mathrm{dxo}}} \\[1ex]
\mathrm{dxm}_{\mathrm{dxo\_total}} &= \frac{\mathrm{Cve}_{\mathrm{dxm}}}{\mathrm{Cve}_{\mathrm{dxo}} + \mathrm{Cve}_{\mathrm{dxo\_glu}}} \\[1ex]
\mathrm{Aurine}_{\mathrm{dxo\_total}} &= \mathrm{Aurine}_{\mathrm{dxo}} + \mathrm{Aurine}_{\mathrm{dxo\_glu}} \\[1ex]
\mathrm{dxm}_{\mathrm{dxo\_urine}} &= \frac{\mathrm{Aurine}_{\mathrm{dxm}}}{\mathrm{Aurine}_{\mathrm{dxo}}} \\[1ex]
\mathrm{dxm}_{\mathrm{dxo\_total\_urine}} &= \frac{\mathrm{Aurine}_{\mathrm{dxm}}}{\mathrm{Aurine}_{\mathrm{dxo}} + \mathrm{Aurine}_{\mathrm{dxo\_glu}}} \\[1ex]
\mathrm{KI}_{\mathrm{\_GFR}} &= \mathrm{KI}_{\mathrm{\_f\_renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}} \\[1ex]
\mathrm{LI}_{\mathrm{\_cyp2d6\_activity1}} &= \begin{cases} \frac{\mathrm{LI}_{\mathrm{\_cyp2d6\_ac}}}{2} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = -1 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a0}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 0 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a1}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 1 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a2}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 2 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a3}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 3 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a4}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 4 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a5}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 5 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a6}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 6 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a7}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 7 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a8}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 8 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a9}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 9 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a10}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 10 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a11}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 11 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a12}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 12 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a13}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 13 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a14}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 14 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a15}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 15 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a16}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 16 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a17}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 17 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a18}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 18 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a19}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 19 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a20}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 20 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a21}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 21 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a22}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 22 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a23}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 23 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a24}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 24 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a25}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 25 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a26}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 26 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a27}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 27 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a28}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 28 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a29}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 29 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a30}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 30 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a31}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 31 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a32}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 32 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a33}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 33 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a34}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 34 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a35}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 35 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a36}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 36 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a37}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 37 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a38}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 38 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a39}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 39 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a40}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 40 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a41}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 41 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a42}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 42 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a43}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 43 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a44}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 44 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a45}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 45 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a46}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 46 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a47}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 47 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a48}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 48 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a49}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 49 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a50}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 50 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a51}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 51 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a52}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 52 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a53}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 53 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a54}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 54 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a55}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 55 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a56}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 56 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a57}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 57 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a58}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 58 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a59}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 59 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a60}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 60 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a61}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 61 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a62}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 62 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a63}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 63 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a64}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 64 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a65}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 65 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a66}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 66 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a67}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 67 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a68}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 68 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a69}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 69 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a70}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 70 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a71}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 71 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a72}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 72 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a73}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 73 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a74}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 74 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a75}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 75 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a76}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 76 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a77}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 77 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a78}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 78 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a79}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 79 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a80}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 80 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a81}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 81 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a82}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 82 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a83}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 83 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a84}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele1}} = 84 \\ \frac{\mathrm{LI}_{\mathrm{\_cyp2d6\_ac}}}{2} & \text{otherwise} \end{cases} \\[1ex]
\mathrm{LI}_{\mathrm{\_cyp2d6\_activity2}} &= \begin{cases} \frac{\mathrm{LI}_{\mathrm{\_cyp2d6\_ac}}}{2} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = -1 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a0}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 0 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a1}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 1 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a2}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 2 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a3}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 3 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a4}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 4 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a5}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 5 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a6}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 6 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a7}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 7 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a8}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 8 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a9}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 9 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a10}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 10 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a11}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 11 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a12}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 12 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a13}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 13 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a14}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 14 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a15}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 15 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a16}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 16 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a17}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 17 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a18}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 18 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a19}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 19 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a20}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 20 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a21}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 21 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a22}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 22 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a23}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 23 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a24}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 24 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a25}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 25 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a26}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 26 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a27}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 27 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a28}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 28 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a29}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 29 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a30}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 30 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a31}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 31 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a32}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 32 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a33}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 33 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a34}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 34 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a35}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 35 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a36}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 36 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a37}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 37 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a38}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 38 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a39}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 39 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a40}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 40 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a41}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 41 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a42}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 42 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a43}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 43 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a44}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 44 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a45}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 45 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a46}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 46 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a47}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 47 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a48}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 48 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a49}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 49 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a50}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 50 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a51}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 51 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a52}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 52 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a53}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 53 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a54}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 54 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a55}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 55 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a56}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 56 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a57}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 57 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a58}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 58 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a59}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 59 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a60}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 60 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a61}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 61 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a62}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 62 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a63}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 63 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a64}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 64 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a65}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 65 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a66}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 66 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a67}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 67 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a68}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 68 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a69}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 69 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a70}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 70 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a71}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 71 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a72}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 72 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a73}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 73 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a74}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 74 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a75}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 75 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a76}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 76 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a77}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 77 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a78}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 78 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a79}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 79 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a80}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 80 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a81}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 81 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a82}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 82 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a83}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 83 \\ \mathrm{LI}_{\mathrm{\_cyp2d6\_a84}} & \text{if } \mathrm{LI}_{\mathrm{\_cyp2d6\_allele2}} = 84 \\ \frac{\mathrm{LI}_{\mathrm{\_cyp2d6\_ac}}}{2} & \text{otherwise} \end{cases} \\[1ex]
\mathrm{LI}_{\mathrm{\_cyp2d6\_activity}} &= \mathrm{LI}_{\mathrm{\_cyp2d6\_activity1}} + \mathrm{LI}_{\mathrm{\_cyp2d6\_activity2}} \\[1ex]
\mathrm{GU}_{\mathrm{\_absorption\_dxm}} &= \mathrm{GU}_{\mathrm{\_DXMABS\_k}} \cdot \mathrm{Vgu} \cdot \mathrm{Cgulumen}_{\mathrm{dxm}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{transport\_ki\_dxm}}$ | `transport_ki_dxm` | transport dextromethorphan | $\mathrm{Cki}_{\mathrm{plasma\_dxm}} \rightleftharpoons \mathrm{Cki}_{\mathrm{dxm}}$ |
| $v_{\mathrm{transport\_li\_dxm}}$ | `transport_li_dxm` | transport dextromethorphan | $\mathrm{Cli}_{\mathrm{plasma\_dxm}} \rightleftharpoons \mathrm{Cli}_{\mathrm{dxm}}$ |
| $v_{\mathrm{transport\_lu\_dxm}}$ | `transport_lu_dxm` | transport dextromethorphan | $\mathrm{Clu}_{\mathrm{plasma\_dxm}} \rightleftharpoons \mathrm{Clu}_{\mathrm{dxm}}$ |
| $v_{\mathrm{transport\_gu\_dxm}}$ | `transport_gu_dxm` | transport dextromethorphan | $\mathrm{Cgu}_{\mathrm{plasma\_dxm}} \rightleftharpoons \mathrm{Cgu}_{\mathrm{dxm}}$ |
| $v_{\mathrm{transport\_re\_dxm}}$ | `transport_re_dxm` | transport dextromethorphan | $\mathrm{Cre}_{\mathrm{plasma\_dxm}} \rightleftharpoons \mathrm{Cre}_{\mathrm{dxm}}$ |
| $v_{\mathrm{iv\_dxm}}$ | `iv_dxm` | iv dextromethorphan | $\varnothing \longrightarrow \mathrm{Cve}_{\mathrm{dxm}}$ |
| $v_{\mathrm{Flow\_ve\_lu\_dxm}}$ | `Flow_ve_lu_dxm` | inflow lung dextromethorphan | $\mathrm{Cve}_{\mathrm{dxm}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_dxm}}$ |
| $v_{\mathrm{Flow\_lu\_ar\_dxm}}$ | `Flow_lu_ar_dxm` | outflow lung dextromethorphan | $\mathrm{Clu}_{\mathrm{plasma\_dxm}} \longrightarrow \mathrm{Car}_{\mathrm{dxm}}$ |
| $v_{\mathrm{Flow\_ar\_ki\_dxm}}$ | `Flow_ar_ki_dxm` | inflow kidney dextromethorphan | $\mathrm{Car}_{\mathrm{dxm}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_dxm}}$ |
| $v_{\mathrm{Flow\_ki\_ve\_dxm}}$ | `Flow_ki_ve_dxm` | outflow kidney dextromethorphan | $\mathrm{Cki}_{\mathrm{plasma\_dxm}} \longrightarrow \mathrm{Cve}_{\mathrm{dxm}}$ |
| $v_{\mathrm{Flow\_ar\_re\_dxm}}$ | `Flow_ar_re_dxm` | inflow rest dextromethorphan | $\mathrm{Car}_{\mathrm{dxm}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_dxm}}$ |
| $v_{\mathrm{Flow\_re\_ve\_dxm}}$ | `Flow_re_ve_dxm` | outflow rest dextromethorphan | $\mathrm{Cre}_{\mathrm{plasma\_dxm}} \longrightarrow \mathrm{Cve}_{\mathrm{dxm}}$ |
| $v_{\mathrm{Flow\_ar\_gu\_dxm}}$ | `Flow_ar_gu_dxm` | inflow gut dextromethorphan | $\mathrm{Car}_{\mathrm{dxm}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_dxm}}$ |
| $v_{\mathrm{Flow\_gu\_po\_dxm}}$ | `Flow_gu_po_dxm` | outflow gut dextromethorphan | $\mathrm{Cgu}_{\mathrm{plasma\_dxm}} \longrightarrow \mathrm{Cpo}_{\mathrm{dxm}}$ |
| $v_{\mathrm{Flow\_ar\_li\_dxm}}$ | `Flow_ar_li_dxm` | arterial inflow liver dextromethorphan | $\mathrm{Car}_{\mathrm{dxm}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_dxm}}$ |
| $v_{\mathrm{Flow\_po\_li\_dxm}}$ | `Flow_po_li_dxm` | outflow po dextromethorphan | $\mathrm{Cpo}_{\mathrm{dxm}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_dxm}}$ |
| $v_{\mathrm{Flow\_li\_hv\_dxm}}$ | `Flow_li_hv_dxm` | outflow liver dextromethorphan | $\mathrm{Cli}_{\mathrm{plasma\_dxm}} \longrightarrow \mathrm{Chv}_{\mathrm{dxm}}$ |
| $v_{\mathrm{Flow\_hv\_ve\_dxm}}$ | `Flow_hv_ve_dxm` | outflow hepatic vein dextromethorphan | $\mathrm{Chv}_{\mathrm{dxm}} \longrightarrow \mathrm{Cve}_{\mathrm{dxm}}$ |
| $v_{\mathrm{transport\_ki\_dxo}}$ | `transport_ki_dxo` | transport dextrorphan | $\mathrm{Cki}_{\mathrm{plasma\_dxo}} \rightleftharpoons \mathrm{Cki}_{\mathrm{dxo}}$ |
| $v_{\mathrm{transport\_li\_dxo}}$ | `transport_li_dxo` | transport dextrorphan | $\mathrm{Cli}_{\mathrm{plasma\_dxo}} \rightleftharpoons \mathrm{Cli}_{\mathrm{dxo}}$ |
| $v_{\mathrm{transport\_lu\_dxo}}$ | `transport_lu_dxo` | transport dextrorphan | $\mathrm{Clu}_{\mathrm{plasma\_dxo}} \rightleftharpoons \mathrm{Clu}_{\mathrm{dxo}}$ |
| $v_{\mathrm{transport\_gu\_dxo}}$ | `transport_gu_dxo` | transport dextrorphan | $\mathrm{Cgu}_{\mathrm{plasma\_dxo}} \rightleftharpoons \mathrm{Cgu}_{\mathrm{dxo}}$ |
| $v_{\mathrm{transport\_re\_dxo}}$ | `transport_re_dxo` | transport dextrorphan | $\mathrm{Cre}_{\mathrm{plasma\_dxo}} \rightleftharpoons \mathrm{Cre}_{\mathrm{dxo}}$ |
| $v_{\mathrm{Flow\_ve\_lu\_dxo}}$ | `Flow_ve_lu_dxo` | inflow lung dextrorphan | $\mathrm{Cve}_{\mathrm{dxo}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_dxo}}$ |
| $v_{\mathrm{Flow\_lu\_ar\_dxo}}$ | `Flow_lu_ar_dxo` | outflow lung dextrorphan | $\mathrm{Clu}_{\mathrm{plasma\_dxo}} \longrightarrow \mathrm{Car}_{\mathrm{dxo}}$ |
| $v_{\mathrm{Flow\_ar\_ki\_dxo}}$ | `Flow_ar_ki_dxo` | inflow kidney dextrorphan | $\mathrm{Car}_{\mathrm{dxo}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_dxo}}$ |
| $v_{\mathrm{Flow\_ki\_ve\_dxo}}$ | `Flow_ki_ve_dxo` | outflow kidney dextrorphan | $\mathrm{Cki}_{\mathrm{plasma\_dxo}} \longrightarrow \mathrm{Cve}_{\mathrm{dxo}}$ |
| $v_{\mathrm{Flow\_ar\_re\_dxo}}$ | `Flow_ar_re_dxo` | inflow rest dextrorphan | $\mathrm{Car}_{\mathrm{dxo}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_dxo}}$ |
| $v_{\mathrm{Flow\_re\_ve\_dxo}}$ | `Flow_re_ve_dxo` | outflow rest dextrorphan | $\mathrm{Cre}_{\mathrm{plasma\_dxo}} \longrightarrow \mathrm{Cve}_{\mathrm{dxo}}$ |
| $v_{\mathrm{Flow\_ar\_gu\_dxo}}$ | `Flow_ar_gu_dxo` | inflow gut dextrorphan | $\mathrm{Car}_{\mathrm{dxo}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_dxo}}$ |
| $v_{\mathrm{Flow\_gu\_po\_dxo}}$ | `Flow_gu_po_dxo` | outflow gut dextrorphan | $\mathrm{Cgu}_{\mathrm{plasma\_dxo}} \longrightarrow \mathrm{Cpo}_{\mathrm{dxo}}$ |
| $v_{\mathrm{Flow\_ar\_li\_dxo}}$ | `Flow_ar_li_dxo` | arterial inflow liver dextrorphan | $\mathrm{Car}_{\mathrm{dxo}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_dxo}}$ |
| $v_{\mathrm{Flow\_po\_li\_dxo}}$ | `Flow_po_li_dxo` | outflow po dextrorphan | $\mathrm{Cpo}_{\mathrm{dxo}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_dxo}}$ |
| $v_{\mathrm{Flow\_li\_hv\_dxo}}$ | `Flow_li_hv_dxo` | outflow liver dextrorphan | $\mathrm{Cli}_{\mathrm{plasma\_dxo}} \longrightarrow \mathrm{Chv}_{\mathrm{dxo}}$ |
| $v_{\mathrm{Flow\_hv\_ve\_dxo}}$ | `Flow_hv_ve_dxo` | outflow hepatic vein dextrorphan | $\mathrm{Chv}_{\mathrm{dxo}} \longrightarrow \mathrm{Cve}_{\mathrm{dxo}}$ |
| $v_{\mathrm{transport\_ki\_dxo\_glu}}$ | `transport_ki_dxo_glu` | transport dextrorphan glucuronide | $\mathrm{Cki}_{\mathrm{plasma\_dxo\_glu}} \rightleftharpoons \mathrm{Cki}_{\mathrm{dxo\_glu}}$ |
| $v_{\mathrm{transport\_li\_dxo\_glu}}$ | `transport_li_dxo_glu` | transport dextrorphan glucuronide | $\mathrm{Cli}_{\mathrm{plasma\_dxo\_glu}} \rightleftharpoons \mathrm{Cli}_{\mathrm{dxo\_glu}}$ |
| $v_{\mathrm{transport\_lu\_dxo\_glu}}$ | `transport_lu_dxo_glu` | transport dextrorphan glucuronide | $\mathrm{Clu}_{\mathrm{plasma\_dxo\_glu}} \rightleftharpoons \mathrm{Clu}_{\mathrm{dxo\_glu}}$ |
| $v_{\mathrm{transport\_gu\_dxo\_glu}}$ | `transport_gu_dxo_glu` | transport dextrorphan glucuronide | $\mathrm{Cgu}_{\mathrm{plasma\_dxo\_glu}} \rightleftharpoons \mathrm{Cgu}_{\mathrm{dxo\_glu}}$ |
| $v_{\mathrm{transport\_re\_dxo\_glu}}$ | `transport_re_dxo_glu` | transport dextrorphan glucuronide | $\mathrm{Cre}_{\mathrm{plasma\_dxo\_glu}} \rightleftharpoons \mathrm{Cre}_{\mathrm{dxo\_glu}}$ |
| $v_{\mathrm{Flow\_ve\_lu\_dxo\_glu}}$ | `Flow_ve_lu_dxo_glu` | inflow lung dextrorphan glucuronide | $\mathrm{Cve}_{\mathrm{dxo\_glu}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_dxo\_glu}}$ |
| $v_{\mathrm{Flow\_lu\_ar\_dxo\_glu}}$ | `Flow_lu_ar_dxo_glu` | outflow lung dextrorphan glucuronide | $\mathrm{Clu}_{\mathrm{plasma\_dxo\_glu}} \longrightarrow \mathrm{Car}_{\mathrm{dxo\_glu}}$ |
| $v_{\mathrm{Flow\_ar\_ki\_dxo\_glu}}$ | `Flow_ar_ki_dxo_glu` | inflow kidney dextrorphan glucuronide | $\mathrm{Car}_{\mathrm{dxo\_glu}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_dxo\_glu}}$ |
| $v_{\mathrm{Flow\_ki\_ve\_dxo\_glu}}$ | `Flow_ki_ve_dxo_glu` | outflow kidney dextrorphan glucuronide | $\mathrm{Cki}_{\mathrm{plasma\_dxo\_glu}} \longrightarrow \mathrm{Cve}_{\mathrm{dxo\_glu}}$ |
| $v_{\mathrm{Flow\_ar\_re\_dxo\_glu}}$ | `Flow_ar_re_dxo_glu` | inflow rest dextrorphan glucuronide | $\mathrm{Car}_{\mathrm{dxo\_glu}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_dxo\_glu}}$ |
| $v_{\mathrm{Flow\_re\_ve\_dxo\_glu}}$ | `Flow_re_ve_dxo_glu` | outflow rest dextrorphan glucuronide | $\mathrm{Cre}_{\mathrm{plasma\_dxo\_glu}} \longrightarrow \mathrm{Cve}_{\mathrm{dxo\_glu}}$ |
| $v_{\mathrm{Flow\_ar\_gu\_dxo\_glu}}$ | `Flow_ar_gu_dxo_glu` | inflow gut dextrorphan glucuronide | $\mathrm{Car}_{\mathrm{dxo\_glu}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_dxo\_glu}}$ |
| $v_{\mathrm{Flow\_gu\_po\_dxo\_glu}}$ | `Flow_gu_po_dxo_glu` | outflow gut dextrorphan glucuronide | $\mathrm{Cgu}_{\mathrm{plasma\_dxo\_glu}} \longrightarrow \mathrm{Cpo}_{\mathrm{dxo\_glu}}$ |
| $v_{\mathrm{Flow\_ar\_li\_dxo\_glu}}$ | `Flow_ar_li_dxo_glu` | arterial inflow liver dextrorphan glucuronide | $\mathrm{Car}_{\mathrm{dxo\_glu}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_dxo\_glu}}$ |
| $v_{\mathrm{Flow\_po\_li\_dxo\_glu}}$ | `Flow_po_li_dxo_glu` | outflow po dextrorphan glucuronide | $\mathrm{Cpo}_{\mathrm{dxo\_glu}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_dxo\_glu}}$ |
| $v_{\mathrm{Flow\_li\_hv\_dxo\_glu}}$ | `Flow_li_hv_dxo_glu` | outflow liver dextrorphan glucuronide | $\mathrm{Cli}_{\mathrm{plasma\_dxo\_glu}} \longrightarrow \mathrm{Chv}_{\mathrm{dxo\_glu}}$ |
| $v_{\mathrm{Flow\_hv\_ve\_dxo\_glu}}$ | `Flow_hv_ve_dxo_glu` | outflow hepatic vein dextrorphan glucuronide | $\mathrm{Chv}_{\mathrm{dxo\_glu}} \longrightarrow \mathrm{Cve}_{\mathrm{dxo\_glu}}$ |
| $v_{\mathrm{transport\_ki\_mm}}$ | `transport_ki_mm` | transport N-demethylated morphinans | $\mathrm{Cki}_{\mathrm{plasma\_mm}} \rightleftharpoons \mathrm{Cki}_{\mathrm{mm}}$ |
| $v_{\mathrm{transport\_li\_mm}}$ | `transport_li_mm` | transport N-demethylated morphinans | $\mathrm{Cli}_{\mathrm{plasma\_mm}} \rightleftharpoons \mathrm{Cli}_{\mathrm{mm}}$ |
| $v_{\mathrm{transport\_lu\_mm}}$ | `transport_lu_mm` | transport N-demethylated morphinans | $\mathrm{Clu}_{\mathrm{plasma\_mm}} \rightleftharpoons \mathrm{Clu}_{\mathrm{mm}}$ |
| $v_{\mathrm{transport\_gu\_mm}}$ | `transport_gu_mm` | transport N-demethylated morphinans | $\mathrm{Cgu}_{\mathrm{plasma\_mm}} \rightleftharpoons \mathrm{Cgu}_{\mathrm{mm}}$ |
| $v_{\mathrm{transport\_re\_mm}}$ | `transport_re_mm` | transport N-demethylated morphinans | $\mathrm{Cre}_{\mathrm{plasma\_mm}} \rightleftharpoons \mathrm{Cre}_{\mathrm{mm}}$ |
| $v_{\mathrm{Flow\_ve\_lu\_mm}}$ | `Flow_ve_lu_mm` | inflow lung N-demethylated morphinans | $\mathrm{Cve}_{\mathrm{mm}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_mm}}$ |
| $v_{\mathrm{Flow\_lu\_ar\_mm}}$ | `Flow_lu_ar_mm` | outflow lung N-demethylated morphinans | $\mathrm{Clu}_{\mathrm{plasma\_mm}} \longrightarrow \mathrm{Car}_{\mathrm{mm}}$ |
| $v_{\mathrm{Flow\_ar\_ki\_mm}}$ | `Flow_ar_ki_mm` | inflow kidney N-demethylated morphinans | $\mathrm{Car}_{\mathrm{mm}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_mm}}$ |
| $v_{\mathrm{Flow\_ki\_ve\_mm}}$ | `Flow_ki_ve_mm` | outflow kidney N-demethylated morphinans | $\mathrm{Cki}_{\mathrm{plasma\_mm}} \longrightarrow \mathrm{Cve}_{\mathrm{mm}}$ |
| $v_{\mathrm{Flow\_ar\_re\_mm}}$ | `Flow_ar_re_mm` | inflow rest N-demethylated morphinans | $\mathrm{Car}_{\mathrm{mm}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_mm}}$ |
| $v_{\mathrm{Flow\_re\_ve\_mm}}$ | `Flow_re_ve_mm` | outflow rest N-demethylated morphinans | $\mathrm{Cre}_{\mathrm{plasma\_mm}} \longrightarrow \mathrm{Cve}_{\mathrm{mm}}$ |
| $v_{\mathrm{Flow\_ar\_gu\_mm}}$ | `Flow_ar_gu_mm` | inflow gut N-demethylated morphinans | $\mathrm{Car}_{\mathrm{mm}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_mm}}$ |
| $v_{\mathrm{Flow\_gu\_po\_mm}}$ | `Flow_gu_po_mm` | outflow gut N-demethylated morphinans | $\mathrm{Cgu}_{\mathrm{plasma\_mm}} \longrightarrow \mathrm{Cpo}_{\mathrm{mm}}$ |
| $v_{\mathrm{Flow\_ar\_li\_mm}}$ | `Flow_ar_li_mm` | arterial inflow liver N-demethylated morphinans | $\mathrm{Car}_{\mathrm{mm}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_mm}}$ |
| $v_{\mathrm{Flow\_po\_li\_mm}}$ | `Flow_po_li_mm` | outflow po N-demethylated morphinans | $\mathrm{Cpo}_{\mathrm{mm}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_mm}}$ |
| $v_{\mathrm{Flow\_li\_hv\_mm}}$ | `Flow_li_hv_mm` | outflow liver N-demethylated morphinans | $\mathrm{Cli}_{\mathrm{plasma\_mm}} \longrightarrow \mathrm{Chv}_{\mathrm{mm}}$ |
| $v_{\mathrm{Flow\_hv\_ve\_mm}}$ | `Flow_hv_ve_mm` | outflow hepatic vein N-demethylated morphinans | $\mathrm{Chv}_{\mathrm{mm}} \longrightarrow \mathrm{Cve}_{\mathrm{mm}}$ |
| $v_{\mathrm{KI\_\_DXMEX}}$ | `KI__DXMEX` | dextromethorphan renal excretion | $\mathrm{Cki}_{\mathrm{plasma\_dxm}} \longrightarrow \mathrm{Aurine}_{\mathrm{dxm}}$ |
| $v_{\mathrm{KI\_\_DXOEX}}$ | `KI__DXOEX` | dextrorphan renal excretion | $\mathrm{Cki}_{\mathrm{plasma\_dxo}} \longrightarrow \mathrm{Aurine}_{\mathrm{dxo}}$ |
| $v_{\mathrm{KI\_\_DXOGLUEX}}$ | `KI__DXOGLUEX` | dextrorphan glucuronide renal excretion | $\mathrm{Cki}_{\mathrm{plasma\_dxo\_glu}} \longrightarrow \mathrm{Aurine}_{\mathrm{dxo\_glu}}$ |
| $v_{\mathrm{KI\_\_MMEX}}$ | `KI__MMEX` | N-demethylated morphinans renal excretion | $\mathrm{Cki}_{\mathrm{plasma\_mm}} \longrightarrow \mathrm{Aurine}_{\mathrm{mm}}$ |
| $v_{\mathrm{LI\_\_DXMCYP2D6}}$ | `LI__DXMCYP2D6` | dextromethorphan -&gt; dextrorphan (CYP2D6) | $\mathrm{Cli}_{\mathrm{dxm}} \longrightarrow \mathrm{Cli}_{\mathrm{dxo}}$ |
| $v_{\mathrm{LI\_\_DXMCYPX}}$ | `LI__DXMCYPX` | dextromethorphan -&gt; dextrorphan (CYP3A4) | $\mathrm{Cli}_{\mathrm{dxm}} \longrightarrow \mathrm{Cli}_{\mathrm{dxo}}$ |
| $v_{\mathrm{LI\_\_DXMNDM}}$ | `LI__DXMNDM` | dextromethorphan -&gt; N-demethylated morphinans (CYP3A4) | $\mathrm{Cli}_{\mathrm{dxm}} \longrightarrow \mathrm{Cli}_{\mathrm{mm}}$ |
| $v_{\mathrm{LI\_\_DXONDM}}$ | `LI__DXONDM` | dextrorphan -&gt; N-demethylated morphinans (CYP3A4) | $\mathrm{Cli}_{\mathrm{dxo}} \longrightarrow \mathrm{Cli}_{\mathrm{mm}}$ |
| $v_{\mathrm{LI\_\_DXOUGT}}$ | `LI__DXOUGT` | dextrorphan -&gt; dextrorphan glucuronide (UGT2B15) | $\mathrm{Cli}_{\mathrm{dxo}} \longrightarrow \mathrm{Cli}_{\mathrm{dxo\_glu}}$ |
| $v_{\mathrm{GU\_\_dissolution\_dxm}}$ | `GU__dissolution_dxm` | dissolution dextromethorphan | $\mathrm{GU}_{\mathrm{\_dxm\_stomach}} \longrightarrow \mathrm{Cgulumen}_{\mathrm{dxm}}$ |
| $v_{\mathrm{GU\_\_DXMABS}}$ | `GU__DXMABS` | absorption dextromethorphan | $\mathrm{Cgulumen}_{\mathrm{dxm}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_dxm}}$ |
| $v_{\mathrm{GU\_\_DXMEXC}}$ | `GU__DXMEXC` | excretion dextromethorphan (feces) | $\mathrm{Cgulumen}_{\mathrm{dxm}} \longrightarrow \mathrm{Afeces}_{\mathrm{dxm}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{transport\_ki\_dxm}} &= \frac{\mathrm{ftissue}_{\mathrm{fast}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cki}_{\mathrm{plasma\_dxm}} \cdot \mathrm{Kp}_{\mathrm{dxm}} - \mathrm{Cki}_{\mathrm{dxm}}\right) \\[1ex]
v_{\mathrm{transport\_li\_dxm}} &= \frac{\mathrm{ftissue}_{\mathrm{fast}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cli}_{\mathrm{plasma\_dxm}} \cdot \mathrm{Kp}_{\mathrm{dxm}} - \mathrm{Cli}_{\mathrm{dxm}}\right) \\[1ex]
v_{\mathrm{transport\_lu\_dxm}} &= \frac{\mathrm{ftissue}_{\mathrm{dxm}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_dxm}} \cdot \mathrm{Kp}_{\mathrm{dxm}} - \mathrm{Clu}_{\mathrm{dxm}}\right) \\[1ex]
v_{\mathrm{transport\_gu\_dxm}} &= \frac{\mathrm{ftissue}_{\mathrm{fast}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cgu}_{\mathrm{plasma\_dxm}} \cdot \mathrm{Kp}_{\mathrm{dxm}} - \mathrm{Cgu}_{\mathrm{dxm}}\right) \\[1ex]
v_{\mathrm{transport\_re\_dxm}} &= \frac{\mathrm{ftissue}_{\mathrm{dxm}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_dxm}} \cdot \mathrm{Kp}_{\mathrm{dxm}} - \mathrm{Cre}_{\mathrm{dxm}}\right) \\[1ex]
v_{\mathrm{iv\_dxm}} &= \frac{\mathrm{Ki}_{\mathrm{dxm}} \cdot \mathrm{IVDOSE}_{\mathrm{dxm}}}{\mathrm{Mr}_{\mathrm{dxm}}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_dxm}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{dxm}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_dxm}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_dxm}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_dxm}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{dxm}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_dxm}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_dxm}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_dxm}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{dxm}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_dxm}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_dxm}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_dxm}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{dxm}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_dxm}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_dxm}} \\[1ex]
v_{\mathrm{Flow\_ar\_li\_dxm}} &= \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{dxm}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_dxm}} &= \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{dxm}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_dxm}} &= \mathrm{Qh} \cdot \mathrm{Cli}_{\mathrm{plasma\_dxm}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_dxm}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{dxm}} \\[1ex]
v_{\mathrm{transport\_ki\_dxo}} &= \frac{\mathrm{ftissue}_{\mathrm{fast}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cki}_{\mathrm{plasma\_dxo}} \cdot \mathrm{Kp}_{\mathrm{dxo}} - \mathrm{Cki}_{\mathrm{dxo}}\right) \\[1ex]
v_{\mathrm{transport\_li\_dxo}} &= \frac{\mathrm{ftissue}_{\mathrm{fast}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cli}_{\mathrm{plasma\_dxo}} \cdot \mathrm{Kp}_{\mathrm{dxo}} - \mathrm{Cli}_{\mathrm{dxo}}\right) \\[1ex]
v_{\mathrm{transport\_lu\_dxo}} &= \frac{\mathrm{ftissue}_{\mathrm{dxo}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_dxo}} \cdot \mathrm{Kp}_{\mathrm{dxo}} - \mathrm{Clu}_{\mathrm{dxo}}\right) \\[1ex]
v_{\mathrm{transport\_gu\_dxo}} &= \frac{\mathrm{ftissue}_{\mathrm{fast}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cgu}_{\mathrm{plasma\_dxo}} \cdot \mathrm{Kp}_{\mathrm{dxo}} - \mathrm{Cgu}_{\mathrm{dxo}}\right) \\[1ex]
v_{\mathrm{transport\_re\_dxo}} &= \frac{\mathrm{ftissue}_{\mathrm{dxo}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_dxo}} \cdot \mathrm{Kp}_{\mathrm{dxo}} - \mathrm{Cre}_{\mathrm{dxo}}\right) \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_dxo}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{dxo}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_dxo}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_dxo}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_dxo}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{dxo}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_dxo}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_dxo}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_dxo}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{dxo}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_dxo}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_dxo}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_dxo}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{dxo}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_dxo}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_dxo}} \\[1ex]
v_{\mathrm{Flow\_ar\_li\_dxo}} &= \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{dxo}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_dxo}} &= \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{dxo}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_dxo}} &= \mathrm{Qh} \cdot \mathrm{Cli}_{\mathrm{plasma\_dxo}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_dxo}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{dxo}} \\[1ex]
v_{\mathrm{transport\_ki\_dxo\_glu}} &= \frac{\mathrm{ftissue}_{\mathrm{fast}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cki}_{\mathrm{plasma\_dxo\_glu}} \cdot \mathrm{Kp}_{\mathrm{dxo\_glu}} - \mathrm{Cki}_{\mathrm{dxo\_glu}}\right) \\[1ex]
v_{\mathrm{transport\_li\_dxo\_glu}} &= \frac{\mathrm{ftissue}_{\mathrm{fast}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cli}_{\mathrm{plasma\_dxo\_glu}} \cdot \mathrm{Kp}_{\mathrm{dxo\_glu}} - \mathrm{Cli}_{\mathrm{dxo\_glu}}\right) \\[1ex]
v_{\mathrm{transport\_lu\_dxo\_glu}} &= \frac{\mathrm{ftissue}_{\mathrm{dxo\_glu}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_dxo\_glu}} \cdot \mathrm{Kp}_{\mathrm{dxo\_glu}} - \mathrm{Clu}_{\mathrm{dxo\_glu}}\right) \\[1ex]
v_{\mathrm{transport\_gu\_dxo\_glu}} &= \frac{\mathrm{ftissue}_{\mathrm{fast}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cgu}_{\mathrm{plasma\_dxo\_glu}} \cdot \mathrm{Kp}_{\mathrm{dxo\_glu}} - \mathrm{Cgu}_{\mathrm{dxo\_glu}}\right) \\[1ex]
v_{\mathrm{transport\_re\_dxo\_glu}} &= \frac{\mathrm{ftissue}_{\mathrm{dxo\_glu}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_dxo\_glu}} \cdot \mathrm{Kp}_{\mathrm{dxo\_glu}} - \mathrm{Cre}_{\mathrm{dxo\_glu}}\right) \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_dxo\_glu}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{dxo\_glu}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_dxo\_glu}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_dxo\_glu}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_dxo\_glu}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{dxo\_glu}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_dxo\_glu}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_dxo\_glu}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_dxo\_glu}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{dxo\_glu}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_dxo\_glu}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_dxo\_glu}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_dxo\_glu}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{dxo\_glu}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_dxo\_glu}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_dxo\_glu}} \\[1ex]
v_{\mathrm{Flow\_ar\_li\_dxo\_glu}} &= \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{dxo\_glu}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_dxo\_glu}} &= \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{dxo\_glu}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_dxo\_glu}} &= \mathrm{Qh} \cdot \mathrm{Cli}_{\mathrm{plasma\_dxo\_glu}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_dxo\_glu}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{dxo\_glu}} \\[1ex]
v_{\mathrm{transport\_ki\_mm}} &= \frac{\mathrm{ftissue}_{\mathrm{fast}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cki}_{\mathrm{plasma\_mm}} \cdot \mathrm{Kp}_{\mathrm{mm}} - \mathrm{Cki}_{\mathrm{mm}}\right) \\[1ex]
v_{\mathrm{transport\_li\_mm}} &= \frac{\mathrm{ftissue}_{\mathrm{fast}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cli}_{\mathrm{plasma\_mm}} \cdot \mathrm{Kp}_{\mathrm{mm}} - \mathrm{Cli}_{\mathrm{mm}}\right) \\[1ex]
v_{\mathrm{transport\_lu\_mm}} &= \frac{\mathrm{ftissue}_{\mathrm{mm}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_mm}} \cdot \mathrm{Kp}_{\mathrm{mm}} - \mathrm{Clu}_{\mathrm{mm}}\right) \\[1ex]
v_{\mathrm{transport\_gu\_mm}} &= \frac{\mathrm{ftissue}_{\mathrm{fast}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cgu}_{\mathrm{plasma\_mm}} \cdot \mathrm{Kp}_{\mathrm{mm}} - \mathrm{Cgu}_{\mathrm{mm}}\right) \\[1ex]
v_{\mathrm{transport\_re\_mm}} &= \frac{\mathrm{ftissue}_{\mathrm{mm}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_mm}} \cdot \mathrm{Kp}_{\mathrm{mm}} - \mathrm{Cre}_{\mathrm{mm}}\right) \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_mm}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{mm}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_mm}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_mm}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_mm}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{mm}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_mm}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_mm}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_mm}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{mm}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_mm}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_mm}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_mm}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{mm}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_mm}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_mm}} \\[1ex]
v_{\mathrm{Flow\_ar\_li\_mm}} &= \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{mm}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_mm}} &= \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{mm}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_mm}} &= \mathrm{Qh} \cdot \mathrm{Cli}_{\mathrm{plasma\_mm}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_mm}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{mm}} \\[1ex]
v_{\mathrm{KI\_\_DXMEX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{fu}_{\mathrm{dxm}} \cdot \mathrm{KI}_{\mathrm{\_DXMEX\_f}} \cdot \mathrm{Cki}_{\mathrm{plasma\_dxm}} \\[1ex]
v_{\mathrm{KI\_\_DXOEX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{fu}_{\mathrm{dxo}} \cdot \mathrm{KI}_{\mathrm{\_DXOEX\_f}} \cdot \mathrm{Cki}_{\mathrm{plasma\_dxo}} \\[1ex]
v_{\mathrm{KI\_\_DXOGLUEX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{fu}_{\mathrm{dxo\_glu}} \cdot \mathrm{KI}_{\mathrm{\_DXOGLUEX\_f}} \cdot \mathrm{Cki}_{\mathrm{plasma\_dxo\_glu}} \\[1ex]
v_{\mathrm{KI\_\_MMEX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{fu}_{\mathrm{mm}} \cdot \mathrm{KI}_{\mathrm{\_MMEX\_f}} \cdot \mathrm{Cki}_{\mathrm{plasma\_mm}} \\[1ex]
v_{\mathrm{LI\_\_DXMCYP2D6}} &= \frac{\frac{\mathrm{LI}_{\mathrm{\_f\_cyp2d6}} \cdot \mathrm{LI}_{\mathrm{\_cyp2d6\_activity}}}{\mathrm{LI}_{\mathrm{\_cyp2d6\_activity\_ref}}} \cdot \mathrm{LI}_{\mathrm{\_DXMCYP2D6\_Vmax}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{Cli}_{\mathrm{dxm}}}{\mathrm{LI}_{\mathrm{\_DXMCYP2D6\_Km\_dxm}} + \mathrm{Cli}_{\mathrm{dxm}}} \\[1ex]
v_{\mathrm{LI\_\_DXMCYPX}} &= \frac{\mathrm{LI}_{\mathrm{\_f\_cyp3a4}} \cdot \mathrm{LI}_{\mathrm{\_DXMCYPX\_Vmax}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{Cli}_{\mathrm{dxm}}}{\mathrm{LI}_{\mathrm{\_DXMCYPX\_Km\_dxm}} + \mathrm{Cli}_{\mathrm{dxm}}} \\[1ex]
v_{\mathrm{LI\_\_DXMNDM}} &= \frac{\mathrm{LI}_{\mathrm{\_f\_cyp3a4}} \cdot \mathrm{LI}_{\mathrm{\_DXMNDM\_Vmax}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{Cli}_{\mathrm{dxm}}}{\mathrm{LI}_{\mathrm{\_DXMNDM\_Km\_dxm}} + \mathrm{Cli}_{\mathrm{dxm}}} \\[1ex]
v_{\mathrm{LI\_\_DXONDM}} &= \frac{\mathrm{LI}_{\mathrm{\_f\_cyp3a4}} \cdot \mathrm{LI}_{\mathrm{\_DXONDM\_Vmax}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{Cli}_{\mathrm{dxo}}}{\mathrm{LI}_{\mathrm{\_DXONDM\_Km\_dxo}} + \mathrm{Cli}_{\mathrm{dxo}}} \\[1ex]
v_{\mathrm{LI\_\_DXOUGT}} &= \frac{\mathrm{LI}_{\mathrm{\_f\_ugt2b15}} \cdot \mathrm{LI}_{\mathrm{\_DXOUGT\_Vmax}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{Cli}_{\mathrm{dxo}}}{\mathrm{LI}_{\mathrm{\_DXOUGT\_Km\_dxo}} + \mathrm{Cli}_{\mathrm{dxo}}} \\[1ex]
v_{\mathrm{GU\_\_dissolution\_dxm}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{dis\_dxm}}}{60} \cdot \mathrm{PODOSE}_{\mathrm{dxm}}}{\mathrm{Mr}_{\mathrm{dxm}}} \\[1ex]
v_{\mathrm{GU\_\_DXMABS}} &= \mathrm{GU}_{\mathrm{\_F\_dxm\_abs}} \cdot \mathrm{GU}_{\mathrm{\_absorption\_dxm}} \\[1ex]
v_{\mathrm{GU\_\_DXMEXC}} &= \mathopen{}\left(1 - \mathrm{GU}_{\mathrm{\_F\_dxm\_abs}}\right) \cdot \mathrm{GU}_{\mathrm{\_absorption\_dxm}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_dxm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_ki\_dxm}} + v_{\mathrm{Flow\_ar\_ki\_dxm}} - v_{\mathrm{Flow\_ki\_ve\_dxm}} - v_{\mathrm{KI\_\_DXMEX}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_dxm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_li\_dxm}} + v_{\mathrm{Flow\_ar\_li\_dxm}} + v_{\mathrm{Flow\_po\_li\_dxm}} - v_{\mathrm{Flow\_li\_hv\_dxm}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_dxm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_dxm}} + v_{\mathrm{Flow\_ve\_lu\_dxm}} - v_{\mathrm{Flow\_lu\_ar\_dxm}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_dxm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_gu\_dxm}} + v_{\mathrm{Flow\_ar\_gu\_dxm}} - v_{\mathrm{Flow\_gu\_po\_dxm}} + v_{\mathrm{GU\_\_DXMABS}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_dxm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_dxm}} + v_{\mathrm{Flow\_ar\_re\_dxm}} - v_{\mathrm{Flow\_re\_ve\_dxm}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{dxm}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( v_{\mathrm{Flow\_lu\_ar\_dxm}} - v_{\mathrm{Flow\_ar\_ki\_dxm}} - v_{\mathrm{Flow\_ar\_re\_dxm}} - v_{\mathrm{Flow\_ar\_gu\_dxm}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_li\_dxm}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{dxm}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}} \Bigl( v_{\mathrm{iv\_dxm}} - v_{\mathrm{Flow\_ve\_lu\_dxm}} + v_{\mathrm{Flow\_ki\_ve\_dxm}} + v_{\mathrm{Flow\_re\_ve\_dxm}} \\
&\quad {} + v_{\mathrm{Flow\_hv\_ve\_dxm}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{dxm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_gu\_po\_dxm}} - v_{\mathrm{Flow\_po\_li\_dxm}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{dxm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_li\_hv\_dxm}} - v_{\mathrm{Flow\_hv\_ve\_dxm}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{dxm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_ki\_dxm}}}{\mathrm{Vki}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{dxm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_li\_dxm}} - v_{\mathrm{LI\_\_DXMCYP2D6}} - v_{\mathrm{LI\_\_DXMCYPX}} - v_{\mathrm{LI\_\_DXMNDM}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{dxm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_dxm}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{dxm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_gu\_dxm}}}{\mathrm{Vgu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{dxm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_dxm}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{dxm}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_DXMEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_dxo}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_ki\_dxo}} + v_{\mathrm{Flow\_ar\_ki\_dxo}} - v_{\mathrm{Flow\_ki\_ve\_dxo}} - v_{\mathrm{KI\_\_DXOEX}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_dxo}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_li\_dxo}} + v_{\mathrm{Flow\_ar\_li\_dxo}} + v_{\mathrm{Flow\_po\_li\_dxo}} - v_{\mathrm{Flow\_li\_hv\_dxo}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_dxo}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_dxo}} + v_{\mathrm{Flow\_ve\_lu\_dxo}} - v_{\mathrm{Flow\_lu\_ar\_dxo}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_dxo}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_gu\_dxo}} + v_{\mathrm{Flow\_ar\_gu\_dxo}} - v_{\mathrm{Flow\_gu\_po\_dxo}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_dxo}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_dxo}} + v_{\mathrm{Flow\_ar\_re\_dxo}} - v_{\mathrm{Flow\_re\_ve\_dxo}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{dxo}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( v_{\mathrm{Flow\_lu\_ar\_dxo}} - v_{\mathrm{Flow\_ar\_ki\_dxo}} - v_{\mathrm{Flow\_ar\_re\_dxo}} - v_{\mathrm{Flow\_ar\_gu\_dxo}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_li\_dxo}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{dxo}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_ve\_lu\_dxo}} + v_{\mathrm{Flow\_ki\_ve\_dxo}} + v_{\mathrm{Flow\_re\_ve\_dxo}} + v_{\mathrm{Flow\_hv\_ve\_dxo}}}{\mathrm{Vve}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{dxo}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_gu\_po\_dxo}} - v_{\mathrm{Flow\_po\_li\_dxo}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{dxo}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_li\_hv\_dxo}} - v_{\mathrm{Flow\_hv\_ve\_dxo}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{dxo}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_ki\_dxo}}}{\mathrm{Vki}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{dxo}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vli}_{\mathrm{tissue}}} \Bigl( v_{\mathrm{transport\_li\_dxo}} + v_{\mathrm{LI\_\_DXMCYP2D6}} + v_{\mathrm{LI\_\_DXMCYPX}} - v_{\mathrm{LI\_\_DXONDM}} \\
&\quad {} - v_{\mathrm{LI\_\_DXOUGT}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{dxo}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_dxo}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{dxo}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_gu\_dxo}}}{\mathrm{Vgu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{dxo}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_dxo}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{dxo}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_DXOEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_dxo\_glu}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_ki\_dxo\_glu}} + v_{\mathrm{Flow\_ar\_ki\_dxo\_glu}} - v_{\mathrm{Flow\_ki\_ve\_dxo\_glu}} - v_{\mathrm{KI\_\_DXOGLUEX}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_dxo\_glu}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_li\_dxo\_glu}} + v_{\mathrm{Flow\_ar\_li\_dxo\_glu}} + v_{\mathrm{Flow\_po\_li\_dxo\_glu}} - v_{\mathrm{Flow\_li\_hv\_dxo\_glu}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_dxo\_glu}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_dxo\_glu}} + v_{\mathrm{Flow\_ve\_lu\_dxo\_glu}} - v_{\mathrm{Flow\_lu\_ar\_dxo\_glu}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_dxo\_glu}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_gu\_dxo\_glu}} + v_{\mathrm{Flow\_ar\_gu\_dxo\_glu}} - v_{\mathrm{Flow\_gu\_po\_dxo\_glu}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_dxo\_glu}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_dxo\_glu}} + v_{\mathrm{Flow\_ar\_re\_dxo\_glu}} - v_{\mathrm{Flow\_re\_ve\_dxo\_glu}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{dxo\_glu}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( v_{\mathrm{Flow\_lu\_ar\_dxo\_glu}} - v_{\mathrm{Flow\_ar\_ki\_dxo\_glu}} - v_{\mathrm{Flow\_ar\_re\_dxo\_glu}} - v_{\mathrm{Flow\_ar\_gu\_dxo\_glu}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_li\_dxo\_glu}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{dxo\_glu}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_ve\_lu\_dxo\_glu}} + v_{\mathrm{Flow\_ki\_ve\_dxo\_glu}} + v_{\mathrm{Flow\_re\_ve\_dxo\_glu}} + v_{\mathrm{Flow\_hv\_ve\_dxo\_glu}}}{\mathrm{Vve}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{dxo\_glu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_gu\_po\_dxo\_glu}} - v_{\mathrm{Flow\_po\_li\_dxo\_glu}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{dxo\_glu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_li\_hv\_dxo\_glu}} - v_{\mathrm{Flow\_hv\_ve\_dxo\_glu}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{dxo\_glu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_ki\_dxo\_glu}}}{\mathrm{Vki}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{dxo\_glu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_li\_dxo\_glu}} + v_{\mathrm{LI\_\_DXOUGT}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{dxo\_glu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_dxo\_glu}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{dxo\_glu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_gu\_dxo\_glu}}}{\mathrm{Vgu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{dxo\_glu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_dxo\_glu}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{dxo\_glu}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_DXOGLUEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_mm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_ki\_mm}} + v_{\mathrm{Flow\_ar\_ki\_mm}} - v_{\mathrm{Flow\_ki\_ve\_mm}} - v_{\mathrm{KI\_\_MMEX}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_mm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_li\_mm}} + v_{\mathrm{Flow\_ar\_li\_mm}} + v_{\mathrm{Flow\_po\_li\_mm}} - v_{\mathrm{Flow\_li\_hv\_mm}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_mm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_mm}} + v_{\mathrm{Flow\_ve\_lu\_mm}} - v_{\mathrm{Flow\_lu\_ar\_mm}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_mm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_gu\_mm}} + v_{\mathrm{Flow\_ar\_gu\_mm}} - v_{\mathrm{Flow\_gu\_po\_mm}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_mm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_mm}} + v_{\mathrm{Flow\_ar\_re\_mm}} - v_{\mathrm{Flow\_re\_ve\_mm}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{mm}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( v_{\mathrm{Flow\_lu\_ar\_mm}} - v_{\mathrm{Flow\_ar\_ki\_mm}} - v_{\mathrm{Flow\_ar\_re\_mm}} - v_{\mathrm{Flow\_ar\_gu\_mm}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_li\_mm}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{mm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_ve\_lu\_mm}} + v_{\mathrm{Flow\_ki\_ve\_mm}} + v_{\mathrm{Flow\_re\_ve\_mm}} + v_{\mathrm{Flow\_hv\_ve\_mm}}}{\mathrm{Vve}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{mm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_gu\_po\_mm}} - v_{\mathrm{Flow\_po\_li\_mm}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{mm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_li\_hv\_mm}} - v_{\mathrm{Flow\_hv\_ve\_mm}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{mm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_ki\_mm}}}{\mathrm{Vki}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{mm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_li\_mm}} + v_{\mathrm{LI\_\_DXMNDM}} + v_{\mathrm{LI\_\_DXONDM}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{mm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_mm}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{mm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_gu\_mm}}}{\mathrm{Vgu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{mm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_mm}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{mm}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_MMEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgulumen}_{\mathrm{dxm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_dissolution\_dxm}} - v_{\mathrm{GU\_\_DXMABS}} - v_{\mathrm{GU\_\_DXMEXC}}}{\mathrm{Vgulumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Afeces}_{\mathrm{dxm}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_DXMEXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{IVDOSE}_{\mathrm{dxm}}}{\mathrm{d} t} &= -v_{\mathrm{iv\_dxm}} \cdot \mathrm{Mr}_{\mathrm{dxm}} + \mathrm{Ri}_{\mathrm{dxm}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cum}_{\mathrm{dose\_dxm}}}{\mathrm{d} t} &= \mathrm{Ri}_{\mathrm{dxm}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{dxm}}}{\mathrm{d} t} &= -v_{\mathrm{GU\_\_dissolution\_dxm}} \cdot \mathrm{Mr}_{\mathrm{dxm}} \qquad \text{(rate rule)}
\end{aligned}
$$
