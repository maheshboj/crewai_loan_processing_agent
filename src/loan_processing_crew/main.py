#!/usr/bin/env python
import os
from loan_processing_crew.crew import LoanProcessingCrew

os.makedirs("output", exist_ok=True)


def run():
    """Run the loan processing crew."""
    inputs = {
        "application_id": "LOAN-2026-00142"
    }

    result = LoanProcessingCrew().crew().kickoff(inputs=inputs)

    print("\n\n" + "=" * 60)
    print("       LOAN PROCESSING COMPLETE")
    print("=" * 60 + "\n")
    print(result.raw)
    print("\n\nFull decision saved to: output/loan_decision.md")


if __name__ == "__main__":
    run()