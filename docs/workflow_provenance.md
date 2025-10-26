# Project Workflow & Provenance

## 1. Data Acquisition
- **Source:** Dunnhumby “The Complete Journey” dataset (Kaggle)  
  [Link to Dataset](https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey)
- **Files used:**  
  - `campaign_desc.csv`, `campaign_table.csv`, `coupon.csv`, `coupon_redempt.csv`  
  - `causal_data.csv`, `product.csv`, `transaction_data.csv`, `hh_demographic.csv`
- **Provenance info recorded:**  
  - Source URL, dataset, log files.
- **Raw Data Folder:** `data/raw/`

---
## 2. Data Cleaning
- **Duplicate Handling:**  
  - Removed duplicate rows from all datasets and recorded % duplicates removed in provenance logs
- **Missing & Unknown Values:**  
  - Identified columns with `NaN` or placeholder values like `"Unknown"`, `"None/Unknown"`, `""`, `"NaN"`.
  - Recorded counts and percentages of missing/unknown values per column for all datasets
  - No critical columns were arbitrarily dropped; missing values were perseved for diversity
- **Standardization:**  
  - Trimmed leading/trailing spaces in string columns.  
- **Invalid Transaction Filtering:**  
  - Removed transactions with non-positive `QUANTITY` or `SALES_VALUE`
- **Provenance Logging:**  
  - All cleaning steps, counts, and percentages recorded in `cleaned_log.txt`
- **Cleaned Data Folder:** `data/cleaned/`
    - Every cleaning step logged with timestamps, dataset name, and row impact
    - **Cleaned CSVs stored at:** `data/cleaned/`

---
## 3. Data Integration and Analysis
## Customer Segmentation
- **Merging Steps:**  
  - Merged `transactions` with `hh_demographic` on `household_key`.  
  - Merged with `products` on `PRODUCT_ID`.  
 
- **Processed Data Output:**  
  - Saved merged dataset as `transactions_merged.csv` in `data/customer_segmentation/`.  
  - All steps recorded in `provenance_log.txt`.

### Data Filtering

| Step | Description | Rows Dropped | % of Total |
|------|--------------|--------------|-------------|
| Missing MARITAL_STATUS_CODE or INCOME_DESC | Pre-aggregation filter | 1,747,722 | 67.82% |
| Missing demographics post-merge | Post-aggregation filter | 2,338 | 93.52% |

Cleaning ensured data quality, a significant portion of records (≈68%) was excluded due to missing demographic fields such as marital status and income.

#### Data Loss Impact

The reduction may bias and reduced diversity of the customer segments toward households with complete demographic profiles.

**Possible Mitigations**
- Resampling of dataset to balance diverity of demographic profile
- Generation of Synthetic dataset that mimic real world households & customers

---

## 4. Visualization

### Demographic Distribution Pie Charts
Pie charts were generated for key categorical demographics:
- `AGE_DESC`
- `MARITAL_STATUS_CODE`
- `INCOME_DESC`
- `HOMEOWNER_DESC`
- `HH_COMP_DESC`
- `HOUSEHOLD_SIZE_DESC`
- `KID_CATEGORY_DESC`

**[Saved to figures](../data/customer_segmentation/figures/)**

---

## 5. Workflow 

| Stage        | Operation                       | Output                     | Description         |
|--------------|--------------------------------|----------------------------|---------------------|
| Cleaning     | Remove invalid & duplicate rows | Cleaned CSVs               | Varies              |
| Integration  | Merge datasets                  | `transactions_merged.csv`  | (2.57M, 25)         |
| Filtering    | Drop NaN in marital/income      | —                          | 67.82% rows removed |
| Aggregation  | Household-level roll-up         | 2,500 → 162 households    | (162, 14)           |
| Visualization| Demographic pie charts          | `.png` in `figures/`       | 7 charts            |

---

## 6. Provenance and Reproducibility

Input/output paths and file shapes are logged to:
- [`cleaned/cleaned_log.txt`](../data/cleaned/cleaned_log.txt)
- [`customer_segmentation/provenance_log.txt`](../data/customer_segmentation/provenance_log.txt)

Implemented in **Python Jupyter notebooks**:
  - [`01_data_exploration.ipynb`](../notebooks/01_data_exploration.ipynb) → loading and verifying raw data
  - [`02_data_cleaning.ipynb`](../notebooks/02_data_cleaning.ipynb) →  potentially making data analysis ready 
  - [`03_processing_analysis.ipynb`](../notebooks/customer_segmentation/03_processing_analysis.ipynb) → customer segmentation processing, analysis and visualisation