"""
pricing_analysis.py
--------------------
Recovers the discrete price ladder encoded in the WanderLost campaign data.

Dividing Revenue_INR by Purchases for each converting campaign collapses to a
small set of clean price points -- the menu the simulated data was generated
from. (On real-world data the same computation instead estimates average order
value, since prices, discounts, and basket sizes vary per transaction.)

Usage:
    python pricing_analysis.py
"""

import pandas as pd

CSV_PATH = "data/WanderLost_Cleaned.csv"
MIN_CAMPAIGNS_PER_TIER = 50   # threshold to treat a price point as a real tier vs. a blended average


def main() -> None:
    df = pd.read_csv(CSV_PATH)

    converting = df[df["Purchases"] > 0].copy()
    converting["price_per_booking"] = (
        converting["Revenue_INR"] / converting["Purchases"]
    ).round(0)

    counts = converting["price_per_booking"].value_counts()
    tiers = counts[counts > MIN_CAMPAIGNS_PER_TIER].sort_index()

    total_revenue = df["Revenue_INR"].sum()
    total_spend = df["Spend_INR"].sum()
    total_bookings = df["Purchases"].sum()
    coverage = tiers.sum() / len(converting) * 100

    print("Price tiers encoded in the data (per booking):")
    for price, n in tiers.items():
        print(f"  Rs {int(price):>9,}  -  {int(n):>4,} campaigns")

    print()
    print(f"Tier coverage of converting campaigns : {coverage:.1f}%")
    print(f"Booking-weighted average price (AOV)  : Rs {total_revenue / total_bookings:,.0f}")
    print(f"Total bookings (guests served)        : {int(total_bookings):,}")
    print(f"Total revenue                         : Rs {total_revenue:,.0f}")
    print(f"Total ad spend                        : Rs {total_spend:,.0f}")
    print(f"Blended ROAS                          : {total_revenue / total_spend:.2f}x")


if __name__ == "__main__":
    main()
