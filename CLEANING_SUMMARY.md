# Data Cleaning Summary

## Overview
This document summarizes the data cleaning process applied to the fertility rate dataset.

## Cleaning Script Location
- **Script**: `scripts/clean_dataset.py`
- **Original Dataset**: `data/clean/final_merged_dataset_v2.csv`
- **Cleaned Dataset**: `data/clean/final_merged_dataset_cleaned.csv`

## Changes Applied

### 1. Removed Regional Aggregates
**Problem**: Dataset contained 269 regional aggregate entries (e.g., "Africa Eastern and Southern", "Arab World") without country codes that were skewing the analysis.

**Solution**: Removed all rows without country codes
- **Rows removed**: 4,746
- **Before**: 18,634 rows
- **After**: 13,888 rows

### 2. Fixed Data Quality Issues

#### a. Life Expectancy
- **Problem**: Values outside realistic range (>100 or <20 years)
- **Found**: 9 suspicious values (max was 274 years!)
- **Solution**: Set unrealistic values to NaN

#### b. Infant Mortality
- **Problem**: Values >300 per 1,000 births (unrealistic)
- **Found**: 1 value (472.5)
- **Solution**: Set unrealistic values to NaN

#### c. Labor Force Participation Rate
- **Problem**: Values >100% (impossible for a percentage)
- **Found**: 42 values (max was 126.96%)
- **Solution**: Set values >100 to NaN

### 3. Fixed Column Name Typos
- `Fertirity rate` → `Fertility rate`
- `Capitial GDP in USD` → `Capital GDP in USD`

### 4. Removed Rows with Missing Year
- Removed rows where Year was missing (0 rows affected)

## Final Dataset Summary

### Dataset Size
- **Final shape**: 13,888 rows × 15 columns
- **Unique countries**: 217
- **Year range**: 1960 - 2023
- **Rows with Fertility rate**: 13,856 (99.8%)

### Missing Data by Column (sorted by % missing)

| Column | Missing Count | Missing % |
|--------|--------------|-----------|
| Female share of employment in senior and middle management (%) | 12,231 | 88.07% |
| advanced_education_pct | 11,611 | 83.60% |
| basic_education_pct | 11,596 | 83.50% |
| Labor force participation rate, female (%) | 9,308 | 67.02% |
| WagedFemale | 8,150 | 58.68% |
| Access to electricity (% of population) | 7,356 | 52.97% |
| Maternal mortality ratio (per 100,000 live births) | 6,322 | 45.52% |
| InfantMortality | 3,018 | 21.73% |
| Capital GDP in USD | 2,522 | 18.16% |
| LifeExpectancy | 939 | 6.76% |
| Urban population over total population | 128 | 0.92% |
| Fertility rate | 32 | 0.23% |

## Updated EDA Notebook

The EDA notebook (`data-analysis/fertility_rate_eda.ipynb`) has been updated to:
1. Use the cleaned dataset (`final_merged_dataset_cleaned.csv`)
2. Use the corrected column name (`Fertility rate` instead of `Fertirity rate`)

## Next Steps

Now that the data is cleaned, you can:
1. Re-run the EDA notebook to see updated statistics
2. Proceed with feature engineering
3. Build predictive models with confidence that the data quality issues have been addressed

## How to Run the Cleaning Script Again

If you need to re-run the cleaning process:

```bash
cd scripts
/opt/anaconda3/bin/python clean_dataset.py
```

The script will regenerate the cleaned dataset at `data/clean/final_merged_dataset_cleaned.csv`.
