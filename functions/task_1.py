from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import json

def task_1(folder='tutorial', output1='config.json'):
    os.makedirs(folder, exist_ok=True)
    config = {'rows': 5, 'cols': 5, 'min_val': 0, 'max_val': 100}
    output_path = os.path.join(folder, output1)
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=4)
    print(f'Configuration saved to {output_path}')
    faasr_put_file(local_file='tutorial/config.json', remote_folder=folder, remote_file='config.json')