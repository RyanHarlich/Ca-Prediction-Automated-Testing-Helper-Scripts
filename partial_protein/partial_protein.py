import os
import json
import shutil
import time

__author__ = 'Michael Ryan Harlich'


def update_paths(paths):
    paths['partial_prediction'] = paths['output'] + 'partial_predication.ent'
    paths['partial_ground_truth'] = paths['output'] + 'partial_ground_truth.ent'
    paths['aligned_prediction'] = paths['output'] + 'aligned_prediction.pdb'

def execute(paths):
    align(paths)
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
        #if 'phenix_chain_comparison_path' not in paths:
        #    p_partial_file = open(paths['partial_prediction'], 'w')
        #    save_partial_file(start_residue, end_residue, p_file, p_partial_file)
        #    p_partial_file.close()   
        #else:
        #    shutil.copyfile(paths['prediction'], paths['partial_prediction'])
        p_partial_file = open(paths['partial_prediction'], 'w')
        save_partial_file(start_residue, end_residue, p_file, p_partial_file)
        p_partial_file.close()  
        
        gt_partial_file = open(paths['partial_ground_truth'], 'w')
        save_partial_file(start_residue, end_residue, gt_file, gt_partial_file)
        gt_partial_file.close()       
        
        p_file.close()
        gt_file.close()
        
        
        return

def save_partial_file(start_residue, end_residue, src_file, des_file):
    for line in src_file:
        tokens = line.split()
        if len(tokens) > 0:
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

def align(paths):
    try:
        os.system(paths['tmalign_path'] + ' ' + paths['prediction'] + ' ' + paths['ground_truth'] + ' -o ' + paths['output'] + 'TM.sup')
        time.sleep(1)
        ap_file = open(paths['aligned_prediction'], 'w')
        tm_sup = open(paths['output'] + 'TM.sup_all', 'r')
        on = False
        for line in tm_sup:
            tokens = line.split()
            if len(tokens) > 0:
                if tokens[0] == 'TER':
                    on = False
            if on == True:
                    ap_file.write(line)
            if len(tokens) > 1:
                if tokens[1] == 'Aligned':
                    on = True
        ap_file.close()
        tm_sup.close()
    except Exception:
        print('Error aligning')
        pass