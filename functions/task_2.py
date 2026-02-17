import os
import json

def task_2(folder='tutorial', input1='dataset1.json', input2='dataset2.json', output1='datasets_validated.json', output2='validation_error.json'):
    faasr_get_file(remote_folder=folder, remote_file='dataset1.json', local_file='dataset1.json')
    faasr_get_file(remote_folder=folder, remote_file='dataset2.json', local_file='dataset2.json')
    os.makedirs(folder, exist_ok=True)
    path1 = os.path.join(folder, input1)
    path2 = os.path.join(folder, input2)
    out_valid = os.path.join(folder, output1)
    out_error = os.path.join(folder, output2)

    def is_number_list(lst):
        if not isinstance(lst, list):
            return False
        for x in lst:
            if not isinstance(x, (int, float)):
                return False
        return True
    try:
        with open(path1, 'r') as f1:
            data1 = json.load(f1)
        with open(path2, 'r') as f2:
            data2 = json.load(f2)
    except Exception as e:
        error_report = {'error': f'Failed to read input files: {str(e)}'}
        with open(out_error, 'w') as ef:
            json.dump(error_report, ef, indent=2)
        return
    errors = []
    if not is_number_list(data1):
        errors.append(f'{input1} does not contain a JSON array of numerical values.')
    if not is_number_list(data2):
        errors.append(f'{input2} does not contain a JSON array of numerical values.')
    if len(data1) != len(data2):
        errors.append('The two datasets are not of equal length.')
    if errors:
        error_report = {'validation_errors': errors}
        with open(out_error, 'w') as ef:
            json.dump(error_report, ef, indent=2)
    else:
        combined = {'dataset1': data1, 'dataset2': data2}
        with open(out_valid, 'w') as vf:
            json.dump(combined, vf, indent=2)
    faasr_put_file(local_file='datasets_validated.json', remote_folder=folder, remote_file='datasets_validated.json')
    faasr_put_file(local_file='validation_error.json', remote_folder=folder, remote_file='validation_error.json')