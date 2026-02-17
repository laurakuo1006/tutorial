import os
import pandas as pd
import numpy as np

def task_3(folder='tutorial', input1='consistent_dataset.csv', output1='cleaned_dataset.csv'):
    os.makedirs(folder, exist_ok=True)
    input_path = os.path.join(folder, input1)
    output_path = os.path.join(folder, output1)
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f'Input file not found: {input_path}')
    faasr_get_file(remote_folder=folder, remote_file='consistent_dataset.csv', local_file='consistent_dataset.csv')
    df = pd.read_csv(input_path)
    df.columns = [c.strip().lower() for c in df.columns]
    possible_precip_cols = ['prcp', 'precip', 'precipitation']
    possible_tmin_cols = ['tmin', 'mintemp', 'min_temperature']
    possible_tmax_cols = ['tmax', 'maxtemp', 'max_temperature']

    def find_col(possible_names):
        for name in possible_names:
            if name in df.columns:
                return name
        return None
    prcp_col = find_col(possible_precip_cols)
    tmin_col = find_col(possible_tmin_cols)
    tmax_col = find_col(possible_tmax_cols)
    climate_cols = [c for c in [prcp_col, tmin_col, tmax_col] if c is not None]
    if not climate_cols:
        df_clean = df.dropna(how='all')
        df_clean.to_csv(output_path, index=False)
        return
    for col in climate_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    climate_na_count = df[climate_cols].isna().sum(axis=1)
    threshold = len(climate_cols) / 2.0
    df = df[climate_na_count <= threshold].copy()
    if df.empty:
        df.to_csv(output_path, index=False)
        return
    date_col_candidates = [c for c in df.columns if 'date' in c]
    if date_col_candidates:
        date_col = date_col_candidates[0]
        try:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df = df.sort_values(by=date_col)
        except Exception:
            pass
    station_col_candidates = [c for c in df.columns if c in ('station', 'station_id', 'id', 'stid')]
    if station_col_candidates:
        station_col = station_col_candidates[0]
        df = df.sort_values(by=[station_col] + ([date_col] if date_col_candidates else []))
        df[climate_cols] = df.groupby(station_col)[climate_cols].apply(lambda g: g.interpolate(method='linear', limit_direction='both')).reset_index(level=0, drop=True)
    else:
        df[climate_cols] = df[climate_cols].interpolate(method='linear', limit_direction='both')
    climate_na_count_after = df[climate_cols].isna().sum(axis=1)
    df_clean = df[climate_na_count_after <= threshold].copy()
    df_clean.to_csv(output_path, index=False)
    faasr_put_file(local_file='cleaned_dataset.csv', remote_folder=folder, remote_file='cleaned_dataset.csv')