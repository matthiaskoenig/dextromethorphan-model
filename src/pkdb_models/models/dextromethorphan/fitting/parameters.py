"""The fit parameters of the dextromethorphan model.

The pharmacokinetics are fitted on the plasma concentrations, the urinary
amounts and the metabolic ratios of dextromethorphan, dextrorphan, its
glucuronide and the lumped N-demethylated morphinans. The fit adjusts the
dissolution and the fraction absorbed, the maximal rates of the hepatic
pathways, the partition coefficients of the metabolites and of
dextromethorphan and the renal clearances.

Fixed are the Michaelis constants of the hepatic pathways (the hepatic
concentrations are far below them, so only the intrinsic clearance `Vmax/Km`
is identified), the absorption from the lumen (`GU__DXMABS_k`, in series with
the dissolution and not identified apart from it), the exchange of the
eliminating organs with their plasma (`ftissue_fast`) and the exchange of the
metabolites with the tissues (`ftissue_<sid>`, their distribution is perfusion
limited), the
partition coefficient of free dextrorphan (`Kp_dxo`, its concentration is
formation limited, no observable depends on it), the fractions unbound and
the factors of the CYP2D6 activity score, of the interactions and of the
renal function.

The start values are the values the model had before its first fit, chosen
by hand for the literature; the model takes the values of the adopted fit
(`models/fits.py`). At the start values the O-demethylation by CYP2D6 gives
extensive metabolizers an oral bioavailability of 3.9 % and an AUC of 9.4
µg*h/l after 22 mg (Capon1996: 9), the CYP2D6-independent pathways give poor
metabolizers CL/F 248 ml/min (Schadel1995: 275 +- 95) with the half-life of
20 hr (Capon1996 19.1, Schadel1995 29.5), and the partition coefficient of
dextromethorphan a volume of distribution of 6.0 l/kg (5-6.7 reported).
"""

from sbmlsim.fit import FitParameter

#: the parameters of the pharmacokinetics
parameters_pk: list[FitParameter] = [
    # dissolution and gastric emptying: tmax 2.4 hr in extensive and 4-5.5 hr
    # in poor metabolizers (Capon1996, Schadel1995)
    FitParameter(
        pid="Ka_dis_dxm",
        start_value=0.4,
        lower_bound=0.05,
        upper_bound=10,
        unit="1/hr",
    ),
    # fraction absorbed: the urinary recoveries of dextromethorphan and of its
    # metabolites (26 % unchanged in poor metabolizers, Capon1996; 55-97 % of
    # a dose as the sum of the analytes, Schadel1995, Jones1996). The model has
    # no other route of the metabolites than the urine, so the fraction
    # absorbed also carries the part of a dose which leaves as metabolites
    # which are not measured
    FitParameter(
        pid="GU__F_dxm_abs",
        start_value=0.9,
        lower_bound=0.3,
        upper_bound=1.0,
        unit="dimensionless",
    ),
    # O-demethylation by CYP2D6, the clearance of extensive metabolizers
    FitParameter(
        pid="LI__DXMCYP2D6_Vmax",
        start_value=0.0187,
        lower_bound=1e-4,
        upper_bound=1.0,
        unit="mmole/min/l",
    ),
    # CYP2D6-independent O-demethylation, the dextrorphan of poor metabolizers
    FitParameter(
        pid="LI__DXMCYPX_Vmax",
        start_value=0.00055,
        lower_bound=1e-6,
        upper_bound=1e-2,
        unit="mmole/min/l",
    ),
    # N-demethylation of dextromethorphan, the main CYP2D6-independent
    # clearance (3-methoxymorphinan in the urine of poor metabolizers)
    FitParameter(
        pid="LI__DXMNDM_Vmax",
        start_value=0.0107,
        lower_bound=1e-5,
        upper_bound=1.0,
        unit="mmole/min/l",
    ),
    # N-demethylation of dextrorphan (3-hydroxymorphinan, 16 % of a dose in
    # the urine of extensive metabolizers)
    FitParameter(
        pid="LI__DXONDM_Vmax",
        start_value=0.65,
        lower_bound=1e-3,
        upper_bound=50,
        unit="mmole/min/l",
    ),
    # glucuronidation of dextrorphan: about 96 % of the dextrorphan of the
    # plasma is conjugated (Nagai1996)
    FitParameter(
        pid="LI__DXOUGT_Vmax",
        start_value=0.895,
        lower_bound=1e-2,
        upper_bound=1e2,
        unit="mmole/min/l",
    ),
    # distribution of dextromethorphan: the half-lives of extensive (2.4-3.6
    # hr) and poor metabolizers (19-30 hr reported, 45-65 hr in the terminal
    # phase of Capon1996 and Eichhold2007), Vss 5-6.7 l/kg
    FitParameter(
        pid="Kp_dxm",
        start_value=5.0,
        lower_bound=1.0,
        upper_bound=20,
        unit="dimensionless",
    ),
    # distribution of the lumped N-demethylated morphinans: the peak and the
    # decline of the 3-hydroxymorphinan of the plasma (Nagai1996, Schadel1995)
    FitParameter(
        pid="Kp_mm",
        start_value=0.3,
        lower_bound=0.02,
        upper_bound=3,
        unit="dimensionless",
    ),
    # renal clearance relative to the filtration of the unbound substance: the
    # renal clearance of dextromethorphan in poor metabolizers is 41-78 ml/min
    # (Schadel1995, Capon1996), the urinary recoveries give the others
    FitParameter(
        pid="KI__DXMEX_f",
        start_value=1.5,
        lower_bound=0.05,
        upper_bound=10,
        unit="dimensionless",
    ),
    FitParameter(
        pid="KI__DXOEX_f",
        start_value=3.0,
        lower_bound=0.05,
        upper_bound=50,
        unit="dimensionless",
    ),
    FitParameter(
        pid="KI__DXOGLUEX_f",
        start_value=1.6,
        lower_bound=0.05,
        upper_bound=20,
        unit="dimensionless",
    ),
    FitParameter(
        pid="KI__MMEX_f",
        start_value=3.0,
        lower_bound=0.05,
        upper_bound=20,
        unit="dimensionless",
    ),
]
