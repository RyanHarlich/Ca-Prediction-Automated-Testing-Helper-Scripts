import partial_protein.partial_protein as partial
import score.score as score
import os
import sys
from multiprocessing import cpu_count, Pool
import traceback
from .evaluate import build_excel

__author__ = 'Michael Ryan Harlich'

PIPELINE = [
    partial,
    score
]

def run(input_path, output_path, selections_file):
    params_list = [(emdb_id, input_path, output_path, selections_file) 
                   for emdb_id in filter(lambda d: os.path.isdir(input_path + d), os.listdir(input_path))]

    os.system("rm " + output_path + "* -r")

    pool = Pool(min(cpu_count(), len(params_list)))
    pool.map(run_steps, params_list)

    build_excel(output_path, params_list, selections_file)


def run_steps(params):
    emdb_id, input_path, output_path, selections_file = params
    paths = make_paths(input_path, emdb_id, selections_file)

    for step in PIPELINE:
        paths['output'] = output_path + emdb_id + '/' + step.__name__.split('.')[0] + '/'
        os.makedirs(paths['output'], exist_ok=True)
        try:
            step.update_paths(paths)
            step.execute(paths)
        except:
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)


def make_paths(input_path, emdb_id, selections_file):
    prediction_file = get_file(input_path + emdb_id, ['pdb', 'ent'])
    gt_file = get_file(input_path + emdb_id, ['pdb', 'ent'], ['native'])
    paths = {
        'prediction': input_path + emdb_id + '/' + prediction_file,
        'ground_truth': input_path + emdb_id + '/' + gt_file
    }

    if selections_file is not None:
        paths['selections_file'] = selections_file

    return paths


def get_file(path, allowed_extensions, filename=None):
    if filename is None:
        file = next(f for f in os.listdir(path) if f.split('.')[-1] in allowed_extensions and f.split('.')[0] not in ['native'])
    else:
        file = next(f for f in os.listdir(path) if f.split('.')[-1] in allowed_extensions and f.split('.')[0] in filename)
    return file
    
    
