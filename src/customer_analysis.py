# --------------------------------------------------
# Customer Analysis Pipeline
# --------------------------------------------------

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt

from src.utils.log_util import log

# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = os.path.abspath(os.getcwd())
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "customer_segmentation")
CLEANED_DATA_DIR = os.path.join(PROCESSED_DATA_DIR, "cleaned")
FIGURES_DIR = os.path.join(PROCESSED_DATA_DIR, "figures")
AGG_FIGURES_DIR = os.path.join(FIGURES_DIR, "agg_metrics")
os.makedirs(CLEANED_DATA_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# --------------------------------------------------
# Load Cleaned Datasets
# --------------------------------------------------

def load_cleaned_datasets(cleaned_data_dir: str) -> dict:
    """
    Loads all required cleaned datasets and returns a dict of DataFrames.
    """
    files = {
        "transactions": "transaction_data_cleaned.csv",
        "products": "product_cleaned.csv",
        "demographics": "hh_demographic_cleaned.csv"
    }

    data = {}
    for key, filename in files.items():
        path = os.path.join(cleaned_data_dir, filename)
        if not os.path.exists(path):
            log(f"❌ File not found: {path}")
            raise FileNotFoundError(f"{path} does not exist")
        data[key] = pd.read_csv(path)
        log(f"Loaded {filename} with shape {data[key].shape}")

    return data

# --------------------------------------------------
# Merge Transactions with Demographics and Products
# --------------------------------------------------

def merge_datasets(transactions: pd.DataFrame,
                   products: pd.DataFrame,
                   demographics: pd.DataFrame) -> pd.DataFrame:
    log("Merging datasets...")

    if "household_key" not in transactions.columns or "household_key" not in demographics.columns:
        raise KeyError("'household_key' missing in transactions or demographics")

    merged = transactions.merge(demographics, on="household_key", how="left")
    log(f"After merging demographics: {merged.shape}")

    if "PRODUCT_ID" not in merged.columns or "PRODUCT_ID" not in products.columns:
        raise KeyError("'PRODUCT_ID' missing in merged transactions or products")

    merged = merged.merge(products, on="PRODUCT_ID", how="left")
    log(f"After merging products: {merged.shape}")

    return merged

# --------------------------------------------------
# Clean Demographics in Transactions
# --------------------------------------------------

def clean_demographics(df: pd.DataFrame) -> pd.DataFrame:
    critical_cols = ['MARITAL_STATUS_CODE', 'INCOME_DESC']
    missing_values = ["Unknown", ""]

    initial_rows = df.shape[0]
    mask_missing = df[critical_cols].apply(
        lambda col: col.isna() | col.astype(str).str.strip().isin(missing_values)
    ).any(axis=1)

    df_clean = df[~mask_missing].reset_index(drop=True)
    num_dropped = mask_missing.sum()
    log(f"Dropped {num_dropped} rows with missing critical demographics ({num_dropped / initial_rows * 100:.2f}%)")

    return df_clean

# --------------------------------------------------
# Household-Level Aggregation
# --------------------------------------------------

def aggregate_households(df: pd.DataFrame) -> pd.DataFrame:
    log("Aggregating household-level metrics...")

    agg = df.groupby("household_key").agg({
        "SALES_VALUE": "sum",
        "QUANTITY": "sum",
        "BASKET_ID": pd.Series.nunique,
        "COUPON_DISC": lambda x: (x > 0).sum()
    }).reset_index()

    agg = agg.rename(columns={
        "SALES_VALUE": "total_spent",
        "QUANTITY": "total_quantity",
        "BASKET_ID": "num_transactions",
        "COUPON_DISC": "num_coupons_redeemed"
    })

    agg["avg_basket_size"] = agg["total_quantity"] / agg["num_transactions"]
    agg["coupon_redemption_rate"] = agg["num_coupons_redeemed"] / agg["num_transactions"]

    log(f"Aggregated {agg.shape[0]} households")
    return agg

# --------------------------------------------------
# Merge Aggregated Data with Demographics
# NOTE:
    # - KID_CATEGORY_DESC is intentionally *not* treated as a required field.
    #   Values like "None" or "Unknown" in this column do not necessarily indicate 
    #   missing data.
# --------------------------------------------------

def merge_household_demographics(agg: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    demo_cols = [
        "household_key", "AGE_DESC", "MARITAL_STATUS_CODE", "INCOME_DESC",
        "HOMEOWNER_DESC", "HH_COMP_DESC", "HOUSEHOLD_SIZE_DESC", "KID_CATEGORY_DESC"
    ]
    merged = agg.merge(df[demo_cols].drop_duplicates(), on="household_key", how="left")

    missing_values = ["Unknown", "NULL", "nan", "NA", "Not Available", " "]
    required_cols = [
        "AGE_DESC",
        "MARITAL_STATUS_CODE",
        "INCOME_DESC",
        "HOMEOWNER_DESC", 
        "HOUSEHOLD_SIZE_DESC"
    ]

    mask_missing = merged[required_cols].apply(
        lambda col: col.isna() | col.astype(str).str.strip().isin(missing_values)
    ).any(axis=1)

    removed = mask_missing.sum()
    merged = merged[~mask_missing].reset_index(drop=True)
    log(f"Dropped {removed} households with missing demographics ({removed / agg.shape[0] * 100:.2f}%)")

    return merged

# --------------------------------------------------
# Generate Charts
# --------------------------------------------------

def generate_demographic_piecharts(df: pd.DataFrame, output_dir: str = FIGURES_DIR):
    demo_cols = [
        'AGE_DESC', 'MARITAL_STATUS_CODE', 'INCOME_DESC',
        'HOMEOWNER_DESC', 'HH_COMP_DESC', 'HOUSEHOLD_SIZE_DESC', 'KID_CATEGORY_DESC'
    ]

    for col in demo_cols:
        plt.figure(figsize=(6, 6))
        counts = df[col].value_counts()
        plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%', startangle=140)
        plt.title(f"Distribution of {col.replace('_', ' ')}", fontsize=12)
        plt.tight_layout()
        filename=f"{col.lower()}_piechart.png"
        outpath = os.path.join(output_dir, filename)
        plt.savefig(outpath)
        plt.close()
        log(f"Saved pie chart: {filename}")

def generate_aggregate_visuals(df):
    plot_metric_vs_category(df, "total_spent", "INCOME_DESC")
    plot_metric_vs_category(df, "total_spent", "AGE_DESC")
    plot_metric_vs_category(df, "num_transactions", "INCOME_DESC")
    plot_metric_vs_category(df, "num_transactions", "AGE_DESC")

def plot_metric_vs_category(df, metric, category, output_dir=AGG_FIGURES_DIR):
    os.makedirs(output_dir, exist_ok=True)

    if metric not in df.columns or category not in df.columns:
        print(f"Missing required column: {metric} or {category}")
        return

    df_clean = df.dropna(subset=[category, metric])

    summary = (
        df_clean.groupby(category)[metric]
        .mean()
        .sort_index()
    )

    plt.figure(figsize=(8,5))
    plt.bar(summary.index, summary.values)

    plt.xticks(rotation=45, ha="right")
    plt.xlabel(category.replace("_", " ").title())
    plt.ylabel(metric.replace("_", " ").title())
    plt.title(f"{metric.replace('_',' ').title()} by {category.replace('_',' ').title()}")

    plt.tight_layout()

    filename = f"{metric}_vs_{category}.png".replace(" ", "_").lower()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

    log(f"Saved aggregated metric chart: {filename}")

# --------------------------------------------------
# End-to-End Pipeline
# --------------------------------------------------

def run_customer_analysis():
    log("=== Customer Analysis Pipeline Started ===")

    datasets = load_cleaned_datasets(CLEANED_DATA_DIR)
    merged = merge_datasets(datasets["transactions"], datasets["products"], datasets["demographics"])
    cleaned = clean_demographics(merged)
    agg = aggregate_households(cleaned)
    final = merge_household_demographics(agg, cleaned)
    generate_demographic_piecharts(final)
    generate_aggregate_visuals(final)
    
    log("=== Customer Analysis Pipeline Completed ===")
    return final
