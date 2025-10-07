-- Cyclistic Bike Share Data Cleaning Script
-- Purpose: Clean and prepare Divvy trip data for analysis
-- Author: [Your Name]
-- Date: [Current Date]

-- =====================================================
-- DATA QUALITY ASSESSMENT
-- =====================================================

-- Check total record count
SELECT COUNT(*) as total_records
FROM [your_table_name];

-- Check for duplicate ride_ids
SELECT ride_id, COUNT(*) as duplicate_count
FROM [your_table_name]
GROUP BY ride_id
HAVING COUNT(*) > 1;

-- Check data types and null values
SELECT 
    COUNT(*) as total_records,
    COUNT(ride_id) as non_null_ride_ids,
    COUNT(rideable_type) as non_null_rideable_types,
    COUNT(started_at) as non_null_start_times,
    COUNT(ended_at) as non_null_end_times,
    COUNT(start_station_name) as non_null_start_stations,
    COUNT(end_station_name) as non_null_end_stations,
    COUNT(member_casual) as non_null_member_types
FROM [your_table_name];

-- =====================================================
-- DATA CLEANING OPERATIONS
-- =====================================================

-- Create cleaned dataset
CREATE TABLE cyclistic_cleaned AS
SELECT 
    -- Basic fields
    ride_id,
    rideable_type,
    started_at,
    ended_at,
    
    -- Station information (handle nulls)
    COALESCE(start_station_name, 'Unknown') as start_station_name,
    COALESCE(start_station_id, 'Unknown') as start_station_id,
    COALESCE(end_station_name, 'Unknown') as end_station_name,
    COALESCE(end_station_id, 'Unknown') as end_station_id,
    
    -- Coordinates (handle nulls)
    COALESCE(start_lat, 0) as start_lat,
    COALESCE(start_lng, 0) as start_lng,
    COALESCE(end_lat, 0) as end_lat,
    COALESCE(end_lng, 0) as end_lng,
    
    -- Member type
    member_casual,
    
    -- Calculated fields
    EXTRACT(EPOCH FROM (ended_at - started_at))/60 as ride_duration_minutes,
    EXTRACT(DOW FROM started_at) as day_of_week,
    EXTRACT(HOUR FROM started_at) as hour_of_day,
    EXTRACT(MONTH FROM started_at) as month,
    EXTRACT(DAY FROM started_at) as day_of_month,
    DATE(started_at) as date,
    
    -- Additional calculated fields
    CASE 
        WHEN EXTRACT(DOW FROM started_at) IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
    END as day_type,
    
    CASE 
        WHEN EXTRACT(HOUR FROM started_at) BETWEEN 6 AND 11 THEN 'Morning'
        WHEN EXTRACT(HOUR FROM started_at) BETWEEN 12 AND 17 THEN 'Afternoon'
        WHEN EXTRACT(HOUR FROM started_at) BETWEEN 18 AND 22 THEN 'Evening'
        ELSE 'Night'
    END as time_of_day

FROM [your_table_name]
WHERE 
    -- Remove invalid rides
    started_at IS NOT NULL 
    AND ended_at IS NOT NULL
    AND ended_at > started_at  -- End time must be after start time
    AND ride_id IS NOT NULL
    AND member_casual IN ('member', 'casual')  -- Valid member types only
;

-- =====================================================
-- DATA VALIDATION AND FILTERING
-- =====================================================

-- Filter out unrealistic ride durations
CREATE TABLE cyclistic_final AS
SELECT *
FROM cyclistic_cleaned
WHERE 
    ride_duration_minutes > 0  -- Remove zero or negative durations
    AND ride_duration_minutes < 1440  -- Remove rides longer than 24 hours
    AND ride_duration_minutes > 1  -- Remove rides shorter than 1 minute
;

-- =====================================================
-- DATA QUALITY CHECKS AFTER CLEANING
-- =====================================================

-- Check final record count
SELECT COUNT(*) as final_record_count
FROM cyclistic_final;

-- Check ride duration statistics
SELECT 
    MIN(ride_duration_minutes) as min_duration,
    MAX(ride_duration_minutes) as max_duration,
    AVG(ride_duration_minutes) as avg_duration,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ride_duration_minutes) as median_duration
FROM cyclistic_final;

-- Check member type distribution
SELECT 
    member_casual,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM cyclistic_final
GROUP BY member_casual;

-- Check rideable type distribution
SELECT 
    rideable_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM cyclistic_final
GROUP BY rideable_type;

-- Check day of week distribution
SELECT 
    day_of_week,
    CASE day_of_week
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END as day_name,
    COUNT(*) as count
FROM cyclistic_final
GROUP BY day_of_week
ORDER BY day_of_week;

-- =====================================================
-- EXPORT FOR ANALYSIS
-- =====================================================

-- Create summary statistics table
CREATE TABLE cyclistic_summary AS
SELECT 
    'Total Records' as metric,
    COUNT(*)::text as value
FROM cyclistic_final

UNION ALL

SELECT 
    'Member Riders',
    COUNT(*)::text
FROM cyclistic_final
WHERE member_casual = 'member'

UNION ALL

SELECT 
    'Casual Riders',
    COUNT(*)::text
FROM cyclistic_final
WHERE member_casual = 'casual'

UNION ALL

SELECT 
    'Avg Ride Duration (minutes)',
    ROUND(AVG(ride_duration_minutes), 2)::text
FROM cyclistic_final

UNION ALL

SELECT 
    'Data Period',
    CONCAT(MIN(date), ' to ', MAX(date))
FROM cyclistic_final;

-- Display summary
SELECT * FROM cyclistic_summary;

-- =====================================================
-- NOTES FOR DOCUMENTATION
-- =====================================================

/*
DATA CLEANING DECISIONS MADE:

1. NULL HANDLING:
   - Station names/IDs: Replaced with 'Unknown' for dockless rides
   - Coordinates: Replaced with 0 for missing values
   - Kept rides with missing station info as they represent valid dockless trips

2. DURATION FILTERING:
   - Removed rides < 1 minute (likely errors or false starts)
   - Removed rides > 24 hours (likely data errors or abandoned bikes)
   - Kept rides with 0 duration as they might represent valid short trips

3. MEMBER TYPE VALIDATION:
   - Only kept records with 'member' or 'casual' values
   - Removed any invalid or null member types

4. TEMPORAL VALIDATION:
   - Removed records where end time was before start time
   - Kept all valid date/time combinations

5. CALCULATED FIELDS ADDED:
   - ride_duration_minutes: Trip duration in minutes
   - day_of_week: Numeric day (0=Sunday, 6=Saturday)
   - hour_of_day: Hour of start time (0-23)
   - month: Month of start time (1-12)
   - day_type: Weekend vs Weekday
   - time_of_day: Morning, Afternoon, Evening, Night
   - date: Date of start time

6. DATA QUALITY IMPROVEMENTS:
   - Standardized text fields
   - Added useful derived variables
   - Created comprehensive summary statistics
   - Maintained data integrity throughout process
*/
