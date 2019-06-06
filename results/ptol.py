from argparse import ArgumentParser

from path import Path
import pandas as pd


parser = ArgumentParser()
parser.add_argument('--file', '-f', type=str)
flags = parser.parse_args()
fn = Path(flags.file)

df = pd.read_csv(fn, index_col=['depth', 'iterations'])
df.to_latex(f'{fn.stripext()}.tex')
