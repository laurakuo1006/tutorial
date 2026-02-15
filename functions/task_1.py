import os
import csv
import random

def task_1(folder='tutorial', output1='dataset1.csv', output2='dataset2.csv'):
    os.makedirs(folder, exist_ok=True)
    length = 10
    data1 = [round(random.uniform(1, 100), 2) for _ in range(length)]
    data2 = [round(random.uniform(1, 100), 2) for _ in range(length)]
    path1 = os.path.join(folder, output1)
    path2 = os.path.join(folder, output2)
    with open(path1, mode='w', newline='') as f1:
        writer1 = csv.writer(f1)
        writer1.writerow(['value'])
        for val in data1:
            writer1.writerow([val])
    with open(path2, mode='w', newline='') as f2:
        writer2 = csv.writer(f2)
        writer2.writerow(['value'])
        for val in data2:
            writer2.writerow([val])
    faasr_put_file(local_file='dataset1.csv', remote_folder=folder, remote_file='dataset1.csv')
    faasr_put_file(local_file='dataset2.csv', remote_folder=folder, remote_file='dataset2.csv')