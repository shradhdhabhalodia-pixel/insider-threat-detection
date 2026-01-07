# 🔐 Insider Threat Detection using CERT r5.2

## 📌 Project Overview
This project implements an **industry-grade insider threat detection system** using the CERT r5.2 dataset.  
The system identifies **potential malicious insiders** by combining multiple behavioral signals:

- Login behavior
- File access patterns
- Web activity
- Psychometric risk indicators

The approach is **unsupervised, explainable, and SOC-aligned**, making it suitable for real-world deployment.

---

## 🎯 Problem Statement
Insider threats are difficult to detect because:
- Labels are scarce
- Malicious behavior looks similar to normal activity
- Risk develops over time

This project addresses the problem by building **behavioral baselines** and **aggregating multi-source risk signals**.

---

## 🧠 Solution Architecture

Raw CERT Data -> Feature Engineering (Per Data Source) -> Unsupervised Anomaly Detection (Isolation Forest) -> Risk Score Aggregation -> Explainable Insider Threat Dashboard

## 📂 Dataset
- **Source:** CERT Insider Threat Dataset r5.2
- **Data Access**
    Due to size constraints, raw CERT dataset files are not included in this repository.
    Users should download the dataset separately and place files under `data/raw/`.
- **Files Used:**
  - `logon.csv`
  - `file.csv`
  - `http.csv`
  - `psychometric.csv`

> Raw data is excluded from GitHub due to size and privacy constraints.

---

## 🛠️ Tech Stack
- Python
- Pandas, NumPy
- Scikit-learn
- Streamlit
- Matplotlib
- Git & GitHub

---

## 📊 Model & Evaluation

### Modeling Approach
- Unsupervised anomaly detection using **Isolation Forest**
- Per-source behavior modeling
- Weighted risk aggregation

### Evaluation Methodology
Since ground truth labels are unavailable, the system is evaluated using:
- Risk score distribution analysis
- Multi-signal consistency checks
- Stability across random seeds
- Behavioral explainability

> Traditional accuracy metrics are **not applicable** for this domain.

---

## 🖥️ Streamlit Dashboard
The interactive dashboard allows:
- Organization-level risk overview
- User-level risk drill-down
- Feature contribution explanations
- CSV export for audit purposes

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python src/preprocess/logon_features.py
python src/preprocess/file_features.py
python src/preprocess/http_features.py
python src/preprocess/psycho_features.py

python src/modeling/logon_model.py
python src/modeling/file_model.py
python src/modeling/http_model.py
python src/modeling/risk_aggregator.py

streamlit run src/app.py


