import os
from src.data_cleaning import clean_data
from src.customer_analysis import run_customer_analysis
from src.utils.log_util import init_log, log

def run_full_customer_workflow(project_root: str) -> None:
    """
    Full workflow:
    1. Clean raw data
    2. Run customer segmentation analysis
    """
    raw_data_path = os.path.join(project_root, "data", "raw")

    # Initialize workflow-level log
    log_dir = os.path.join(project_root, "logs")
    os.makedirs(log_dir, exist_ok=True)
    init_log(log_dir, prefix="workflow")
    log("🚀 Starting full customer analysis workflow.")

    # Step 1 — Data cleaning
    log("Step 1: Cleaning raw datasets...")
    clean_data(raw_data_path)
    log(f"✔ Step 1 complete. Cleaned data saved to: data/cleaned/")

    # Step 2 — Customer analysis
    log("Step 2: Running customer analysis pipeline...")
    run_customer_analysis()
    log(f"✔ Step 2 complete. Results saved to: data/customer_segmentation/")
    log("🎉 Workflow completed successfully!")


if __name__ == "__main__":
    PROJECT_ROOT = os.path.abspath(os.path.join(os.getcwd(), ""))
    run_full_customer_workflow(PROJECT_ROOT)
