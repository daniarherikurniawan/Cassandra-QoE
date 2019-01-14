import numpy as np
import pandas as pd
import sys
import random


folder_name = 'rabbitmqdata/'


def FIFO_file_processing():

    throughput = [90, 95, 100, 105, 110, 115, 120]
    per_req_msec = 30

    filename_array = []

    for thrs in throughput:
        filename = 'results_onerf_fifo/workload_'+str(thrs)+'.txt'
        filename_array.append(filename)

    for index in range(0, len(filename_array)):
        filename = filename_array[index]
        t_data = np.loadtxt(filename)
        data_use = t_data[:, 1]
        min_value = data_use.min()
        min_value = per_req_msec - min_value
        data_use = data_use + min_value
        save_filename = folder_name + 'workload_' + str(throughput[index]) + '_fifo.txt'
        np.savetxt(save_filename, data_use)

    return 0

def Pri_file_processing():

    throughput = [90, 95, 100, 105, 110, 115, 120]
    per_req_msec = 10

    filename_array = []

    for thrs in throughput:
        filename = 'results_onerf_priority/workload_'+str(thrs)+'.txt'
        filename_array.append(filename)

    max_pri = 19 # include max_pri, [0, max_pri]

    for file_index in range(0, len(filename_array)):
        filename = filename_array[file_index]
        file_data = np.loadtxt(filename)

        t_file_data = file_data[:, 1]
        min_value = t_file_data.min()
        min_value = per_req_msec - min_value

        for priority in range(0, max_pri + 1):
            id_filter = np.where(file_data[:, 0] == priority)
            data_filter = file_data[id_filter]
            data_use = data_filter[:, 1]
            data_use = data_use + min_value
            filepri = priority + 1
            save_filename = folder_name + 'workload_' + str(throughput[file_index]) + '_priority_' + str(filepri) + '.txt'
            np.savetxt(save_filename, data_use)

    return 0


if __name__ == '__main__':
    print('Hello, file processing begins')
    FIFO_file_processing()
    Pri_file_processing()
    print('File processing ends.')