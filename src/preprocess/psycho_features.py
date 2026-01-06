import pandas as pd # pyright: ignore[reportMissingModuleSource]

def process_psychometric_data(input_path, output_path):
    df = pd.read_csv(input_path)

    # Detect user column automatically
    possible_user_cols = ['user', 'userid', 'employee_name', 'id']
    user_col = None

    for col in possible_user_cols:
        if col in df.columns:
            user_col = col
            break

    if user_col is None:
        raise ValueError("No user identifier column found in psychometric data")

    # Normalize Big-5 traits (assuming scale 0–100)
    traits = ['O', 'C', 'E', 'A', 'N']
    df[traits] = df[traits] / 100.0

    # Psychometric risk calculation (simple + explainable)
    df['psycho_risk'] = (
        0.5 * df['N'] +
        0.3 * (1 - df['C']) +
        0.2 * (1 - df['A'])
    )

    output_df = df[[user_col, 'psycho_risk']].rename(
        columns={user_col: 'user'}
    )

    output_df.to_csv(output_path, index=False)
    print("Psychometric features saved successfully.")

if __name__ == "__main__":
    process_psychometric_data(
        "data/raw/psychometric.csv",
        "data/processed/psycho_risk.csv"
    )
