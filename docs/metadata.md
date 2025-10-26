# Dataset Metadata

## Overview

This document provides metadata for datasets used in analysis.

## Datasets

### 1. campaign_desc.csv

* **Shape:** (30, 4)
* **Description:** Campaign descriptions
* **Columns:**
	+ `DESCRIPTION` (object): Campaign description
	+ `CAMPAIGN` (int64): Campaign ID
	+ `START_DAY` (int64): Start day of the campaign
	+ `END_DAY` (int64): End day of the campaign
* **Missing Values:** None

### 2. campaign_table.csv

* **Shape:** (7208, 3)
* **Description:** Campaign table
* **Columns:**
	+ `DESCRIPTION` (object): Campaign description
	+ `household_key` (int64): Household key
	+ `CAMPAIGN` (int64): Campaign ID
* **Missing Values:** None

### 3. coupon.csv

* **Shape:** (124548, 3)
* **Description:** Coupon information
* **Columns:**
	+ `COUPON_UPC` (int64): Coupon UPC
	+ `PRODUCT_ID` (int64): Product ID
	+ `CAMPAIGN` (int64): Campaign ID
* **Missing Values:** None

### 4. coupon_redempt.csv

* **Shape:** (2318, 4)
* **Description:** Coupon redemption information
* **Columns:**
	+ `household_key` (int64): Household key
	+ `DAY` (int64): Day of redemption
	+ `COUPON_UPC` (int64): Coupon UPC
	+ `CAMPAIGN` (int64): Campaign ID
* **Missing Values:** None

### 5. causal_data.csv

* **Shape:** (36786524, 5)
* **Description:** Causal data
* **Columns:**
	+ `PRODUCT_ID` (int64): Product ID
	+ `STORE_ID` (int64): Store ID
	+ `WEEK_NO` (int64): Week number
	+ `display` (object): Display information
	+ `mailer` (object): Mailer information
* **Missing Values:** None

### 6. product.csv

* **Shape:** (92353, 7)
* **Description:** Product information
* **Columns:**
	+ `PRODUCT_ID` (int64): Product ID
	+ `MANUFACTURER` (int64): Manufacturer ID
	+ `DEPARTMENT` (object): Department description
	+ `BRAND` (object): Brand description
	+ `COMMODITY_DESC` (object): Commodity description
	+ `SUB_COMMODITY_DESC` (object): Sub-commodity description
	+ `CURR_SIZE_OF_PRODUCT` (object): Current size of product
* **Missing Values:**
	+ `COMMODITY_DESC`: 15 unknown values (0.016%)
	+ `CURR_SIZE_OF_PRODUCT`: 30607 unknown values (33.14%)
	+ `DEPARTMENT`: 15 unknown values (0.016%)
	+ `SUB_COMMODITY_DESC`: 15 unknown values (0.016%)

### 7. transaction_data.csv

* **Shape:** (2595732, 12)
* **Description:** Transaction data
* **Columns:**
	+ `household_key` (int64): Household key
	+ `BASKET_ID` (int64): Basket ID
	+ `DAY` (int64): Day of transaction
	+ `PRODUCT_ID` (int64): Product ID
	+ `QUANTITY` (int64): Quantity purchased
	+ `SALES_VALUE` (float64): Sales value
	+ `STORE_ID` (int64): Store ID
	+ `RETAIL_DISC` (float64): Retail discount
	+ `TRANS_TIME` (int64): Transaction time
	+ `WEEK_NO` (int64): Week number
	+ `COUPON_DISC` (float64): Coupon discount
	+ `COUPON_MATCH_DISC` (float64): Coupon match discount
* **Missing Values:** None

### 8. hh_demographic.csv

* **Shape:** (801, 8)
* **Description:** Household demographic information
* **Columns:**
	+ `AGE_DESC` (object): Age description
	+ `MARITAL_STATUS_CODE` (object): Marital status code
	+ `INCOME_DESC` (object): Income description
	+ `HOMEOWNER_DESC` (object): Homeowner description
	+ `HH_COMP_DESC` (object): Household composition description
	+ `HOUSEHOLD_SIZE_DESC` (object): Household size description
	+ `KID_CATEGORY_DESC` (object): Kid category description
	+ `household_key` (int64): Household key
* **Missing Values:**
	+ `HH_COMP_DESC`: 73 unknown values (9.11%)
	+ `HOMEOWNER_DESC`: 233 unknown values (29.09%)
	+ `KID_CATEGORY_DESC`: 558 unknown values (69.66%)
	+ `MARITAL_STATUS_CODE`: 344 unknown values (42.95%)