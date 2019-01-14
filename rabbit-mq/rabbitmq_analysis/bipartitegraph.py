import sys
import load_curve as lc
import pandas as pd
import numpy as np
import time
import getSession as gs
import random


inf = 1e10
eps = 1e-6
qoe_curve_filename = 'qoe_bins'

num_a = 0
num_b = 0
num_c = 0

def dfs(x, matchx, matchy, lx, ly, visx, visy, slack, weight):
    visx[x] = True
    for y in range(0, len(ly)):
        if visy[y]:
            continue
        tmp = lx[x] + ly[y] - weight[x][y]
        if abs(tmp) <= eps:
            visy[y] = True
            if matchy[y] == -1 or dfs(matchy[y], matchx, matchy, lx, ly, visx, visy, slack, weight):
                matchx[x] = y
                matchy[y] = x
                return True
        else:
            slack[y] = min(slack[y], tmp)
    return False


def bipartite_graph(weight):
    num = len(weight)
    answer_qoe = 0
    matchx = [-1] * num
    matchy = [-1] * num

    lx = []
    ly = [0] * num

    slack = []

    for i in range(0, num):
        lx.append(-inf)
        for j in range(0, num):
            # print(i, j, weight[0][0])
            lx[i] = max(lx[i], weight[i][j])

    for i in range(0, num):
        for j in range(0, num):
            if len(slack) >= j+1:
                slack[j] = inf
            else:
                slack.append(inf)
        while True:
            visx = [False] * num
            visy = [False] * num
            if dfs(i, matchx, matchy, lx, ly, visx, visy, slack, weight) == True:
                break
            temp = inf
            for j in range(0, num):
                if visy[j] == False:
                    temp = min(temp, slack[j])
            for j in range(0, num):
                if visx[j] == True:
                    lx[j] -= temp
            for j in range(0, num):
                if visy[j] == True:
                    ly[j] += temp
                else:
                    slack[j] -= temp


    for i in range(0, num):
        answer_qoe += weight[i][matchx[i]]

    return matchx, answer_qoe

def GreedyImportance(weight):
    num = len(weight)
    flagx = [False] * num
    flagy = [False] * num
    matchx = [0] * num
    matchy = [0] * num
    for i in range(0, num):
        t_max = -inf
        x_index = 0
        y_index = 0
        for j in range(0, num):
            for k in range(0, num):
                if flagx[j]==False and flagy[k]==False and weight[j][k] > t_max:
                    t_max = weight[j][k]
                    x_index = j
                    y_index = k
        flagx[x_index] = True
        flagy[y_index] = True
        matchx[x_index] = y_index
        matchy[y_index] = x_index

    answer_qoe = 0.0
    for i in range(0, num):
        answer_qoe += w[i][matchx[i]]

    return answer_qoe

def GreedySlope(bk_latency, nbk_latency, load_data):

    answer_qoe = 0.0
    task_num = len(bk_latency)
    bk_latency.sort()
    nbk_latency.sort(key = lambda ele: gs.QoESlope(ele, load_data), reverse = True)

    for i in range(0, task_num):
        answer_qoe += gs.QoECurve(bk_latency[i] + nbk_latency[i], load_data)

    '''
    test
    '''
    # answer_qoe = 0.0
    # for i in range(0, task_num):
    #     if nbk_latency[i] < 1200 or nbk_latency[i] > 4000:
    #         answer_qoe += gs.QoECurve(bk_latency[i] + nbk_latency[i], load_data)
    '''
    test
    '''
    return answer_qoe

def filterData(ori):
    # pages = ['SearchResults', 'Apps/Games PDP', 'PDP', 'SFW Category Page Template', 'RefineList']
    pages = ['Apps/Games PDP']
    ori = ori[ori['TTOL'] <200000]
    ori = ori[ori['non_backend'] > 10]

    ori = ori[(ori['pageType'].isin(pages))]
    return ori

def make_graph(load_data):
    bin_num = len(load_data)

    task_num = 200
    file = 'AM_12'
    ori_data = pd.read_csv('data_hourly/' + file)
    ori_data = filterData(ori_data)

    # bk_latency_all = ori_data['real_backend'].tolist()
    # np.savetxt('ALL_backend_RefineList.txt',  np.array(bk_latency_all), delimiter=',')

    o_data_sample = ori_data.sample(n=task_num, random_state=int(time.time()), axis=0)

    nb_delay = []
    b_delay = []

    random.seed(time.time())
    for index, row in o_data_sample.iterrows():

        nb_delay.append(row['non_backend'])
        b_delay.append(row['real_backend'])
        # kk = random.randint(30, 2000)
        # b_delay.append(kk)

        # global g_bk_latency,g_nbk_latnency
        # g_bk_latency.append(row['real_backend'])
        # # g_nbk_latnency.append(kk)
        # g_nbk_latnency.append(row['non_backend'])

        # if row['non_backend'] < 1200:
        #     global num_a
        #     num_a += 1
        # elif row['non_backend'] < 4035:
        #     global num_b
        #     num_b += 1
        # else:
        #     global num_c
        #     num_c += 1

    task_num = len(nb_delay)
    '''
    Adjust the percentage of ABC
    '''
    # task_num = 150
    # b_delay = []
    # nb_delay = []
    # for i in range(0, int(task_num/2)):
    #     b_delay.append(random.randint(50, 80))
    #     b_delay.append(random.randint(1200, 2200))
    #     nb_delay.append(random.randint(800, 1220))
    #     nb_delay.append(random.randint(4035, 7200))
    #
    # for i in range(0, int(task_num/18)):
    #     b_delay.append(random.randint(50, 80))
    #     b_delay.append(random.randint(1200, 2200))
    #     nb_delay.append(random.randint(1220, 1700))
    #     nb_delay.append(random.randint(1220, 1700))
    #
    # task_num = len(b_delay)

    '''
    End test
    '''

    w = []
    for i in range(0, task_num):
        w.append([])
        for j in range(0, task_num):
            w[i].append(0.0)
    for i in range(0, task_num):
        for j in range(0, task_num):
            w[i][j] = (gs.QoECurve(nb_delay[i] + b_delay[j], load_data))

    '''
    waiting for delete
    '''

    original_qoe = 0.0
    zero_qoe = 0.0
    for i in range(0, task_num):
        original_qoe += gs.QoECurve(nb_delay[i] + b_delay[i],load_data)
        zero_qoe += gs.QoECurve(nb_delay[i], load_data)

    '''
    waiting for delete
    '''
    answer_qoe = GreedySlope(bk_latency=b_delay, nbk_latency=nb_delay, load_data= load_data)
    return w, answer_qoe, original_qoe, zero_qoe

def make_graph_queueing():
    task_num = 200
    job_length = 2
    bk_latency = []
    nbk_latency = []
    random.seed(time.time())
    for i in range(0, task_num):
        bk = random.randint(2, job_length * task_num)
        bk_latency.append(bk  + 0.0)
        nbk = random.randint(100, 700)
        nbk_latency.append(nbk + 0.0)


    w = []
    for i in range(0, task_num):
        w.append([])
        for j in range(0, task_num):
            w[i].append(0.0)
    for i in range(0, task_num):
        for j in range(0, task_num):
            w[i][j] = lc.qoe_latency(nbk_latency[i] + bk_latency[j])

    answer_qoe = 0.0
    bk_latency.sort()
    nbk_latency.sort(key = lambda ele: lc.qoe_latency_slope(ele), reverse = True)
    # print(nbk_latency)
    # print(bk_latency)
    for i in range(0, task_num):
        answer_qoe += lc.qoe_latency(bk_latency[i] + nbk_latency[i])
    return w, answer_qoe


def make_graph_Example(load_data):
    task_num = 50
    bk_latency = []
    nbk_latency = []
    random.seed(time.time())
    for i in range(0, task_num):
        dice = random.random()
        bk = 0
        nbk = 0
        if dice<0.5:
            bk = random.randint(150, 300)
            nbk = 20
        else:
            bk = random.randint(550, 900)
            nbk = 300
        bk_latency.append(bk + 0.0)
        nbk_latency.append(nbk + 0.0)

    w = []
    for i in range(0, task_num):
        w.append([])
        for j in range(0, task_num):
            w[i].append(0.0)
    for i in range(0, task_num):
        for j in range(0, task_num):
            w[i][j] = lc.qoe_latency(nbk_latency[i] + bk_latency[j])

    answer_qoe = 0.0

    return w, answer_qoe

def getcurve(filename):

    load_data = np.genfromtxt(filename, delimiter='\t')
    bin_num = len(load_data)
    min_qoe_scale = 1.0
    min_qoe = 0.2
    x_scale = 0.7
    y_scale = 1.9

    for xx in range(0, bin_num):
        load_data[xx][1] = (load_data[xx][1] - min_qoe_scale) * y_scale + min_qoe
        load_data[xx][0] = load_data[xx][0] * x_scale

    return load_data

if __name__ == '__main__':
    print('Hello World')
    qoe_curve = getcurve(qoe_curve_filename)
    optimal_counter = 0.0
    importance_counter = 0.0
    slope_counter = 0.0
    original_counter = 0.0
    zero_counter = 0.0


    for times in range(0, 20):
        w, slope_matching, original_matching, zero_matching = make_graph(qoe_curve)
        # w, slope_matching = make_graph_queueing()
        # w, greedy_matching = make_graph_Example(qoe_curve)

        optimal_matching = bipartite_graph(w)
        # importance_matching = GreedyImportance(w)

        optimal_counter += optimal_matching
        slope_counter += slope_matching

        zero_counter += zero_matching
        original_counter += original_matching

        print('Optimal:', optimal_matching, 'Slope:', slope_matching, 'Original:', original_matching, 'Zero:', zero_matching)
        print('Gain Opt:', optimal_matching/original_matching -1, 'Slope:', slope_matching/original_matching-1, 'Zero:', zero_matching/original_matching -1)
        # importance_counter += importance_matching
        # print('Optimal:', optimal_matching, 'Slope:',slope_matching, 'Importance:', importance_matching)
        # print('Slope Gain:', optimal_matching/slope_matching -1, 'Importance Gain', optimal_matching/importance_matching -1)
    # print('Slope Gain:', optimal_counter/slope_counter -1)
    print('Gain Opt:', optimal_counter / original_counter - 1, 'Slope:', slope_counter / original_counter - 1,
          'Zero:', zero_counter / original_counter - 1)

    # print(num_a, num_b, num_c)

