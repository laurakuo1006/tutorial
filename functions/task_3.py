import os
import pandas as pd
import numpy as np

def task_3(folder='tutorial', input1='summed_dataset.csv', output1='summed_dataset.csv'):
    faasr_get_file(remote_folder=folder, remote_file='summed_dataset.csv', local_file='summed_dataset.csv')
    os.makedirs(folder, exist_ok=True)
    length = 100
    data1 = np.random.randint(0, 100, size=length)
    data2 = np.random.randint(0, 100, size=length)
    summed = data1 + data2
    df_summed = pd.DataFrame(summed, columns=['sum'])
    output_path = os.path.join(folder, output1)
    df_summed.to_csv(output_path, index=False)
    faasr_put_file(local_file='summed_dataset.csv', remote_folder=folder, remote_file='summed_dataset.csv')