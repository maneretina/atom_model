
import numpy as np
import pandas as pd
import os
from os.path import join as join
from itertools import combinations
import re


ion = 35009.8140

path = os.path.dirname(os.path.abspath(__file__))

'''
k1_nist.dat - пользовательские данные об атомных уровнях
kuruzc.dat - справочник, теоретические данные
'''

dat = np.loadtxt(join(path, 'k1_nist.dat'), dtype=str)

kur = np.loadtxt(join(path, 'kuruzc.dat'), dtype=str)


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


rex = re.compile('\d+')
'''
Функции gen_left() и gen_right() используются для чтения справочника, чтобы названия уровней в справочнике и у пользователя совпадали
'''
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




def main():
    name = dat[:, 0]
    data = dat[:, 1:].astype(float)

    levels_list = pd.DataFrame(columns=['name', 'g', 'e'])

    levels_list = levels(levels_list, name, data)

    levels_list.to_csv('levels_list.dat', sep='\t', index=False)

    transitions = pd.DataFrame(list(filter(check_transition, combinations(levels_list['name'], 2))))  #Из всех возможных комбинаций уровней, выбираем разрешенные       правилами отбора
    print(transitions)

    lower_level = transitions.iloc[:, 0]
    upper_level = transitions.iloc[:, 1]


    df_kur = pd.DataFrame(kur)  # справочная таблица

    df_kur['left'] = df_kur.apply(gen_left, axis=1)
    df_kur['right'] = df_kur.apply(gen_right, axis=1)

    df_kur['pair'] = df_kur.apply(gen_sorted_tuple, axis=1) # групируем верхний и нижний уровень, чтобы переход просходил с меньшего n на большее

    transitions.columns = ['left', 'right']

    transitions['pair'] = transitions.apply(gen_sorted_tuple, axis=1)

    kur_transitions = pd.merge(df_kur, transitions, on='pair', ) # в справочнике ищем только те переходы, которые задействованы в нашей модели

    kur_transitions.sort_values(by='pair', ascending=True, inplace=True)

    kur_transitions = kur_transitions[[1, 4, 8, 'left_x', 'right_x']].copy()
    kur_transitions.columns = ['loggf', 'j1', 'j2', 'left', 'right']

    kur_transitions = kur_transitions.astype({
        'loggf': float, 'j1': float, 'j2': float, 'left': str, 'right': str
    }, copy=False)

    loggf = kur_transitions['loggf']
    kur_transitions.to_csv('kur_transitions.dat', sep='\t', index=False)


if __name__ == '__main__':
    main()
