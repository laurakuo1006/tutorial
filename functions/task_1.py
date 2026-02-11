import os
import csv
import random

def task_1(folder='tutorial', output1='dataset1.csv', output2='dataset2.csv'):
    os.makedirs(folder, exist_ok=True)
    length = 100
    low, high = (1, 1000)
    data1 = [random.randint(low, high) for _ in range(length)]
    data2 = [random.randint(low, high) for _ in range(length)]
    path1 = os.path.join(folder, output1)
    path2 = os.path.join(folder, output2)
    with open(path1, 'w', newline='') as f1:
        writer = csv.writer(f1)
        for val in data1:
            writer.writerow([val])
    with open(path2, 'w', newline='') as f2:
        writer = csv.writer(f2)
        for val in data2:
            writer.writerow([val])
    faasr_put_file(local_file='dataset1.csv', remote_folder=folder, remote_file='dataset1.csv')
    faasr_put_file(local_file='dataset2.csv', remote_folder=folder, remote_file='dataset2.csv')