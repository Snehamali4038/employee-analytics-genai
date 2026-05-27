# ============================================================
#  data_loader.py  —  Reads and filters the employee CSV
# ============================================================

import pandas as pd
from config import DATA_PATH

def load_data():
    """Load the full employee dataset."""
    df = pd.read_csv(DATA_PATH)
    return df

def get_summary(df):
    """Return a quick summary string of the dataset."""
    return f"""
Dataset Summary:
- Total Employees  : {len(df)}
- Total Columns    : {len(df.columns)}
- Resigned         : {(df['Employee_Resignation_Status'] == 'Yes').sum()}
- Avg Performance  : {df['Performance_Rating'].mean():.2f}
"""

def get_columns(df, cols):
    """Return only the requested columns (drop nulls)."""
    return df[cols].dropna()

def get_stats(df, cols):
    """Return basic stats only for numeric columns."""
    numeric_cols = [c for c in cols if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        return "No numeric columns found."
    return df[numeric_cols].describe().round(2).to_string()

def filter_rows(df, column, condition, value):
    """
    Filter rows by condition.
    condition: 'eq', 'gt', 'lt', 'gte', 'lte'
    """
    if condition == 'eq':
        return df[df[column] == value]
    elif condition == 'gt':
        return df[df[column] > value]
    elif condition == 'lt':
        return df[df[column] < value]
    elif condition == 'gte':
        return df[df[column] >= value]
    elif condition == 'lte':
        return df[df[column] <= value]
    return df

def group_mean(df, group_col, value_col):
    """Return mean of value_col grouped by group_col (numeric only)."""
    if not pd.api.types.is_numeric_dtype(df[value_col]):
        return f"{value_col} is not numeric."
    return df.groupby(group_col)[value_col].mean().round(2).to_string()

def correlation(df, col1, col2):
    """Return correlation between two numeric columns."""
    if not pd.api.types.is_numeric_dtype(df[col1]):
        return f"{col1} is not numeric"
    if not pd.api.types.is_numeric_dtype(df[col2]):
        return f"{col2} is not numeric"
    return round(df[col1].corr(df[col2]), 4)