import os
import csv
import random

def task_1(folder='tutorial', output1='random_integers_1.csv'):
    os.makedirs(folder, exist_ok=True)
    path_out1 = os.path.join(folder, output1)
    with open(path_out1, mode='w', newline='') as f1:
        writer = csv.writer(f1)
        for _ in range(20):
            writer.writerow([random.randint(-1000, 1000)])
    faasr_put_file(local_file='random_integers_1.csv', remote_folder=folder, remote_file='random_integers_1.csv')