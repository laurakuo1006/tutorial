import os
import zipfile
import io

def task_8(folder: str='tutorial', input1: str='precipitation_trends.png', input2: str='min_temperature_trends.png', input3: str='max_temperature_trends.png', output1: str='formatted_visualizations.zip'):
    faasr_get_file(remote_folder=folder, remote_file='precipitation_trends.png', local_file='precipitation_trends.png')
    faasr_get_file(remote_folder=folder, remote_file='min_temperature_trends.png', local_file='min_temperature_trends.png')
    faasr_get_file(remote_folder=folder, remote_file='max_temperature_trends.png', local_file='max_temperature_trends.png')
    os.makedirs(folder, exist_ok=True)
    input_files = [input1, input2, input3]
    existing_files = []
    for fname in input_files:
        in_path = os.path.join(folder, fname)
        if os.path.exists(in_path):
            existing_files.append((fname, in_path))
    if not existing_files:
        return
    out_zip_path = os.path.join(folder, output1)
    with zipfile.ZipFile(out_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for fname, in_path in existing_files:
            base, ext = os.path.splitext(fname)
            out_name = f'{base}_formatted{ext}'
            with open(in_path, 'rb') as f:
                data = f.read()
            buf = io.BytesIO(data)
            zf.writestr(out_name, buf.getvalue())
    faasr_put_file(local_file='formatted_visualizations.zip', remote_folder=folder, remote_file='formatted_visualizations.zip')