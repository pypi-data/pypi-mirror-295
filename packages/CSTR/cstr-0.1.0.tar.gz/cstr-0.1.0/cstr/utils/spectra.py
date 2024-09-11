from typing import Sequence

import numpy as np
import torch

from .chem import (
    vec_to_formula,
    get_all_subsets,
    ion_to_mass,
    clipped_ppm,
    SmilesStandardizer,
    formula_to_dense,
)


def assign_subforms(form: str, spec: np.ndarray, adduct, mass_diff_thresh=15) -> dict[str, list] | None:
    """
    Assign subformulas to peaks in a spectrum

    form: The molecular formula of the precursor
    spec: The spectrum
    adduct: The adduct
    mass_diff_thresh: The mass difference threshold (ppm)
    """
    cross_prod, masses = get_all_subsets(form)
    spec_masses, spec_intens = spec[:, 0], spec[:, 1]

    ion_masses = ion_to_mass[adduct]
    masses_with_ion = masses + ion_masses
    ion_types = np.array([adduct] * len(masses_with_ion))

    mass_diffs = np.abs(spec_masses[:, None] - masses_with_ion[None, :])

    formula_inds = mass_diffs.argmin(-1)
    min_mass_diff = mass_diffs[np.arange(len(mass_diffs)), formula_inds]
    rel_mass_diff = clipped_ppm(min_mass_diff, spec_masses)

    # Filter by mass diff threshold (ppm)
    valid_mask = rel_mass_diff < mass_diff_thresh
    spec_masses = spec_masses[valid_mask]
    spec_intens = spec_intens[valid_mask]
    min_mass_diff = min_mass_diff[valid_mask]
    formula_inds = formula_inds[valid_mask]

    formulas = np.array([vec_to_formula(j) for j in cross_prod[formula_inds]])
    formula_masses = masses_with_ion[formula_inds]
    ion_types = ion_types[formula_inds]

    # Build mask for uniqueness on formula and ionization
    # note that ionization are all the same for one subformula assignment
    # hence we only need to consider the uniqueness of the formula
    formula_idx_dict = {}
    uniq_mask = []
    for idx, formula in enumerate(formulas):
        uniq_mask.append(formula not in formula_idx_dict)
        gather_ind = formula_idx_dict.get(formula, None)
        if gather_ind is None:
            continue
        spec_intens[gather_ind] += spec_intens[idx]
        formula_idx_dict[formula] = idx

    spec_masses = spec_masses[uniq_mask]
    spec_intens = spec_intens[uniq_mask]
    min_mass_diff = min_mass_diff[uniq_mask]
    formula_masses = formula_masses[uniq_mask]
    formulas = formulas[uniq_mask]

    # To calculate explained intensity, preserve the original normalized
    # intensity
    if spec_intens.size == 0:
        result = None
    else:
        result = {
            "mz": list(spec_masses),
            "ms2_inten": list(spec_intens),
            "mono_mass": list(formula_masses),
            "abs_mass_diff": list(min_mass_diff),
            "formula": list(formulas),
        }
    return result


smile_standardizer = SmilesStandardizer()


def _tensorize_peak(ion: int, formula: str, intensity: float, precursor_tensor: torch.Tensor) -> torch.Tensor:
    """
    Tensorize a single fragment peak

    formula: The subformula of the peak
    intensity: The relative intensity of the peak
    precursor_tensor: The precursor tensor

    Returns: A tensor of shape (2*len(valid_atoms)+1) = 36 + 2 = 38
    """
    frag_tensor = torch.from_numpy(formula_to_dense(formula))
    nl_tensor = precursor_tensor - frag_tensor
    return torch.cat([frag_tensor, nl_tensor, torch.tensor([intensity]), torch.tensor([ion])])


def tensorize_peaks(sub_formulas: Sequence, intensities: Sequence, precursor_formula: str, adduct: str) -> torch.Tensor:
    """
    Tensorize a list of fragment peaks

    sub_formulas: A list of subformulas
    intensities: A list of intensities
    precursor_formula: The precursor formula

    Returns: A tensor of shape (num_peaks, 2*len(valid_atoms)+1+1)
    """
    assert sub_formulas is not None
    ion = 0 if adduct.strip()[-1] == "+" else 1
    precursor_tensor = torch.from_numpy(formula_to_dense(precursor_formula))
    peaks = torch.stack([_tensorize_peak(ion, formula, intensity, precursor_tensor)
                         for formula, intensity in zip(sub_formulas, intensities)
                         if formula is not None])
    return peaks
