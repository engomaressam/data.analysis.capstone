# Cyclistic Data Collection Plan

## Data Source Information

**Organization**: Divvy (Chicago's bike-share program)  
**Website**: https://www.divvybikes.com/system-data  
**Data Type**: Historical trip data  
**Format**: CSV files  
**Update Frequency**: Monthly  
**License**: Divvy Data License Agreement

## Required Data Files

For a comprehensive 12-month analysis, we need to download the following files:

### 2024 Data (Most Recent)
- [ ] 202412-divvy-tripdata.csv
- [ ] 202411-divvy-tripdata.csv
- [ ] 202410-divvy-tripdata.csv
- [ ] 202409-divvy-tripdata.csv
- [ ] 202408-divvy-tripdata.csv
- [ ] 202407-divvy-tripdata.csv
- [ ] 202406-divvy-tripdata.csv
- [ ] 202405-divvy-tripdata.csv
- [ ] 202404-divvy-tripdata.csv
- [ ] 202403-divvy-tripdata.csv
- [ ] 202402-divvy-tripdata.csv
- [ ] 202401-divvy-tripdata.csv

### 2023 Data (If needed for seasonal analysis)
- [ ] 202312-divvy-tripdata.csv
- [ ] Additional months as needed

## Data Dictionary

Based on Divvy's data documentation, each CSV file contains the following columns:

| Column Name | Data Type | Description | Notes |
|-------------|-----------|-------------|-------|
| ride_id | Character | Unique identifier for each ride | Primary key |
| rideable_type | Character | Type of bike (electric, classic, docked) | Categorical variable |
| started_at | DateTime | Start time and date of ride | Format: YYYY-MM-DD HH:MM:SS |
| ended_at | DateTime | End time and date of ride | Format: YYYY-MM-DD HH:MM:SS |
| start_station_name | Character | Name of starting station | May contain nulls |
| start_station_id | Character | Unique identifier for start station | May contain nulls |
| start_lat | Numeric | Starting latitude coordinate | May contain nulls |
| start_lng | Numeric | Starting longitude coordinate | May contain nulls |
| end_station_name | Character | Name of ending station | May contain nulls |
| end_station_id | Character | Unique identifier for end station | May contain nulls |
| end_lat | Numeric | Ending latitude coordinate | May contain nulls |
| end_lng | Numeric | Ending longitude coordinate | May contain nulls |
| member_casual | Character | Type of rider (member, casual) | Target variable |

## Data Quality Considerations

### Known Issues to Address:
1. **Missing Station Information**: Some rides may not have start/end station data
2. **Data Format Inconsistencies**: Date/time formats may vary
3. **Outlier Rides**: Very short or very long rides that may be errors
4. **Duplicate Entries**: Potential duplicate ride_ids
5. **Data Completeness**: Missing values in various columns

### Validation Rules:
1. **Ride Duration**: Filter out rides < 1 minute or > 24 hours
2. **Station Validation**: Ensure station names and IDs are consistent
3. **Coordinate Validation**: Verify lat/lng are within Chicago area bounds
4. **Date Validation**: Ensure start time is before end time
5. **Member Type**: Validate only "member" or "casual" values

## Download Instructions

### Step 1: Access the Data Portal
1. Navigate to https://www.divvybikes.com/system-data
2. Review the data license agreement
3. Accept terms if required

### Step 2: Download Monthly Files
1. Click on each monthly file link
2. Save to `data/raw/` directory
3. Maintain original file names for tracking

### Step 3: Organize Files
```
data/
├── raw/
│   ├── 202412-divvy-tripdata.csv
│   ├── 202411-divvy-tripdata.csv
│   ├── 202410-divvy-tripdata.csv
│   └── ... (all monthly files)
├── processed/
│   └── (cleaned and combined data)
└── documentation/
    └── data_dictionary.md
```

## File Size Estimates

Based on typical Divvy data:
- **Monthly file size**: ~50-100 MB per month
- **Annual data size**: ~600-1200 MB total
- **Record count**: ~300,000-500,000 rides per month

## Next Steps After Download

1. **Initial Data Assessment**:
   - Check file sizes and record counts
   - Examine data structure and formats
   - Identify any immediate data quality issues

2. **Data Import Testing**:
   - Test importing one month of data
   - Verify column names and data types
   - Check for encoding issues

3. **Quality Assessment**:
   - Run basic data quality checks
   - Identify patterns in missing data
   - Document data quality issues

4. **Combined Dataset Creation**:
   - Merge all monthly files
   - Create consistent data structure
   - Add calculated fields (ride duration, day of week, etc.)

---

*This plan will be updated as we proceed with data collection and encounter any issues or insights.*
