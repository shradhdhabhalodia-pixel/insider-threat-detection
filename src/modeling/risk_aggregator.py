import pandas as pd # pyright: ignore[reportMissingModuleSource]

def aggregate_risk():
    logon = pd.read_csv("data/processed/logon_risk.csv")
    file = pd.read_csv("data/processed/file_risk.csv")
    web = pd.read_csv("data/processed/web_risk.csv")
    psycho = pd.read_csv("data/processed/psycho_risk.csv")

    logon_m = pd.read_csv("data/processed/logon_model_output.csv")
    file_m = pd.read_csv("data/processed/file_model_output.csv")
    web_m = pd.read_csv("data/processed/http_model_output.csv")

    df = (
        logon.merge(file, on='user', how='left')
             .merge(web, on='user', how='left')
             .merge(psycho, on='user', how='left')
             .merge(logon_m, on='user', how='left')
             .merge(file_m, on='user', how='left')
             .merge(web_m, on='user', how='left')
    )

    df.fillna(0, inplace=True)

    # Final risk formula (feature + anomaly aware)
    df['final_risk'] = (
        0.25 * df['logon_risk'] +
        0.25 * df['file_risk'] +
        0.20 * df['web_risk'] +
        0.10 * df['psycho_risk'] +
        0.10 * df['logon_anomaly'] +
        0.05 * df['file_anomaly'] +
        0.05 * df['web_anomaly']
    )

    def label(r):
        if r > 0.7:
            return "High Insider Threat"
        elif r > 0.4:
            return "Medium Risk"
        else:
            return "Low Risk"

    df['risk_label'] = df['final_risk'].apply(label)

    df.to_csv("data/processed/final_insider_risk.csv", index=False)
    print("Final insider threat risk computed.")

if __name__ == "__main__":
    aggregate_risk()
