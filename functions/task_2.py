import os
import json

def task_2(folder='tutorial', input1='datasets.json', output1='final_output.txt'):
    faasr_get_file(remote_folder=tutorial, remote_file='datasets.json', local_file='datasets.json')
    os.makedirs(folder, exist_ok=True)
    input_path = os.path.join(folder, input1)
    output_path = os.path.join(folder, output1)
    with open(input_path, 'r') as f:
        data = json.load(f)
    dataset1 = data['dataset1']
    dataset2 = data['dataset2']
    element_wise_sum = [a + b for a, b in zip(dataset1, dataset2)]
    with open(output_path, 'w') as f:
        f.write('Element-wise Sum Result:\n')
        for value in element_wise_sum:
            f.write(f'{value}\n')
    print(f'Element-wise sum computed and written to {output_path}')
    print(f'Result: {element_wise_sum}')
    faasr_put_file(local_file='final_output.txt', remote_folder=tutorial, remote_file='final_output.txt')
task_2('tutorial', 'datasets.json', 'final_output.txt')