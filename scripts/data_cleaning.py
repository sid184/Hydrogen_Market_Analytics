"""
data_cleaning.py
----------------
Comprehensive cleaning and preprocessing script for global and European hydrogen datasets.
Cleans and standardizes multiple CSV files, removes incomplete records,
imputes missing values, and prepares consistent data for downstream analytics.

Author: [Siddharta Adaikalaraj]
Date: [06/10/2025]
"""

import pandas as pd
import os

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def clean_iea_projects(filepath: str, output_path: str) -> pd.DataFrame:
    """
    Clean IEA Hydrogen Projects dataset:
    - Removes confidential and empty entries
    - Drops irrelevant columns
    - Filters out projects missing a 'Date online' field
    """
    df = pd.read_csv(filepath, skiprows=2)
    df = df[~df['Project name'].str.contains("confidential", case=False, na=False)]
    df = df.dropna(how='all')
    df = df.drop(columns=['Refs'], errors='ignore')

    columns_to_drop = [
        'Capacity_t CO₂ captured/y',
        'References',
        'Latitude',
        'Longitude'
    ] + [f'Unnamed: {i}' for i in range(35, 40)]
    df = df.drop(columns=columns_to_drop, errors='ignore')

    df = df.dropna(subset=['Date online'])
    df.to_csv(output_path, index=False)

    print(f" Cleaned IEA Projects saved as: {output_path} | Shape: {df.shape}")
    return df


def clean_europe_datasets(filepath: str, output_path: str) -> pd.DataFrame:
    """
    Clean European hydrogen datasets (Demand, Production Costs, Breakeven Price):
    - Uses correct header row (index 6)
    - Removes empty columns and rows
    """
    df = pd.read_csv(filepath, header=6)
    df = df.dropna(axis=1, how='all').dropna(how='all')
    df.to_csv(output_path, index=False)

    print(f" Cleaned {os.path.basename(filepath)} saved as: {output_path} | Shape: {df.shape}")
    return df


def impute_cost_values(filepath: str, output_path: str) -> pd.DataFrame:
    """
    Forward and backward fill missing hydrogen cost values.
    """
    df = pd.read_csv(filepath)
    df['Value (€/kg)'] = df['Value (€/kg)'].fillna(method='ffill').fillna(method='bfill')
    df.to_csv(output_path, index=False)

    print(f" Imputed missing values in {os.path.basename(filepath)} | Output: {output_path}")
    print("Remaining missing values:\n", df.isnull().sum())
    return df


def update_north2_date(filepath: str, output_path: str) -> pd.DataFrame:
    """
    Fix missing commissioning date for the NortH2 project.
    """
    df = pd.read_csv(filepath)
    df.loc[df['Project name'].str.contains("NortH2", case=False, na=False), 'Date online'] = 2020.0
    df.to_csv(output_path, index=False)

    print(f" Updated NortH2 entry in {output_path}")
    return df


def update_refinery_region(filepath: str, output_path: str) -> pd.DataFrame:
    """
    Ensure correct region label for 2030 electrolysis projects in refining demand data.
    """
    df = pd.read_csv(filepath)
    mask = (
        (df['year'] == 2030) &
        (df['technology'] == "Electrolysis") &
        (df['status'] == "Operational")
    )
    df.loc[mask, 'region'] = "Global"
    df.to_csv(output_path, index=False)

    print(f"[✔] Updated refinery region data saved to {output_path}")
    return df

# ---------------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # === 1. Clean Hydrogen Projects (IEA) ===
    clean_iea_projects("HydrogenProjects_IEA_Ori.csv", "HydrogenProjects_Final.csv")

    # === 2. Clean European Datasets ===
    clean_europe_datasets("Europe_Hydrogen_Demand.csv", "Europe_Hydrogen_Demand_Cleaned.csv")
    clean_europe_datasets("Hydrogen_Production_Costs_Europe.csv", "Hydrogen_Production_Costs_Europe_Cleaned.csv")
    clean_europe_datasets("BreakevenPrice_Hydrogen_Europe.csv", "BreakevenPrice_Hydrogen_Europe_Cleaned.csv")

    # === 3. Impute Missing Values ===
    impute_cost_values("Hydrogen_Production_Costs_Europe_Cleaned.csv", "Hydrogen_Production_Costs_Europe_Imputed.csv")

    # === 4. Update Specific Project Entries ===
    update_north2_date("HydrogenProjects_Supply.csv", "HydrogenProjects_Supply_Updated.csv")
    update_refinery_region("Hydrogen_Oil_Refine_Demand.csv", "Hydrogen_Oil_Refine_Demand_Updated.csv")

    print("\n All datasets cleaned and updated successfully.")
