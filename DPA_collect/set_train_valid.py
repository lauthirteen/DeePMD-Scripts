import argparse
from typing import Dict, List, Optional
import os
import json


def parse_args(args: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-t",
        "--train",
        type=str,
        default='',
        help="txt file of train systems",
    )
    parser.add_argument(
        "-v",
        "--valid",
        type=str,
        default='',
        help="txt file of valid systems",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default='input.json',
        help="input file to be changed",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default='input_new.json',
        help="input file changed",
    )
    parser.add_argument(
        "-s",
        "--systems",
        type=str,
        default=None,
        help="which systems to set",
    )
    parsed_args = parser.parse_args(args=args)
    return parsed_args
    print(parsed_args)


if __name__ == '__main__':
    args = parse_args()
    dict_args = vars(args)
    train_systems = sorted([i.strip()
                           for i in open(dict_args['train'], 'r').readlines()])
    valid_systems = sorted([i.strip()
                           for i in open(dict_args['valid'], 'r').readlines()])
    js_old = json.load(open(dict_args['input'], 'r'))
    if 'fitting_net_dict' not in js_old['model'].keys():
        js_old['training']['training_data']['systems'] = train_systems
        js_old['training']['validation_data']['systems'] = valid_systems
        with open(dict_args['output'], 'w') as ff:
            json.dump(js_old, ff, indent=1)
        print('put {} and {} into train and valid data, and output {} done!'.format(
            dict_args['train'], dict_args['valid'], dict_args['output']))
    else:
        systems = dict_args['systems']
        assert systems is not None, 'multi-task mode must define the systems (-s) to set!'
        assert systems in js_old['model']['fitting_net_dict'].keys(), \
            'Data key {} not contained in fitting keys of {}!'.format(
                systems, dict_args['input'])
        js_old['training']['data_dict'][systems]['training_data']['systems'] = train_systems
        js_old['training']['data_dict'][systems]['validation_data']['systems'] = valid_systems
        with open(dict_args['output'], 'w') as ff:
            json.dump(js_old, ff, indent=1)
        print('put {} and {} into train and valid data of {}, and output {} done!'.format(dict_args['train'],
                                                                                          dict_args['valid'],
                                                                                          systems,
                                                                                          dict_args['output']))
