from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import json
import numpy as np
import csv

def task_2(folder='tutorial', input1='config.json', output1='dataset1.csv'):
    faasr_get_file(remote_folder=folder, remote_file='config.json', local_file='tutorial/config.json')
    os.makedirs(folder, exist_ok=True)
    config_path = os.path.join(folder, input1)
    with open(config_path, 'r') as f:
        config = json.load(f)
    rows = config.get('rows', 5)
    cols = config.get('cols', 5)
    int_min = config.get('int_min', 0)
    int_max = config.get('int_max', 100)
    matrix = np.random.randint(int_min, int_max + 1, size=(rows, cols))
    output_path = os.path.join(folder, output1)
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in matrix:
            writer.writerow(row)
    print(f'Generated {rows}x{cols} matrix saved to {output_path}')
    faasr_put_file(local_file='tutorial/dataset1.csv', remote_folder=folder, remote_file='dataset1.csv')