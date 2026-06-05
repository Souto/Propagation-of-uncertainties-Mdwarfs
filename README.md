# M-dwarf Abundance Uncertainty Propagation

A Python tool for computing total chemical abundance uncertainties in M dwarf stars from APOGEE *H*-band spectra. Uncertainties from three independent sources are propagated via a quadratic sum, following the methodology of [Melo et al. 2024 (ApJ 973, 90)](https://doi.org/10.3847/1538-4357/ad5004).

---

## Background

Determining precise chemical abundances for M dwarf stars requires quantifying how errors in atmospheric parameters, spectral signal-to-noise ratio (S/N), and pseudocontinuum placement each contribute to the final abundance uncertainty. This tool encodes the sensitivity tables from Melo et al. (2024) — covering 16 elements across the effective temperature range 3200–3900 K — and combines them into a total 1σ uncertainty estimate:

$$\sigma_\mathrm{total} = \sqrt{\,\sigma_\mathrm{atm}^2 + \sigma_\mathrm{S/N}^2 + \sigma_\mathrm{pseudo}^2\,}$$

where the atmospheric term itself is:

$$\sigma_\mathrm{atm} = \sqrt{\,\sigma_{T_\mathrm{eff}}^2 + \sigma_{\log g}^2 + \sigma_{[\mathrm{Fe/H}]}^2 + \sigma_\xi^2\,}$$

Each partial uncertainty is read from pre-computed sensitivity tables and linearly interpolated to match the user's actual 1σ parameter errors.

---

## Elements supported

| Symbol | Species |
|--------|---------|
| `Fe`   | Fe I atomic lines |
| `FeH`  | Iron hydride molecular lines |
| `CO`   | CO molecular lines (carbon abundance) |
| `OH`   | OH molecular lines (oxygen abundance) |
| `H2O`  | Water vapour molecular lines |
| `Na`   | Na I |
| `Mg`   | Mg I |
| `Al`   | Al I |
| `Si`   | Si I |
| `K`    | K I |
| `Ca`   | Ca I |
| `Ti`   | Ti I |
| `V`    | V I |
| `Cr`   | Cr I |
| `Mn`   | Mn I |
| `Ni`   | Ni I |

> Not all elements are measurable at every temperature. The tool automatically skips elements with no usable spectral lines at the requested T_eff.

---

## Installation

Requires Python 3.8 or later.

```bash
git clone https://github.com/souto/Propagation-of-uncertainties.git
cd Propagation-of-uncertainties
pip install -r requirements.txt
```

---

## Usage

Run the interactive script:

```bash
python3 main.py
```

You will be prompted for the following inputs. Press **Enter** to accept the default value shown in brackets.

### Stellar parameters

| Prompt | Description | Example |
|--------|-------------|---------|
| `Stellar T_eff (K)` | Effective temperature of your star | `3900` |
| `Element` | Element to analyse, or press Enter for all | `Mg` |

### Measurement uncertainties (1σ errors on your derived parameters)

| Prompt | Description | Default |
|--------|-------------|---------|
| `sigma(T_eff) in K` | 1σ error on effective temperature | `100` |
| `sigma(log g) in dex` | 1σ error on surface gravity | `0.13` |
| `sigma([Fe/H]) in dex` | 1σ error on metallicity | `0.09` |
| `sigma(xi) in km/s` | 1σ error on microturbulence velocity | `0.50` |

> **These are your measurement errors, not the parameter values themselves.** For example, if you derived T_eff = 3519 ± 100 K, enter `100`.

### Spectrum quality

| Prompt | Description | Notes |
|--------|-------------|-------|
| `S/N` | Signal-to-noise ratio of your spectrum | Table range: 40–300 |
| `Displacement in %` | Expected pseudocontinuum displacement | Enter `0.5`, `1`, or `2` |

The pseudocontinuum displacement represents how accurately the local pseudo-continuum was placed. The paper adopts 1% as the standard estimate; 0.5% is derived by scaling the 1% table values by a factor of 0.5.

---

## Example session

```
============================================================
  M-dwarf Abundance Uncertainty Propagation
  Based on Melo et al. 2024 (ApJ 973, 90)
============================================================

--- Stellar parameters ---
  Stellar T_eff (K, e.g. 3900): 3900
  Element [...] [press Enter for all elements]: Mg

--- Your measurement uncertainties (1-sigma) ---
  sigma(T_eff)  in K       [default: 100]: 100
  sigma(log g) in dex      [default: 0.13]: 0.13
  sigma([Fe/H]) in dex     [default: 0.09]: 0.09
  sigma(xi)    in km/s     [default: 0.50]:

--- Spectrum quality ---
  S/N of your spectrum     [table range: 40–300, default: 100]: 150
  Displacement in %        [0.5, 1, or 2 — default: 1]: 1

============================================================
  Uncertainty budget for [Mg] (dex)
============================================================
    sigma(Teff)  contribution           -0.3000 dex
    sigma(logg)  contribution           +0.1140 dex
    sigma([Fe/H]) contribution          -0.0450 dex
    sigma(xi)    contribution           +0.0000 dex
  sigma(atm) [quadratic sum]          0.3241 dex
  sigma(S/N)                          0.0200 dex
  sigma(pseudocontinuum)              0.0940 dex

  TOTAL uncertainty (quadratic sum)   0.3380 dex
```

### All-elements output (default)

Pressing Enter at the element prompt runs the calculation for every measurable element and prints a compact summary table:

```
=============================================================================
  Uncertainty budget — all elements (dex)
  T_eff=3900K  σ(Teff)=100K  σ(logg)=0.13  σ([Fe/H])=0.09  σ(ξ)=0.50  S/N=150  psd=1.0%
=============================================================================
  Element  σ(Teff)  σ(logg)  σ([FeH])    σ(ξ)  │  σ(atm)  σ(S/N)  σ(psd)  │   TOTAL
  -------------------------------------------------------------------------
       Fe  -0.1700  +0.0620   -0.0090  +0.0000  │  0.1814  0.0100  0.0840  │  0.2023
      FeH  +0.0300  +0.0360   +0.0360  -0.0500  │  0.0793  0.0100  0.0990  │  0.1258
  ...
```

---

## How the uncertainties are computed

### Atmospheric parameters

The sensitivity tables record ΔA (abundance change in dex) for fixed perturbations of ±50 K and ±100 K in T_eff, ±0.10 and ±0.20 dex in log *g*, ±0.10 and ±0.20 dex in [Fe/H], and ±0.25 and ±0.50 km s⁻¹ in ξ. For a user-specified σ that falls between two table entries, the sensitivity is **linearly interpolated**; values outside the table range are linearly extrapolated. The total atmospheric uncertainty is the quadratic sum of the four contributions.

### S/N

A lookup table gives the abundance scatter measured from repeated synthetic spectra at each S/N level (40–300 in steps of 20). The nearest tabulated S/N is used; intermediate values are mapped to the closest entry.

### Pseudocontinuum displacement

A lookup table gives the abundance change caused by shifting the pseudo-continuum by ±1% and ±2%. A 0.5% displacement is estimated as half the 1% sensitivity (linear scaling). The tool always uses the positive-displacement column and scales by the ratio of the user's displacement to the reference.

---

## File structure

```
.
├── main.py                          # Interactive entry point
├── atmospheric_parameters.py        # Sensitivity tables for Teff, log g, [Fe/H], ξ
├── signal_to_noise_ratio_changes.py # Sensitivity tables for S/N
├── pseudocontinuum_displacements.py # Sensitivity tables for pseudocontinuum shifts
├── spectral_lines.py                # Recommended spectral lines by temperature
└── requirements.txt
```

---

## Temperature coverage

| T_eff (K) | Measurable elements |
|-----------|-------------------|
| 3900–3800 | Fe, FeH, CO, OH, H2O, Na, Mg, Al, Si, K, Ca, Ti, V, Cr, Mn, Ni |
| 3700–3600 | Fe, FeH, CO, OH, H2O, Na, Mg, Al, Si, K, Ca, Ti, V, Cr, Mn |
| 3500      | Fe, FeH, CO, OH, H2O, Na, Mg, Al, Si, K, Ca, Ti, V |
| 3400–3300 | Fe, FeH, CO, OH, H2O, Na, Mg, Al, Si, K, Ca, Ti, V |
| 3200      | FeH, CO, OH, H2O, Na, Mg, Al, Si, K, Ca, Ti, V |

For temperatures between table entries, the nearest tabulated value is used.

---

## Citation

If you use this tool in your research, please cite:

```
Melo et al. 2024, ApJ, 973, 90
https://doi.org/10.3847/1538-4357/ad5004
```

---

## Authors

Sensitivity tables and methodology: Edypo Melo, Diogo Souto et al. (2024)  
Python implementation: developed in the Stellar Spectroscopy group, Universidade Federal de Sergipe.
