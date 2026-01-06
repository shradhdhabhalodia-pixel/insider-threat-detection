import pandas as pd # pyright: ignore[reportMissingModuleSource]
import matplotlib.pyplot as plt # pyright: ignore[reportMissingModuleSource]

def visualize_results():
    df = pd.read_csv("data/processed/final_insider_risk.csv")

    # 1️⃣ Risk Score Distribution
    plt.figure()
    plt.hist(df['final_risk'], bins=30)
    plt.title("Distribution of Final Risk Scores")
    plt.xlabel("Risk Score")
    plt.ylabel("User Count")
    plt.show()

    # 2️⃣ Risk Label Count
    df['risk_label'].value_counts().plot(kind='bar')
    plt.title("Insider Threat Risk Categories")
    plt.xlabel("Risk Label")
    plt.ylabel("Number of Users")
    plt.show()

    # 3️⃣ Top 10 High-Risk Users
    top_users = df.sort_values('final_risk', ascending=False).head(10)
    print("Top 10 High-Risk Users:")
    print(top_users[['user', 'final_risk', 'risk_label']])

    # 4️⃣ Feature Contribution Visualization
    features = [
        'logon_risk', 'file_risk', 'web_risk',
        'psycho_risk', 'logon_anomaly',
        'file_anomaly', 'web_anomaly'
    ]

    top_users.set_index('user')[features].plot(kind='bar', stacked=True)
    plt.title("Risk Contribution Breakdown (Top 10 Users)")
    plt.ylabel("Risk Contribution")
    plt.show()

if __name__ == "__main__":
    visualize_results()
