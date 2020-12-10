import csv
import cpsc2018
import os
import argparse
import numpy as np
import sys

'''
cspc2018_challenge score
Written by:  Xingyao Wang, Feifei Liu, Chengyu Liu
             School of Instrument Science and Engineering
             Southeast University, China
             chengyu@seu.edu.cn
'''

'''
Score the prediction answers by comparing answers.csv and REFERENCE.csv in validation_set folder,
The scoring uses a F1 measure, which is an average of the nice F1 values from each classification
type. The specific score rules will be found on http://www.icbeb.org/Challenge.html.
Matrix A follows the format as:
                                     Predicted
                      Normal  AF  I-AVB  LBBB  RBBB  PAC  PVC  STD  STE
               Normal  N11   N12   N13   N14   N15   N16  N17  N18  N19
               AF      N21   N22   N23   N24   N25   N26  N27  N28  N29
               I-AVB   N31   N32   N33   N34   N35   N36  N37  N38  N39
               LBBB    N41   N42   N43   N44   N45   N46  N47  N48  N49
Reference      RBBB    N51   N52   N53   N54   N55   N56  N57  N58  N59
               PAC     N61   N62   N63   N64   N65   N66  N67  N68  N69
               PVC     N71   N72   N73   N74   N75   N76  N77  N78  N79
               STD     N81   N82   N83   N84   N85   N86  N87  N88  N89
               STE     N91   N92   N93   N94   N95   N96  N97  N98  N99

For each of the nine types, F1 is defined as:
Normal: F11=2*N11/(N1x+Nx1) AF: F12=2*N22/(N2x+Nx2) I-AVB: F13=2*N33/(N3x+Nx3) LBBB: F14=2*N44/(N4x+Nx4) RBBB: F15=2*N55/(N5x+Nx5)
PAC: F16=2*N66/(N6x+Nx6)    PVC: F17=2*N77/(N7x+Nx7)    STD: F18=2*N88/(N8x+Nx8)    STE: F19=2*N99/(N9x+Nx9)

The final challenge score is defined as:
F1 = (F11+F12+F13+F14+F15+F16+F17+F18+F19)/9

In addition, we alse calculate the F1 measures for each of the four sub-abnormal types:
            AF: Faf=2*N22/(N2x+Nx2)                         Block: Fblock=2*(N33+N44+N55)/(N3x+Nx3+N4x+Nx4+N5x+Nx5)
Premature contraction: Fpc=2*(N66+N77)/(N6x+Nx6+N7x+Nx7)    ST-segment change: Fst=2*(N88+N99)/(N8x+Nx8+N9x+Nx9)

The static of predicted answers and the final score are saved to score.txt in local path.
'''

def score(answers_csv_path, reference_csv_path):
    answers = dict()
    reference = dict()
    A = np.zeros((9, 9), dtype=np.float)
    with open(answers_csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            answers.setdefault(row['Recording'], []).append(row['Result'])
            # answers.setdefault(row['RECORDS'], []).append(row['classifyResult'])
        f.close()
    with open(reference_csv_path) as ref:
        reader = csv.DictReader(ref)
        for row in reader:
            reference.setdefault(row['Recording'], []).append([row['First_label'], row['Second_label'], row['Third_label']])
        ref.close()

    for key in answers.keys():
        value = []
        for item in answers[key]:
            predict = np.int(item)
        for item in reference[key][0]:
            if item == '':
                item = 0
            value.append(np.int(item))

        if predict in value:
            A[predict-1][predict-1] += 1
        else:
            A[value[0]-1][predict-1] += 1

    F11 = 2 * A[0][0] / (np.sum(A[0, :]) + np.sum(A[:, 0]))
    F12 = 2 * A[1][1] / (np.sum(A[1, :]) + np.sum(A[:, 1]))
    F13 = 2 * A[2][2] / (np.sum(A[2, :]) + np.sum(A[:, 2]))
    F14 = 2 * A[3][3] / (np.sum(A[3, :]) + np.sum(A[:, 3]))
    F15 = 2 * A[4][4] / (np.sum(A[4, :]) + np.sum(A[:, 4]))
    F16 = 2 * A[5][5] / (np.sum(A[5, :]) + np.sum(A[:, 5]))
    F17 = 2 * A[6][6] / (np.sum(A[6, :]) + np.sum(A[:, 6]))
    F18 = 2 * A[7][7] / (np.sum(A[7, :]) + np.sum(A[:, 7]))
    F19 = 2 * A[8][8] / (np.sum(A[8, :]) + np.sum(A[:, 8]))

    F1 = (F11+F12+F13+F14+F15+F16+F17+F18+F19) / 9

    ## following is calculating scores for 4 types: AF, Block, Premature contraction, ST-segment change.

    Faf = 2.0 * A[1][1] / (np.sum(A[1, :]) + np.sum(A[:, 1]))
    Fblock = 2.0 * (A[2][2] + A[3][3] + A[4][4]) / (np.sum(A[2:5, :]) + np.sum(A[:, 2:5]))
    Fpc = 2.0 * (A[5][5] + A[6][6]) / (np.sum(A[5:7, :]) + np.sum(A[:, 5:7]))
    Fst = 2.0 * (A[7][7] + A[8][8]) / (np.sum(A[7:9, :]) + np.sum(A[:, 7:9]))

    # print(A)
    print('Total File Number: ', np.sum(A))

    print("F11: ", F11)
    print("F12: ", F12)
    print("F13: ", F13)
    print("F14: ", F14)
    print("F15: ", F15)
    print("F16: ", F16)
    print("F17: ", F17)
    print("F18: ", F18)
    print("F19: ", F19)
    print("F1: ", F1)

    print("Faf: ", Faf)
    print("Fblock: ", Fblock)
    print("Fpc: ", Fpc)
    print("Fst: ", Fst)

    with open('score.txt', 'w') as score_file:
        # print >> score_file, A
        print >> score_file, 'Total File Number: %d\n' %(np.sum(A))
        print >> score_file, 'F11: %0.3f' %F11
        print >> score_file, 'F12: %0.3f' %F12
        print >> score_file, 'F13: %0.3f' %F13
        print >> score_file, 'F14: %0.3f' %F14
        print >> score_file, 'F15: %0.3f' %F15
        print >> score_file, 'F16: %0.3f' %F16
        print >> score_file, 'F17: %0.3f' %F17
        print >> score_file, 'F18: %0.3f' %F18
        print >> score_file, 'F19: %0.3f\n' %F19
        print >> score_file, 'F1: %0.3f\n' %F1
        print >> score_file, 'Faf: %0.3f' %Faf
        print >> score_file, 'Fblock: %0.3f' %Fblock
        print >> score_file, 'Fpc: %0.3f' %Fpc
        print >> score_file, 'Fst: %0.3f' %Fst

        score_file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r',
                        '--reference_path',
                        help='path saving reference file')

    args = parser.parse_args()
    score('answers.csv', args.reference_path)
    # score('./score_test/classifyResult_random.csv', args.recording_path)
