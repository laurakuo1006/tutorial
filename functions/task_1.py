import os
import random

def task_1(folder='tutorial', output1='dataset1.csv', output2='dataset2.csv'):
    os.makedirs(folder, exist_ok=True)
    random.seed(42)
    values1 = [round(random.uniform(1.0, 50.0), 2) for _ in range(10)]
    output1_path = os.path.join(folder, output1)
    with open(output1_path, 'w') as f:
        f.write('value\n')
        for v in values1:
            f.write(f'{v}\n')
    random.seed(99)
    values2 = [round(random.uniform(51.0, 100.0), 2) for _ in range(10)]
    output2_path = os.path.join(folder, output2)
    with open(output2_path, 'w') as f:
        f.write('value\n')
        for v in values2:
            f.write(f'{v}\n')
    print(f'Created {output1_path} and {output2_path}')
    faasr_put_file(local_file='dataset1.csv', remote_folder=tutorial, remote_file='dataset1.csv')
    faasr_put_file(local_file='dataset2.csv', remote_folder=tutorial, remote_file='dataset2.csv')
task_1('tutorial', 'dataset1.csv', 'dataset2.csv')