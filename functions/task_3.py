import os
import csv

def task_3(folder='tutorial', input1='random_integers_1.csv', input2='random_integers_2.csv'):
    faasr_get_file(remote_folder=folder, remote_file='random_integers_1.csv', local_file='random_integers_1.csv')
    faasr_get_file(remote_folder=folder, remote_file='random_integers_2.csv', local_file='random_integers_2.csv')
    os.makedirs(folder, exist_ok=True)
    path1 = os.path.join(folder, input1)
    path2 = os.path.join(folder, input2)

    def read_and_validate(path):
        with open(path, newline='') as f:
            reader = csv.reader(f)
            data = []
            for row in reader:
                if len(row) != 1:
                    raise ValueError(f'File {path} contains a row with more than one column.')
                try:
                    val = int(row[0])
                except:
                    raise ValueError(f'File {path} contains non-integer value: {row[0]}')
                data.append(val)
        if len(data) != 20:
            raise ValueError(f'File {path} does not contain exactly 20 integers.')
        return data
    data1 = read_and_validate(path1)
    data2 = read_and_validate(path2)