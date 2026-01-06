import pandas as pd # pyright: ignore[reportMissingModuleSource]
from sklearn.ensemble import IsolationForest

def train_http_model():
    df = pd.read_csv("data/processed/web_risk.csv")

    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42
    )

    df['anomaly_score'] = model.fit_predict(df[['web_risk']])
    df['web_anomaly'] = df['anomaly_score'].apply(lambda x: 1 if x == -1 else 0)

    df[['user', 'web_anomaly']].to_csv(
        "data/processed/http_model_output.csv",
        index=False
    )

    print("HTTP model completed.")

if __name__ == "__main__":
    train_http_model()
