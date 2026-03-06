from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import random

def task_1(folder='tutorial', output1='file1.csv', output2='file2.csv'):
    os.makedirs(folder, exist_ok=True)
    values1 = [random.randint(1, 100) for _ in range(10)]
    values2 = [random.randint(1, 100) for _ in range(10)]
    path1 = os.path.join(folder, output1)
    with open(path1, mode='w', encoding='utf-8', newline='\n') as f:
        f.write('value\n')
        for v in values1:
            f.write(f'{v}\n')
    path2 = os.path.join(folder, output2)
    with open(path2, mode='w', encoding='utf-8', newline='\n') as f:
        f.write('value\n')
        for v in values2:
            f.write(f'{v}\n')
    sums = [v1 + v2 for v1, v2 in zip(values1, values2)]
    result_path = os.path.join(folder, 'result.csv')
    with open(result_path, mode='w', encoding='utf-8', newline='\n') as f:
        f.write('value\n')
        for s in sums:
            f.write(f'{s}\n')
    faasr_put_file(local_file='tutorial/file1.csv', remote_folder=folder, remote_file='file1.csv')
    faasr_put_file(local_file='tutorial/file2.csv', remote_folder=folder, remote_file='file2.csv')