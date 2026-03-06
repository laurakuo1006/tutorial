from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import csv
import random

def task_1(folder='tutorial', output1='integers_a.csv', output2='integers_b.csv'):
    os.makedirs(folder, exist_ok=True)
    path_a = os.path.join(folder, output1)
    path_b = os.path.join(folder, output2)
    values_a = [random.randint(1, 100) for _ in range(15)]
    values_b = [random.randint(1, 100) for _ in range(15)]
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
    print(f'Generated {path_a} and {path_b} with 15 rows each.')
    faasr_put_file(local_file='tutorial/integers_a.csv', remote_folder=folder, remote_file='integers_a.csv')
    faasr_put_file(local_file='tutorial/integers_b.csv', remote_folder=folder, remote_file='integers_b.csv')