import pandas as pd
import random
import string

payload = 2000  #1000 - 1K; 1000000 - 1M
top_num = min(60000, int(1000000000/payload))

def change_pay_load(file_name, payload, top_num):

    df =pd.read_csv(file_name, sep = '|')
    df = df.head(top_num)
    newphone = []
    row_num = len(df)
    for i in range(0, row_num):
        newstring = ''.join(random.choices(string.ascii_letters + string.digits, k=payload))
        newphone.append(newstring)

    new_df = pd.DataFrame({'phone': newphone})
    df.update(new_df)
    df.to_csv(filename, sep = '|', index=False)
    return 0

if __name__ == '__main__':
    for i in range(1, 11):
        filename = 'data-users-' + str(i) + '.csv'
        change_pay_load(filename, payload, top_num)
