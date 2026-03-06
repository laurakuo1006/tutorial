from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import csv
import random

def task_2(folder='tutorial', input1='integers_a.csv', input2='integers_b.csv', output1='summed_results.csv'):
    os.makedirs(folder, exist_ok=True)
    faasr_get_file(remote_folder=folder, remote_file='integers_a.csv', local_file='tutorial/integers_a.csv')
    faasr_get_file(remote_folder=folder, remote_file='integers_b.csv', local_file='tutorial/integers_b.csv')
    path_a = os.path.join(folder, input1)
    path_b = os.path.join(folder, input2)
    path_out = os.path.join(folder, output1)
    if not os.path.exists(path_a):
        with open(path_a, 'w', newline='') as f:
            writer = csv.writer(f)
            for _ in range(10):
                writer.writerow([random.randint(1, 100)])
    if not os.path.exists(path_b):
        with open(path_b, 'w', newline='') as f:
            writer = csv.writer(f)
            for _ in range(10):
                writer.writerow([random.randint(1, 100)])
    with open(path_a, 'r', newline='') as f:
        reader = csv.reader(f)
        values_a = [int(row[0]) for row in reader]
    with open(path_b, 'r', newline='') as f:
        reader = csv.reader(f)
        values_b = [int(row[0]) for row in reader]
    sums = [a + b for a, b in zip(values_a, values_b)]
    with open(path_out, 'w', newline='') as f:
        writer = csv.writer(f)
        for s in sums:
            writer.writerow([int(s)])
    print(f'Written {len(sums)} summed values to {path_out}')
    faasr_put_file(local_file='tutorial/summed_results.csv', remote_folder=folder, remote_file='summed_results.csv')