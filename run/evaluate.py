import xlwt
import json

def build_excel(output_path, params_list, selections_file):
    book = xlwt.Workbook()
    sh = book.add_sheet('results')

    sh.write(0, 0, 'EMDB ID')
    sh.write(0, 1, 'Start residue')
    sh.write(0, 2, 'End residue')
    sh.write(0, 3, 'RMSD')
    sh.write(0, 4, 'TMScore')
    sh.write(0, 5, 'Matching Ca %')

    # 15 characters wide
    sh.col(1).width = 256*15
    sh.col(2).width = 256*15
    # 25 characters wide
    sh.col(3).width = 256*25
    sh.col(4).width = 256*25

    if selections_file is not None:
        with open(selections_file) as f:
            selections = json.load(f)

    sum_rmsd = 0
    sum_tmscore = 0
    sum_matching_ca = 0
    count_rmsd = len(params_list)
    count_tmscore = len(params_list)
    for i in range(len(params_list)):
        emdb_id = params_list[i][0]
        sh.write(1 + i, 0, emdb_id )
        score_file_path = output_path + emdb_id + '/score/score.txt'
        score_file = open(score_file_path, 'r')

        if selections_file is not None and emdb_id in selections:
            start, end = selections[emdb_id]
        else:
            start = 'All'
            end = 'All'

        sh.write(1 + i, 1, start)
        sh.write(1 + i, 2, end)

        rmsd = score_file.readline().split()[-1]
        sh.write(1 + i, 3, float(rmsd))

        if params_list[0][4] is None:
            tmscore = score_file.readline().split()[-1]
            sh.write(1 + i, 4, tmscore)
        else:
            matching_ca = score_file.readline().split()[-1]
            sh.write(1 + i, 5, float(matching_ca))
            sum_matching_ca += float(matching_ca)
        
        try:
            sum_rmsd += float(rmsd)
        except:
            count_rmsd = count_rmsd - 1

        if params_list[0][4] is None:
            try:
                sum_tmscore += float(tmscore)
            except:
                count_tmscore = count_tmscore - 1

        score_file.close()

    sh.write(len(params_list) + 1, 0, 'Avg.')
    avg_rmsd = sum_rmsd / count_rmsd
    avg_tmscore = sum_tmscore / count_tmscore
    sh.write(len(params_list) + 1, 3, avg_rmsd)
    sh.write(len(params_list) + 1, 4, avg_tmscore)
    sh.write(len(params_list) + 1, 5, float(sum_matching_ca / count_rmsd))

    book.save(output_path + 'results.xls')
