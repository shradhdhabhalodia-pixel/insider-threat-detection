import pandas as pd # pyright: ignore[reportMissingModuleSource]
from sklearn.ensemble import IsolationForest

def train_logon_model():
    df = pd.read_csv("data/processed/logon_risk.csv")

    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42
    )

    df['anomaly_score'] = model.fit_predict(df[['logon_risk']])

    # Convert {-1, 1} → {1, 0}
    df['logon_anomaly'] = df['anomaly_score'].apply(lambda x: 1 if x == -1 else 0)

    df[['user', 'logon_anomaly']].to_csv(
        "data/processed/logon_model_output.csv",
        index=False
    )

    print("Logon model completed.")

if __name__ == "__main__":
    train_logon_model()
