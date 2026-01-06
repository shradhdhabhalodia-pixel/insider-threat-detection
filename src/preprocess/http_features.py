import pandas as pd # pyright: ignore[reportMissingModuleSource]

SUSPICIOUS_KEYWORDS = [
    'job', 'resume', 'linkedin',
    'dropbox', 'drive.google', 'onedrive'
]

def process_http_data(input_path, output_path):
    df = pd.read_csv(input_path)

    df['url'] = df['url'].astype(str).str.lower()

    df['suspicious'] = df['url'].apply(
        lambda x: 1 if any(k in x for k in SUSPICIOUS_KEYWORDS) else 0
    )

    features = df.groupby('user').agg(
        total_urls=('url', 'count'),
        suspicious_urls=('suspicious', 'sum')
    ).reset_index()

    features['web_risk'] = (
        features['suspicious_urls'] / features['total_urls']
    )

    features[['user', 'web_risk']].to_csv(output_path, index=False)
    print("Web activity features saved.")

if __name__ == "__main__":
    process_http_data(
        "data/raw/http.csv",
        "data/processed/web_risk.csv"
    )
