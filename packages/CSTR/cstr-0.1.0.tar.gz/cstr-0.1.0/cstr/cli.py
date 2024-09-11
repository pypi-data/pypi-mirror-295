from pathlib import Path

import click
from matchms import Spectrum
from matchms.importing import load_from_mgf, load_from_msp

from .predictor import Predictor
from .preprocessor import check, preprocess
from .utils.chem import canonicalize_smiles


def import_spectrum(input: str) -> Spectrum | None:
    sufix = Path(input).suffix
    if sufix == ".mgf":
        spectra = list(load_from_mgf(input))
    elif sufix == ".msp":
        spectra = list(load_from_msp(input))
    else:
        click.echo("Input file must be in mgf or msp format.")
        return None
    if len(spectra) != 1:
        click.echo("Input file must contain exactly one spectrum.")
        return None
    try:
        check(spectra[0])
    except AssertionError as e:
        click.echo(e)
        return None
    return preprocess(spectra[0])


@click.group()
def cli():
    pass


@cli.command()
@click.argument('input', type=str)
@click.option('--stream', is_flag=True, help="Stream the output")
def generate(input, stream):
    """
    Generate one SMILES from MS/MS spectra

    :param input: MS/MS spectrum (mgf or msp)
    :param stream: Enable streaming output
    :return: SMILES notation of the annotated metabolite structure
    """
    sp = import_spectrum(input)
    if sp is None:
        click.echo("Preprocessing failed.")
        return
    model = Predictor()
    if stream:
        for token in model(sp):
            click.echo(token, nl=False)
        click.echo()
    else:
        smiles = [token for token in model(sp)]
        click.echo("".join(smiles))


@cli.command()
@click.argument('input', type=str)
@click.option('--beam', type=int, default=5, help="Beam width for beam search")
@click.option('--alpha', type=float, default=0.75, help="Alpha value for length normalization")
def propose(input, beam, alpha):
    """
    Generate many SMILES using beam search

    :param input: MS/MS spectrum (mgf or msp)
    :param beam: Beam width for beam search
    :param alpha: Alpha value for length normalization
    :return: Ranked list of SMILES notation of generated metabolite structures
    """
    sp = import_spectrum(input)
    if sp is None:
        click.echo("Preprocessing failed.")
        return
    model = Predictor()
    ranked = model.beam_predict(sp, beam, alpha)
    smiles_list = [smiles for smiles, _ in ranked]
    for smiles in smiles_list:
        click.echo(smiles)


@cli.command()
@click.argument('input', type=str)
@click.option('--candidates', type=click.File('r'), help="TXT file containing candidate SMILES, one per line",
              required=True)
def rank(input, candidates):
    """
    Rank the candidate SMILES based on MS/MS spectra

    :param input: MS/MS spectrum (mgf or msp)
    :param candidates: File containing candidate SMILES
    :return: Ranked list of candidate SMILES, together with their scores
    """
    sp = import_spectrum(input)
    if sp is None:
        click.echo("Preprocessing failed.")
        return
    model = Predictor()
    smiles = [line.strip() for line in candidates]
    canonical_smiles = [canonicalize_smiles(smile) for smile in smiles]
    scores = [model.sample_prob(sp, smile) for smile in canonical_smiles]
    ranked = sorted(zip(smiles, scores), key=lambda x: x[1], reverse=True)
    click.echo("Candidate SMILES:\tScore")
    for smile, score in ranked:
        click.echo(f"{smile}:\t{score:.4f}")


if __name__ == '__main__':
    cli()
