import os
import matplotlib
matplotlib.use('Agg') 

import matplotlib.pyplot as plt
import pandas as pd
from src.utils.log_util import log_step
import os

def save_pie_chart(data: pd.DataFrame, col_name: str, output_dir: str, log_file: str):
    """Generate and save a pie chart for a given column."""
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(6, 6))
    counts = data[col_name].value_counts(dropna=False)
    plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%', startangle=140)
    plt.title(f"Distribution of {col_name.replace('_', ' ')}", fontsize=12)
    plt.tight_layout()

    fig_path = os.path.join(output_dir, f"{col_name.lower()}_piechart.png")
    plt.savefig(fig_path)
    plt.close()

    log_step(log_file, f"Saved pie chart for {col_name} to {fig_path}")

def generate_demographic_piecharts(data: pd.DataFrame, output_dir: str, log_file: str):
    """Generate pie charts for all demographic columns."""
    demo_cols = [
        'AGE_DESC', 'MARITAL_STATUS_CODE', 'INCOME_DESC',
        'HOMEOWNER_DESC', 'HH_COMP_DESC', 'HOUSEHOLD_SIZE_DESC', 'KID_CATEGORY_DESC'
    ]
    log_step(log_file, "Starting demographic distribution pie chart generation...")
    for col in demo_cols:
        save_pie_chart(data, col, output_dir, log_file)
    log_step(log_file, f"Completed saving all demographic pie charts to {output_dir}")
