from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import numpy as np
import pandas as pd

def task_4(folder='tutorial', input1='dataset1.csv', input2='dataset2.csv', output1='summed_result.csv'):
    os.makedirs(folder, exist_ok=True)
    path1 = os.path.join(folder, input1)
    path2 = os.path.join(folder, input2)
    out_path = os.path.join(folder, output1)
    faasr_get_file(remote_folder=folder, remote_file='dataset1.csv', local_file='tutorial/dataset1.csv')
    faasr_get_file(remote_folder=folder, remote_file='dataset2.csv', local_file='tutorial/dataset2.csv')
    df1 = pd.read_csv(path1, header=None)
    df2 = pd.read_csv(path2, header=None)
    matrix1 = df1.values
    matrix2 = df2.values
    summed = matrix1 + matrix2
    print('Summed Result Matrix:')
    print(summed)
    result_df = pd.DataFrame(summed)
    result_df.to_csv(out_path, index=False, header=False)
    faasr_put_file(local_file='tutorial/summed_result.csv', remote_folder=folder, remote_file='summed_result.csv')
    print(f'Summed result saved to: {out_path}')