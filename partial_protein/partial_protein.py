import os
import json
import shutil

__author__ = 'Michael Ryan Harlich'


def update_paths(paths):
    paths['partial_prediction'] = paths['output'] + 'partial_predication.ent'
    paths['partial_ground_truth'] = paths['output'] + 'partial_ground_truth.ent'

def execute(paths):
    start_residue, end_residue = get_start_and_end_residue(paths)
    save_partial_protein(start_residue, end_residue, paths)
    pass


def save_partial_protein(start_residue, end_residue, paths):
    if start_residue is None and end_residue is None:
        shutil.copyfile(paths['prediction'], paths['partial_prediction'])
        shutil.copyfile(paths['ground_truth'], paths['partial_ground_truth'])
        return
    else:
        p_file = open(paths['prediction'], 'r')
        gt_file = open(paths['ground_truth'], 'r')
        p_partial_file = open(paths['partial_prediction'], 'w')
        gt_partial_file = open(paths['partial_ground_truth'], 'w')
        save_partial_file(start_residue, end_residue, p_file, p_partial_file)
        save_partial_file(start_residue, end_residue, gt_file, gt_partial_file)
        p_file.close()
        gt_file.close()
        p_partial_file.close()
        gt_partial_file.close()
        return

def save_partial_file(start_residue, end_residue, src_file, des_file):
    for line in src_file:
        tokens = line.split()
        if tokens[0] == 'ATOM':
            if int(tokens[5]) >= int(start_residue) and int(tokens[5]) <= int(end_residue):
                des_file.write(line)


def get_start_and_end_residue(paths):
    if 'selections_file' in paths:
        emdb_id = paths['prediction'].split('/')[-2]

        with open(paths['selections_file']) as f:
            selections = json.load(f)

        if emdb_id in selections:
            return selections[emdb_id]

    return (None, None)

