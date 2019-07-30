import argparse
import get_simulated_data as this
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get and save simulated data and generate and save its density map')
    parser.add_argument('pdb_id', type=str, help='Name of simulated PDB')
    parser.add_argument('resolution', type=str, help='Resolution to generate simulated PDB\'s density map at')
    args = parser.parse_args()
    this.run(args.pdb_id, args.resolution)

def run(pdb_id, res):
    cwd = os.getcwd().replace(os.sep,'/') + '/'
    chimera_script = open(cwd + 'chimera_script.cmd', 'w')
    os.makedirs(cwd + pdb_id, exist_ok=True)

    # DOES NOT WORK WITH --nogui
    #chimera_script.write('open ' + pdb_id + '\n'
    #                     'write #0 ' + cwd + pdb_id + '/native.ent\n'
    #                     'molmap #0 ' + res + ' gridSpacing 1\n'
    #                     'volume #0.1 save ' + cwd + pdb_id + '/' + pdb_id + '.mrc')

    chimera_script.write('open ' + pdb_id + '.pdb\n'
                         'write #0 ' + cwd + pdb_id + '/native.ent\n'
                         'molmap #0 ' + res + ' gridSpacing 1\n'
                         'volume #0.1 save ' + cwd + pdb_id + '/' + pdb_id + '.mrc')

    chimera_script.close()
    os.system('C:/"Program Files"/"Chimera 1.13.1"/bin/chimera --nogui ' + chimera_script.name)
    os.remove(chimera_script.name)