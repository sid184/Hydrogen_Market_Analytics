"""
demand_analysis.py
------------------
Exploratory analysis and visualization of global hydrogen demand data
across regions, sectors, technologies, and time horizons.

Author: [Siddharta Adaikalaraj]
Date: [06/10/2025]
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Helper: set consistent plot style
# ---------------------------------------------------------------------------
sns.set_style("whitegrid")


# ---------------------------------------------------------------------------
# 1. Hydrogen Demand by Region
# ---------------------------------------------------------------------------
def plot_demand_by_region(filepath: str) -> None:
    """Visualize hydrogen demand share by region (bar, pie, and trend charts)."""
    df = pd.read_csv(filepath)
    latest_year = df["year"].max()
    df_latest = df[df["year"] == latest_year]

    # --- Bar Chart ---
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df_latest.sort_values("share_percent", ascending=False),
        x="share_percent",
        y="region",
        palette="viridis",
    )
    plt.title(f"Hydrogen Demand by Region in {latest_year}")
    plt.xlabel("Share of Global Demand (%)")
    plt.ylabel("Region")
    plt.tight_layout()
    plt.show()

    # --- Pie Chart ---
    plt.figure(figsize=(8, 8))
    plt.pie(
        df_latest["share_percent"],
        labels=df_latest["region"],
        autopct="%1.1f%%",
        startangle=140,
    )
    plt.title(f"Hydrogen Demand by Region in {latest_year}")
    plt.tight_layout()
    plt.show()

    # --- Stacked Area Chart ---
    if df["year"].nunique() > 1:
        df_pivot = df.pivot(index="year", columns="region", values="share_percent").fillna(0)
        df_pivot.plot(kind="area", stacked=True, figsize=(12, 7), alpha=0.8)
        plt.title("Hydrogen Demand Share by Region Over Time")
        plt.xlabel("Year")
        plt.ylabel("Share of Global Demand (%)")
        plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        plt.show()

    # --- Line Chart (Trends) ---
    if df["year"].nunique() > 1:
        plt.figure(figsize=(12, 7))
        sns.lineplot(data=df, x="year", y="share_percent", hue="region", marker="o")
        plt.title("Regional Trends in Hydrogen Demand Share Over Time")
        plt.xlabel("Year")
        plt.ylabel("Share of Global Demand (%)")
        plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        plt.show()


# ---------------------------------------------------------------------------
# 2. Demand by Sector and Offtake by Region
# ---------------------------------------------------------------------------
def plot_demand_sector_and_offtake(sector_file: str, offtake_file: str) -> None:
    """Compare sectoral demand growth and regional offtake distribution (side-by-side plots)."""
    df_sector = pd.read_csv(sector_file)
    df_sector = df_sector[(df_sector["year"] >= 2020) & (df_sector["year"] <= 2025)]
    df_pivot_sector = df_sector.pivot(index="year", columns="sector", values="demand (Mtpa H_2)").fillna(0)
    df_pivot_sector["Total Demand"] = df_pivot_sector.sum(axis=1)

    df_offtake = pd.read_csv(offtake_file)
    df_pivot_offtake = (
        df_offtake.pivot(index="role", columns="region", values="share_percent")
        .fillna(0)
        .div(df_offtake.groupby("role")["share_percent"].transform("sum"), axis=0)
        * 100
    )

    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    # --- Left: Demand by Sector ---
    df_pivot_sector.drop(columns="Total Demand").plot(kind="bar", stacked=True, ax=axes[0], width=0.8)
    axes[0].plot(
        range(len(df_pivot_sector)),
        df_pivot_sector["Total Demand"],
        color="black",
        marker="o",
        linewidth=2,
        label="Total Demand",
    )
    axes[0].set_xticks(range(len(df_pivot_sector)))
    axes[0].set_xticklabels(df_pivot_sector.index)
    axes[0].set_title("Hydrogen Demand by Sector (2020–2025)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Demand (Mtpa H₂)")
    for y in range(0, int(df_pivot_sector["Total Demand"].max()) + 5, 5):
        axes[0].axhline(y, color="gray", linestyle="--", linewidth=0.7, alpha=0.7)
    axes[0].legend(title="Sector + Total", loc="upper left", frameon=True, facecolor="white", framealpha=0.7)

    # --- Right: Offtake by Region ---
    df_pivot_offtake.plot(kind="bar", stacked=True, ax=axes[1], colormap="tab20")
    for y in range(20, 101, 20):
        axes[1].axhline(y, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
    axes[1].set_title("Regional Distribution of Hydrogen Producers vs Consumers (2020–2025)")
    axes[1].set_ylabel("Share of Global Offtake Agreements (%)")
    axes[1].tick_params(axis="x", rotation=0)
    axes[1].legend(title="Region", loc="upper left", frameon=True, facecolor="white", framealpha=0.7)

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# 3. Oil Refining Demand
# ---------------------------------------------------------------------------
def plot_refining_demand(filepath: str) -> None:
    """Show hydrogen demand in oil refining, split by technology and region."""
    df = pd.read_csv(filepath)
    df = df[(df["year"] >= 2021) & (df["year"] <= 2030)]
    technologies = df["technology"].unique()

    fig, axes = plt.subplots(1, len(technologies), figsize=(14, 6), sharey=True)
    for i, tech in enumerate(technologies):
        df_tech = df[df["technology"] == tech]
        pivot = df_tech.pivot_table(index="year", columns="region", values="value (ktpa H_2)", aggfunc="sum").fillna(0)
        pivot.plot(kind="area", stacked=True, ax=axes[i], alpha=0.8)
        axes[i].set_title(f"{tech} – Regional Breakdown (2021–2030)")
        axes[i].set_xlabel("Year")
        axes[i].set_ylabel("Capacity (ktpa H₂)")
        axes[i].grid(True, axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# 4. Industrial Demand
# ---------------------------------------------------------------------------
def plot_industrial_demand(filepath: str) -> None:
    """Visualize hydrogen demand in industrial applications by technology and sector."""
    df = pd.read_csv(filepath)
    df = df[(df["year"] >= 2021) & (df["year"] <= 2030)]
    technologies = df["technology"].unique()

    fig, axes = plt.subplots(1, len(technologies), figsize=(14, 6), sharey=True)
    for i, tech in enumerate(technologies):
        df_tech = df[df["technology"] == tech]
        pivot = df_tech.pivot_table(index="year", columns="sector", values="production (ktpa H_2)", aggfunc="sum").fillna(0)
        pivot.plot(kind="area", stacked=True, ax=axes[i], alpha=0.8)
        axes[i].set_title(f"{tech} – Sector Breakdown (2021–2030)")
        axes[i].set_xlabel("Year")
        axes[i].set_ylabel("Production (ktpa H₂)")
        axes[i].grid(True, axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    plot_demand_by_region("Demand_by_Region.csv")
    plot_demand_sector_and_offtake("Demand_by_Sector.csv", "Offtake_by_Region.csv")
    plot_refining_demand("Hydrogen_Oil_Refine_Demand_Cleaned.csv")
    plot_industrial_demand("Hydrogen_Industry_Demand.csv")

    print("\n Demand analysis complete.")
