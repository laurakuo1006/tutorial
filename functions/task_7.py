import os
import pandas as pd

def task_7(folder='tutorial', input1='extracted_data.csv', output1='max_temperature_trends.png'):
    os.makedirs(folder, exist_ok=True)
    input_path = os.path.join(folder, input1)
    output_path = os.path.join(folder, output1)
    faasr_get_file(remote_folder=folder, remote_file='extracted_data.csv', local_file='extracted_data.csv')
    df = pd.read_csv(input_path)
    date_col_candidates = ['date', 'DATE', 'Date']
    date_col = None
    for c in date_col_candidates:
        if c in df.columns:
            date_col = c
            break
    if date_col is None:
        raise ValueError("No date column found. Expected one of: 'date', 'DATE', 'Date'.")
    tmax_candidates = ['TMAX', 'tmax', 'Tmax', 'max_temp', 'max_temperature']
    tmax_col = None
    for c in tmax_candidates:
        if c in df.columns:
            tmax_col = c
            break
    if tmax_col is None:
        raise ValueError('No max temperature column found. Expected one of: ' + ', '.join(tmax_candidates))
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])
    df = df.sort_values(by=date_col)
    tmax_series = pd.to_numeric(df[tmax_col], errors='coerce')
    df = df.assign(_tmax_processed=tmax_series)
    df = df.dropna(subset=['_tmax_processed'])
    tmax_series = df['_tmax_processed']
    if tmax_series.abs().max() > 200:
        tmax_series = tmax_series / 10.0
    summary_df = pd.DataFrame({'date': df[date_col].dt.strftime('%Y-%m-%d'), 'max_temperature_C': tmax_series.values})
    with open(output_path, 'w', encoding='utf-8') as f:
        summary_df.to_csv(f, index=False)
    faasr_put_file(local_file='max_temperature_trends.png', remote_folder=folder, remote_file='max_temperature_trends.png')