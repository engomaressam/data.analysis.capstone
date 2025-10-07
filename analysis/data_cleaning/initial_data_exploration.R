# Cyclistic Data Exploration - Initial Assessment
# Author: [Your Name]
# Date: [Current Date]
# Purpose: Initial exploration of downloaded Divvy data

# =====================================================
# SETUP AND LIBRARIES
# =====================================================

# Load required libraries
library(tidyverse)
library(lubridate)
library(readr)
library(dplyr)
library(ggplot2)

# Set working directory
setwd("C:/Users/Diaa/data.analysis.capstone")

# =====================================================
# DATA IMPORT AND STRUCTURE EXAMINATION
# =====================================================

# Function to examine file structure
examine_file_structure <- function(file_path) {
  cat("=== FILE STRUCTURE EXAMINATION ===\n")
  cat("File:", file_path, "\n")
  
  # Check if file exists
  if (!file.exists(file_path)) {
    cat("File not found!\n")
    return(NULL)
  }
  
  # Get file info
  file_info <- file.info(file_path)
  cat("File size:", round(file_info$size / (1024*1024), 2), "MB\n")
  
  # Read first few rows to examine structure
  sample_data <- read_csv(file_path, n_max = 5, show_col_types = FALSE)
  
  cat("Number of columns:", ncol(sample_data), "\n")
  cat("Column names:\n")
  print(names(sample_data))
  
  cat("Column types:\n")
  print(sapply(sample_data, class))
  
  cat("First few rows:\n")
  print(sample_data)
  
  return(sample_data)
}

# =====================================================
# EXAMINE RECENT FILES
# =====================================================

# List of recent files to examine (last 3 months)
recent_files <- c(
  "data/raw/202412-divvy-tripdata/202412-divvy-tripdata.csv",
  "data/raw/202411-divvy-tripdata/202411-divvy-tripdata.csv",
  "data/raw/202410-divvy-tripdata/202410-divvy-tripdata.csv"
)

# Examine each file
for (file in recent_files) {
  examine_file_structure(file)
  cat("\n" + rep("=", 50) + "\n\n")
}

# =====================================================
# LOAD AND EXAMINE ONE COMPLETE FILE
# =====================================================

# Load one recent file for detailed analysis
file_path <- "data/raw/202412-divvy-tripdata/202412-divvy-tripdata.csv"

if (file.exists(file_path)) {
  cat("Loading complete file for analysis:", file_path, "\n")
  
  # Read the complete file
  cyclistic_data <- read_csv(file_path, show_col_types = FALSE)
  
  cat("Total records loaded:", nrow(cyclistic_data), "\n")
  cat("Total columns:", ncol(cyclistic_data), "\n")
  
  # =====================================================
  # BASIC DATA OVERVIEW
  # =====================================================
  
  cat("\n=== BASIC DATA OVERVIEW ===\n")
  
  # Data structure
  str(cyclistic_data)
  
  # Summary statistics
  summary(cyclistic_data)
  
  # Check for missing values
  missing_summary <- cyclistic_data %>%
    summarise_all(~sum(is.na(.))) %>%
    gather(key = "variable", value = "missing_count") %>%
    mutate(
      total_records = nrow(cyclistic_data),
      missing_percentage = round(missing_count / total_records * 100, 2)
    )
  
  cat("\nMissing Values Summary:\n")
  print(missing_summary)
  
  # =====================================================
  # DATA QUALITY CHECKS
  # =====================================================
  
  cat("\n=== DATA QUALITY CHECKS ===\n")
  
  # Check for duplicate ride_ids
  duplicate_rides <- cyclistic_data %>%
    group_by(ride_id) %>%
    summarise(count = n()) %>%
    filter(count > 1)
  
  cat("Duplicate ride_ids found:", nrow(duplicate_rides), "\n")
  
  # Check member_casual values
  member_types <- table(cyclistic_data$member_casual, useNA = "ifany")
  cat("\nMember type distribution:\n")
  print(member_types)
  
  # Check rideable_type values
  bike_types <- table(cyclistic_data$rideable_type, useNA = "ifany")
  cat("\nBike type distribution:\n")
  print(bike_types)
  
  # Check date ranges
  if ("started_at" %in% names(cyclistic_data)) {
    cyclistic_data$started_at <- as.POSIXct(cyclistic_data$started_at)
    cyclistic_data$ended_at <- as.POSIXct(cyclistic_data$ended_at)
    
    cat("\nDate range:\n")
    cat("Earliest start:", min(cyclistic_data$started_at, na.rm = TRUE), "\n")
    cat("Latest end:", max(cyclistic_data$ended_at, na.rm = TRUE), "\n")
    
    # Calculate ride duration
    cyclistic_data$ride_duration_minutes <- as.numeric(
      difftime(cyclistic_data$ended_at, cyclistic_data$started_at, units = "mins")
    )
    
    # Duration statistics
    duration_stats <- summary(cyclistic_data$ride_duration_minutes)
    cat("\nRide duration statistics (minutes):\n")
    print(duration_stats)
    
    # Check for invalid durations
    invalid_durations <- cyclistic_data %>%
      filter(ride_duration_minutes <= 0 | ride_duration_minutes > 1440)
    
    cat("Invalid durations (<= 0 or > 24 hours):", nrow(invalid_durations), "\n")
  }
  
  # =====================================================
  # INITIAL PATTERN ANALYSIS
  # =====================================================
  
  cat("\n=== INITIAL PATTERN ANALYSIS ===\n")
  
  # Member vs casual distribution
  member_distribution <- cyclistic_data %>%
    count(member_casual) %>%
    mutate(percentage = round(n / sum(n) * 100, 2))
  
  cat("Member distribution:\n")
  print(member_distribution)
  
  # Bike type preferences by member type
  bike_preferences <- cyclistic_data %>%
    group_by(member_casual, rideable_type) %>%
    summarise(count = n(), .groups = "drop") %>%
    group_by(member_casual) %>%
    mutate(percentage = round(count / sum(count) * 100, 2))
  
  cat("\nBike preferences by member type:\n")
  print(bike_preferences)
  
  # Station usage (top 10)
  if ("start_station_name" %in% names(cyclistic_data)) {
    top_stations <- cyclistic_data %>%
      filter(!is.na(start_station_name)) %>%
      count(start_station_name, sort = TRUE) %>%
      head(10)
    
    cat("\nTop 10 start stations:\n")
    print(top_stations)
  }
  
  # =====================================================
  # TIME-BASED ANALYSIS
  # =====================================================
  
  if ("started_at" %in% names(cyclistic_data)) {
    cat("\n=== TIME-BASED ANALYSIS ===\n")
    
    # Add time-based variables
    cyclistic_data$hour <- hour(cyclistic_data$started_at)
    cyclistic_data$day_of_week <- wday(cyclistic_data$started_at)
    cyclistic_data$is_weekend <- cyclistic_data$day_of_week %in% c(1, 7)
    
    # Hourly usage
    hourly_usage <- cyclistic_data %>%
      group_by(hour, member_casual) %>%
      summarise(count = n(), .groups = "drop")
    
    cat("Peak usage hours by member type:\n")
    peak_hours <- hourly_usage %>%
      group_by(member_casual) %>%
      slice_max(count, n = 3)
    print(peak_hours)
    
    # Weekend vs weekday usage
    weekend_usage <- cyclistic_data %>%
      group_by(is_weekend, member_casual) %>%
      summarise(count = n(), .groups = "drop") %>%
      group_by(member_casual) %>%
      mutate(percentage = round(count / sum(count) * 100, 2))
    
    cat("\nWeekend vs weekday usage:\n")
    print(weekend_usage)
  }
  
  # =====================================================
  # DATA QUALITY SUMMARY
  # =====================================================
  
  cat("\n=== DATA QUALITY SUMMARY ===\n")
  
  quality_summary <- data.frame(
    Metric = c(
      "Total Records",
      "Complete Records",
      "Duplicate Ride IDs",
      "Invalid Durations",
      "Missing Start Stations",
      "Missing End Stations",
      "Invalid Member Types"
    ),
    Count = c(
      nrow(cyclistic_data),
      sum(complete.cases(cyclistic_data)),
      nrow(duplicate_rides),
      nrow(invalid_durations),
      sum(is.na(cyclistic_data$start_station_name)),
      sum(is.na(cyclistic_data$end_station_name)),
      sum(!cyclistic_data$member_casual %in% c("member", "casual"), na.rm = TRUE)
    ),
    Percentage = c(
      100,
      round(sum(complete.cases(cyclistic_data)) / nrow(cyclistic_data) * 100, 2),
      round(nrow(duplicate_rides) / nrow(cyclistic_data) * 100, 2),
      round(nrow(invalid_durations) / nrow(cyclistic_data) * 100, 2),
      round(sum(is.na(cyclistic_data$start_station_name)) / nrow(cyclistic_data) * 100, 2),
      round(sum(is.na(cyclistic_data$end_station_name)) / nrow(cyclistic_data) * 100, 2),
      round(sum(!cyclistic_data$member_casual %in% c("member", "casual"), na.rm = TRUE) / nrow(cyclistic_data) * 100, 2)
    )
  )
  
  print(quality_summary)
  
  # =====================================================
  # SAVE EXPLORATION RESULTS
  # =====================================================
  
  # Create output directory if it doesn't exist
  if (!dir.exists("analysis/exploratory")) {
    dir.create("analysis/exploratory", recursive = TRUE)
  }
  
  # Save quality summary
  write.csv(quality_summary, "analysis/exploratory/data_quality_summary.csv", row.names = FALSE)
  
  # Save member distribution
  write.csv(member_distribution, "analysis/exploratory/member_distribution.csv", row.names = FALSE)
  
  # Save bike preferences
  write.csv(bike_preferences, "analysis/exploratory/bike_preferences.csv", row.names = FALSE)
  
  cat("\n=== EXPLORATION COMPLETE ===\n")
  cat("Results saved to analysis/exploratory/ directory\n")
  cat("Next steps: Review results and plan data cleaning approach\n")
  
} else {
  cat("File not found:", file_path, "\n")
  cat("Please check the file path and ensure data is properly organized\n")
}

# =====================================================
# NEXT STEPS RECOMMENDATIONS
# =====================================================

cat("\n=== RECOMMENDED NEXT STEPS ===\n")
cat("1. Review the data quality summary above\n")
cat("2. Plan data cleaning strategy based on findings\n")
cat("3. Implement SQL cleaning script for all files\n")
cat("4. Run comprehensive exploratory analysis\n")
cat("5. Begin statistical analysis and visualization\n")
