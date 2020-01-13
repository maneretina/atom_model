
import numpy as np
import pandas as pd
import os
from os.path import join as join
from itertools import combinations
import re


ion = 35009.8140

path = os.path.dirname(os.path.abspath(__file__))

dat = np.loadtxt(join(path, 'k1_nist.dat'), dtype=str)
kur = np.loadtxt(join(path, 'kuruzc.dat'), dtype=str)
# transitions = np.loadtxt(join(path, 'list_of_transitions.dat'), dtype=str)
transitions = None

def main():
    name = dat[:, 0]
    data = dat[:, 1:].astype(float)

    levels_list = pd.DataFrame(columns=['name', 'g', 'e'])

    levels_list = levels(levels_list, name, data)

    levels_list.to_csv('levels_list.dat', sep='\t', index=False)

    #  Generating transitions
    rex = re.compile('\d+')

    available_trans_ = {
        's': ['p'],
        'p': ['s', 'd'],
        'd': ['p', 'f'],
        'f': ['d'],
    }

    def check_transition(data):
        f = data[0]
        s = data[1]

        f_int = rex.findall(f)[0]
        s_int = rex.findall(s)[0]

        if int(f_int) > int(s_int):
            return False
        if f[len(f_int)] not in available_trans_:
            return False
        return s[len(s_int)] in available_trans_[f[len(f_int)]]

    global transitions
    transitions = pd.DataFrame(list(filter(check_transition, combinations(levels_list['name'], 2))))
    print(transitions)

    lower_level = transitions.iloc[:, 0]
    upper_level = transitions.iloc[:, 1]

    # ----

    #  ==============
    # loggf = kur[:, 1].astype(float)
    # j1 = kur[:, 4].astype(float)
    # name1_1 = kur[:, 5]
    # name1_2 = kur[:, 6]
    # name1 = np.char.add(name1_1, name1_2)
    # # print(name1)
    # j2 = kur[:, 8].astype(float)
    # name2_1 = kur[:, 9]
    # name2_2 = kur[:, 10]
    # name2 = np.char.add(name2_1, name2_2)
    # kur_transitions = pd.DataFrame(columns=['name1', 'name2', 'loggf', 'j1', 'j2'])
    #
    # kur_transitions = transitions1(kur_transitions, loggf, name1, name2, j1, j2, lower_level,
    #                                upper_level)
    #  ==============
    # kur_transitions
    def gen_left(x):
        return x[5] + x[6]

    def gen_right(x):
        return x[9] + x[10]

    def gen_sorted_tuple(x):
        left_num = int(rex.findall(x['left'])[0])
        right_num = int(rex.findall(x['right'])[0])

        if left_num <= right_num:
            return x['left'] + ',' + x['right']
        else:
            return x['right'] + ',' + x['left']

    df_kur = pd.DataFrame(kur)
    df_kur['left'] = df_kur.apply(gen_left, axis=1)
    df_kur['right'] = df_kur.apply(gen_right, axis=1)
    df_kur['pair'] = df_kur.apply(gen_sorted_tuple, axis=1)

    transitions.columns = ['left', 'right']
    transitions['pair'] = transitions.apply(gen_sorted_tuple, axis=1)

    kur_transitions = pd.merge(df_kur, transitions, on='pair', )
    kur_transitions.sort_values(by='pair', ascending=True, inplace=True)
    kur_transitions = kur_transitions[[1, 4, 8, 'left_x', 'right_x']].copy()
    kur_transitions.columns = ['loggf', 'j1', 'j2', 'left', 'right']
    kur_transitions = kur_transitions.astype({
        'loggf': float, 'j1': float, 'j2': float, 'left': str, 'right': str
    }, copy=False)

    # ===============
    loggf = kur_transitions['loggf']
    f = 10 ** loggf

    kur_transitions['f'] = f

    # kur_transitions.to_csv('f',float_format='%.5f',sep = '\t', index = False)
    kur_transitions.to_csv('kur_transitions.dat', sep='\t', index=False)
    '''
    for i in range(len(kur_transitions)-1):
     f= 10**loggf 
     #print ("%.4f" % f[i]) 
    kur_transitions['f'] = f
    print(kur_transitions)
    '''
    kur_final = pd.DataFrame(columns=['name1', 'name2', 'f_total'])
'''
    count_flag = False
    for i in range(len(kur_transitions) - 1):
        for k in range(len(kur_transitions) - 1):

            # for (i!=k):
            if count_flag:
                count_flag = False
                continue

            if i != k:

                if all([name1[i] == name1[k], name2[i] == name2[k], name2[i] != name2[i - 2]]):
                    # print(name1[i],name2[i])

                    count_flag = True

    for i in range(len(kur_transitions) - 2):
        if all([name1[i] == name1[i + 1], name2[i] == name2[i + 1],
                name2[i] != name2[i + 2] or name1[i] != name1[i + 2]]):
            ftot = ((2 * j1[i] + 1) * f[i] + (2 * j1[i + 1] + 1) * f[i + 1]) / (
                    (2 * j1[i] + 1) + (2 * j1[i + 1] + 1))
            # print(name1[i],name2[i],"%.4f" %ftot)
            # print(name1[i],"    ",name2[i],"     ","%.5f" %ftot)
            kur_final = kur_final.append({'name1': name1[i], 'name2': name2[i], 'f_total': ftot},
                                         ignore_index=True)

    for i in range(len(kur_transitions) - 2):
        if all([name1[i] == name1[i + 1], name2[i] == name2[i + 1], name2[i] == name2[i + 2]]):
            ftot = ((2 * j1[i] + 1) * f[i] + (2 * j1[i] + 1) * f[i + 1] + (2 * j1[i + 2] + 1) * f[
                i + 2]) / ((2 * j1[i] + 1) + (2 * j1[i + 2] + 1))
            kur_final = kur_final.append({'name1': name1[i], 'name2': name2[i], 'f_total': ftot},
                                         ignore_index=True)
    # print(name1[i],"    ",name2[i],"     ","%.5f" %ftot)

    for i in range(len(kur_transitions) - 2):
        if all([name1[i] == name1[i + 2], name2[i] == name2[i + 2],
                name2[i] != name2[i + 1] or name1[i] != name1[i + 1]]):
            ftot = ((2 * j1[i] + 1) * f[i] + (2 * j1[i] + 1) * f[i] + (2 * j1[i + 2] + 1) * f[
                i + 2]) / ((2 * j1[i] + 1) + (2 * j1[i + 2] + 1))
            kur_final = kur_final.append({'name1': name1[i], 'name2': name2[i], 'f_total': ftot},
                                         ignore_index=True)
        # print(name1[i],"    ",name2[i],"     ","%.5f" %ftot)

    kur_final.to_csv('kur_final.dat', sep='\t', index=False)

'''
def levels(levels_list, name, data):
    '''
    Функция читает названия уровней, если названия двух соседних уровней совпадают
    (но различается проекция спина), уровни объединяются. В итоге получаем список
     уникальных уровней, g-факторы и энергии ионизации
     '''

    count_flag = False
    for i in range(len(dat) - 1):
        if count_flag:
            count_flag = False
            continue
        if name[i] == name[i + 1]:
            # print(name[i])
            g_sum = (2 * data[i, 0] + 1) + (2 * data[i + 1, 0] + 1)
            en = (((2 * data[i, 0] + 1) * data[i, 1] + (2 * data[i + 1, 0] + 1) * data[
                i + 1, 1]) / ((2 * data[i, 0] + 1) + (2 * data[i + 1, 0] + 1)))
            levels_list = levels_list.append({'name': name[i], 'g': g_sum, 'e': en},
                                             ignore_index=True)
            count_flag = True
        else:
            levels_list = levels_list.append(
                {'name': name[i], 'g': 2 * data[i, 0] + 1, 'e': data[i, 1]}, ignore_index=True)
    # print(levels_list)

    e = levels_list['e']
    # print(e)

    nu = 0.2997925 * (ion - e) * 100000000000
    # print(nu)
    levels_list['energy'] = nu
    # print(levels_list)
    del levels_list['e']
    # print(levels_list)

    return levels_list


def transitions1(kur_transitions, loggf, name1, name2, j1, j2, lower_level, upper_level):
    '''Сравниваем названия уровней из списка list_of_transitions.dat и данных Куруца. Если названия как нижнего, так и верхнего уровней совпадают, записываем итоговые уровни и информацию о них в отдельный файл kur_transitios.dat (здесь еще уровни не объединены) '''
    for i in range(len(kur) - 1):
        for k in range(transitions.shape[0] - 1):
            if all([name1[i] == lower_level[k], name2[i] == upper_level[k]]):
                kur_transitions = kur_transitions.append(
                    {'name1': name1[i], 'name2': name2[i], 'loggf': loggf[i], 'j1': j1[i],
                     'j2': j2[i]}, ignore_index=True)
    # print(kur_transitions)
    # elif all([name1[i]==upper_level[k],name2[i]==lower_level[k]]):
    # print(name1[i],name2[i],gf[i],j1[i],g2[i])

    for i in range(len(kur) - 1):
        for k in range(transitions.shape[0] - 1):

            # elif all([name1[i]==lower_level[k],name2[i]==upper_level[k]]):
            if all([name1[i] == upper_level[k], name2[i] == lower_level[k]]):
                kur_transitions = kur_transitions.append(
                    {'name1': name1[i], 'name2': name2[i], 'loggf': loggf[i], 'j1': j1[i],
                     'j2': j2[i]}, ignore_index=True)
        # print(name1[i],name2[i],gf[i],j1[i],g2[i])

    # print(kur_transitions)
    # kur_transitions.to_csv('kur_transitions.dat',sep = '\t', index = False)

    return kur_transitions


if __name__ == '__main__':
    main()

