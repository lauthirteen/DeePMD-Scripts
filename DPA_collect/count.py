import dpdata
from IPython import embed
from tqdm import tqdm
import argparse
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
        default='',
        help="txt file to output",
    )
    parsed_args = parser.parse_args(args=args)
    return parsed_args
if __name__ == '__main__':
    args = parse_args()
    dict_args = vars(args)
    datafile = dict_args['path_file']
    data_sys = open(datafile, 'r')
    data_sys = [i.strip() for i in data_sys.readlines()]
    out_file = dict_args['out_file']
    out_sys = open(out_file, 'w')
    out_sys_list = []
    all_frames = 0
    for single_system in tqdm(data_sys):
        try:
            temps = dpdata.LabeledSystem(single_system, fmt='deepmd/npy')
        except:
            print('not a system in{}'.format(single_system))
            continue
        temp_type = temps.get_atom_numbs()
        temp_nframes = temps.get_nframes()
        all_frames += temp_nframes
        temp_natoms = temps.get_natoms()
        out_sys_list.append('{}__NF_{}_TYPE_{}_NA_{}\n'.format(single_system, temp_nframes, temp_type, temp_natoms))
    out_sys.writelines(out_sys_list)
    out_sys.write('all frames: {}\n'.format(all_frames))
    out_sys.close()
    
