import json
import os
from pathlib import Path
from datetime import datetime

import streamlit as st

DATA_FILE = Path(os.getcwd()) / "synthetic_data" / "loan_applications.json"


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # if file is malformed or not a list, start fresh
                return []
    else:
        return []


def save_data(list_data):
    # ensure parent dir exists
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(list_data, f, indent=2)


def generate_application_id(existing):
    year = datetime.now().year
    existing_ids = [a.get("application_id", "") for a in existing]
    nums = []
    for _id in existing_ids:
        parts = _id.split("-")
        if parts and parts[-1].isdigit():
            nums.append(int(parts[-1]))
    nextnum = max(nums) + 1 if nums else 1
    return f"LOAN-{year}-{nextnum:05d}"


def main():
    st.title("Loan Application Builder")

    data = load_data()
    st.write(f"Currently stored applications: {len(data)}")

    with st.form("loan_form"):
        st.header("Applicant Information")
        full_name = st.text_input("Full Name")
        date_of_birth = st.date_input("Date of Birth")
        ssn_last_four = st.text_input("SSN Last Four", max_chars=4)
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        street = st.text_input("Street")
        city = st.text_input("City")
        state = st.text_input("State")
        zip_code = st.text_input("Zip")

        st.header("Employment")
        employer = st.text_input("Employer")
        position = st.text_input("Position")
        years_employed = st.number_input("Years Employed", min_value=0.0, format="%.2f")
        annual_salary = st.number_input("Annual Salary", min_value=0.0)
        employment_type = st.selectbox("Employment Type", ["Full-Time", "Part-Time", "Self-Employed", "Contract"])

        st.header("Financial Profile")
        credit_score = st.number_input("Credit Score", min_value=0, max_value=850, step=1)
        monthly_debt_payments = st.number_input("Monthly Debt Payments", min_value=0.0)
        monthly_housing_cost = st.number_input("Monthly Housing Cost", min_value=0.0)
        checking_account_balance = st.number_input("Checking Account Balance", min_value=0.0)
        savings_account_balance = st.number_input("Savings Account Balance", min_value=0.0)
        existing_loans = st.text_area(
            "Existing Loans (JSON list)",
            value="[]",
            help='Example: [{"type":"Auto Loan","remaining_balance":12000,"monthly_payment":450}]'
        )
        bankruptcies = st.number_input("Bankruptcies", min_value=0, step=1)
        late_payments_last_24_months = st.number_input("Late Payments (24 mo)", min_value=0, step=1)

        st.header("Loan Request")
        loan_amount = st.number_input("Loan Amount", min_value=0.0)
        loan_purpose = st.text_input("Loan Purpose")
        requested_term_months = st.number_input("Requested Term (months)", min_value=0, step=1)
        preferred_rate_type = st.selectbox("Preferred Rate Type", ["Fixed", "Variable"])

        st.header("Documents Submitted")
        documents = st.text_area("Documents (one per line)", value="")

        submitted = st.form_submit_button("Submit Application")

    if submitted:
        try:
            loans_list = json.loads(existing_loans)
        except json.JSONDecodeError:
            st.error("Existing loans field contains invalid JSON.")
            return

        documents_list = [d.strip() for d in documents.splitlines() if d.strip()]

        record = {
            "application_id": generate_application_id(data),
            "applicant": {
                "full_name": full_name,
                "date_of_birth": date_of_birth.strftime("%Y-%m-%d"),
                "ssn_last_four": ssn_last_four,
                "email": email,
                "phone": phone,
                "address": {
                    "street": street,
                    "city": city,
                    "state": state,
                    "zip": zip_code,
                },
            },
            "employment": {
                "employer": employer,
                "position": position,
                "years_employed": years_employed,
                "annual_salary": annual_salary,
                "employment_type": employment_type,
            },
            "financial_profile": {
                "credit_score": credit_score,
                "monthly_debt_payments": monthly_debt_payments,
                "monthly_housing_cost": monthly_housing_cost,
                "checking_account_balance": checking_account_balance,
                "savings_account_balance": savings_account_balance,
                "existing_loans": loans_list,
                "bankruptcies": bankruptcies,
                "late_payments_last_24_months": late_payments_last_24_months,
            },
            "loan_request": {
                "loan_amount": loan_amount,
                "loan_purpose": loan_purpose,
                "requested_term_months": requested_term_months,
                "preferred_rate_type": preferred_rate_type,
            },
            "documents_submitted": documents_list,
        }

        data.append(record)
        save_data(data)
        st.success(f"Application {record['application_id']} added.")


if __name__ == "__main__":
    main()