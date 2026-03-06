from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import random
import csv

def task_1(folder='tutorial', output1='source_a.csv', output2='source_b.csv'):
    os.makedirs(folder, exist_ok=True)
    seed_a = random.randint(1, 10 ** 9)
    rng_a = random.Random(seed_a)
    print(f'source_a.csv seed used: {seed_a}')
    values_a = [rng_a.randint(1, 100) for _ in range(10)]
    print(f'source_a values: {values_a}')
    path_a = os.path.join(folder, output1)
    with open(path_a, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['value'])
        for v in values_a:
            writer.writerow([v])
    seed_b = seed_a
    while seed_b == seed_a:
        seed_b = random.randint(1, 10 ** 9)
    rng_b = random.Random(seed_b)
    print(f'source_b.csv seed used: {seed_b}')
    values_b = [rng_b.randint(1, 100) for _ in range(10)]
    print(f'source_b values: {values_b}')
    path_b = os.path.join(folder, output2)
    with open(path_b, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['value'])
        for v in values_b:
            writer.writerow([v])
    faasr_put_file(local_file='tutorial/source_a.csv', remote_folder=folder, remote_file='source_a.csv')
    faasr_put_file(local_file='tutorial/source_b.csv', remote_folder=folder, remote_file='source_b.csv')