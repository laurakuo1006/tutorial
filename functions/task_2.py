import os
import csv
from FaaSr_py.client.py_client_stubs import (
    faasr_put_file,
    faasr_get_file,
)

def task_2(folder='tutorial', input1='dataset1.csv', input2='dataset2.csv', output1='summed_result.csv'):
    os.makedirs(folder, exist_ok=True)
    path1 = os.path.join(folder, input1)
    path2 = os.path.join(folder, input2)
    out_path = os.path.join(folder, output1)

    faasr_get_file(remote_folder=folder, remote_file=input1, local_file=path1)
    faasr_get_file(remote_folder=folder, remote_file=input2, local_file=path2)

    with open(path1, newline='') as f1:
        reader1 = csv.DictReader(f1)
        rows1 = list(reader1)
    with open(path2, newline='') as f2:
        reader2 = csv.DictReader(f2)
        rows2 = list(reader2)

    count1 = len(rows1)
    count2 = len(rows2)
    print(f'Row count for {input1}: {count1}')
    print(f'Row count for {input2}: {count2}')

    if count1 != 10:
        raise ValueError(f'{input1} does not contain exactly 10 data rows (found {count1}).')
    if count2 != 10:
        raise ValueError(f'{input2} does not contain exactly 10 data rows (found {count2}).')
    if count1 != count2:
        raise ValueError(f'Row count mismatch: {input1} has {count1} rows, {input2} has {count2} rows.')

    summed = []
    for r1, r2 in zip(rows1, rows2):
        val1 = float(r1['value'])
        val2 = float(r2['value'])
        summed.append(round(val1 + val2, 2))

    with open(out_path, 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(['summed_result'])
        for s in summed:
            writer.writerow([s])

    print(f'Summed result written to {out_path}')
    faasr_put_file(local_file=out_path, remote_folder=folder, remote_file=output1)
