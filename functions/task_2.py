from faasr import faasr_get_file, faasr_put_file
import os
import pandas as pd

def task_2(output_folder='data', input_1='dataset1.csv', input_2='dataset2.csv', output_1='summed_dataset.csv'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    input_path_1 = os.path.join(output_folder, input_1)
    input_path_2 = os.path.join(output_folder, input_2)
    output_path_1 = os.path.join(output_folder, output_1)
    faasr_get_file(remote_folder='tutorial', remote_file='dataset1.csv', local_folder=output_folder, local_file='dataset1.csv')
    faasr_get_file(remote_folder='tutorial', remote_file='dataset2.csv', local_folder=output_folder, local_file='dataset2.csv')
    dataset1 = pd.read_csv(input_path_1)
    dataset2 = pd.read_csv(input_path_2)
    summed_dataset = dataset1 + dataset2
    summed_dataset.to_csv(output_path_1, index=False)
    faasr_put_file(local_folder=output_folder, local_file='summed_dataset.csv', remote_folder='tutorial', remote_file='summed_dataset.csv')