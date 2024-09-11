from collections import Counter

import numpy as np
from matchms import Spectrum
from matchms.Fragments import Fragments

from .chem import reformat_formula, ION_LST, ion_remap, formula_from_smi, all_valid_elements, ion_to_ESI
from .spectra import smile_standardizer, assign_subforms


def canonicalize_smiles(spec: Spectrum) -> Spectrum:
    spec.set("smiles", smile_standardizer.standardize_smiles(spec.get("smiles")))
    return spec


def add_formula(spec: Spectrum) -> Spectrum:
    if spec.get("formula") is None:
        spec.set("formula", formula_from_smi(spec.get("smiles")))
    return spec


def remove_mz_larger_than_precursor(spec: Spectrum) -> Spectrum:
    new_spec = spec.clone()
    if spec.get("precursor_mz") is not None:
        select = spec.mz <= spec.get("precursor_mz")
        new_spec.peaks = Fragments(mz=new_spec.mz[select], intensities=new_spec.intensities[select])
    return new_spec


def standarize_formula(spec: Spectrum) -> Spectrum:
    spec.set("standard_formula", reformat_formula(spec.get("formula")))
    return spec


def assign_subformula(spec: Spectrum) -> Spectrum:
    spec.peak_comments = None
    if not all_valid_elements(spec.get("formula")):
        return spec
    # to avoid memory error in linear programming
    if Counter(spec.get("standard_formula"))["C"] > 100:
        return spec
    adduct = spec.get("adduct")
    adduct = ion_remap.get(adduct)
    if adduct not in ION_LST:
        return spec
    ionization = ion_to_ESI(adduct)
    if adduct == "[M+H]+" or adduct == "[M-H]-":
        try:
            sub_formulas = assign_subforms(spec.get("formula"), spec.peaks.to_numpy, adduct, 15)
        except np.core._exceptions._ArrayMemoryError:
            return spec
        if sub_formulas is not None:
            look_up = dict(zip(sub_formulas["mz"], sub_formulas["formula"]))
            spec.peak_comments = [look_up.get(mz) for mz in spec.peaks.mz]
    else:
        base_adduct = "[M+H]+" if ionization == "positive" else "[M-H]-"
        try:
            sub_formulas = assign_subforms(spec.get("formula"), spec.peaks.to_numpy, adduct, 10)
            base_formulas = assign_subforms(spec.get("formula"), spec.peaks.to_numpy, base_adduct, 15)
        except np.core._exceptions._ArrayMemoryError:
            return spec
        if base_formulas is not None:
            look_up = dict(zip(base_formulas["mz"], base_formulas["formula"]))
        else:
            look_up = {}
        if sub_formulas is not None:
            look_up.update(dict(zip(sub_formulas["mz"], sub_formulas["formula"])))
        if len(look_up) > 0:
            spec.peak_comments = [look_up.get(mz) for mz in spec.peaks.mz]
    return spec


def remove_isotope(spec: Spectrum | None, instrument_type=None, m_plus_n=3) -> Spectrum | None:
    if spec is None:
        return None
    tolerance = 0.01 if instrument_type == 'Orbitrap' else 0.02
    arr = spec.peaks.to_numpy
    mz_values = arr[:, 0]
    intensities = arr[:, 1]
    remain_arr = np.ones(len(arr), dtype=bool)
    mz_offsets = 1.003355 * np.arange(1, m_plus_n + 1)
    mz_offsets_min = mz_offsets - tolerance
    mz_offsets_max = mz_offsets + tolerance
    for idx in range(len(mz_values)):
        if not remain_arr[idx]:
            continue
        mz_val = mz_values[idx]
        intensity_val = intensities[idx]
        mz_ranges_min = mz_val + mz_offsets_min
        mz_ranges_max = mz_val + mz_offsets_max
        candidates = mz_values[idx + 1:]
        intensities_candidates = intensities[idx + 1:]
        within_tolerance = ((candidates[:, None] >= mz_ranges_min) & (candidates[:, None] <= mz_ranges_max)).any(axis=1)
        less_intense = intensities_candidates < intensity_val
        isotopes = within_tolerance & less_intense
        remain_arr[idx + 1:][isotopes] = False
    filtered_arr = arr[remain_arr]
    spec.peaks = Fragments(mz=filtered_arr[:, 0], intensities=filtered_arr[:, 1])
    return spec
