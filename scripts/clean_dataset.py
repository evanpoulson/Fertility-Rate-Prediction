"""
Data Cleaning Script for Fertility Rate Dataset
Removes regional aggregates and fixes data quality issues
"""

import pandas as pd
import numpy as np

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('../data/clean/final_merged_dataset_v2.csv')
print(f"Original shape: {df.shape}")
print(f"Original rows: {len(df):,}")

# 1. Remove rows without country codes (regional aggregates)
print("\n" + "="*80)
print("STEP 1: Removing regional aggregates...")
print("="*80)

# Show some examples before removing
no_code = df[df['Country Code'].isna()]['Country Name'].unique()
print(f"\nFound {len(no_code)} entries without Country Code (regional aggregates):")
print("Sample entries:")
for name in sorted(no_code)[:10]:
    print(f"  - {name}")
if len(no_code) > 10:
    print(f"  ... and {len(no_code) - 10} more")

# Remove rows without country codes
before_count = len(df)
df = df[df['Country Code'].notna()].copy()
after_count = len(df)
print(f"\nRemoved {before_count - after_count:,} rows")
print(f"Remaining rows: {after_count:,}")

# 2. Fix data quality issues
print("\n" + "="*80)
print("STEP 2: Fixing data quality issues...")
print("="*80)

# 2a. Fix LifeExpectancy (should be between 20 and 90 years realistically)
print("\n2a. Cleaning LifeExpectancy...")
life_exp_issues = df[(df['LifeExpectancy'] > 100) | (df['LifeExpectancy'] < 20)]['LifeExpectancy'].notna()
print(f"   Found {life_exp_issues.sum()} suspicious LifeExpectancy values (>100 or <20)")
if life_exp_issues.sum() > 0:
    print(f"   Max value: {df['LifeExpectancy'].max()}")
    print(f"   Min value: {df['LifeExpectancy'].min()}")
    # Set unrealistic values to NaN
    df.loc[(df['LifeExpectancy'] > 100) | (df['LifeExpectancy'] < 20), 'LifeExpectancy'] = np.nan
    print(f"   Set {life_exp_issues.sum()} unrealistic values to NaN")

# 2b. Fix InfantMortality (should be between 0 and 300 per 1000 births)
print("\n2b. Cleaning InfantMortality...")
infant_mort_issues = df[df['InfantMortality'] > 300]['InfantMortality'].notna()
print(f"   Found {infant_mort_issues.sum()} suspicious InfantMortality values (>300)")
if infant_mort_issues.sum() > 0:
    print(f"   Max value: {df['InfantMortality'].max()}")
    # Set unrealistic values to NaN
    df.loc[df['InfantMortality'] > 300, 'InfantMortality'] = np.nan
    print(f"   Set {infant_mort_issues.sum()} unrealistic values to NaN")

# 2c. Fix Labor force participation (should be between 0 and 100%)
print("\n2c. Cleaning Labor force participation rate...")
labor_issues = df[df['Labor force participation rate, female (%)'] > 100]['Labor force participation rate, female (%)'].notna()
print(f"   Found {labor_issues.sum()} values >100%")
if labor_issues.sum() > 0:
    print(f"   Max value: {df['Labor force participation rate, female (%)'].max()}")
    # Set values >100 to NaN
    df.loc[df['Labor force participation rate, female (%)'] > 100, 'Labor force participation rate, female (%)'] = np.nan
    print(f"   Set {labor_issues.sum()} unrealistic values to NaN")

# 2d. Fix other percentage columns that should be 0-100
print("\n2d. Cleaning other percentage columns...")
percentage_cols = [
    'Female share of employment in senior and middle management (%)',
    'advanced_education_pct',
    'basic_education_pct',
    'Urban population over total population',
    'Access to electricity (% of population)'
]

for col in percentage_cols:
    if col in df.columns:
        issues = df[(df[col] < 0) | (df[col] > 100)][col].notna()
        if issues.sum() > 0:
            print(f"   {col}: Found {issues.sum()} values outside 0-100 range")
            df.loc[(df[col] < 0) | (df[col] > 100), col] = np.nan

# 3. Fix column name typos (optional)
print("\n" + "="*80)
print("STEP 3: Fixing column name typos...")
print("="*80)

rename_dict = {
    'Fertirity rate': 'Fertility rate',
    'Capitial GDP in USD': 'Capital GDP in USD'
}

df.rename(columns=rename_dict, inplace=True)
for old, new in rename_dict.items():
    print(f"   Renamed: '{old}' -> '{new}'")

# 4. Remove rows where Year is missing
print("\n" + "="*80)
print("STEP 4: Removing rows with missing Year...")
print("="*80)
before_count = len(df)
df = df[df['Year'].notna()].copy()
after_count = len(df)
print(f"   Removed {before_count - after_count:,} rows with missing Year")

# 5. Summary statistics
print("\n" + "="*80)
print("FINAL DATASET SUMMARY")
print("="*80)
print(f"\nFinal shape: {df.shape}")
print(f"Final rows: {len(df):,}")
print(f"Final columns: {df.shape[1]}")
print(f"\nUnique countries: {df['Country Name'].nunique()}")
print(f"Year range: {df['Year'].min():.0f} - {df['Year'].max():.0f}")
print(f"\nRows with Fertility rate: {df['Fertility rate'].notna().sum():,} ({df['Fertility rate'].notna().sum()/len(df)*100:.1f}%)")

# Show missing data percentage
print("\n" + "="*80)
print("Missing data by column:")
print("="*80)
missing = pd.DataFrame({
    'Missing_Count': df.isnull().sum(),
    'Missing_Pct': (df.isnull().sum() / len(df) * 100).round(2)
}).sort_values('Missing_Pct', ascending=False)
print(missing[missing['Missing_Count'] > 0])

# Save cleaned dataset
output_file = '../data/clean/final_merged_dataset_cleaned.csv'
df.to_csv(output_file, index=False)
print(f"\n{'='*80}")
print(f"Cleaned dataset saved to: {output_file}")
print(f"{'='*80}")
