# CSTR: Chemical Structure Transformer Ranker

The **Chemical Structure Transformer Ranker (CSTR)** is a tool designed to rank and generate chemical structures based
on MS/MS spectrum data.
It leverages transformers to perform de novo chemical structure generation and ranking of candidate molecules.

## Installation

We recommend using [conda](https://docs.anaconda.com/miniconda/) to create a virtual environment and install the dependencies.

```bash
conda create -n CSTR python=3.10
conda activate CSTR
```

To install the package, run the following command:

```bash
pip install CSTR
```

To test the installation, run the following command:

```bash
cstr --help
```

If the installation is successful, you should see the help message for the CSTR CLI.

## Usage Instructions

We provide example data in the `example` directory to demonstrate the usage of CSTR.
You can use the example data to test the CLI commands.

### De Novo Generation of Chemical Structures

To start the de novo generation, you must provide an MS/MS spectrum in either an MSP or MGF file format.
The file must have a .msp or .mgf extension. One file can only contain one spectrum.

The essential properties required in the file are:

* FORMULA: Molecular formula of the compound.
* IONMODE: Ionization mode (positive or negative).
* PRECURSOR_MZ: Precursor mass/charge ratio.
* ADDUCT: The adduct form.

One example of such a file is provided in the `example/lipid.mgf` file.

To annotate the molecular formula, you can use external tools like [Buddy](https://github.com/Philipbear/msbuddy)
or [SIRIUS](https://www.google.com/search?client=safari&rls=en&q=sirius+bocker&ie=UTF-8&oe=UTF-8).

To generate one structure, run the following command:

```bash
cstr generate <path_to_msp_or_mgf_file>
```

You can enable stream mode to actually see the generation process:

```bash
cstr generate --stream <path_to_msp_or_mgf_file>
```

To generate 10 structures using beam search, run the following command:

```bash
cstr propose --beam 10 <path_to_msp_or_mgf_file>
```

### Ranking Candidate Structures

To rank candidate chemical structures, provide the MS/MS spectrum file along with a file containing candidate structures
in SMILES format.

A recommended approach is to annotate the molecular formula first, then retrieve the candidate structures with the
same molecular formula from a database like PubChem.

The candidate SMILES should be stored in a .txt file, with one SMILES string per line.

One example of the candidate SMILES file is provided in the `example/isomers.txt` file.

To rank the candidate structures based on the MS/MS spectrum:

```bash
cstr rank <path_to_msp_or_mgf_file> --candidates <path_to_candidate_smiles_file>
```