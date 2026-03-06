from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import csv
import random

def task_2(folder='tutorial', input1='source_a.csv', input2='source_b.csv', output1='result.csv'):
    faasr_get_file(remote_folder=folder, remote_file='source_a.csv', local_file='tutorial/source_a.csv')
    faasr_get_file(remote_folder=folder, remote_file='source_b.csv', local_file='tutorial/source_b.csv')
    os.makedirs(folder, exist_ok=True)
    path_a = os.path.join(folder, input1)
    path_b = os.path.join(folder, input2)
    path_result = os.path.join(folder, output1)
    with open(path_a, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['value'])
        for _ in range(10):
            writer.writerow([random.randint(1, 100)])
    with open(path_b, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['value'])
        for _ in range(10):
            writer.writerow([random.randint(1, 100)])
    with open(path_a, 'r', newline='') as f:
        reader = csv.DictReader(f)
        values_a = [int(row['value']) for row in reader]
    with open(path_b, 'r', newline='') as f:
        reader = csv.DictReader(f)
        values_b = [int(row['value']) for row in reader]
    if len(values_a) != 10:
        raise ValueError(f'source_a.csv has {len(values_a)} data rows, expected 10.')
    if len(values_b) != 10:
        raise ValueError(f'source_b.csv has {len(values_b)} data rows, expected 10.')
    sums = [a + b for a, b in zip(values_a, values_b)]
    with open(path_result, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sum'])
        for s in sums:
            writer.writerow([s])
    print(f'result.csv written with {len(sums)} rows of sums.')
    faasr_put_file(local_file='tutorial/result.csv', remote_folder=folder, remote_file='result.csv')