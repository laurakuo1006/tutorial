import os
import json
import random

def task_1(folder='tutorial', output1='datasets.json'):
    os.makedirs(folder, exist_ok=True)
    dataset1 = [random.randint(1, 100) for _ in range(5)]
    dataset2 = [random.randint(1, 100) for _ in range(5)]
    data = {'dataset1': dataset1, 'dataset2': dataset2}
    output_path = os.path.join(folder, output1)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f'dataset1: {dataset1}')
    print(f'dataset2: {dataset2}')
    element_wise_sum = [a + b for a, b in zip(dataset1, dataset2)]
    total_sum = sum(dataset1) + sum(dataset2)
    print(f'Element-wise sum: {element_wise_sum}')
    print(f'Total sum: {total_sum}')
    print(f'Saved datasets to {output_path}')
    faasr_put_file(local_file='datasets.json', remote_folder=tutorial, remote_file='datasets.json')
task_1('tutorial', 'datasets.json')