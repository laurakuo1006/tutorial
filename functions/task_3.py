import os
import csv

def task_3(folder='tutorial', input1='dataset1.csv', input2='dataset2.csv', output1='summed_data.csv'):
    faasr_get_file(remote_folder=folder, remote_file='dataset1.csv', local_file='dataset1.csv')
    faasr_get_file(remote_folder=folder, remote_file='dataset2.csv', local_file='dataset2.csv')
    os.makedirs(folder, exist_ok=True)
    path1 = os.path.join(folder, input1)
    path2 = os.path.join(folder, input2)
    out_path = os.path.join(folder, output1)
    with open(path1, newline='') as f1:
        reader1 = csv.DictReader(f1)
        if reader1.fieldnames != ['value']:
            raise ValueError(f"{input1} header must be ['value']")
        data1 = [row['value'] for row in reader1]
    if len(data1) != 20:
        raise ValueError(f'{input1} must contain exactly 20 rows')
    try:
        data1_int = [int(x) for x in data1]
    except:
        raise ValueError(f'{input1} must contain only integers')
    with open(path2, newline='') as f2:
        reader2 = csv.DictReader(f2)
        if reader2.fieldnames != ['value']:
            raise ValueError(f"{input2} header must be ['value']")
        data2 = [row['value'] for row in reader2]
    if len(data2) != 20:
        raise ValueError(f'{input2} must contain exactly 20 rows')
    try:
        data2_int = [int(x) for x in data2]
    except:
        raise ValueError(f'{input2} must contain only integers')
    summed = [a + b for a, b in zip(data1_int, data2_int)]
    with open(out_path, 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(['summed_value'])
        for val in summed:
            writer.writerow([val])
    faasr_put_file(local_file='summed_data.csv', remote_folder=folder, remote_file='summed_data.csv')