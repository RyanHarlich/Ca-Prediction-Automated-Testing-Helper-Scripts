import argparse
import os

def run(input_file):
    paths = {
        'prediction': os.getcwd() + '\\' + args.input,
        'prediction_connected': os.getcwd() + '\\' + args.input.split('.')[0] +
            '_connected.' + args.input.split('.')[-1]
    }

    missed = 0
    with open(paths['prediction'], 'r') as p_file:
        with open(paths['prediction_connected'], 'w') as p_con_file:
            for line in p_file:
                tokens = line.split()
                if len(tokens) <= 0:
                    continue
                if tokens[0] == 'TER':
                    missed += 1
                    continue
                
                if tokens[0] == 'ATOM':
                    line = line[:23] + str(int(tokens[5]) - missed).rjust(3) + line[26:]
                
                p_con_file.write(line)
            
            
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Connect predicted structures from EMD maps')
    parser.add_argument('input', type=str, help='input file')
    
    args = parser.parse_args()
       
    run(args.input)