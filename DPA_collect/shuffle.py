from IPython import embed
from tqdm import tqdm
import argparse
from random import shuffle
from typing import Dict, List, Optional
def parse_args(args: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-i",
        "--path_file",
        type=str,
        default='.',
        help="path file to explore",
    )
    parser.add_argument(
        "-o",
        "--out_file",
        type=str,
        default='.',
        help="path file to save random",
    )
    parsed_args = parser.parse_args(args=args)
    return parsed_args
if __name__ == '__main__':
    args = parse_args()
    dict_args = vars(args)
    datafile = dict_args['path_file']
    outfile = dict_args['out_file']
    data_sys = open(datafile, 'r')
    data_sys = data_sys.readlines()
    shuffle(data_sys)
    data_sys_rf = open(outfile, 'w')
    data_sys_rf.writelines(data_sys)
    data_sys_rf.close()
