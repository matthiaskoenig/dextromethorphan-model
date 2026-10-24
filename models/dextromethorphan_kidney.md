# Dextromethorphan (DXM) kidney model

Model `dextromethorphan_kidney`, SBML Level 3 Version 2, read from dextromethorphan\_kidney.xml, written by sbmlode 0.3.0.

Kidney model of the renal excretion of dextromethorphan

The renal clearance of a substance is GFR \* fu\_&lt;sid&gt; \* &lt;X&gt;EX\_f, the filtration of its unbound fraction times a factor: 1 is filtration alone, above 1 a net tubular secretion, below 1 a net reabsorption. The glomerular filtration rate is GFR = f\_renal\_function \* GFR\_base, GFR\_base is 101 ml/min at 75 kg and scales with the renal blood flow; a measured creatinine clearance of X ml/min is the renal function X/101.

The factors are of the renal clearances and the urinary recoveries of the literature: the renal clearance of dextromethorphan in poor metabolizers is 41-78 ml/min (Schadel1995, Capon1996) with 11-26 % of an oral dose excreted unchanged, extensive metabolizers excrete 0.2 % unchanged and 27-39 % as total dextrorphan.

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
| $\mathrm{Vext}$ | `Vext` | plasma | $1$ | l | ✓ |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{dxm}_{\mathrm{ext}}$ | `dxm_ext` | dextromethorphan (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{dxm}_{\mathrm{urine}}$ | `dxm_urine` | dextromethorphan (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{dxo}_{\mathrm{ext}}$ | `dxo_ext` | dextrorphan (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{dxo}_{\mathrm{urine}}$ | `dxo_urine` | dextrorphan (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{dxo}_{\mathrm{glu\_ext}}$ | `dxo_glu_ext` | dextrorphan glucuronide (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{dxo}_{\mathrm{glu\_urine}}$ | `dxo_glu_urine` | dextrorphan glucuronide (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{mm}_{\mathrm{ext}}$ | `mm_ext` | N-demethylated morphinans (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{mm}_{\mathrm{urine}}$ | `mm_urine` | N-demethylated morphinans (urine) | $\mathrm{Vurine}$ |  | mmol | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $f_{\mathrm{renal\_function}}$ | `f_renal_function` | renal function | $1$ | \- | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate (healthy) | $101$ | ml/min |  |
| $\mathrm{GFR}$ | `GFR` | glomerular filtration rate |  | ml/min |  |
| $\mathrm{fu}_{\mathrm{dxm}}$ | `fu_dxm` | fraction unbound in plasma dextromethorphan | $0.5$ | \- | ✓ |
| $\mathrm{DXMEX}_{\mathrm{f}}$ | `DXMEX_f` | renal clearance of unbound dextromethorphan relative to the GFR | $0.656113552124429$ | \- | ✓ |
| $\mathrm{fu}_{\mathrm{dxo}}$ | `fu_dxo` | fraction unbound in plasma dextrorphan | $0.55$ | \- | ✓ |
| $\mathrm{DXOEX}_{\mathrm{f}}$ | `DXOEX_f` | renal clearance of unbound dextrorphan relative to the GFR | $1.86913741202018$ | \- | ✓ |
| $\mathrm{fu}_{\mathrm{dxo\_glu}}$ | `fu_dxo_glu` | fraction unbound in plasma dextrorphan glucuronide | $0.44$ | \- | ✓ |
| $\mathrm{DXOGLUEX}_{\mathrm{f}}$ | `DXOGLUEX_f` | renal clearance of unbound dextrorphan glucuronide relative to the GFR | $2.2657913496198$ | \- | ✓ |
| $\mathrm{fu}_{\mathrm{mm}}$ | `fu_mm` | fraction unbound in plasma N-demethylated morphinans | $0.5$ | \- | ✓ |
| $\mathrm{MMEX}_{\mathrm{f}}$ | `MMEX_f` | renal clearance of unbound N-demethylated morphinans relative to the GFR | $1.66127389767754$ | \- | ✓ |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{dxm}_{\mathrm{urine}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{dxo}_{\mathrm{urine}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{dxo}_{\mathrm{glu\_urine}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{mm}_{\mathrm{urine}} &= 0 \cdot \mathrm{Vurine}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{GFR} &= f_{\mathrm{renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{DXMEX}}$ | `DXMEX` | dextromethorphan renal excretion | $\mathrm{dxm}_{\mathrm{ext}} \longrightarrow \mathrm{dxm}_{\mathrm{urine}}$ |
| $v_{\mathrm{DXOEX}}$ | `DXOEX` | dextrorphan renal excretion | $\mathrm{dxo}_{\mathrm{ext}} \longrightarrow \mathrm{dxo}_{\mathrm{urine}}$ |
| $v_{\mathrm{DXOGLUEX}}$ | `DXOGLUEX` | dextrorphan glucuronide renal excretion | $\mathrm{dxo}_{\mathrm{glu\_ext}} \longrightarrow \mathrm{dxo}_{\mathrm{glu\_urine}}$ |
| $v_{\mathrm{MMEX}}$ | `MMEX` | N-demethylated morphinans renal excretion | $\mathrm{mm}_{\mathrm{ext}} \longrightarrow \mathrm{mm}_{\mathrm{urine}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{DXMEX}} &= \mathrm{GFR} \cdot 0.001 \cdot \mathrm{fu}_{\mathrm{dxm}} \cdot \mathrm{DXMEX}_{\mathrm{f}} \cdot \mathrm{dxm}_{\mathrm{ext}} \\[1ex]
v_{\mathrm{DXOEX}} &= \mathrm{GFR} \cdot 0.001 \cdot \mathrm{fu}_{\mathrm{dxo}} \cdot \mathrm{DXOEX}_{\mathrm{f}} \cdot \mathrm{dxo}_{\mathrm{ext}} \\[1ex]
v_{\mathrm{DXOGLUEX}} &= \mathrm{GFR} \cdot 0.001 \cdot \mathrm{fu}_{\mathrm{dxo\_glu}} \cdot \mathrm{DXOGLUEX}_{\mathrm{f}} \cdot \mathrm{dxo}_{\mathrm{glu\_ext}} \\[1ex]
v_{\mathrm{MMEX}} &= \mathrm{GFR} \cdot 0.001 \cdot \mathrm{fu}_{\mathrm{mm}} \cdot \mathrm{MMEX}_{\mathrm{f}} \cdot \mathrm{mm}_{\mathrm{ext}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{dxm}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{DXMEX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{dxm}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{DXMEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{dxo}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{DXOEX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{dxo}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{DXOEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{dxo}_{\mathrm{glu\_ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{DXOGLUEX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{dxo}_{\mathrm{glu\_urine}}}{\mathrm{d} t} &= v_{\mathrm{DXOGLUEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{mm}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{MMEX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{mm}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{MMEX}}
\end{aligned}
$$
