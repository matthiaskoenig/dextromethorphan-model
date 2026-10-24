# Dextromethorphan (DXM) intestine model

Model `dextromethorphan_intestine`, SBML Level 3 Version 2, read from dextromethorphan\_intestine.xml, written by sbmlode 0.3.0.

Intestine model of the oral absorption of dextromethorphan

An oral dose dissolves and passes the stomach with the rate Ka\_dis\_dxm into the lumen of the small intestine, from which the fraction F\_dxm\_abs is absorbed into the portal plasma with the rate DXMABS\_k, the rest is excreted in the feces. The oral bioavailability is the fraction absorbed times the fraction which escapes the first pass through the liver; the first pass of dextromethorphan is hepatic, the intestinal CYP3A4 is a few tenths of a percent of a dose and is not part of the model.

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
| $\mathrm{Vgu}$ | `Vgu` | intestine | $1.2825$ | l |  |
| $\mathrm{Vlumen}$ | `Vlumen` | intestinal lumen (inner part of intestine) | $1.15425$ | l |  |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vstomach}$ | `Vstomach` | stomach | $1$ | l | ✓ |
| $\mathrm{Vapical}$ | `Vapical` | apical membrane (intestinal membrane enterocytes) | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{dxm}_{\mathrm{stomach}}$ | `dxm_stomach` | dextromethorphan (stomach) | $\mathrm{Vstomach}$ |  | mmol | amount, boundary |
| $\mathrm{dxm}_{\mathrm{lumen}}$ | `dxm_lumen` | dextromethorphan (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{dxm}_{\mathrm{ext}}$ | `dxm_ext` | dextromethorphan (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{dxm}_{\mathrm{feces}}$ | `dxm_feces` | dextromethorphan (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $F_{\mathrm{dxm\_abs}}$ | `F_dxm_abs` | fraction absorbed dextromethorphan | $0.523770919743564$ | \- | ✓ |
| $\mathrm{DXMABS}_{\mathrm{k}}$ | `DXMABS_k` | rate of the absorption of dextromethorphan | $0.08$ | 1/min | ✓ |
| $\mathrm{PODOSE}_{\mathrm{dxm}}$ | `PODOSE_dxm` | oral dose dextromethorphan \[mg\] | $0$ | mg |  |
| $\mathrm{Ka}_{\mathrm{dis\_dxm}}$ | `Ka_dis_dxm` | Ka\_dis \[1/hr\] dissolution dextromethorphan | $0.401682131288553$ | 1/hr | ✓ |
| $\mathrm{Mr}_{\mathrm{dxm}}$ | `Mr_dxm` | Molecular weight dextromethorphan \[g/mole\] | $271.404$ | g/mol | ✓ |
| $\mathrm{absorption}_{\mathrm{dxm}}$ | `absorption_dxm` | absorption dextromethorphan |  | mmol/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{dxm}_{\mathrm{stomach}} &= 0 \cdot \mathrm{Vstomach} \\[1ex]
\mathrm{dxm}_{\mathrm{feces}} &= 0 \cdot \mathrm{Vfeces}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{absorption}_{\mathrm{dxm}} &= \mathrm{DXMABS}_{\mathrm{k}} \cdot \mathrm{Vgu} \cdot \mathrm{dxm}_{\mathrm{lumen}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{dissolution\_dxm}}$ | `dissolution_dxm` | dissolution dextromethorphan | $\mathrm{dxm}_{\mathrm{stomach}} \longrightarrow \mathrm{dxm}_{\mathrm{lumen}}$ |
| $v_{\mathrm{DXMABS}}$ | `DXMABS` | absorption dextromethorphan | $\mathrm{dxm}_{\mathrm{lumen}} \longrightarrow \mathrm{dxm}_{\mathrm{ext}}$ |
| $v_{\mathrm{DXMEXC}}$ | `DXMEXC` | excretion dextromethorphan (feces) | $\mathrm{dxm}_{\mathrm{lumen}} \longrightarrow \mathrm{dxm}_{\mathrm{feces}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{dissolution\_dxm}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{dis\_dxm}}}{60} \cdot \mathrm{PODOSE}_{\mathrm{dxm}}}{\mathrm{Mr}_{\mathrm{dxm}}} \\[1ex]
v_{\mathrm{DXMABS}} &= F_{\mathrm{dxm\_abs}} \cdot \mathrm{absorption}_{\mathrm{dxm}} \\[1ex]
v_{\mathrm{DXMEXC}} &= \mathopen{}\left(1 - F_{\mathrm{dxm\_abs}}\right) \cdot \mathrm{absorption}_{\mathrm{dxm}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{dxm}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{v_{\mathrm{dissolution\_dxm}} - v_{\mathrm{DXMABS}} - v_{\mathrm{DXMEXC}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{dxm}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{DXMABS}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{dxm}_{\mathrm{feces}}}{\mathrm{d} t} &= v_{\mathrm{DXMEXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{dxm}}}{\mathrm{d} t} &= -v_{\mathrm{dissolution\_dxm}} \cdot \mathrm{Mr}_{\mathrm{dxm}} \qquad \text{(rate rule)}
\end{aligned}
$$
