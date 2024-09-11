import re
from functools import reduce

import numpy as np
import torch
from rdkit import Chem
from rdkit import RDLogger
from rdkit.Chem import Atom
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

P_TBL = Chem.GetPeriodicTable()

ROUND_FACTOR = 4

ELECTRON_MASS = 0.00054858

CHEM_FORMULA_SIZE = re.compile("([A-Z][a-z]*)([0-9]*)")

VALID_ELEMENTS = ["C", "H", "As", "B", "Br", "Cl", "Co", "F", "Fe",
                  "I", "K", "N", "Na", "O", "P", "S", "Se", "Si", ]
VALID_ATOM_NUM = [Atom(i).GetAtomicNum() for i in VALID_ELEMENTS]

CHEM_ELEMENT_NUM = len(VALID_ELEMENTS)

ATOM_NUM_TO_ONEHOT = torch.zeros((max(VALID_ATOM_NUM) + 1, CHEM_ELEMENT_NUM))

# Convert to onehot
ATOM_NUM_TO_ONEHOT[VALID_ATOM_NUM, torch.arange(CHEM_ELEMENT_NUM)] = 1

VALID_MONO_MASSES = np.array(
    [P_TBL.GetMostCommonIsotopeMass(i) for i in VALID_ELEMENTS]
)
CHEM_MASSES = VALID_MONO_MASSES[:, None]

ELEMENT_VECTORS = np.eye(len(VALID_ELEMENTS))
ELEMENT_VECTORS_MASS = np.hstack([ELEMENT_VECTORS, CHEM_MASSES])
ELEMENT_TO_MASS = dict(zip(VALID_ELEMENTS, CHEM_MASSES.squeeze()))

ELEMENT_DIM_MASS = len(ELEMENT_VECTORS_MASS[0])
ELEMENT_DIM = len(ELEMENT_VECTORS[0])

# Reasonable normalization vector for elements
# Estimated by max counts (+ 1 when zero)
NORM_VEC = np.array([81, 158, 2, 1, 3, 10, 1, 17,
                     1, 6, 1, 19, 2, 34, 6, 6, 2, 6])

NORM_VEC_NL_MASS_INT = np.array(NORM_VEC.tolist() * 2 + [1471] * 3 + [1])

NORM_VEC_MASS = np.array(NORM_VEC.tolist() + [1471])

# Assume 64 is the highest repeat of any 1 atom
MAX_ELEMENT_NUM = 64

element_to_ind = dict(zip(VALID_ELEMENTS, np.arange(len(VALID_ELEMENTS))))
element_to_position = dict(zip(VALID_ELEMENTS, ELEMENT_VECTORS))
element_to_position_mass = dict(zip(VALID_ELEMENTS, ELEMENT_VECTORS_MASS))

ION_LST = [
    "[M+H]+",
    "[M+Na]+",
    "[M+K]+",
    "[M-H2O+H]+",
    "[M+H3N+H]+",
    "[M]+",
    "[M-H4O2+H]+",
    "[M-H]-",
    "[M+Cl]⁻",
    "[M+Br]⁻",
    "[M-H20-H]-",
    "[M+HCOOH-H]-",
    "[M+CH3COOH-H]-"
]

ion_remap = dict(zip(ION_LST, ION_LST))
ion_remap.update(
    {
        "[M+NH4]+": "[M+H3N+H]+",
        "M+H": "[M+H]+",
        "M+Na": "[M+Na]+",
        "M+H-H2O": "[M-H2O+H]+",
        "M-H2O+H": "[M-H2O+H]+",
        "M+NH4": "[M+H3N+H]+",
        "M-2H2O+H": "[M-H4O2+H]+",
        "[M-2H2O+H]+": "[M-H4O2+H]+",
        "M-H2O-H": "[M-H20-H]-",
        "M+HCOOH-H": "[M+HCOOH-H]-",
        "[M+FA-H]-": "[M+HCOOH-H]-",
        "[M+Hac-H]-": "[M+CH3COOH-H]-",
        "[M+HCOO]-": "[M+HCOOH-H]-",
        "[M+CH3COO]-": "[M+CH3COOH-H]-",
    }
)

ion_to_idx = dict(zip(ION_LST, np.arange(len(ION_LST))))

ion_to_mass = {
    "[M+H]+": ELEMENT_TO_MASS["H"] - ELECTRON_MASS,
    "[M+Na]+": ELEMENT_TO_MASS["Na"] - ELECTRON_MASS,
    "[M+K]+": ELEMENT_TO_MASS["K"] - ELECTRON_MASS,
    "[M-H2O+H]+": -ELEMENT_TO_MASS["O"] - ELEMENT_TO_MASS["H"] - ELECTRON_MASS,
    "[M+H3N+H]+": ELEMENT_TO_MASS["N"] + ELEMENT_TO_MASS["H"] * 4 - ELECTRON_MASS,
    "[M]+": 0 - ELECTRON_MASS,
    "[M-H4O2+H]+": -ELEMENT_TO_MASS["O"] * 2 - ELEMENT_TO_MASS["H"] * 3 - ELECTRON_MASS,
    "[M-H]-": -ELEMENT_TO_MASS["H"] + ELECTRON_MASS,
    "[M+Cl]⁻": ELEMENT_TO_MASS["Cl"] + ELECTRON_MASS,
    "[M+Br]⁻": ELEMENT_TO_MASS["Br"] + ELECTRON_MASS,
    "[M-H20-H]-": -ELEMENT_TO_MASS["O"] - ELEMENT_TO_MASS["H"] * 3 + ELECTRON_MASS,
    "[M+HCOOH-H]-": ELEMENT_TO_MASS["C"] + ELEMENT_TO_MASS["O"] * 2 + ELEMENT_TO_MASS["H"] + ELECTRON_MASS,
    "[M+CH3COOH-H]-": ELEMENT_TO_MASS["C"] + ELEMENT_TO_MASS["O"] * 2 + ELEMENT_TO_MASS["H"] * 3 + ELECTRON_MASS,
}

ion_to_add_vec = {
    "[M+H]+": element_to_position["H"],
    "[M+Na]+": element_to_position["Na"],
    "[M+K]+": element_to_position["K"],
    "[M-H2O+H]+": -element_to_position["O"] - element_to_position["H"],
    "[M+H3N+H]+": element_to_position["N"] + element_to_position["H"] * 4,
    "[M]+": np.zeros_like(element_to_position["H"]),
    "[M-H4O2+H]+": -element_to_position["O"] * 2 - element_to_position["H"] * 3,
    "[M-H]-": -element_to_position["H"],
    "[M+Cl]⁻": element_to_position["Cl"],
    "[M+Br]⁻": element_to_position["Br"],
    "[M-H20-H]-": -element_to_position["O"] - element_to_position["H"] * 3,
    "[M+HCOOH-H]-": element_to_position["C"] + element_to_position["O"] * 2 + element_to_position["H"],
    "[M+CH3COOH-H]-": element_to_position["C"] + element_to_position["O"] * 2 + element_to_position["H"] * 3,
}


def ion_to_ESI(x): return "positive" if x.strip()[-1] == "+" else "negative"


# Define rdbe mult
rdbe_mult = np.zeros_like(ELEMENT_VECTORS[0])
els = ["C", "N", "P", "H", "Cl", "Br", "I", "F"]
weights = [2, 1, 1, -1, -1, -1, -1, -1]
for k, v in zip(els, weights):
    rdbe_mult[element_to_ind[k]] = v


def all_valid_elements(chem_formula: str) -> bool:
    """
    Check if the chemical formula is all valid elements
    """
    for (chem_symbol, num) in re.findall(CHEM_FORMULA_SIZE, chem_formula):
        if chem_symbol not in VALID_ELEMENTS:
            return False
    return True


def _cross_sum(x, y):
    """cross_sum."""
    return (np.expand_dims(x, 0) + np.expand_dims(y, 1)).reshape(-1, y.shape[-1])


def _get_all_subsets_dense(
        dense_formula: str,
        element_vectors: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    non_zero = np.argwhere(dense_formula > 0).flatten()

    vectorized_formula = []
    for nonzero_ind in non_zero:
        temp = element_vectors[nonzero_ind] * np.arange(
            0, dense_formula[nonzero_ind] + 1
        ).reshape(-1, 1)
        vectorized_formula.append(temp)

    zero_vec = np.zeros((1, element_vectors.shape[-1]))
    cross_prod = reduce(_cross_sum, vectorized_formula, zero_vec)

    cross_prod_inds = _rdbe_filter(cross_prod)
    cross_prod = cross_prod[cross_prod_inds]
    all_masses = cross_prod.dot(VALID_MONO_MASSES)
    return cross_prod, all_masses


def get_all_subsets(chem_formula: str) -> tuple[np.ndarray, np.ndarray]:
    dense_formula = formula_to_dense(chem_formula)
    return _get_all_subsets_dense(dense_formula, element_vectors=ELEMENT_VECTORS)


def _rdbe_filter(cross_prod):
    """rdbe_filter.
    Args:
        cross_prod:
    """
    rdbe_total = 1 + 0.5 * cross_prod.dot(rdbe_mult)
    filter_inds = np.argwhere(rdbe_total >= 0).flatten()
    return filter_inds


def formula_to_dense(chem_formula: str) -> np.ndarray:
    """
    Convert chemical formula to element counts vector

    chem_formula: str

    return: np.ndarray of vector with size 18
    """
    total_onehot = []
    for (chem_symbol, num) in re.findall(CHEM_FORMULA_SIZE, chem_formula):
        # Convert num to int
        num = 1 if num == "" else int(num)
        one_hot = element_to_position[chem_symbol].reshape(1, -1)
        one_hot_repeats = np.repeat(one_hot, repeats=num, axis=0)
        total_onehot.append(one_hot_repeats)

    # Check if null
    if len(total_onehot) == 0:
        dense_vec = np.zeros(len(element_to_position))
    else:
        dense_vec = np.vstack(total_onehot).sum(0)

    return dense_vec


def formula_to_dense_mass(chem_formula: str) -> np.ndarray:
    """
    Convert chemical formula to element counts vector with mass

    chem_formula: str

    return: np.ndarray of vector
    """
    total_onehot = []
    for (chem_symbol, num) in re.findall(CHEM_FORMULA_SIZE, chem_formula):
        # Convert num to int
        num = 1 if num == "" else int(num)
        one_hot = element_to_position_mass[chem_symbol].reshape(1, -1)
        one_hot_repeats = np.repeat(one_hot, repeats=num, axis=0)
        total_onehot.append(one_hot_repeats)

    # Check if null
    if len(total_onehot) == 0:
        dense_vec = np.zeros(len(element_to_position_mass["H"]))
    else:
        dense_vec = np.vstack(total_onehot).sum(0)

    return dense_vec


def formula_to_dense_mass_norm(chem_formula: str) -> np.ndarray:
    """formula_to_dense_mass_norm.

    Return formula including full compound mass and normalized

    Args:
        chem_formula (str): Input chemical formal
    Return:
        np.ndarray of vector

    """
    dense_vec = formula_to_dense_mass(chem_formula)
    dense_vec = dense_vec / NORM_VEC_MASS

    return dense_vec


def formula_mass(chem_formula: str) -> float:
    """get formula mass"""
    mass = 0
    for (chem_symbol, num) in re.findall(CHEM_FORMULA_SIZE, chem_formula):
        # Convert num to int
        num = 1 if num == "" else int(num)
        mass += ELEMENT_TO_MASS[chem_symbol] * num
    return mass


def formula_to_dict(chem_formula: str) -> dict:
    """formula_to_dict."""
    items = list()
    for (chem_symbol, num) in re.findall(CHEM_FORMULA_SIZE, chem_formula):
        # Convert num to int
        num = 1 if num == "" else int(num)
        items.append((chem_symbol, num))
    sorted_items = sorted(items, key=lambda x: x[0])
    return dict(sorted_items)


def vec_to_formula(form_vec: np.ndarray) -> str:
    """vec_to_formula."""
    build_str = ""
    for i in np.argwhere(form_vec > 0).flatten():
        el = VALID_ELEMENTS[i]
        ct = int(form_vec[i])
        new_item = f"{el}{ct}" if ct > 1 else f"{el}"
        build_str = build_str + new_item
    return build_str


def formula_from_smi(smi: str) -> str:
    """
    Get formula from SMILES

    Args:
        smi (str): SMILES string

    Return:
        str: Chemical formula
    """
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        raise ValueError(f"Invalid smiles {smi}")
    else:
        return CalcMolFormula(mol)


class SmilesStandardizer:
    """
    Standardize smiles
    """

    def standardize_smiles(self, smi):
        """Standardize smiles string"""
        try:
            mol = Chem.MolFromSmiles(smi)
            return self.standardize_mol(mol)
        except TypeError:
            return ''

    def standardize_mol(self, mol) -> str:
        """Standardize smiles string"""
        # sanitize
        Chem.SanitizeMol(mol)
        return Chem.MolToSmiles(mol, isomericSmiles=False, canonical=True)


standardizer = SmilesStandardizer()


def canonicalize_smiles(smi: str) -> str:
    """canonicalize_smiles."""
    return standardizer.standardize_smiles(smi)


def min_formal_from_smi(smi: str):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return 0
    else:
        formal = np.array([j.GetFormalCharge() for j in mol.GetAtoms()])
        return formal.min()


def max_formal_from_smi(smi: str):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return 0
    else:
        formal = np.array([j.GetFormalCharge() for j in mol.GetAtoms()])
        return formal.max()


def atoms_from_smi(smi: str) -> int:
    """atoms_from_smi.

    Args:
        smi (str): smi

    Return:
        int
    """
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return 0
    else:
        return mol.GetNumAtoms()


def add_ion(form: str, ion: str):
    """add_ion.
    Args:
        form (str): form
        ion (str): ion
    """
    ion_vec = ion_to_add_vec[ion]
    form_vec = formula_to_dense(form)
    return vec_to_formula(form_vec + ion_vec)


def clipped_ppm(mass_diff: np.ndarray, parentmass: np.ndarray) -> np.ndarray:
    """clipped_ppm.

    Args:
        mass_diff (np.ndarray): mass_diff
        parentmass (np.ndarray): parentmass

    Returns:
        np.ndarray:
    """
    parentmass_copy = parentmass * 1
    parentmass_copy[parentmass < 200] = 200
    ppm = mass_diff / parentmass_copy * 1e6
    return ppm


def clipped_ppm_single(
        cls_mass_diff: float,
        parentmass: float,
):
    """clipped_ppm_single.

    Args:
        cls_mass_diff (float): cls_mass_diff
        parentmass (float): parentmass
    """
    div_factor = 200 if parentmass < 200 else parentmass
    cls_ppm = cls_mass_diff / div_factor * 1e6
    return cls_ppm


def reformat_formula(formula: str) -> str:
    elements = formula_to_dict(formula)
    reformatted = ''.join([k * v for k, v in elements.items() if k != "H"])
    return reformatted


def is_valid_smiles(smiles: str, formula: str) -> bool:
    """
    Check if the smiles is valid based on the formula
    :param smiles:
    :param formula:
    :return:
    """
    # turn off the logging
    lg = RDLogger.logger()
    lg.setLevel(RDLogger.CRITICAL)
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False
    else:
        mol_form = CalcMolFormula(mol)
        return reformat_formula(mol_form) == reformat_formula(formula)
