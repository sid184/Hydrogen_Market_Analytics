"""
price_analysis.py
-----------------
Analyzes hydrogen production costs and breakeven price ranges
across European countries and industrial sectors.

Author: [Siddharta Adaikalaraj]
Date: [06/10/2025]
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


# ---------------------------------------------------------------------------
# 1. Load and clean datasets
# ---------------------------------------------------------------------------
def load_and_clean_data(cost_path: str, price_path: str):
    """Load and preprocess cost and breakeven datasets."""
    df_cost = pd.read_csv(cost_path)
    df_price = pd.read_csv(price_path)

    # Split Min-Max column and convert to numeric
    df_price[["Min", "Max"]] = (
        df_price["Min-max (Eur/kg)"]
        .str.replace(",", ".")
        .str.split("-", expand=True)
    )
    df_price["Min"] = df_price["Min"].astype(float)
    df_price["Max"] = df_price["Max"].astype(float)

    # Strip spaces and lowercase for consistency
    df_price["Category"] = df_price["Category"].str.strip().str.title()

    return df_cost, df_price


# ---------------------------------------------------------------------------
# 2. Plot price comparison
# ---------------------------------------------------------------------------
def plot_price_comparison(df_cost: pd.DataFrame, df_price: pd.DataFrame):
    """Plot hydrogen production costs with breakeven price ranges per sector."""
    selected_countries = [
        "Germany", "France", "United Kingdom", "Spain", "Italy",
        "Netherlands", "Poland", "Sweden", "Norway", "Greece"
    ]
    df_cost_filtered = df_cost[df_cost["Country"].isin(selected_countries)]

    plt.figure(figsize=(12, 6))

    # Define consistent color palette
    colors = {
        "Oil Refining": "#d73027",          # red
        "Maritime Applications": "#4575b4", # blue
        "Heavy-Duty Trucks": "#1a9850"      # green
    }

    # --- Breakeven price ranges (background) ---
    for _, row in df_price.iterrows():
        category = row["Category"].title()
        if category == "Primary Steel Making":
            plt.axhline(row["Min"], color="black", linestyle="-", linewidth=2.5, zorder=1)
        elif row["Min"] != row["Max"]:
            plt.axhspan(
                row["Min"], row["Max"], 
                alpha=0.4,
                color=colors.get(category, "grey"), 
                zorder=1
            )

    # --- Boxplot for production costs ---
    sns.boxplot(
        x="Country",
        y="Value (€/kg)",
        data=df_cost_filtered,
        showfliers=False,
        zorder=2
    )

    plt.title("Hydrogen Production Costs vs. Sector Breakeven Price Ranges (Europe)")
    plt.ylabel("Cost (€/kg H₂)")
    plt.xticks(rotation=45, ha="right")

    # --- Custom legend ---
    legend_elements = [
        Patch(facecolor=colors["Oil Refining"], alpha=0.4, label="Oil Refining"),
        Line2D([0], [0], color="black", lw=2.5, label="Primary Steel Making"),
        Patch(facecolor=colors["Maritime Applications"], alpha=0.4, label="Maritime Applications"),
        Patch(facecolor=colors["Heavy-Duty Trucks"], alpha=0.4, label="Heavy-Duty Trucks")
    ]

    plt.legend(
        handles=legend_elements,
        title="Breakeven Sectors",
        bbox_to_anchor=(1.05, 1),
        loc="upper left"
    )

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# 3. Main Execution
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    df_cost, df_price = load_and_clean_data(
        "Hydrogen_Production_Costs_Europe_Imputed.csv",
        "BreakevenPrice_Hydrogen_Europe_Cleaned.csv"
    )
    plot_price_comparison(df_cost, df_price)

    print("\n Price analysis complete.")
