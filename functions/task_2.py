from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import csv
import random

def task_2(folder='tutorial', input1='file1.csv', input2='file2.csv', output1='sums.csv'):
    faasr_get_file(remote_folder=folder, remote_file='file1.csv', local_file='tutorial/file1.csv')
    faasr_get_file(remote_folder=folder, remote_file='file2.csv', local_file='tutorial/file2.csv')
    os.makedirs(folder, exist_ok=True)
    file1_path = os.path.join(folder, input1)
    file2_path = os.path.join(folder, input2)
    output_path = os.path.join(folder, output1)
    random.seed(42)
    values1 = [random.randint(1, 100) for _ in range(10)]
    values2 = [random.randint(1, 100) for _ in range(10)]
    with open(file1_path, 'w', newline='\n', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['value'])
        for v in values1:
            writer.writerow([v])
    with open(file2_path, 'w', newline='\n', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['value'])
        for v in values2:
            writer.writerow([v])
    with open(file1_path, 'r', newline='\n', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows1 = list(reader)
    if len(rows1) != 10:
        raise ValueError(f'file1.csv must have exactly 10 data rows, found {len(rows1)}')
    for i, row in enumerate(rows1):
        try:
            int(row['value'])
        except (ValueError, KeyError):
            raise ValueError(f"file1.csv row {i + 1} value '{row.get('value')}' is not a valid integer")
        val = int(row['value'])
        if not 1 <= val <= 100:
            raise ValueError(f'file1.csv row {i + 1} value {val} is out of range [1, 100]')
    with open(file2_path, 'r', newline='\n', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows2 = list(reader)
    if len(rows2) != 10:
        raise ValueError(f'file2.csv must have exactly 10 data rows, found {len(rows2)}')
    if len(rows1) != len(rows2):
        raise ValueError(f'Row count mismatch: file1.csv has {len(rows1)}, file2.csv has {len(rows2)}')
    for i, row in enumerate(rows2):
        try:
            int(row['value'])
        except (ValueError, KeyError):
            raise ValueError(f"file2.csv row {i + 1} value '{row.get('value')}' is not a valid integer")
        val = int(row['value'])
        if not 1 <= val <= 100:
            raise ValueError(f'file2.csv row {i + 1} value {val} is out of range [1, 100]')
    sums = [int(rows1[i]['value']) + int(rows2[i]['value']) for i in range(10)]
    with open(output_path, 'w', newline='\n', encoding='utf-8') as f:
        f.write('sum\n')
        for s in sums:
            f.write(f'{s}\n')
    print(f'Written {output_path} with sums: {sums}')
    faasr_put_file(local_file='tutorial/sums.csv', remote_folder=folder, remote_file='sums.csv')