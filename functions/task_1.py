from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import csv
import random

def task_1(folder='tutorial', output1='source_a.csv', output2='source_b.csv'):
    os.makedirs(folder, exist_ok=True)
    path_a = os.path.join(folder, output1)
    path_b = os.path.join(folder, output2)
    values_a = [random.randint(1, 100) for _ in range(10)]
    values_b = [random.randint(1, 100) for _ in range(10)]
    with open(path_a, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['value'])
        for v in values_a:
            writer.writerow([v])
    with open(path_b, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['value'])
        for v in values_b:
            writer.writerow([v])
    print(f'Generated {path_a} with values: {values_a}')
    print(f'Generated {path_b} with values: {values_b}')
    result_path = os.path.join(folder, 'result.csv')
    sums = [a + b for a, b in zip(values_a, values_b)]
    with open(result_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['value'])
        for s in sums:
            writer.writerow([s])
    print(f'Written element-wise sums to {result_path}: {sums}')
    faasr_put_file(local_file='tutorial/source_a.csv', remote_folder=folder, remote_file='source_a.csv')
    faasr_put_file(local_file='tutorial/source_b.csv', remote_folder=folder, remote_file='source_b.csv')