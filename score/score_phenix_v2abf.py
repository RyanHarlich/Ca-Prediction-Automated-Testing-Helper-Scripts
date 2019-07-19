import os

__author__ = 'Michael Ryan Harlich'


def update_paths(paths):
    paths['score'] = paths['output'] + 'score.txt'

def execute(paths):
    score(paths)

def score(paths):
    try:
        # On my local computer: C:\Users\RyanHarlich\Phenix\phenix-installer-1.16-3549-intel-windows-x86_64\build\bin\phenix.chain_comparison.bat
        # On DAIS 3: /home/NETID/harlicm7/phenix-installer-1.16-3549-intel-linux-2.6-x86_64-centos6/build/bin/phenix.chain_comparison 
        f = os.popen(paths['phenix_chain_comparison_path'] + ' ' + paths['partial_prediction'] + ' ' + paths['partial_ground_truth'] + ' | grep \'Unique_target\'')
        line = ''
        for i in f.readlines():
            line = i

    
        line = line.split()
    
        rmsd = line[1]
        matching_ca_perc = line[9]
    except Exception:
        rmsd = str(-1)
        matching_ca_perc = str(-1)


    score_file = open(paths['score'], 'w')
    score_file.write("RMSD: " + str(rmsd) + '\n')
    score_file.write("Matching Ca %: " + matching_ca_perc + '\n')
    score_file.close()