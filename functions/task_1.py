from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import random

def task_1(folder='tutorial', output1='file1.csv', output2='file2.csv'):
    os.makedirs(folder, exist_ok=True)
    random.seed(42)
    values1 = [random.randint(1, 100) for _ in range(10)]
    values2 = [random.randint(1, 100) for _ in range(10)]
    path1 = os.path.join(folder, output1)
    path2 = os.path.join(folder, output2)
    with open(path1, 'w') as f:
        for v in values1:
            f.write(f'{v}\n')
    with open(path2, 'w') as f:
        for v in values2:
            f.write(f'{v}\n')
    faasr_put_file(local_file='tutorial/file1.csv', remote_folder=folder, remote_file='file1.csv')
    faasr_put_file(local_file='tutorial/file2.csv', remote_folder=folder, remote_file='file2.csv')
    print(f'Written {path1} with values: {values1}')
    print(f'Written {path2} with values: {values2}')