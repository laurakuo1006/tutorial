import os
import csv
import random

def task_1(folder='tutorial', output1='dataset1.csv'):
    os.makedirs(folder, exist_ok=True)
    path_out = os.path.join(folder, output1)
    data = [random.uniform(0, 100) for _ in range(100)]
    with open(path_out, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['value'])
        for val in data:
            writer.writerow([val])
    faasr_put_file(local_file='dataset1.csv', remote_folder=folder, remote_file='dataset1.csv')