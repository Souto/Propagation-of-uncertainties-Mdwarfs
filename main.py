import numpy as np
from spectral_lines import get_spectral_lines
from atmospheric_parameters import get_uncertainty_atmospheric
from signal_to_noise_ratio_changes import get_uncertainty_signal, dataframes as snr_dataframes
from pseudocontinuum_displacements import get_uncertainty_pseudocontinuum

ELEMENTS = ["Fe", "FeH", "CO", "OH", "H2O", "Na", "Mg", "Al", "Si", "K",
            "Ca", "Ti", "V", "Cr", "Mn", "Ni"]


def ask(prompt, default):
    """Prompt the user; return default if they press Enter without typing."""
    raw = input(prompt).strip().strip("'\"")
    return raw if raw else str(default)


def is_measurable(elemento, temperatura):
    """Return True if the element has non-zero SNR table entries at this temperature."""
    df = snr_dataframes.get(elemento)
    if df is None:
        return False
    temp_cols = [c for c in df.columns if isinstance(c, int)]
    nearest = min(temp_cols, key=lambda x: abs(x - temperatura))
    return bool(df[nearest].any())


def print_single(elemento, temperatura, sigma_teff, sigma_logg, sigma_feh,
                 sigma_xi, snr, pseudo_pct):
    atm = get_uncertainty_atmospheric(
        temperatura, sigma_teff, sigma_logg, sigma_feh, sigma_xi, elemento
    )
    snr_result  = get_uncertainty_signal(temperatura, int(snr), elemento)
    psd_result  = get_uncertainty_pseudocontinuum(temperatura, float(pseudo_pct), elemento)

    print()
    print("=" * 60)
    print(f"  Uncertainty budget for [{elemento}] (dex)")
    print("=" * 60)

    if "Erro" in atm:
        print(f"  ERROR: {atm['Erro']}")
        print("  Check that the element name is correct (case-sensitive).")
        return

    for key, val in atm.items():
        if key != "sigma(atm) [quadratic sum]":
            print(f"    {key:<35} {val:+.4f} dex")
    print(f"  {'sigma(atm) [quadratic sum]':<35} {atm['sigma(atm) [quadratic sum]']:.4f} dex")

    u_snr   = list(snr_result[0].values())[0]  if snr_result[0]  is not None else None
    u_pseudo = list(psd_result[0].values())[0] if psd_result[0]  is not None else None

    if u_snr is not None:
        print(f"  {'sigma(S/N)':<35} {u_snr:.4f} dex")
    else:
        print("  sigma(S/N): not available for this element/temperature.")

    if u_pseudo is not None:
        print(f"  {'sigma(pseudocontinuum)':<35} {u_pseudo:.4f} dex")
    else:
        print("  sigma(pseudocontinuum): not available for this element/temperature.")

    if u_snr is not None and u_pseudo is not None:
        u_atm   = atm["sigma(atm) [quadratic sum]"]
        u_total = np.sqrt(u_atm**2 + u_snr**2 + u_pseudo**2)
        print()
        print(f"  {'TOTAL uncertainty (quadratic sum)':<35} {u_total:.4f} dex")
    else:
        print()
        print("  TOTAL: could not be computed (missing component).")


def print_all(temperatura, sigma_teff, sigma_logg, sigma_feh,
              sigma_xi, snr, pseudo_pct):
    atm_all = get_uncertainty_atmospheric(
        temperatura, sigma_teff, sigma_logg, sigma_feh, sigma_xi, "all"
    )

    print()
    print("=" * 77)
    print("  Uncertainty budget — all elements (dex)")
    print(f"  T_eff={temperatura}K  σ(Teff)={float(sigma_teff):.0f}K  "
          f"σ(logg)={float(sigma_logg):.2f}  σ([Fe/H])={float(sigma_feh):.2f}  "
          f"σ(ξ)={float(sigma_xi):.2f}  S/N={snr}  psd={float(pseudo_pct):.1f}%")
    print("=" * 77)

    hdr = (f"  {'Element':>7}  {'σ(Teff)':>7}  {'σ(logg)':>7}  "
           f"{'σ([FeH])':>8}  {'σ(ξ)':>6}  │  "
           f"{'σ(atm)':>6}  {'σ(S/N)':>6}  {'σ(psd)':>6}  │  {'TOTAL':>6}")
    sep = "  " + "-" * 73
    print(hdr)
    print(sep)

    for elem in ELEMENTS:
        if not is_measurable(elem, temperatura):
            continue

        atm_e = atm_all.get(elem)
        snr_r = get_uncertainty_signal(temperatura, int(snr), elem)
        psd_r = get_uncertainty_pseudocontinuum(temperatura, float(pseudo_pct), elem)

        if atm_e is None:
            continue

        u_snr   = list(snr_r[0].values())[0] if snr_r[0]  is not None else 0.0
        u_psd   = list(psd_r[0].values())[0] if psd_r[0]  is not None else 0.0
        u_atm   = atm_e["sigma(atm)"]
        u_total = np.sqrt(u_atm**2 + u_snr**2 + u_psd**2)

        print(f"  {elem:>7}  "
              f"{atm_e['sigma(Teff)']:>+7.4f}  "
              f"{atm_e['sigma(logg)']:>+7.4f}  "
              f"{atm_e['sigma([Fe/H])']:>+8.4f}  "
              f"{atm_e['sigma(xi)']:>+6.4f}  │  "
              f"{u_atm:>6.4f}  "
              f"{u_snr:>6.4f}  "
              f"{u_psd:>6.4f}  │  "
              f"{u_total:>6.4f}")


# ── Main ─────────────────────────────────────────────────────────────────────

print("=" * 60)
print("  M-dwarf Abundance Uncertainty Propagation")
print("  Based on Melo et al. 2024 (ApJ 973, 90)")
print("=" * 60)
print()

print("--- Stellar parameters ---")
temperatura = int(ask("  Stellar T_eff (K, e.g. 3900): ", 3900))
elemento    = ask(f"  Element {ELEMENTS}\n"
                  f"  [press Enter for all elements]: ", "all")

print()
print("--- Your measurement uncertainties (1-sigma) ---")
print("  (These are the ERRORS on your derived parameters,")
print("   not the parameter values themselves.)")
print("  Press Enter to accept the default shown in brackets.")
sigma_teff = ask("  sigma(T_eff)  in K       [default: 100]: ", 100)
sigma_logg = ask("  sigma(log g) in dex      [default: 0.13]: ", 0.13)
sigma_feh  = ask("  sigma([Fe/H]) in dex     [default: 0.09]: ", 0.09)
sigma_xi   = ask("  sigma(xi)    in km/s     [default: 0.50]: ", 0.50)

print()
print("--- Spectrum quality ---")
snr = ask("  S/N of your spectrum     [table range: 40–300, default: 100]: ", 100)
print("  Pseudocontinuum displacement to test.")
print("  0.5% is estimated as half the 1% table value (linear scaling).")
pseudo_pct = ask("  Displacement in %        [0.5, 1, or 2 — default: 1]: ", 1)

print()
print("=" * 60)
print(f"  Recommended spectral lines for T_eff = {temperatura} K:")
print("=" * 60)
print(get_spectral_lines(temperatura).to_string(index=False))

if elemento.lower() == "all":
    print_all(temperatura, sigma_teff, sigma_logg, sigma_feh,
              sigma_xi, snr, pseudo_pct)
else:
    print_single(elemento, temperatura, sigma_teff, sigma_logg, sigma_feh,
                 sigma_xi, snr, pseudo_pct)
