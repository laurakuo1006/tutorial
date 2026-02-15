import os
import json

def task_3(folder='tutorial', input1='dataset1.json', input2='dataset2.json', input3='summed_dataset.json', output1='final_output.json'):
    faasr_get_file(remote_folder=folder, remote_file='dataset1.json', local_file='dataset1.json')
    faasr_get_file(remote_folder=folder, remote_file='dataset2.json', local_file='dataset2.json')
    faasr_get_file(remote_folder=folder, remote_file='summed_dataset.json', local_file='summed_dataset.json')
    os.makedirs(folder, exist_ok=True)
    path1 = os.path.join(folder, input1)
    path2 = os.path.join(folder, input2)
    path3 = os.path.join(folder, input3)
    out_path = os.path.join(folder, output1)
    with open(path1, 'r') as f1, open(path2, 'r') as f2:
        dataset1 = json.load(f1)
        dataset2 = json.load(f2)
    summed_dataset = [a + b for a, b in zip(dataset1, dataset2)]
    with open(path3, 'w') as f3:
        json.dump(summed_dataset, f3)
    combined = {'dataset1': dataset1, 'dataset2': dataset2, 'summed_dataset': summed_dataset}
    with open(out_path, 'w') as fout:
        json.dump(combined, fout, indent=2)
    faasr_put_file(local_file='final_output.json', remote_folder=folder, remote_file='final_output.json')