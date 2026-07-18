# Data Cleaning & Preparation — E-Commerce Orders Dataset

Project 1 of the DecodeLabs Data Analytics Industrial Training Kit (Batch 2026).

## Overview
Cleaned a 1,200-row e-commerce orders dataset by auditing and resolving missing values, duplicate records, and formatting inconsistencies (dates, currency precision, text). The goal wasn't just to run cleaning functions — it was to **audit first, then document what was actually found**, since real-world "dirty" data doesn't always match the textbook checklist.

## What was found
| Check | Result |
|---|---|
| Missing values | `CouponCode` had 309 nulls (25.8%) — meant "no coupon used," not an error |
| Duplicate rows | 0 |
| Duplicate OrderIDs / TrackingNumbers | 0 |
| Numeric precision | 29 `UnitPrice`/`TotalPrice` values had floating-point artifacts (e.g. `769.3799999999999`) |
| Date format | Standardized to ISO 8601 (`YYYY-MM-DD`) |
| Formula check | `TotalPrice = Quantity × UnitPrice` verified on all rows — 0 mismatches |

## How it was cleaned
- **Missing values:** imputed `CouponCode` nulls with `"No Coupon"` rather than dropping rows — dropping would have discarded 309 otherwise-valid orders over one non-critical field.
- **Duplicates:** checked full-row duplicates and duplicate unique identifiers explicitly; confirmed none existed rather than assuming.
- **Numeric precision:** rounded currency fields to 2 decimals to fix floating-point representation errors.
- **Dates:** standardized to ISO 8601 for consistency and easier downstream analysis.
- **Text fields:** trimmed whitespace defensively across all string columns.

## Tech
- Python 3, pandas
- openpyxl (Excel I/O)

## Run it
```bash
pip install pandas openpyxl
python clean_dataset.py
```

## Files
- `clean_dataset.py` — cleaning pipeline
- `Dataset_for_Data_Analytics.xlsx` — raw input data
- `Cleaned_Dataset_for_Data_Analytics.xlsx` — cleaned output
- `Data_Cleaning_Change_Log.pdf` — documented audit trail of every change made

## Note
This dataset turned out to be largely clean going in (no messy city-name variants, no bulk duplicates). Rather than force unnecessary "cleaning" to pad the deliverable, this project documents the audit process itself — proving the checks were run, not just assuming issues existed.
