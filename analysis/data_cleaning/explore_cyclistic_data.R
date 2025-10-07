# Cyclistic Data Exploration - Actual Dataset Analysis
# Author: Omar Essam El-Din Mohamed
# Date: Current Date
# Purpose: Explore the downloaded Cyclistic data files

# =====================================================
# SETUP AND LIBRARIES
# =====================================================

# Load required libraries
library(tidyverse)
library(lubridate)
library(readr)
library(dplyr)
library(ggplot2)
library(scales)

# Set working directory
setwd("C:/Users/Diaa/data.analysis.capstone")

# =====================================================
# DATA FILE DISCOVERY
# =====================================================

# Function to find CSV files in the raw data directory
find_csv_files <- function() {
  raw_dir <- "data/raw"
  
  # Get all subdirectories
  subdirs <- list.dirs(raw_dir, recursive = FALSE)
  
  # Find CSV files in each subdirectory
  csv_files <- c()
  for (subdir in subdirs) {
    files <- list.files(subdir, pattern = "\\.csv$", full.names = TRUE)
    csv_files <- c(csv_files, files)
  }
  
  return(csv_files)
}

# Find all CSV files
csv_files <- find_csv_files()

cat("Found", length(csv_files), "CSV files:\n")
for (i in seq_along(csv_files)) {
  cat(i, ":", csv_files[i], "\n")
}

# =====================================================
# SAMPLE FILE ANALYSIS
# =====================================================

# Function to analyze a single CSV file
analyze_csv_file <- function(file_path) {
  cat("\n" + rep("=", 80) + "\n")
  cat("ANALYZING FILE:", file_path, "\n")
  cat(rep("=", 80) + "\n")
  
  # Check if file exists
  if (!file.exists(file_path)) {
    cat("❌ File not found!\n")
    return(NULL)
  }
  
  # Get file info
  file_info <- file.info(file_path)
  cat("📁 File size:", round(file_info$size / (1024*1024), 2), "MB\n")
  cat("📅 Last modified:", file_info$mtime, "\n")
  
  # Try to read the file
  tryCatch({
    # Read first few rows to check structure
    sample_data <- read_csv(file_path, n_max = 5, show_col_types = FALSE)
    
    cat("📊 Columns found:", ncol(sample_data), "\n")
    cat("📋 Column names:\n")
    for (i in seq_along(names(sample_data))) {
      cat("  ", i, ":", names(sample_data)[i], "\n")
    }
    
    # Check data types
    cat("\n🔍 Data types:\n")
    for (i in seq_along(sample_data)) {
      cat("  ", names(sample_data)[i], ":", class(sample_data[[i]])[1], "\n")
    }
    
    # Show sample data
    cat("\n📄 Sample data (first 3 rows):\n")
    print(head(sample_data, 3))
    
    return(sample_data)
    
  }, error = function(e) {
    cat("❌ Error reading file:", e$message, "\n")
    return(NULL)
  })
}

# =====================================================
# ANALYZE RECENT FILES
# =====================================================

# Focus on recent files (2024 data)
recent_files <- csv_files[grepl("2024", csv_files)]

if (length(recent_files) > 0) {
  cat("\n🎯 FOCUSING ON RECENT FILES (2024):\n")
  
  # Analyze first few recent files
  files_to_analyze <- head(recent_files, 3)
  
  for (file in files_to_analyze) {
    analyze_csv_file(file)
  }
} else {
  cat("\n⚠️ No 2024 files found. Analyzing available files...\n")
  files_to_analyze <- head(csv_files, 3)
  
  for (file in files_to_analyze) {
    analyze_csv_file(file)
  }
}

# =====================================================
# LOAD AND ANALYZE ONE COMPLETE FILE
# =====================================================

# Select a file for complete analysis
if (length(recent_files) > 0) {
  target_file <- recent_files[1]  # Use first recent file
} else {
  target_file <- csv_files[1]     # Use first available file
}

cat("\n" + rep("=", 80) + "\n")
cat("COMPLETE ANALYSIS OF:", target_file, "\n")
cat(rep("=", 80) + "\n")

if (file.exists(target_file)) {
  # Read the complete file
  cat("📥 Loading complete dataset...\n")
  
  tryCatch({
    # Read the file
    cyclistic_data <- read_csv(target_file, show_col_types = FALSE)
    
    cat("✅ Successfully loaded", nrow(cyclistic_data), "records\n")
    cat("📊 Total columns:", ncol(cyclistic_data), "\n")
    
    # =====================================================
    # DATA OVERVIEW
    # =====================================================
    
    cat("\n📋 DATA OVERVIEW:\n")
    cat("Records:", nrow(cyclistic_data), "\n")
    cat("Columns:", ncol(cyclistic_data), "\n")
    
    # Column information
    cat("\n📝 Column Details:\n")
    for (i in seq_along(cyclistic_data)) {
      col_name <- names(cyclistic_data)[i]
      col_type <- class(cyclistic_data[[i]])[1]
      non_null <- sum(!is.na(cyclistic_data[[i]]))
      cat(sprintf("  %2d. %-25s | %-10s | %8d non-null\n", 
                  i, col_name, col_type, non_null))
    }
    
    # =====================================================
    # DATA QUALITY ASSESSMENT
    # =====================================================
    
    cat("\n🔍 DATA QUALITY ASSESSMENT:\n")
    
    # Missing values
    missing_summary <- cyclistic_data %>%
      summarise_all(~sum(is.na(.))) %>%
      gather(key = "variable", value = "missing_count") %>%
      mutate(
        total_records = nrow(cyclistic_data),
        missing_percentage = round(missing_count / total_records * 100, 2)
      )
    
    cat("\nMissing Values:\n")
    for (i in 1:nrow(missing_summary)) {
      var <- missing_summary$variable[i]
      count <- missing_summary$missing_count[i]
      pct <- missing_summary$missing_percentage[i]
      
      if (count > 0) {
        cat(sprintf("  %-25s: %8d (%5.1f%%)\n", var, count, pct))
      }
    }
    
    # =====================================================
    # MEMBER TYPE ANALYSIS
    # =====================================================
    
    if ("member_casual" %in% names(cyclistic_data)) {
      cat("\n👥 MEMBER TYPE DISTRIBUTION:\n")
      member_dist <- table(cyclistic_data$member_casual, useNA = "ifany")
      member_pct <- round(prop.table(member_dist) * 100, 2)
      
      for (i in seq_along(member_dist)) {
        cat(sprintf("  %-10s: %8d (%5.1f%%)\n", 
                    names(member_dist)[i], member_dist[i], member_pct[i]))
      }
    }
    
    # =====================================================
    # BIKE TYPE ANALYSIS
    # =====================================================
    
    if ("rideable_type" %in% names(cyclistic_data)) {
      cat("\n🚴 BIKE TYPE DISTRIBUTION:\n")
      bike_dist <- table(cyclistic_data$rideable_type, useNA = "ifany")
      bike_pct <- round(prop.table(bike_dist) * 100, 2)
      
      for (i in seq_along(bike_dist)) {
        cat(sprintf("  %-15s: %8d (%5.1f%%)\n", 
                    names(bike_dist)[i], bike_dist[i], bike_pct[i]))
      }
    }
    
    # =====================================================
    # DATE/TIME ANALYSIS
    # =====================================================
    
    if ("started_at" %in% names(cyclistic_data)) {
      cat("\n📅 DATE/TIME ANALYSIS:\n")
      
      # Convert to datetime
      cyclistic_data$started_at <- as.POSIXct(cyclistic_data$started_at)
      cyclistic_data$ended_at <- as.POSIXct(cyclistic_data$ended_at)
      
      cat("Date range:\n")
      cat("  Start:", min(cyclistic_data$started_at, na.rm = TRUE), "\n")
      cat("  End  :", max(cyclistic_data$started_at, na.rm = TRUE), "\n")
      
      # Calculate duration
      cyclistic_data$ride_duration_minutes <- as.numeric(
        difftime(cyclistic_data$ended_at, cyclistic_data$started_at, units = "mins")
      )
      
      cat("\nRide Duration Statistics:\n")
      duration_stats <- summary(cyclistic_data$ride_duration_minutes)
      print(duration_stats)
      
      # Check for invalid durations
      invalid_durations <- sum(cyclistic_data$ride_duration_minutes <= 0 | 
                              cyclistic_data$ride_duration_minutes > 1440, na.rm = TRUE)
      cat("Invalid durations (<= 0 or > 24 hours):", invalid_durations, "\n")
    }
    
    # =====================================================
    # STATION ANALYSIS
    # =====================================================
    
    if ("start_station_name" %in% names(cyclistic_data)) {
      cat("\n🚉 STATION ANALYSIS:\n")
      
      # Top start stations
      top_start <- cyclistic_data %>%
        filter(!is.na(start_station_name)) %>%
        count(start_station_name, sort = TRUE) %>%
        head(5)
      
      cat("Top 5 Start Stations:\n")
      for (i in 1:nrow(top_start)) {
        cat(sprintf("  %2d. %-30s: %6d rides\n", 
                    i, top_start$start_station_name[i], top_start$n[i]))
      }
    }
    
    # =====================================================
    # SAVE RESULTS
    # =====================================================
    
    # Create output directory
    if (!dir.exists("analysis/exploratory")) {
      dir.create("analysis/exploratory", recursive = TRUE)
    }
    
    # Save data quality summary
    write.csv(missing_summary, "analysis/exploratory/data_quality_summary.csv", row.names = FALSE)
    
    # Save member distribution
    if ("member_casual" %in% names(cyclistic_data)) {
      member_df <- data.frame(
        member_type = names(member_dist),
        count = as.numeric(member_dist),
        percentage = as.numeric(member_pct)
      )
      write.csv(member_df, "analysis/exploratory/member_distribution.csv", row.names = FALSE)
    }
    
    # Save sample of data for further analysis
    sample_size <- min(10000, nrow(cyclistic_data))
    sample_data <- cyclistic_data[sample(nrow(cyclistic_data), sample_size), ]
    write.csv(sample_data, "analysis/exploratory/sample_data.csv", row.names = FALSE)
    
    cat("\n✅ Analysis complete! Results saved to analysis/exploratory/\n")
    
  }, error = function(e) {
    cat("❌ Error loading file:", e$message, "\n")
  })
  
} else {
  cat("❌ Target file not found:", target_file, "\n")
}

# =====================================================
# SUMMARY AND NEXT STEPS
# =====================================================

cat("\n" + rep("=", 80) + "\n")
cat("EXPLORATION SUMMARY AND NEXT STEPS\n")
cat(rep("=", 80) + "\n")

cat("\n📋 What we accomplished:\n")
cat("   ✅ Discovered", length(csv_files), "CSV files in the dataset\n")
cat("   ✅ Analyzed file structure and data quality\n")
cat("   ✅ Examined member types and bike types\n")
cat("   ✅ Assessed date/time data and ride durations\n")
cat("   ✅ Identified top stations and usage patterns\n")
cat("   ✅ Saved results for further analysis\n")

cat("\n🎯 Recommended next steps:\n")
cat("   1. Review the data quality summary\n")
cat("   2. Plan data cleaning strategy\n")
cat("   3. Implement SQL cleaning script\n")
cat("   4. Run comprehensive exploratory analysis\n")
cat("   5. Create visualizations and dashboards\n")

cat("\n📁 Files created:\n")
cat("   • analysis/exploratory/data_quality_summary.csv\n")
cat("   • analysis/exploratory/member_distribution.csv\n")
cat("   • analysis/exploratory/sample_data.csv\n")

cat("\n🚀 Ready for the next phase of your capstone project!\n")
