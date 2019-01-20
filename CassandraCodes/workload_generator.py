import numpy as np
import pandas as pd
import sys
import random
import time
import uuid
import string

system_size = 2500000000

def sys_main(row_size):

    random.seed(time.time())

    row_num = int(system_size / row_size)
    col_name = ['y_id']
    field_size = int(row_size / 10)

    # creat 10 cols
    for i in range(0, 10):
        field_name = 'field' + str(i)
        col_name.append(field_name)

    payloads = []
    payloads_size = 100
    for i in range(0, payloads_size):
        payload = ''.join([random.choice(string.ascii_letters + string.digits) for nn in range(field_size)])
        payloads.append(payload)

    # creat dataframe
    df = pd.DataFrame(columns=col_name)
    for i in range(0, row_num):
        if i % 1000 == 0:
            print(i, row_num, int(i/row_num*100), '%')
        new_col = [uuid.uuid1()]
        for j in range(1, 11):
            payload = random.sample(payloads, 1)[0]
            new_col.append(payload)
        df_t = pd.DataFrame([new_col], columns=col_name)
        df = pd.concat([df, df_t], ignore_index=True)

    df.to_csv('cassdataset.csv', sep=',', index=0)
    ids = df['y_id']
    ids.to_csv('y_id.csv', sep=',', index=0, header=True)
    return 0


if __name__ == '__main__':
    print('workload generator starts.')
    row_size = int(sys.argv[1])
    sys_main(row_size=row_size)
    print('workload is finished!')
