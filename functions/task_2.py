from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import csv
import random

def task_2(folder='tutorial', input1='source_a.csv', input2='source_b.csv', output1='summed_output.csv'):
    faasr_get_file(remote_folder=folder, remote_file='source_a.csv', local_file='tutorial/source_a.csv')
    faasr_get_file(remote_folder=folder, remote_file='source_b.csv', local_file='tutorial/source_b.csv')
    os.makedirs(folder, exist_ok=True)
    path_a = os.path.join(folder, input1)
    path_b = os.path.join(folder, input2)
    path_out = os.path.join(folder, output1)
    values_a = [random.randint(1, 100) for _ in range(10)]
    with open(path_a, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['value'])
        for v in values_a:
            writer.writerow([v])
    values_b = [random.randint(1, 100) for _ in range(10)]
    with open(path_b, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['value'])
        for v in values_b:
            writer.writerow([v])
    with open(path_a, 'r', newline='') as f:
        reader = csv.DictReader(f)
        rows_a = list(reader)
    if len(rows_a) != 10:
        print(f'ERROR: source_a.csv contains {len(rows_a)} data rows, expected 10.')
        return
    with open(path_b, 'r', newline='') as f:
        reader = csv.DictReader(f)
        rows_b = list(reader)
    if len(rows_b) != 10:
        print(f'ERROR: source_b.csv contains {len(rows_b)} data rows, expected 10.')
        return
    int_values_a = []
    for i, row in enumerate(rows_a, start=1):
        raw = row['value'].strip()
        try:
            val = int(raw)
        except ValueError:
            print(f'ERROR: source_a.csv contains an invalid value at row {i}: {raw}')
            return
        if val < 1 or val > 100:
            print(f'ERROR: source_a.csv contains an invalid value at row {i}: {raw}')
            return
        int_values_a.append(val)
    int_values_b = []
    for i, row in enumerate(rows_b, start=1):
        raw = row['value'].strip()
        try:
            val = int(raw)
        except ValueError:
            print(f'ERROR: source_b.csv contains an invalid value at row {i}: {raw}')
            return
        if val < 1 or val > 100:
            print(f'ERROR: source_b.csv contains an invalid value at row {i}: {raw}')
            return
        int_values_b.append(val)
    print(f'source_a values: {int_values_a}')
    print(f'source_b values: {int_values_b}')
    summed = [a + b for a, b in zip(int_values_a, int_values_b)]
    print(f'summed values: {summed}')
    with open(path_out, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sum'])
        for s in summed:
            writer.writerow([s])
    faasr_put_file(local_file='tutorial/summed_output.csv', remote_folder=folder, remote_file='summed_output.csv')