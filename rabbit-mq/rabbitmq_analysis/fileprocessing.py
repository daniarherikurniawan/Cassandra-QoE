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
        if min_value < per_req_msec:
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

    max_pri = 99 # include max_pri, [0, max_pri]

    for file_index in range(0, len(filename_array)):
        filename = filename_array[file_index]
        file_data = np.loadtxt(filename)

        for priority in range(0, max_pri + 1):
            id_filter = np.where(file_data[:, 0] == priority)
            data_filter = file_data[id_filter]
            data_use = data_filter[:, 1]
            min_value = data_use.min()
            if min_value < per_req_msec:
                min_value = per_req_msec - min_value
            data_use = data_use + min_value
            filepri = priority + 1
            save_filename = folder_name + 'workload_' + str(throughput[file_index]) + '_priority_' + str(filepri) + '.txt'
            np.savetxt(save_filename, data_use)


#     for i = 1: length(filename_array)
#     filename_cell = filename_array(i);
#     filename = filename_cell
#     {1};
#     t_data = importdata(filename);
#
#     for pri = 0: max_pri
#     id_filter = find(t_data(:, 1) == pri);
#     data_filter = t_data(id_filter,:);
#     data_use = data_filter(:, 2)';
#     min_value = min(data_use);
#     if min_value < req_per_sec
#         min_value = req_per_sec - min_value;
#     end
#     data_use = data_use + min_value;
#     data_use = data_use
#     ';
#     filepri = pri + 1;
#     savefilename = ['rabbitmqdata\workload_', num2str(throughput(i)), '_priority_', num2str(filepri), '.txt'];
#     dlmwrite(savefilename, data_use)
#
#
# end
# end
    return 0


if __name__ == '__main__':
    print('Hello, file processing begins')
    FIFO_file_processing()
    Pri_file_processing()
    print('File processing ends.')