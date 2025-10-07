# Cyclistic Bike Share - Exploratory Data Analysis
# Author: [Your Name]
# Date: [Current Date]
# Purpose: Comprehensive exploratory analysis of bike-share data

# =====================================================
# SETUP AND LIBRARIES
# =====================================================

# Load required libraries
library(tidyverse)
library(lubridate)
library(ggplot2)
library(dplyr)
library(scales)
library(gridExtra)
library(corrplot)
library(RColorBrewer)

# Set working directory and load data
# setwd("path/to/your/data")
# cyclistic_data <- read.csv("data/processed/cyclistic_cleaned.csv")

# For this template, we'll create sample data structure
# Replace with your actual data loading code

# =====================================================
# DATA OVERVIEW
# =====================================================

# Basic data structure
glimpse(cyclistic_data)

# Summary statistics
summary(cyclistic_data)

# Check for missing values
missing_summary <- cyclistic_data %>%
  summarise_all(~sum(is.na(.))) %>%
  gather(key = "variable", value = "missing_count") %>%
  mutate(missing_percentage = round(missing_count / nrow(cyclistic_data) * 100, 2))

print("Missing Values Summary:")
print(missing_summary)

# =====================================================
# RIDE DURATION ANALYSIS
# =====================================================

# Duration statistics by member type
duration_stats <- cyclistic_data %>%
  group_by(member_casual) %>%
  summarise(
    count = n(),
    mean_duration = round(mean(ride_duration_minutes, na.rm = TRUE), 2),
    median_duration = round(median(ride_duration_minutes, na.rm = TRUE), 2),
    min_duration = min(ride_duration_minutes, na.rm = TRUE),
    max_duration = max(ride_duration_minutes, na.rm = TRUE),
    sd_duration = round(sd(ride_duration_minutes, na.rm = TRUE), 2)
  )

print("Ride Duration Statistics by Member Type:")
print(duration_stats)

# Duration distribution plot
duration_plot <- ggplot(cyclistic_data, aes(x = ride_duration_minutes, fill = member_casual)) +
  geom_histogram(bins = 50, alpha = 0.7, position = "identity") +
  facet_wrap(~member_casual, scales = "free_y") +
  labs(
    title = "Distribution of Ride Durations by Member Type",
    x = "Ride Duration (minutes)",
    y = "Frequency",
    fill = "Member Type"
  ) +
  theme_minimal() +
  scale_x_continuous(limits = c(0, 120)) + # Focus on rides under 2 hours
  scale_fill_manual(values = c("casual" = "#FF6B6B", "member" = "#4ECDC4"))

print(duration_plot)

# Box plot for duration comparison
duration_boxplot <- ggplot(cyclistic_data, aes(x = member_casual, y = ride_duration_minutes, fill = member_casual)) +
  geom_boxplot(alpha = 0.7) +
  labs(
    title = "Ride Duration Comparison: Members vs Casual Riders",
    x = "Member Type",
    y = "Ride Duration (minutes)",
    fill = "Member Type"
  ) +
  theme_minimal() +
  scale_y_continuous(limits = c(0, 60)) + # Focus on rides under 1 hour
  scale_fill_manual(values = c("casual" = "#FF6B6B", "member" = "#4ECDC4"))

print(duration_boxplot)

# =====================================================
# TIME-BASED ANALYSIS
# =====================================================

# Usage by day of week
daily_usage <- cyclistic_data %>%
  group_by(day_of_week, member_casual) %>%
  summarise(
    ride_count = n(),
    avg_duration = round(mean(ride_duration_minutes, na.rm = TRUE), 2)
  ) %>%
  ungroup()

# Day of week plot
daily_plot <- ggplot(daily_usage, aes(x = factor(day_of_week), y = ride_count, fill = member_casual)) +
  geom_col(position = "dodge", alpha = 0.8) +
  labs(
    title = "Ride Count by Day of Week",
    x = "Day of Week (0=Sunday, 6=Saturday)",
    y = "Number of Rides",
    fill = "Member Type"
  ) +
  theme_minimal() +
  scale_fill_manual(values = c("casual" = "#FF6B6B", "member" = "#4ECDC4"))

print(daily_plot)

# Usage by hour of day
hourly_usage <- cyclistic_data %>%
  group_by(hour_of_day, member_casual) %>%
  summarise(
    ride_count = n(),
    avg_duration = round(mean(ride_duration_minutes, na.rm = TRUE), 2)
  ) %>%
  ungroup()

# Hour of day plot
hourly_plot <- ggplot(hourly_usage, aes(x = hour_of_day, y = ride_count, color = member_casual)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +
  labs(
    title = "Ride Count by Hour of Day",
    x = "Hour of Day",
    y = "Number of Rides",
    color = "Member Type"
  ) +
  theme_minimal() +
  scale_color_manual(values = c("casual" = "#FF6B6B", "member" = "#4ECDC4")) +
  scale_x_continuous(breaks = seq(0, 23, 2))

print(hourly_plot)

# Monthly usage pattern
monthly_usage <- cyclistic_data %>%
  group_by(month, member_casual) %>%
  summarise(
    ride_count = n(),
    avg_duration = round(mean(ride_duration_minutes, na.rm = TRUE), 2)
  ) %>%
  ungroup()

# Monthly plot
monthly_plot <- ggplot(monthly_usage, aes(x = factor(month), y = ride_count, fill = member_casual)) +
  geom_col(position = "dodge", alpha = 0.8) +
  labs(
    title = "Ride Count by Month",
    x = "Month",
    y = "Number of Rides",
    fill = "Member Type"
  ) +
  theme_minimal() +
  scale_fill_manual(values = c("casual" = "#FF6B6B", "member" = "#4ECDC4"))

print(monthly_plot)

# =====================================================
# BIKE TYPE ANALYSIS
# =====================================================

# Bike type usage by member type
bike_type_usage <- cyclistic_data %>%
  group_by(rideable_type, member_casual) %>%
  summarise(
    ride_count = n(),
    percentage = round(n() / sum(n()) * 100, 2)
  ) %>%
  ungroup()

print("Bike Type Usage by Member Type:")
print(bike_type_usage)

# Bike type preference plot
bike_type_plot <- ggplot(bike_type_usage, aes(x = rideable_type, y = ride_count, fill = member_casual)) +
  geom_col(position = "dodge", alpha = 0.8) +
  labs(
    title = "Bike Type Usage by Member Type",
    x = "Bike Type",
    y = "Number of Rides",
    fill = "Member Type"
  ) +
  theme_minimal() +
  scale_fill_manual(values = c("casual" = "#FF6B6B", "member" = "#4ECDC4")) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

print(bike_type_plot)

# =====================================================
# STATION ANALYSIS
# =====================================================

# Top 10 start stations
top_start_stations <- cyclistic_data %>%
  filter(start_station_name != "Unknown") %>%
  group_by(start_station_name, member_casual) %>%
  summarise(ride_count = n()) %>%
  group_by(start_station_name) %>%
  summarise(
    total_rides = sum(ride_count),
    member_rides = sum(ride_count[member_casual == "member"]),
    casual_rides = sum(ride_count[member_casual == "casual"]),
    member_percentage = round(member_rides / total_rides * 100, 2)
  ) %>%
  arrange(desc(total_rides)) %>%
  head(10)

print("Top 10 Start Stations:")
print(top_start_stations)

# Top 10 end stations
top_end_stations <- cyclistic_data %>%
  filter(end_station_name != "Unknown") %>%
  group_by(end_station_name, member_casual) %>%
  summarise(ride_count = n()) %>%
  group_by(end_station_name) %>%
  summarise(
    total_rides = sum(ride_count),
    member_rides = sum(ride_count[member_casual == "member"]),
    casual_rides = sum(ride_count[member_casual == "casual"]),
    member_percentage = round(member_rides / total_rides * 100, 2)
  ) %>%
  arrange(desc(total_rides)) %>%
  head(10)

print("Top 10 End Stations:")
print(top_end_stations)

# =====================================================
# COMPARATIVE ANALYSIS
# =====================================================

# Key metrics comparison
comparison_metrics <- cyclistic_data %>%
  group_by(member_casual) %>%
  summarise(
    total_rides = n(),
    avg_duration = round(mean(ride_duration_minutes, na.rm = TRUE), 2),
    median_duration = round(median(ride_duration_minutes, na.rm = TRUE), 2),
    weekend_rides = sum(day_of_week %in% c(0, 6)),
    weekday_rides = sum(day_of_week %in% c(1:5)),
    weekend_percentage = round(weekend_rides / total_rides * 100, 2),
    morning_rides = sum(hour_of_day %in% c(6:11)),
    afternoon_rides = sum(hour_of_day %in% c(12:17)),
    evening_rides = sum(hour_of_day %in% c(18:22)),
    night_rides = sum(hour_of_day %in% c(23, 0:5))
  ) %>%
  ungroup()

print("Comparative Analysis - Members vs Casual Riders:")
print(comparison_metrics)

# =====================================================
# VISUALIZATION SUMMARY
# =====================================================

# Create a comprehensive summary plot
# This would be used in your final presentation

summary_plot <- grid.arrange(
  daily_plot,
  hourly_plot,
  duration_boxplot,
  bike_type_plot,
  ncol = 2,
  nrow = 2
)

print(summary_plot)

# =====================================================
# KEY INSIGHTS SUMMARY
# =====================================================

cat("\n=== KEY INSIGHTS FROM EXPLORATORY DATA ANALYSIS ===\n\n")

# Insight 1: Duration differences
casual_avg <- duration_stats$mean_duration[duration_stats$member_casual == "casual"]
member_avg <- duration_stats$mean_duration[duration_stats$member_casual == "member"]
cat("1. DURATION DIFFERENCE:\n")
cat("   - Casual riders average", casual_avg, "minutes per ride\n")
cat("   - Members average", member_avg, "minutes per ride\n")
cat("   - Difference:", round(casual_avg - member_avg, 2), "minutes\n\n")

# Insight 2: Usage patterns
weekend_casual <- comparison_metrics$weekend_percentage[comparison_metrics$member_casual == "casual"]
weekend_member <- comparison_metrics$weekend_percentage[comparison_metrics$member_casual == "member"]
cat("2. WEEKEND USAGE:\n")
cat("   - Casual riders use bikes", weekend_casual, "% of the time on weekends\n")
cat("   - Members use bikes", weekend_member, "% of the time on weekends\n\n")

# Insight 3: Peak usage times
peak_hour_casual <- hourly_usage$hour_of_day[hourly_usage$member_casual == "casual" & 
                                            hourly_usage$ride_count == max(hourly_usage$ride_count[hourly_usage$member_casual == "casual"])]
peak_hour_member <- hourly_usage$hour_of_day[hourly_usage$member_casual == "member" & 
                                            hourly_usage$ride_count == max(hourly_usage$ride_count[hourly_usage$member_casual == "member"])]
cat("3. PEAK USAGE TIMES:\n")
cat("   - Casual riders peak at hour", peak_hour_casual, "\n")
cat("   - Members peak at hour", peak_hour_member, "\n\n")

cat("=== END OF ANALYSIS ===\n")

# =====================================================
# EXPORT RESULTS
# =====================================================

# Save summary statistics
write.csv(duration_stats, "analysis/exploratory/duration_stats.csv", row.names = FALSE)
write.csv(comparison_metrics, "analysis/exploratory/comparison_metrics.csv", row.names = FALSE)
write.csv(top_start_stations, "analysis/exploratory/top_start_stations.csv", row.names = FALSE)
write.csv(top_end_stations, "analysis/exploratory/top_end_stations.csv", row.names = FALSE)

# Save plots (uncomment when ready to export)
# ggsave("visualizations/duration_distribution.png", duration_plot, width = 10, height = 6)
# ggsave("visualizations/daily_usage.png", daily_plot, width = 10, height = 6)
# ggsave("visualizations/hourly_usage.png", hourly_plot, width = 10, height = 6)
# ggsave("visualizations/monthly_usage.png", monthly_plot, width = 10, height = 6)
# ggsave("visualizations/bike_type_usage.png", bike_type_plot, width = 10, height = 6)
# ggsave("visualizations/summary_analysis.png", summary_plot, width = 15, height = 10)

cat("\nAnalysis complete! Results saved to analysis/exploratory/ directory.\n")
