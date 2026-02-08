from faasr import faasr_get_file, faasr_put_file
import os
import pandas as pd
import numpy as np

def task_1(output_folder='data', output_1='dataset1.csv', output_2='dataset2.csv'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    length = 100
    dataset1 = np.random.rand(length)
    dataset2 = np.random.rand(length)
    df1 = pd.DataFrame(dataset1, columns=['Value'])
    df2 = pd.DataFrame(dataset2, columns=['Value'])
    df1.to_csv(os.path.join(output_folder, output_1), index=False)
    df2.to_csv(os.path.join(output_folder, output_2), index=False)
    faasr_put_file(local_folder=output_folder, local_file='dataset1.csv', remote_folder='tutorial', remote_file='dataset1.csv')
    faasr_put_file(local_folder=output_folder, local_file='dataset2.csv', remote_folder='tutorial', remote_file='dataset2.csv')