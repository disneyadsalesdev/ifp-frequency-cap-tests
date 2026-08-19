#!/usr/bin/env python3
"""Build district-organized Excel with capacity and avails paired by zip and month."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def month_columns(months: list[str]) -> list[str]:
    columns: list[str] = ["zip_code"]
    for month in months:
        label = pd.to_datetime(f"{month}-01").strftime("%b %Y")
        columns.extend([f"{label} Capacity", f"{label} Avails"])
    columns.extend(["Total Capacity", "Total Avails", "Total Ratio"])
    return columns


def build_district_sheet(df: pd.DataFrame, months: list[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for zip_code, zip_df in df.groupby("zip_code", sort=True):
        row: dict[str, object] = {"zip_code": zip_code}
        total_capacity = 0
        total_available = 0
        for month in months:
            month_df = zip_df.loc[zip_df["month"] == month]
            capacity = int(month_df["capacity"].sum()) if not month_df.empty else 0
            available = int(month_df["available"].sum()) if not month_df.empty else 0
            label = pd.to_datetime(f"{month}-01").strftime("%b %Y")
            row[f"{label} Capacity"] = capacity
            row[f"{label} Avails"] = available
            total_capacity += capacity
            total_available += available
        row["Total Capacity"] = total_capacity
        row["Total Avails"] = total_available
        row["Total Ratio"] = round(total_available / total_capacity, 6) if total_capacity else None
        rows.append(row)

    result = pd.DataFrame(rows, columns=month_columns(months))
    totals = {"zip_code": "DISTRICT TOTAL"}
    for column in result.columns:
        if column == "zip_code":
            continue
        if column == "Total Ratio":
            cap = totals.get("Total Capacity", 0)
            avail = totals.get("Total Avails", 0)
            totals[column] = round(avail / cap, 6) if cap else None
        else:
            totals[column] = int(result[column].sum())
    return pd.concat([result, pd.DataFrame([totals])], ignore_index=True)


def build_district_summary(monthly: pd.DataFrame, months: list[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for district, district_df in monthly.groupby("district", sort=True):
        row: dict[str, object] = {"district": district, "zip_count": district_df["zip_code"].nunique()}
        total_capacity = 0
        total_available = 0
        for month in months:
            month_df = district_df.loc[district_df["month"] == month]
            capacity = int(month_df["capacity"].sum())
            available = int(month_df["available"].sum())
            label = pd.to_datetime(f"{month}-01").strftime("%b %Y")
            row[f"{label} Capacity"] = capacity
            row[f"{label} Avails"] = available
            total_capacity += capacity
            total_available += available
        row["Total Capacity"] = total_capacity
        row["Total Avails"] = total_available
        row["Total Ratio"] = round(total_available / total_capacity, 6) if total_capacity else None
        rows.append(row)

    columns = ["district", "zip_count"] + month_columns(months)[1:]
    return pd.DataFrame(rows, columns=columns)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build district Excel with avails and capacity by zip/month")
    parser.add_argument(
        "--monthly-csv",
        type=Path,
        default=Path("output/gmmb-by-zip-forecasts-monthly.csv"),
    )
    parser.add_argument(
        "--output-excel",
        type=Path,
        default=Path("output/gmmb-by-zip-by-district.xlsx"),
    )
    args = parser.parse_args()

    monthly = pd.read_csv(args.monthly_csv)
    monthly["zip_code"] = monthly["zip_code"].astype(str).str.zfill(5)
    months = sorted(monthly["month"].unique())
    districts = sorted(monthly["district"].unique())

    args.output_excel.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(args.output_excel, engine="openpyxl") as writer:
        summary = build_district_summary(monthly, months)
        summary.to_excel(writer, sheet_name="District Summary", index=False)

        for district in districts:
            sheet_name = district[:31]
            sheet_df = build_district_sheet(monthly.loc[monthly["district"] == district], months)
            sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Wrote {args.output_excel}")
    print(f"Districts: {len(districts)} | Months: {len(months)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
