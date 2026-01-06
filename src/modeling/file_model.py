import pandas as pd # pyright: ignore[reportMissingModuleSource]
from sklearn.ensemble import IsolationForest

def train_file_model():
    df = pd.read_csv("data/processed/file_risk.csv")

    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42
    )

    df['anomaly_score'] = model.fit_predict(df[['file_risk']])
    df['file_anomaly'] = df['anomaly_score'].apply(lambda x: 1 if x == -1 else 0)

    df[['user', 'file_anomaly']].to_csv(
        "data/processed/file_model_output.csv",
        index=False
    )

    print("File activity model completed.")

if __name__ == "__main__":
    train_file_model()
