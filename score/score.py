import tmscoring
import os

__author__ = 'Michael Ryan Harlich'


def update_paths(paths):
    paths['score'] = paths['output'] + 'score.txt'
    paths['aligned'] = paths['output'] + 'aligned.pdb'

def execute(paths):
    score(paths)

def score(paths):
    alignment = tmscoring.TMscoring(paths['partial_ground_truth'], paths['partial_prediction'])
    
    # Find the optimal alignment
    alignment.optimise()
    # Get the TM score:
    alignment.tmscore(**alignment.get_current_values())
    # Get the TM local scores:
    alignment.tmscore_samples(**alignment.get_current_values())
    # RMSD of the protein aligned according to TM score
    alignment.rmsd(**alignment.get_current_values())
    # Returns the transformation matrix between both structures:
    alignment.get_matrix(**alignment.get_current_values())
    # Save the aligned files:
    alignment.write(outputfile=paths['aligned'], appended=True)

    rmsd = tmscoring.get_rmsd(paths['partial_ground_truth'], paths['partial_prediction'])
    tmscore = tmscoring.get_tm(paths['partial_ground_truth'], paths['partial_prediction'])
    
    score_file = open(paths['score'], 'w')
    score_file.write("RMSD: " + str(rmsd) + '\n')
    score_file.write("TMScore: " + str(tmscore))
    score_file.close()

