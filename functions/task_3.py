import os
import csv

def task_3(folder='tutorial', input1='dataset1.csv', input2='dataset2.csv', output1='combined_dataset.csv'):
    faasr_get_file(remote_folder=folder, remote_file='dataset1.csv', local_file='dataset1.csv')
    faasr_get_file(remote_folder=folder, remote_file='dataset2.csv', local_file='dataset2.csv')
    os.makedirs(folder, exist_ok=True)
    path1 = os.path.join(folder, input1)
    path2 = os.path.join(folder, input2)
    output_path = os.path.join(folder, output1)
    with open(path1, newline='') as f1:
        reader1 = csv.reader(f1)
        header1 = next(reader1, None)
        data1 = [float(row[0]) for row in reader1 if row]
    with open(path2, newline='') as f2:
        reader2 = csv.reader(f2)
        header2 = next(reader2, None)
        data2 = [float(row[0]) for row in reader2 if row]
    min_len = min(len(data1), len(data2))
    data1 = data1[:min_len]
    data2 = data2[:min_len]
    combined = [a + b for a, b in zip(data1, data2)]
    with open(output_path, 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(['sum'])
        for val in combined:
            writer.writerow([val])
    faasr_put_file(local_file='combined_dataset.csv', remote_folder=folder, remote_file='combined_dataset.csv')