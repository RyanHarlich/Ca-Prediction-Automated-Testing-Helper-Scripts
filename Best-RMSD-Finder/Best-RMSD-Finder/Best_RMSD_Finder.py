import argparse
import os
import xlrd
import Best_RMSD_Finder as this
import json
import xlwt
from datetime import timedelta
from distutils.dir_util import copy_tree
import traceback
import sys
import ast

__author__ = 'Michael Ryan Harlich'


class EvaluationResult:

    def __init__(self, name, num_modeled_ca, num_native_ca, num_matching_ca, matching_ca_per, rmsd, num_incorrect,
                 execution_time, fp_per):
        self.name = name
        self.num_modeled_ca = num_modeled_ca
        self.num_native_ca = num_native_ca
        self.num_matching_ca = num_matching_ca
        self.matching_ca_per = matching_ca_per
        self.rmsd = rmsd
        self.num_incorrect = num_incorrect
        self.execution_time = execution_time
        self.fp_per = fp_per

class Evaluator:
    def __init__(self):
        self.evaluation_results = []

    def load(self, best_rmsd):
        for key, item in best_rmsd.items():
            emdb_id = item['row']['EMDB_ID']
            modeled_ca = item['row']['Modeled_Ca']
            native_ca_atoms = item['row']['Native_Ca']
            total_ca = item['row']['Matching_Ca']
            maching_ca = item['row']['Matching_Ca_Perc']
            rmsd = item['row']['RMSD']
            incorrect = item['row']['Incorrect']
            execution_time = item['row']['Execution_Time']
            fp_per = item['row']['FP']
            self.evaluation_results.append(EvaluationResult(emdb_id,
                                                modeled_ca,
                                                native_ca_atoms,
                                                total_ca,
                                                maching_ca,
                                                rmsd,
                                                incorrect,
                                                execution_time,
                                                fp_per))


    def create_report(self, output_path, execution_time):
        """Creates excel document containing evaluation reports"""
        # Don't create report if there are no evaluation results
        if not self.evaluation_results:
            return

        self.evaluation_results.sort(key=lambda r: r.name)

        book = xlwt.Workbook()
        sh = book.add_sheet('results')

        sh.write(0, 0, 'EMDB ID')
        sh.write(0, 1, '# Modeled Ca Atoms')
        sh.write(0, 2, '# Native Ca Atoms')
        sh.write(0, 3, '# Matching Ca Atoms')
        sh.write(0, 4, 'Matching Percentage')
        sh.write(0, 5, 'RMSD')
        sh.write(0, 6, 'Incorrect')
        sh.write(0, 7, 'FP')
        sh.write(0, 8, 'Execution Time')

        for i in range(len(self.evaluation_results)):
            sh.write(1 + i, 0, self.evaluation_results[i].name)
            sh.write(1 + i, 1, self.evaluation_results[i].num_modeled_ca)
            sh.write(1 + i, 2, self.evaluation_results[i].num_native_ca)
            sh.write(1 + i, 3, self.evaluation_results[i].num_matching_ca)
            sh.write(1 + i, 4, self.evaluation_results[i].matching_ca_per)
            sh.write(1 + i, 5, self.evaluation_results[i].rmsd)
            sh.write(1 + i, 6, self.evaluation_results[i].num_incorrect)
            sh.write(1 + i, 7, self.evaluation_results[i].fp_per)
            sh.write(1 + i, 8, self.evaluation_results[i].execution_time)

        rmsd_avg = sum(r.rmsd for r in self.evaluation_results) / len(self.evaluation_results)
        matching_ca_per_avg = sum(r.matching_ca_per for r in self.evaluation_results) / len(self.evaluation_results)
        #execution_time_avg = sum(int(int(r.execution_time.split(':')[2]) + int(r.execution_time.split(':')[1])*60 + int(r.execution_time.split(':')[0])*60*60) for r in self.evaluation_results) / len(self.evaluation_results)
        execution_time_avg = 0
        execution_time_avg = str(timedelta(seconds=execution_time_avg))
        fp_avg = sum(r.fp_per for r in self.evaluation_results) / len(self.evaluation_results)
        sh.write(len(self.evaluation_results) + 1, 0, 'Avg.')
        sh.write(len(self.evaluation_results) + 1, 4, matching_ca_per_avg)
        sh.write(len(self.evaluation_results) + 1, 5, rmsd_avg)
        sh.write(len(self.evaluation_results) + 1, 7, fp_avg)
        sh.write(len(self.evaluation_results) + 1, 8, execution_time_avg)
        sh.write(len(self.evaluation_results) + 2, 0, 'Total')
        sh.write(len(self.evaluation_results) + 2, 8, execution_time)

        book.save(output_path)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find best RMSD')
    parser.add_argument('input', type=str, help='Folder of .xls result files from Ca protein prediction project output and json hyperparameter files that produced those results')
    parser.add_argument('output', type=str, help='Folder where json files are produced with hyperparameters with best RMSD')
    parser.add_argument('-o',  '--option', metavar='option', type=int, default=1, help='Option 1 is best RMSD focus, option 2 is best matching Ca percentage focus')
    parser.add_argument('-s',  '--sort', metavar='sort', action='store_const', const=True, default=False, help='Sorts output folders with emdb_id directories containing predicted structures to a best output folder based on the option selected')

    args = parser.parse_args()

    args.input += '/' if args.input[-1] != '/' else ''
    args.output += '/' if args.output[-1] != '/' else ''

    args.input = os.getcwd().replace(os.sep, '/') + '/' + args.input
    args.output = os.getcwd().replace(os.sep, '/') + '/' + args.output

    this.run(args.input, args.output, args.option, args.sort)



def make_blank_json_file(path, path_to_xls_file):

    best_json = open(path, 'w')

    best_json.write('{\n')

    emdb_list = dict()
    book = xlrd.open_workbook(path_to_xls_file)
    first_sheet = book.sheet_by_index(0)

    for i in range(first_sheet.nrows):
        emdb_id = first_sheet.cell(i,0).value
        if emdb_id == 'EMDB ID' or emdb_id == 'Avg.' or emdb_id == 'Total':
                continue
        emdb_list[emdb_id] = ''


    for i, (key, value) in enumerate(emdb_list.items()):
        best_json.write('  \"')

        
        best_json.write(key)

        best_json.write('\": ' + '\"' + value + '\"')

        if i < len(emdb_list) - 1:
            best_json.write(',\n')
        else:
            best_json.write('\n')
            
    best_json.write('}')    
    best_json.close()


def run(input_path, output_path, option, sort):

    params_list = [{'xls_file': xls_file, 'path_to_xls_file': input_path + xls_file, 'output_path': output_path}
                   for xls_file in filter(lambda d: os.path.isfile(input_path + d) 
                                          and (input_path + d).split('.')[-1] in ['xls'], 
                                          os.listdir(input_path))]

    for param in params_list:
        found = False
        for json_file in filter(lambda d: os.path.isfile(input_path + d) and (input_path + d).split('.')[-1] in ['json'], os.listdir(input_path)):
            if json_file.split('.')[0] == param['xls_file'].split('.')[0]:
                found = True
                break
        if found:
            continue
        else:
            this.make_blank_json_file(input_path + param['xls_file'].split('.')[0] + '.json', param['path_to_xls_file'])



    params_list = [merge(param, json_file, input_path)
                   for param in params_list for json_file in filter(lambda d: os.path.isfile(input_path + d) 
                                          and (input_path + d).split('.')[-1] in ['json'], 
                                          os.listdir(input_path)) if json_file.split('.')[0] == param['xls_file'].split('.')[0]]


    best_rmsd = this.calc_best_rmsd(params_list, option)
    this.make_json_file(params_list, best_rmsd)
    this.make_avg_file(best_rmsd, output_path)
    evaluator = Evaluator()
    evaluator.load(best_rmsd)
    evaluator.create_report(params_list[0]['output_path'] + 'best_results.xls', 0)
    if sort:
        this.sort_results(best_rmsd, output_path, input_path)

def sort_results(best_rmsd, output_path, input_path):

    os.makedirs(output_path + 'best_results', exist_ok=True)

    
    for key, item in best_rmsd.items():
        try:
            source = input_path + item['comment'].split('.')[0] + '/' + key
            destination = output_path + 'best_results' + '/' + key
            copy_tree(source, destination)
        except:
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)

def merge(param, json_file, input_path):
    param.update({'json_file': json_file, 'path_to_json_file': input_path + json_file})
    return param


def calc_best_rmsd(params_list, option):
    best_rmsd = dict()
    for i in range(len(params_list)):
        book = xlrd.open_workbook(params_list[i]['path_to_xls_file'])
        first_sheet = book.sheet_by_index(0)

        for j in range(first_sheet.nrows):
            emdb_id = first_sheet.cell(j,0).value
            if emdb_id == 'EMDB ID' or emdb_id == 'Avg.' or emdb_id == 'Total':
                continue
            rmsd = first_sheet.cell(j,5).value
            matching_percentage = first_sheet.cell(j,4).value

            try:
                if int(get_hyperparameter(params_list, emdb_id, {'comment': params_list[i]['path_to_xls_file'].split('/')[-1]})) == -1:
                    print("Skipped: " + emdb_id)
                    continue
            except:
                pass

            try:
                if -1 in ast.literal_eval(get_hyperparameter(params_list, emdb_id, {'comment': params_list[i]['path_to_xls_file'].split('/')[-1]})):
                    print("Skipped: " + emdb_id)
                    continue
            except:
                pass

            if emdb_id not in best_rmsd:
                best_rmsd[emdb_id] = {'rmsd': rmsd, 'matching_percentage': matching_percentage, 'comment': params_list[i]['path_to_xls_file'].split('/')[-1], 
                                      'row': {'EMDB_ID': first_sheet.cell(j,0).value, 
                                              'Modeled_Ca': first_sheet.cell(j,1).value, 
                                              'Native_Ca': first_sheet.cell(j,2).value, 
                                              'Matching_Ca': first_sheet.cell(j,3).value, 
                                              'Matching_Ca_Perc': first_sheet.cell(j,4).value, 
                                              'RMSD': first_sheet.cell(j,5).value, 
                                              'Incorrect': first_sheet.cell(j,6).value, 
                                              'FP': first_sheet.cell(j,7).value, 
                                              'Execution_Time': first_sheet.cell(j,8).value}}
            else:
                if option == 1:
                    if rmsd < best_rmsd[emdb_id]['rmsd'] and matching_percentage > (best_rmsd[emdb_id]['matching_percentage'] - 0.20):
                        best_rmsd[emdb_id] = {'rmsd': rmsd, 'matching_percentage': matching_percentage, 'comment': params_list[i]['path_to_xls_file'].split('/')[-1],
                                              'row': {'EMDB_ID': first_sheet.cell(j,0).value, 
                                              'Modeled_Ca': first_sheet.cell(j,1).value, 
                                              'Native_Ca': first_sheet.cell(j,2).value, 
                                              'Matching_Ca': first_sheet.cell(j,3).value, 
                                              'Matching_Ca_Perc': first_sheet.cell(j,4).value, 
                                              'RMSD': first_sheet.cell(j,5).value, 
                                              'Incorrect': first_sheet.cell(j,6).value, 
                                              'FP': first_sheet.cell(j,7).value, 
                                              'Execution_Time': first_sheet.cell(j,8).value}}
                elif option == 2:
                    if (rmsd - 1.0) < best_rmsd[emdb_id]['rmsd'] and matching_percentage > (best_rmsd[emdb_id]['matching_percentage']):
                        best_rmsd[emdb_id] = {'rmsd': rmsd, 'matching_percentage': matching_percentage, 'comment': params_list[i]['path_to_xls_file'].split('/')[-1],
                                              'row': {'EMDB_ID': first_sheet.cell(j,0).value, 
                                              'Modeled_Ca': first_sheet.cell(j,1).value, 
                                              'Native_Ca': first_sheet.cell(j,2).value, 
                                              'Matching_Ca': first_sheet.cell(j,3).value, 
                                              'Matching_Ca_Perc': first_sheet.cell(j,4).value, 
                                              'RMSD': first_sheet.cell(j,5).value, 
                                              'Incorrect': first_sheet.cell(j,6).value, 
                                              'FP': first_sheet.cell(j,7).value, 
                                              'Execution_Time': first_sheet.cell(j,8).value}}
                else:
                    print('Invalid option selected. Must be 1 or 2.')
    return best_rmsd



def get_hyperparameter(params_list, key, value):
    for i in range(len(params_list)):
        if value['comment'] == params_list[i]['xls_file']:
            with open(params_list[i]['path_to_json_file']) as f:
                json_file = json.load(f)
            hyper_parameter = json_file[key]
            return str(hyper_parameter)



def make_json_file(params_list, best_rmsd):

    best_json = open(params_list[0]['output_path'] + 'best.json', 'w')
    best_json_comments = open(params_list[0]['output_path'] + 'best_comments.json', 'w')

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
            best_json_comments.write(',' + '  # ' + value['comment'] + '\n')
        else:
            best_json.write('\n')
            best_json_comments.write('   # ' + value['comment'] + '\n')
            
    best_json.write('}')
    best_json_comments.write('}')        
    best_json.close()
    best_json_comments.close()


def make_avg_file(best_rmsd, output_path):

    counter = 0
    rmsd = 0
    matching_ca_perc = 0
    for key, item in best_rmsd.items():
        rmsd += float(item['rmsd'])
        matching_ca_perc += float(item['matching_percentage'])
        counter += 1

    avg_rmsd = rmsd / counter
    avg_matching_ca_perc = matching_ca_perc / counter

    with open(output_path + 'averages', 'w') as avg_file:
        avg_file.write('Avg. RMSD: ' + str(avg_rmsd) + '\n')
        avg_file.write('Avg. matching Ca %: ' + str(avg_matching_ca_perc))


