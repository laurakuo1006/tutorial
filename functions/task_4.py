import os
import csv

def task_4(folder='tutorial', input1='random_integers_1.csv', input2='random_integers_2.csv', output1='summed_dataset.csv'):
    faasr_get_file(remote_folder=folder, remote_file='random_integers_1.csv', local_file='random_integers_1.csv')
    faasr_get_file(remote_folder=folder, remote_file='random_integers_2.csv', local_file='random_integers_2.csv')
    os.makedirs(folder, exist_ok=True)
    path1 = os.path.join(folder, input1)
    path2 = os.path.join(folder, input2)
    out_path = os.path.join(folder, output1)
    with open(path1, newline='') as f1:
        reader1 = csv.reader(f1)
        data1 = [int(row[0]) for row in reader1]
    with open(path2, newline='') as f2:
        reader2 = csv.reader(f2)
        data2 = [int(row[0]) for row in reader2]
    summed = [a + b for a, b in zip(data1, data2)]
    with open(out_path, 'w', newline='') as fout:
        writer = csv.writer(fout)
        for val in summed:
            writer.writerow([val])
    faasr_put_file(local_file='summed_dataset.csv', remote_folder=folder, remote_file='summed_dataset.csv')