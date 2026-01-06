import pandas as pd

def process_logon_data(input_path, output_path):
    df = pd.read_csv(input_path)

    # Parse datetime directly from 'date'
    df['datetime'] = pd.to_datetime(df['date'], errors='coerce')

    # Extract hour
    df['login_hour'] = df['datetime'].dt.hour

    # After-hours login (before 8 AM or after 6 PM)
    df['after_hours'] = df['login_hour'].apply(
        lambda x: 1 if x < 8 or x > 18 else 0
    )

    # Aggregate per user
    features = df.groupby('user').agg(
        total_logins=('login_hour', 'count'),
        after_hours_logins=('after_hours', 'sum')
    ).reset_index()

    features['after_hours_ratio'] = (
        features['after_hours_logins'] / features['total_logins']
    )

    # Risk score (simple & explainable)
    features['logon_risk'] = features['after_hours_ratio']

    features[['user', 'logon_risk']].to_csv(output_path, index=False)
    print("✅ Logon features saved successfully.")

if __name__ == "__main__":
    process_logon_data(
        "data/raw/logon.csv",
        "data/processed/logon_risk.csv"
    )
