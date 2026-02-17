import os
import json
import csv

def task_4(folder='tutorial', input1='summed_data.json', output1='summed_data.csv'):
    faasr_get_file(remote_folder=folder, remote_file='summed_data.json', local_file='summed_data.json')
    os.makedirs(folder, exist_ok=True)
    input_path = os.path.join(folder, input1)
    output_path = os.path.join(folder, output1)
    if not os.path.isfile(input_path):
        return
    with open(input_path, 'r') as f:
        data = json.load(f)
    if not isinstance(data, list) or not all((isinstance(x, (int, float)) for x in data)):
        return
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sum'])
        for val in data:
            writer.writerow([val])
    faasr_put_file(local_file='summed_data.csv', remote_folder=folder, remote_file='summed_data.csv')