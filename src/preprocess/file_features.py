import pandas as pd # pyright: ignore[reportMissingModuleSource]

def process_file_data(input_path, output_path):
    df = pd.read_csv(input_path)

    # Count file activities per user
    features = df.groupby('user').agg(
        file_events=('filename', 'count')
    ).reset_index()

    # Normalize risk
    max_events = features['file_events'].max()
    features['file_risk'] = features['file_events'] / max_events

    features[['user', 'file_risk']].to_csv(output_path, index=False)
    print("File activity features saved.")

if __name__ == "__main__":
    process_file_data(
        "data/raw/file.csv",
        "data/processed/file_risk.csv"
    )
