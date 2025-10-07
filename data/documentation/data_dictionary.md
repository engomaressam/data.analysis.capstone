# Cyclistic Data Dictionary

## Dataset Overview
**Source**: Divvy Bike Share System (Chicago)  
**Website**: https://www.divvybikes.com/system-data  
**License**: Divvy Data License Agreement  
**Update Frequency**: Monthly  

## Column Descriptions

### ride_id
- **Data Type**: Character/String
- **Description**: Unique identifier for each individual ride
- **Format**: Alphanumeric string
- **Example**: "A847FADBBC638E45"
- **Validation**: Must be unique, no duplicates allowed
- **Missing Values**: Not expected

### rideable_type
- **Data Type**: Character/String
- **Description**: Type of bike used for the ride
- **Possible Values**:
  - "electric_bike" - Electric-assist bike
  - "classic_bike" - Traditional pedal bike
  - "docked_bike" - Bike that must be returned to a dock
- **Missing Values**: Not expected
- **Business Context**: Important for understanding user preferences

### started_at
- **Data Type**: DateTime
- **Description**: Start time and date of the ride
- **Format**: YYYY-MM-DD HH:MM:SS
- **Example**: "2024-01-15 14:30:00"
- **Missing Values**: Not expected
- **Business Context**: Used for time-based analysis and peak usage identification

### ended_at
- **Data Type**: DateTime
- **Description**: End time and date of the ride
- **Format**: YYYY-MM-DD HH:MM:SS
- **Example**: "2024-01-15 15:15:00"
- **Missing Values**: Not expected
- **Business Context**: Used to calculate ride duration

### start_station_name
- **Data Type**: Character/String
- **Description**: Name of the station where the ride began
- **Example**: "Streeter Dr & Grand Ave"
- **Missing Values**: May be null for dockless rides
- **Business Context**: Important for geographic analysis and station utilization

### start_station_id
- **Data Type**: Character/String
- **Description**: Unique identifier for the starting station
- **Example**: "13022"
- **Missing Values**: May be null for dockless rides
- **Business Context**: Used for station-specific analysis

### start_lat
- **Data Type**: Numeric
- **Description**: Latitude coordinate of the starting location
- **Range**: 41.6 to 42.1 (Chicago area)
- **Example**: 41.8915
- **Missing Values**: May be null for dockless rides
- **Business Context**: Used for geographic analysis and mapping

### start_lng
- **Data Type**: Numeric
- **Description**: Longitude coordinate of the starting location
- **Range**: -87.9 to -87.5 (Chicago area)
- **Example**: -87.6120
- **Missing Values**: May be null for dockless rides
- **Business Context**: Used for geographic analysis and mapping

### end_station_name
- **Data Type**: Character/String
- **Description**: Name of the station where the ride ended
- **Example**: "Wabash Ave & 16th St"
- **Missing Values**: May be null for dockless rides
- **Business Context**: Important for geographic analysis and station utilization

### end_station_id
- **Data Type**: Character/String
- **Description**: Unique identifier for the ending station
- **Example**: "13023"
- **Missing Values**: May be null for dockless rides
- **Business Context**: Used for station-specific analysis

### end_lat
- **Data Type**: Numeric
- **Description**: Latitude coordinate of the ending location
- **Range**: 41.6 to 42.1 (Chicago area)
- **Example**: 41.8595
- **Missing Values**: May be null for dockless rides
- **Business Context**: Used for geographic analysis and mapping

### end_lng
- **Data Type**: Numeric
- **Description**: Longitude coordinate of the ending location
- **Range**: -87.9 to -87.5 (Chicago area)
- **Example**: -87.6263
- **Missing Values**: May be null for dockless rides
- **Business Context**: Used for geographic analysis and mapping

### member_casual
- **Data Type**: Character/String
- **Description**: Type of rider (our primary analysis variable)
- **Possible Values**:
  - "member" - Annual member with unlimited rides
  - "casual" - Pay-per-ride customer
- **Missing Values**: Not expected
- **Business Context**: This is our target variable for analysis - the key difference we're investigating

## Calculated Fields (To Be Added)

### ride_duration_minutes
- **Calculation**: `(ended_at - started_at) * 24 * 60`
- **Description**: Duration of ride in minutes
- **Business Context**: Key metric for understanding usage patterns

### ride_duration_hours
- **Calculation**: `(ended_at - started_at) * 24`
- **Description**: Duration of ride in hours
- **Business Context**: Alternative duration metric

### day_of_week
- **Calculation**: `WEEKDAY(started_at)`
- **Description**: Day of the week when ride started
- **Possible Values**: 1 (Sunday) through 7 (Saturday)
- **Business Context**: Important for identifying usage patterns

### month
- **Calculation**: `MONTH(started_at)`
- **Description**: Month when ride started
- **Possible Values**: 1 through 12
- **Business Context**: Seasonal analysis

### hour_of_day
- **Calculation**: `HOUR(started_at)`
- **Description**: Hour of day when ride started
- **Possible Values**: 0 through 23
- **Business Context**: Peak usage time analysis

### is_weekend
- **Calculation**: `IF(day_of_week IN (1,7), TRUE, FALSE)`
- **Description**: Boolean indicating if ride occurred on weekend
- **Business Context**: Weekend vs weekday usage patterns

## Data Quality Notes

### Known Issues:
1. **Dockless Rides**: Electric bikes may not have station information
2. **Data Anonymization**: Some data has been pruned for privacy
3. **Outlier Rides**: Some rides may be very short (< 1 minute) or very long (> 24 hours)
4. **Station Name Variations**: Station names may have slight variations in formatting

### Validation Rules:
1. **Ride Duration**: Filter out rides < 1 minute or > 24 hours
2. **Geographic Bounds**: Verify coordinates are within Chicago area
3. **Time Logic**: Ensure start time is before end time
4. **Member Type**: Only "member" or "casual" values allowed

---

*This dictionary will be updated as we work with the data and discover additional insights or issues.*
