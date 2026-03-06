from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import random

def task_2(folder='tutorial', input1='file1.csv', input2='file2.csv', output1='summed_output.csv'):
    os.makedirs(folder, exist_ok=True)
    input1_path = os.path.join(folder, input1)
    input2_path = os.path.join(folder, input2)
    output1_path = os.path.join(folder, output1)
    if not os.path.exists(input1_path):
        values1 = [random.randint(1, 100) for _ in range(10)]
        with open(input1_path, 'w') as f:
            for v in values1:
                f.write(f'{v}\n')
    if not os.path.exists(input2_path):
        values2 = [random.randint(1, 100) for _ in range(10)]
        with open(input2_path, 'w') as f:
            for v in values2:
                f.write(f'{v}\n')
    faasr_get_file(remote_folder=folder, remote_file='file1.csv', local_file='tutorial/file1.csv')
    faasr_get_file(remote_folder=folder, remote_file='file2.csv', local_file='tutorial/file2.csv')
    with open(input1_path, 'r') as f:
        col1 = [int(line.strip()) for line in f if line.strip()]
    with open(input2_path, 'r') as f:
        col2 = [int(line.strip()) for line in f if line.strip()]
    sums = [a + b for a, b in zip(col1, col2)]
    with open(output1_path, 'w') as f:
        for s in sums:
            f.write(f'{s}\n')
    faasr_put_file(local_file='tutorial/summed_output.csv', remote_folder=folder, remote_file='summed_output.csv')
    print(f'Written {len(sums)} rows to {output1_path}')