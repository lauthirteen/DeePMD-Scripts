import argparse
from typing import Dict, List, Optional
import os
import glob
def parse_args(args: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-p",
        "--data_path",
        type=str,
        default='.',
        help="data path to explore",
    )
    parser.add_argument(
        "-o",
        "--out_file",
        type=str,
        default='',
        help="txt file to output",
    )
    parsed_args = parser.parse_args(args=args)
    return parsed_args
if __name__ == '__main__':
    args = parse_args()
    dict_args = vars(args)
    output = open(dict_args['out_file'], 'w')
    data_sys = []
    dirs = glob.glob(dict_args['data_path'])
    for di in dirs:
        for root, dirs, files in os.walk(di):
            for name in files:    
                if 'type.raw' in name and dirs:
                    data_sys.append(root)
                continue
    output.writelines(["{}\n".format(i) for i in sorted(data_sys)])
    output.close() 
