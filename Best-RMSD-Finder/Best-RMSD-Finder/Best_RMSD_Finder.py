import argparse
import os
import xlrd
import Best_RMSD_Finder as this
import json

__author__ = 'Michael Ryan Harlich'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find best RMSD')
    parser.add_argument('input', type=str, help='Folder of .xls result files from Ca protein prediction project output and json hyperparameter files that produced those results')
    parser.add_argument('output', type=str, help='Folder where json files are produced with hyperparameters with best RMSD')

    args = parser.parse_args()

    args.input += '/' if args.input[-1] != '/' else ''
    args.output += '/' if args.output[-1] != '/' else ''

    args.input = os.getcwd().replace(os.sep, '/') + '/' + args.input
    args.output = os.getcwd().replace(os.sep, '/') + '/' + args.output

    this.run(args.input, args.output)



def run(input_path, output_path):

    params_list = [(xls_file, input_path + xls_file, output_path) 
                   for xls_file in filter(lambda d: os.path.isfile(input_path + d) 
                                          and (input_path + d).split('.')[-1] in ['xls'], 
                                          os.listdir(input_path))]

    params_list = [param + (json_file, input_path + json_file) 
                   for param in params_list for json_file in filter(lambda d: os.path.isfile(input_path + d) 
                                          and (input_path + d).split('.')[-1] in ['json'], 
                                          os.listdir(input_path)) if json_file.split('.')[0] == param[0].split('.')[0]]

    best_rmsd = this.calc_best_rmsd(params_list)
    this.make_json_file(params_list, best_rmsd)



def calc_best_rmsd(params_list):
    best_rmsd = dict()
    for i in range(len(params_list)):
        book = xlrd.open_workbook(params_list[i][1])
        first_sheet = book.sheet_by_index(0)

        for j in range(first_sheet.nrows):
            emdb_id = first_sheet.cell(j,0).value
            if emdb_id == 'EMDB ID' or emdb_id == 'Avg.' or emdb_id == 'Total':
                continue
            rmsd = first_sheet.cell(j,5).value
            matching_percentage = first_sheet.cell(j,4).value

            if emdb_id not in best_rmsd:
                best_rmsd[emdb_id] = (rmsd, matching_percentage, params_list[i][1].split('/')[-1])
            else:
                if rmsd < best_rmsd[emdb_id][0] and matching_percentage > (best_rmsd[emdb_id][1] - 0.20):
                    best_rmsd[emdb_id] = (rmsd, matching_percentage, params_list[i][1].split('/')[-1])
    return best_rmsd



def get_hyperparameter(params_list, key, value):
    for i in range(len(params_list)):
        if value[2] == params_list[i][0]:
            with open(params_list[i][4]) as f:
                json_file = json.load(f)
            hyper_parameter = json_file[key]
            return str(hyper_parameter)



def make_json_file(params_list, best_rmsd):

    best_json = open(params_list[0][2] + 'best.json', 'w')
    best_json_comments = open(params_list[0][2] + 'best_comments.json', 'w')

    best_json.write('{\n')
    best_json_comments.write('{\n')

    for i, (key, value) in enumerate(best_rmsd.items()):
        best_json.write('  \"')
        best_json_comments.write('  \"')

        
        best_json.write(key)
        best_json_comments.write(key)

        best_json.write('\": ' + get_hyperparameter(params_list, key, value))
        best_json_comments.write('\": ' + get_hyperparameter(params_list, key, value))

        if i < len(best_rmsd) - 1:
            best_json.write(',\n')
            best_json_comments.write(',' + '  # ' + value[2] + '\n')
        else:
            best_json.write('\n')
            best_json_comments.write('   # ' + value[2] + '\n')
            
    best_json.write('}')
    best_json_comments.write('}')        
    best_json.close()
    best_json_comments.close()
