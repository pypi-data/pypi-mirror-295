import matchms.filtering as filtering
from matchms import Spectrum

from .utils import annotating


def check(spec: Spectrum) -> Spectrum:
    assert spec.get("precursor_mz") is not None
    assert spec.get("formula") is not None
    assert spec.get("adduct") is not None
    return spec


def preprocess(spec: Spectrum) -> Spectrum | None:
    spec = filtering.default_filters(spec)
    spec = filtering.add_parent_mass(spec)
    spec = annotating.remove_mz_larger_than_precursor(spec)
    spec = annotating.remove_isotope(spec)
    spec = filtering.select_by_relative_intensity(spec, intensity_from=0.01)
    spec = filtering.reduce_to_number_of_peaks(spec, 1, 128)
    spec = filtering.normalize_intensities(spec)
    spec = annotating.standarize_formula(spec)
    spec = annotating.assign_subformula(spec)
    if spec.peak_comments is None:
        return None
    return spec
