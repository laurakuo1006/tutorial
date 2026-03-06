from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import json
import numpy as np

def task_3(folder='tutorial', input1='config.json', output1='dataset2.csv'):
    faasr_get_file(remote_folder=folder, remote_file='config.json', local_file='tutorial/config.json')
    os.makedirs(folder, exist_ok=True)
    config_path = os.path.join(folder, input1)
    with open(config_path, 'r') as f:
        config = json.load(f)
    rows = config.get('rows', 5)
    cols = config.get('cols', 5)
    min_val = config.get('min', 0)
    max_val = config.get('max', 100)
    matrix = np.random.randint(min_val, max_val + 1, size=(rows, cols))
    output_path = os.path.join(folder, output1)
    np.savetxt(output_path, matrix, delimiter=',', fmt='%d')
    print(f'Generated dataset2.csv with shape ({rows}, {cols}) and values in range [{min_val}, {max_val}]')
    faasr_put_file(local_file='tutorial/dataset2.csv', remote_folder=folder, remote_file='dataset2.csv')