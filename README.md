# Customer Segmentation & Data Curation Project

## Overview
This project curates and analyzes the **Dunnhumby Complete Journey** dataset to study customer purchasing patterns and market segmentation. The work follows the **Digital Curation Centre (DCC) Data Lifecycle Model** and includes cleaning, metadata creation, and synthetic data augmentation to improve sample diversity.

## Objectives
- Clean and curate the Dunnhumby dataset
- Analyze customer behavior and segmentation
- Analyse campaign effectiveness
- Document reproducible curation workflow

## Data Source
- **Dataset**: Dunnhumby – The Complete Journey  
- **Source**: [Kaggle](https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey)  
- **License**: Open data for research use

## Metadata
Refer to the [metadata documentation](./docs/metadata.md) for information on the dataset's structure, variables, and data types

## Workflow
View the [workflow provenance](./docs/workflow_provenance.md) for a detailed overview of the project's data processing steps

## RUNBOOK — Reproducing the pipeline

### Requirements
- Python 3.10+ (tested)
- Create virtual env:
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt

### Data
- Obtain raw data: Dunnhumby — The Complete Journey (Kaggle)
- Place raw CSVs in `data/raw/` (filenames: transaction_data.csv, hh_demographic.csv, product.csv, coupon.csv, etc.)

### Run pipeline
`python3 -m src.customer_workflow`

This performs:
1. Loading and verification of raw data
2. Cleaning (duplicates, invalid rows, normalization)
3. Demographic mapping & heuristics 
4. Merge & aggregation of household-level metrics
5. Figures generation saved to `data/customer_segmentation/figures/`
6. Writes logs to `logs/workflow.txt`

## Re-running
- Outputs are deterministic given the same raw data and environment.
- To re-run from scratch, remove
`rm -rf data/cleaned/* data/customer_segmentation/*`

## Folder Structure
See `/data`, `/src`,`/notebooks`, `/scripts`, and `/docs` for workflow components.

## Tools
Python (pandas, numpy, matplotlib)  
GitHub for versioning and documentation

## References
Dunnhumby. (n.d.). *The Complete Journey.* Kaggle.  
https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey
