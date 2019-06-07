from argparse import ArgumentParser

from path import Path
import pandas as pd


def convert(fn):
    df = pd.read_csv(fn, index_col=['depth', 'iterations'])
    df.to_latex(f'{fn.stripext()}.tex')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--file', '-f', type=str)
    flags = parser.parse_args()
    convert(Path(flags.file))
