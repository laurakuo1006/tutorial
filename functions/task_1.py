from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import random

def task_1(folder='tutorial', output1='integers_a.csv', output2='integers_b.csv'):
    os.makedirs(folder, exist_ok=True)
    path_a = os.path.join(folder, output1)
    path_b = os.path.join(folder, output2)
    integers_a = [random.randint(1, 100) for _ in range(10)]
    integers_b = [random.randint(1, 100) for _ in range(10)]
    with open(path_a, 'w') as f:
        for val in integers_a:
            f.write(f'{val}\n')
    with open(path_b, 'w') as f:
        for val in integers_b:
            f.write(f'{val}\n')
    print(f'Generated {path_a} with values: {integers_a}')
    print(f'Generated {path_b} with values: {integers_b}')
    faasr_put_file(local_file='tutorial/integers_a.csv', remote_folder=folder, remote_file='integers_a.csv')
    faasr_put_file(local_file='tutorial/integers_b.csv', remote_folder=folder, remote_file='integers_b.csv')