"""
Data Cleaning & Preparation - Project 1
DecodeLabs Data Analytics Industrial Training Kit (Batch 2026)

Cleans raw e-commerce order data by handling missing values, duplicates,
and formatting issues, then writes a cleaned CSV/Excel file plus a
console summary of every change made.

Usage:
    python clean_dataset.py
"""

import pandas as pd

INPUT_FILE = "Dataset_for_Data_Analytics.xlsx"
OUTPUT_FILE = "Cleaned_Dataset_for_Data_Analytics.xlsx"


def load_data(path: str) -> pd.DataFrame:
    """Load the raw dataset."""
    df = pd.read_excel(path)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns from {path}\n")
    return df


def audit_missing_values(df: pd.DataFrame) -> None:
    """Print a report of null/missing values per column."""
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]
    print("=== Missing Value Audit ===")
    if nulls.empty:
        print("No missing values found.\n")
    else:
        for col, count in nulls.items():
            pct = count / len(df) * 100
            print(f"  {col}: {count} missing ({pct:.1f}%)")
        print()


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing CouponCode values with 'No Coupon'.
    A blank coupon code means no promo was applied at checkout -
    it's a legitimate category, not an error, so we impute rather
    than drop the row (dropping would lose otherwise valid order data).
    """
    before = df["CouponCode"].isnull().sum()
    df["CouponCode"] = df["CouponCode"].fillna("No Coupon")
    print(f"Filled {before} missing CouponCode values with 'No Coupon'\n")
    return df


def audit_and_remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Check for full-row duplicates and duplicate unique IDs, then drop any found."""
    full_dupes = df.duplicated().sum()
    id_dupes = df["OrderID"].duplicated().sum()
    tracking_dupes = df["TrackingNumber"].duplicated().sum()

    print("=== Duplicate Audit ===")
    print(f"  Full-row duplicates: {full_dupes}")
    print(f"  Duplicate OrderIDs: {id_dupes}")
    print(f"  Duplicate TrackingNumbers: {tracking_dupes}")

    before = len(df)
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset="OrderID", keep="first")
    removed = before - len(df)
    print(f"  Rows removed: {removed}\n")
    return df


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Trim whitespace on all text columns (defensive - protects against hidden characters)."""
    text_cols = [
        "OrderID", "CustomerID", "Product", "ShippingAddress",
        "PaymentMethod", "OrderStatus", "TrackingNumber",
        "CouponCode", "ReferralSource",
    ]
    changed = 0
    for col in text_cols:
        before = df[col].astype(str)
        after = before.str.strip()
        changed += (before != after).sum()
        df[col] = after
    print(f"=== Text Formatting ===\n  Whitespace trimmed on {changed} values\n")
    return df


def fix_numeric_precision(df: pd.DataFrame) -> pd.DataFrame:
    """Round currency columns to 2 decimal places to remove floating-point artifacts."""
    before = (
        (df["UnitPrice"].round(2) != df["UnitPrice"]).sum()
        + (df["TotalPrice"].round(2) != df["TotalPrice"]).sum()
    )
    df["UnitPrice"] = df["UnitPrice"].round(2)
    df["TotalPrice"] = df["TotalPrice"].round(2)
    print(f"=== Numeric Precision ===\n  Corrected {before} values to 2 decimal places\n")
    return df


def standardize_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Convert Date column to ISO 8601 (YYYY-MM-DD) string format."""
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    print("=== Date Formatting ===\n  Standardized all dates to ISO 8601 (YYYY-MM-DD)\n")
    return df


def verify_totals(df: pd.DataFrame) -> pd.DataFrame:
    """Sanity-check that TotalPrice = Quantity * UnitPrice for every row."""
    expected = (df["Quantity"] * df["UnitPrice"]).round(2)
    mismatches = (expected != df["TotalPrice"]).sum()
    print(f"=== Formula Verification ===\n  TotalPrice mismatches: {mismatches}\n")
    return df


def main():
    df = load_data(INPUT_FILE)

    audit_missing_values(df)
    df = handle_missing_values(df)

    df = audit_and_remove_duplicates(df)
    df = clean_text_columns(df)
    df = fix_numeric_precision(df)
    df = standardize_dates(df)
    df = verify_totals(df)

    df.to_excel(OUTPUT_FILE, index=False)
    print(f"Cleaned dataset saved to {OUTPUT_FILE} ({len(df)} rows)")


if __name__ == "__main__":
    main()
