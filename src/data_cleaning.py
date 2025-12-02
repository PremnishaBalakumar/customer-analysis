import os
import pandas as pd
from src.utils.log_util import init_log, log

# -------------------------------------------
# Global constants
# -------------------------------------------

MISSING_VALUES = ["Unknown", "None", "NONE", "None/Unknown", "", "U", "NaN"]

FILES = [
    "campaign_desc.csv", "campaign_table.csv", "coupon.csv",
    "coupon_redempt.csv", "causal_data.csv", "product.csv",
    "transaction_data.csv", "hh_demographic.csv"
]

# -------------------------------------------
# Helper functions
# -------------------------------------------

def remove_duplicates(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Drops duplicate rows and logs the result."""
    n = len(df)
    dup = df.duplicated().sum()

    if dup > 0:
        df = df.drop_duplicates()
        log(f"{name}: Removed {dup} duplicates ({dup / n * 100:.2f}%).")
    else:
        log(f"{name}: No duplicates.")

    return df


def normalize_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing spaces from all string columns."""
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()
    return df


def normalize_missing(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Replace placeholder missing values with 'Unknown'."""
    n = len(df)

    for col in df.columns:
        ser = df[col].astype(str).str.strip()
        missing = df[col].isna().sum() + ser.isin(MISSING_VALUES).sum()

        if missing > 0:
            log(f"{name}: {col} has {missing} missing ({missing / n * 100:.2f}%).")

            if df[col].dtype == "object":
                df[col] = df[col].replace(MISSING_VALUES, "Unknown")

    return df


def clean_dataframe(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Wrapper that applies full cleaning steps to any dataset."""
    log(f"=== Cleaning {name} ===")
    log(f"Raw shape: {df.shape}")

    df = remove_duplicates(df, name)
    df = normalize_strings(df)
    df = normalize_missing(df, name)

    log(f"Cleaned shape: {df.shape}")
    return df


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Transaction-specific cleaning: remove invalid rows."""
    initial = len(df)
    df = df[(df["QUANTITY"] > 0) & (df["SALES_VALUE"] > 0)]
    removed = initial - len(df)

    log(f"transaction_data.csv: Removed {removed} invalid rows.")
    return df


# -------------------------------------------
# Dataset loading & saving
# -------------------------------------------

def load_datasets(raw_path: str) -> dict:
    """Loads all CSVs listed in FILES."""
    datasets = {}

    for filename in FILES:
        file_path = os.path.join(raw_path, filename)

        try:
            df = pd.read_csv(file_path)
            datasets[filename] = df
            log(f"Loaded {filename} (shape: {df.shape})")
        except FileNotFoundError:
            log(f"⚠ Missing file: {filename}")
        except Exception as e:
            log(f"❌ Failed loading {filename}: {e}")

    return datasets


def save_cleaned_files(datasets: dict, output_path: str):
    """Writes each cleaned dataframe to disk."""
    for fname, df in datasets.items():
        base = fname.replace(".csv", "")
        save_path = os.path.join(output_path, f"{base}_cleaned.csv")
        df.to_csv(save_path, index=False)
        log(f"Saved cleaned dataset: {save_path}")


# -------------------------------------------
# Main cleaning workflow
# -------------------------------------------

def clean_data(raw_data_path: str) -> str:
    """
    Main entrypoint: cleans all raw datasets and writes cleaned versions.
    Returns path to cleaned data directory.
    """
    project_root = os.getcwd()
    cleaned_path = os.path.join(project_root, "data/customer_segmentation", "cleaned")
    os.makedirs(cleaned_path, exist_ok=True)

    log(f"Starting data cleaning. Raw path: {raw_data_path}")

    # Load data
    datasets = load_datasets(raw_data_path)

    # Clean datasets
    for fname, df in datasets.items():
        df = clean_dataframe(df, fname)

        if fname == "transaction_data.csv":
            df = clean_transactions(df)

        datasets[fname] = df

    # Save all cleaned results
    save_cleaned_files(datasets, cleaned_path)

    log("Data cleaning completed successfully.")
    return cleaned_path
