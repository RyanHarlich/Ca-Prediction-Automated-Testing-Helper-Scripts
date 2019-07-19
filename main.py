import argparse
from run.run import run
import os

__author__ = 'Michael Ryan Harlich'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get TMscore and RMSD of partial protein')
    parser.add_argument('input', type=str, help='Folder containing ground truth of protein and prediction or protein')
    parser.add_argument('output', type=str, help='Folder where partial proteins will be stored and resulting TMscore and RMSD')
    parser.add_argument('-s', '--selections', metavar='Selections', type=str, help='JSON file with starting and ending residue')
    parser.add_argument('-p', '--phenixpath', metavar='PhenixPath', type=str, help='Absolute path to phenix.chain_comparison.bat')
    parser.add_argument('-a', '--tmalignpath', metavar='TMAlignPath', type=str, help='Absolute path to TMAlign executable (linux verison only)')

    args = parser.parse_args()

    args.input += '/' if args.input[-1] != '/' else ''
    args.output += '/' if args.output[-1] != '/' else ''

    args.input = os.getcwd().replace(os.sep, '/') + '/' + args.input
    args.output = os.getcwd().replace(os.sep, '/') + '/' + args.output
    if args.selections is not None:
        args.selections = os.getcwd().replace(os.sep, '/') + '/' + args.selections
    if args.tmalignpath is not None:
        args.tmalignpath = os.getcwd().replace(os.sep, '/') + '/' + args.tmalignpath

    run(args.input, args.output, args.selections, args.phenixpath, args.tmalignpath)
